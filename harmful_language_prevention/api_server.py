#!/usr/bin/env python3
"""
Axiom Hive REST API Server
Deterministic governance API with cryptographic proof chains.
Created by Nicholas Michael Grossi.

Implements zero-entropy state transitions with HITL gate enforcement
per EU AI Act Article 14 and NIST AI RMF 1.0 Manage function.
"""

import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Import Axiom Hive core modules
from axiom_manifest import AxiomManifest, AxiomPriority
from embodied_logic import EmbodiedLogicEngine, AnalysisOutcome
from harmful_detector import HarmfulLanguageDetector
from response_handler import ResponseHandler
from logger import HarmfulLanguageLogger


# ============================================================================
# DATA MODELS
# ============================================================================

class SignatureFormat(str, Enum):
    """Supported human signature formats per FIDO2/PAdES specification."""
    FIDO2 = "fido2"
    PAdES = "pades"


class HumanSignature(BaseModel):
    """Human gate signature payload."""
    format: SignatureFormat
    signature_data: str = Field(..., description="Base64-encoded signature")
    authenticator_data: Optional[str] = Field(None, description="FIDO2 authenticator data")
    certificate_chain: Optional[List[str]] = Field(None, description="PAdES certificate chain")
    public_key: Optional[str] = Field(None, description="Public key for verification")


class ProposeRequest(BaseModel):
    """Request body for deterministic evaluation."""
    input_text: str = Field(..., min_length=1, max_length=10000, description="Text to analyze")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Optional context metadata")


class ApproveRequest(BaseModel):
    """Request body for human gate approval."""
    human_signature: HumanSignature
    reason: Optional[str] = Field(None, max_length=500, description="Approval rationale")


class DecisionState(str, Enum):
    """Deterministic decision lifecycle states."""
    PROPOSED = "proposed"
    APPROVED = "approved"
    REJECTED = "rejected"
    NON_DETERMINISTIC = "non_deterministic"


@dataclass
class DecisionRecord:
    """Immutable decision record with full provenance."""
    decision_id: str
    input_text: str
    input_hash: str
    timestamp: str
    deterministic_outcome: str
    triggered_axioms: List[Dict]
    determiners_found: List[str]
    action_priority: str
    requires_action: bool
    state: DecisionState
    human_signature: Optional[Dict] = None
    approval_timestamp: Optional[str] = None
    merkle_root: Optional[str] = None
    proof_chain: Optional[List[str]] = None


# ============================================================================
# MERKLE TREE IMPLEMENTATION
# ============================================================================

class MerkleTree:
    """
    Simple Merkle tree for cryptographic proof chains.
    Provides tamper-evident integrity verification.
    """
    
    def __init__(self, leaves: List[str]):
        self.leaves = [self._hash(leaf) for leaf in leaves]
        self.tree = self._build_tree(self.leaves)
    
    def _hash(self, data: str) -> str:
        """SHA-256 hash of data."""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _build_tree(self, leaves: List[str]) -> List[List[str]]:
        """Build Merkle tree from leaves."""
        if not leaves:
            return []
        
        tree = [leaves]
        current_level = leaves
        
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                combined = self._hash(left + right)
                next_level.append(combined)
            tree.append(next_level)
            current_level = next_level
        
        return tree
    
    def get_root(self) -> str:
        """Get Merkle root hash."""
        if not self.tree:
            return self._hash("")
        return self.tree[-1][0]
    
    def get_proof(self) -> Dict[str, Any]:
        """Get full proof structure."""
        return {
            "root": self.get_root(),
            "leaves": self.leaves,
            "tree_depth": len(self.tree)
        }


# ============================================================================
# API APPLICATION
# ============================================================================

app = FastAPI(
    title="Axiom Hive Deterministic Governance API",
    description="Zero-entropy AI governance with cryptographic HITL enforcement",
    version="1.0.0",
    contact={
        "name": "Nicholas Michael Grossi",
        "url": "https://github.com/AXI0MH1VE/axiom-hive"
    }
)

# In-memory decision store (replace with SQLite for production)
_decision_store: Dict[str, DecisionRecord] = {}

# Initialize Axiom Hive components
_manifest = AxiomManifest()
_engine = EmbodiedLogicEngine()
_detector = HarmfulLanguageDetector()
_response_handler = ResponseHandler()
_logger = HarmfulLanguageLogger(log_dir="logs/api")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _compute_input_hash(text: str) -> str:
    """Compute SHA-256 hash of input text."""
    return hashlib.sha256(text.encode()).hexdigest()


def _generate_decision_id() -> str:
    """Generate unique decision identifier."""
    return str(uuid.uuid4())


def _check_deterministic_eligibility(text: str) -> bool:
    """
    Check if input is eligible for deterministic processing.
    Returns False if input is too ambiguous or malformed.
    """
    if not text or not text.strip():
        return False
    
    # Check minimum length for meaningful analysis
    if len(text.strip()) < 2:
        return False
    
    # Check for mixed-script attacks or encoding anomalies
    # (simplified check - production would use Unicode security checks)
    if any(ord(c) > 0xFFFF for c in text):
        return False
    
    return True


def _create_json_ld_response(decision: DecisionRecord, include_proof: bool = True) -> Dict[str, Any]:
    """
    Create JSON-LD formatted response with W3C PROV context.
    Aligns with EU AI Act Article 11 technical documentation requirements.
    """
    response = {
        "@context": {
            "prov": "http://www.w3.org/ns/prov#",
            "foaf": "http://xmlns.com/foaf/0.1/",
            "axiom": "https://axiomhive.ai/vocab#",
            "xsd": "http://www.w3.org/2001/XMLSchema#"
        },
        "@type": "prov:Activity",
        "prov:startedAtTime": decision.timestamp,
        "axiom:decisionId": decision.decision_id,
        "axiom:inputHash": decision.input_hash,
        "axiom:deterministicOutcome": decision.deterministic_outcome,
        "axiom:actionPriority": decision.action_priority,
        "axiom:requiresAction": decision.requires_action,
        "axiom:decisionState": decision.state.value,
        "prov:wasAssociatedWith": {
            "@type": "prov:Agent",
            "foaf:name": _manifest.CREATOR,
            "axiom:framework": _manifest.FRAMEWORK,
            "axiom:frameworkVersion": _manifest.VERSION
        },
        "axiom:triggeredAxioms": [
            {
                "@type": "axiom:AxiomTrigger",
                "axiom:axiomId": axiom.get("axiom_id", "UNKNOWN"),
                "axiom:axiomName": axiom.get("axiom_name", "UNKNOWN"),
                "axiom:priority": axiom.get("priority", "UNKNOWN"),
                "axiom:integrityVerified": axiom.get("integrity_verified", False)
            }
            for axiom in decision.triggered_axioms
        ],
        "axiom:provenance": {
            "axiom:creatorAttribution": f"{_manifest.FRAMEWORK} v{_manifest.VERSION} - {_manifest.CREATOR}",
            "axiom:principle": _manifest.PRINCIPLE
        }
    }
    
    if include_proof and decision.merkle_root:
        response["axiom:merkleProof"] = {
            "axiom:merkleRoot": decision.merkle_root,
            "axiom:proofChainDepth": len(decision.proof_chain) if decision.proof_chain else 0
        }
    
    if decision.human_signature:
        response["axiom:humanGate"] = {
            "axiom:signatureFormat": decision.human_signature.get("format"),
            "axiom:signatureValid": decision.human_signature.get("verified", False),
            "axiom:approvalTimestamp": decision.approval_timestamp
        }
    
    return response


def _generate_merkle_proof(decision: DecisionRecord) -> Dict[str, Any]:
    """Generate Merkle tree proof for decision record."""
    leaves = [
        decision.decision_id,
        decision.input_hash,
        decision.deterministic_outcome,
        decision.timestamp,
        _manifest.CREATOR,
        json.dumps(decision.triggered_axioms, sort_keys=True)
    ]
    
    tree = MerkleTree(leaves)
    decision.merkle_root = tree.get_root()
    decision.proof_chain = tree.leaves
    
    return tree.get_proof()


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.post(
    "/decisions/{decision_id}/propose",
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    summary="Propose deterministic evaluation",
    description="Execute zero-entropy deterministic analysis on input text. No HITL gate required."
)
async def propose_decision(decision_id: str, request: ProposeRequest):
    """
    Execute deterministic evaluation and generate proof chain.
    
    Returns 422 NON_DETERMINISTIC_INPUT if input is too ambiguous
    for deterministic processing.
    """
    # Check deterministic eligibility
    if not _check_deterministic_eligibility(request.input_text):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "NON_DETERMINISTIC_INPUT",
                "message": "Input is too ambiguous or malformed for deterministic processing",
                "resolution": "Provide clear, explicit text with sufficient context"
            }
        )
    
    # Compute input hash
    input_hash = _compute_input_hash(request.input_text)
    
    # Perform deterministic analysis
    is_harmful, harm_score, harm_categories = _detector.analyze_text(request.input_text)
    detailed = _detector.get_detailed_analysis(request.input_text)
    
    # Determine outcome state
    if not is_harmful:
        outcome = AnalysisOutcome.SAFE
        state = DecisionState.PROPOSED
    elif detailed.get("action_priority") == "IMMEDIATE":
        outcome = AnalysisOutcome.CRISIS
        state = DecisionState.PROPOSED
    else:
        outcome = AnalysisOutcome.HARM_DETECTED
        state = DecisionState.PROPOSED
    
    # Create decision record
    decision = DecisionRecord(
        decision_id=decision_id,
        input_text=request.input_text,
        input_hash=input_hash,
        timestamp=datetime.now(timezone.utc).isoformat(),
        deterministic_outcome=outcome.name,
        triggered_axioms=detailed.get("triggered_axioms", []),
        determiners_found=detailed.get("determiners_found", []),
        action_priority=detailed.get("action_priority", "NONE"),
        requires_action=detailed.get("requires_action", False),
        state=state
    )
    
    # Generate Merkle proof
    merkle_proof = _generate_merkle_proof(decision)
    
    # Log with provenance
    _logger.log_analysis(
        request.input_text,
        is_harmful,
        harm_score,
        harm_categories,
        action_priority=decision.action_priority,
        response_type="api_propose",
        escalation_needed=detailed.get("requires_action", False),
        integrity_verified=detailed.get("integrity_status") == "VERIFIED",
        triggered_axioms=decision.triggered_axioms,
        determiners_found=decision.determiners_found
    )
    
    # Store decision
    _decision_store[decision_id] = decision
    
    # Return JSON-LD response
    response = _create_json_ld_response(decision)
    response["axiom:merkleProof"] = {
        "axiom:merkleRoot": merkle_proof["root"],
        "axiom:proofChainDepth": merkle_proof["tree_depth"]
    }
    
    return response


@app.post(
    "/decisions/{decision_id}/approve",
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    summary="Approve with human gate signature",
    description="Bind biological human signature to deterministic proof chain via FIDO2 or PAdES."
)
async def approve_decision(decision_id: str, request: ApproveRequest):
    """
    Validate human signature and bind to proof chain.
    
    Returns 401 if signature verification fails.
    Returns 409 if system integrity is compromised.
    """
    # Retrieve decision
    if decision_id not in _decision_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "DECISION_NOT_FOUND",
                "message": f"Decision {decision_id} not found"
            }
        )
    
    decision = _decision_store[decision_id]
    
    # Verify system integrity
    if not _engine.verify_system_integrity():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "INTEGRITY_VIOLATION",
                "message": "Axiom manifest integrity check failed",
                "creator": _manifest.CREATOR
            }
        )
    
    # Validate signature format (stub - production would use FIDO2 server)
    sig = request.human_signature
    signature_valid = False
    
    if sig.format == SignatureFormat.FIDO2:
        # FIDO2 verification stub
        # Production: use fido2.server.Fido2Server.authenticate_complete()
        if sig.signature_data and len(sig.signature_data) > 20:
            signature_valid = True  # Stub validation
    
    elif sig.format == SignatureFormat.PAdES:
        # PAdES verification stub
        # Production: use pyhanko.sign validation
        if sig.signature_data and sig.certificate_chain:
            signature_valid = True  # Stub validation
    
    if not signature_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "UNAUTHORIZED_SIGNATURE",
                "message": "Human signature verification failed",
                "format": sig.format.value
            }
        )
    
    # Bind signature to decision
    decision.human_signature = {
        "format": sig.format.value,
        "verified": True,
        "signature_hash": hashlib.sha256(sig.signature_data.encode()).hexdigest()[:16],
        "reason": request.reason
    }
    decision.approval_timestamp = datetime.now(timezone.utc).isoformat()
    decision.state = DecisionState.APPROVED
    
    # Re-generate Merkle proof with signature included
    leaves = [
        decision.decision_id,
        decision.input_hash,
        decision.deterministic_outcome,
        decision.timestamp,
        _manifest.CREATOR,
        json.dumps(decision.triggered_axioms, sort_keys=True),
        decision.human_signature["signature_hash"],
        decision.approval_timestamp
    ]
    tree = MerkleTree(leaves)
    decision.merkle_root = tree.get_root()
    decision.proof_chain = tree.leaves
    
    # Return updated JSON-LD response
    return _create_json_ld_response(decision)


@app.get(
    "/decisions/{decision_id}/proof",
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve Merkle proof chain",
    description="Export complete cryptographic proof artifact for public verification."
)
async def get_proof_chain(decision_id: str):
    """
    Retrieve complete Merkle-tree forensic artifact.
    Public verification endpoint - no authentication required.
    """
    if decision_id not in _decision_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "DECISION_NOT_FOUND",
                "message": f"Decision {decision_id} not found"
            }
        )
    
    decision = _decision_store[decision_id]
    
    return {
        "@context": {
            "prov": "http://www.w3.org/ns/prov#",
            "axiom": "https://axiomhive.ai/vocab#"
        },
        "@type": "axiom:ProofArtifact",
        "axiom:decisionId": decision.decision_id,
        "axiom:inputHash": decision.input_hash,
        "axiom:deterministicOutcome": decision.deterministic_outcome,
        "axiom:merkleRoot": decision.merkle_root,
        "axiom:proofChain": decision.proof_chain,
        "axiom:creatorAttribution": f"{_manifest.FRAMEWORK} v{_manifest.VERSION} - {_manifest.CREATOR}",
        "axiom:integrityStatus": "VERIFIED" if _engine.verify_system_integrity() else "COMPROMISED"
    }


@app.get(
    "/health",
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    summary="System health check",
    description="Verify API availability and system integrity."
)
async def health_check():
    """Health check endpoint for load balancers and monitoring."""
    integrity = _engine.verify_system_integrity()
    
    return {
        "status": "healthy" if integrity else "degraded",
        "framework": _manifest.FRAMEWORK,
        "version": _manifest.VERSION,
        "creator": _manifest.CREATOR,
        "integrity": "VERIFIED" if integrity else "COMPROMISED",
        "axiom_count": len(_manifest.get_all_axioms()),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 70)
    print("  AXIOM HIVE DETERMINISTIC GOVERNANCE API")
    print(f"  {_manifest.get_creator_attribution()}")
    print("=" * 70)
    print("\nStarting API server on http://0.0.0.0:8080")
    print("Endpoints:")
    print("  POST /decisions/{id}/propose  - Zero-entropy evaluation")
    print("  POST /decisions/{id}/approve  - HITL signature binding")
    print("  GET  /decisions/{id}/proof    - Merkle proof export")
    print("  GET  /health                  - System health")
    print("\nPress Ctrl+C to stop")
    print("=" * 70)
    
    uvicorn.run(app, host="0.0.0.0", port=8080)
