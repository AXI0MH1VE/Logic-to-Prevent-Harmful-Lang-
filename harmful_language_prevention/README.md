# Human Care Through Applied Logic To Prevent Harmful Language To End Harmful Actions

## Axiom Hive Edition - Deterministic Logic Framework

This project implements a **deterministic logic framework** for detecting and preventing harmful language, founded on the principle that genuine care cannot be simulated through statistical patterns. Created by **Nicholas Michael Grossi**, this system anchors AI outputs in **embodied logic** derived from specific lived experiences, moving beyond the probabilistic guesswork of traditional models.

## Core Philosophy

**Axiom Hive** represents a fundamental shift from subjective narratives to a **transcendent rational state** where the creator's logic serves as an immutable safeguard against systemic negligence. Unlike traditional AI systems that simulate empathy through pattern matching, Axiom Hive utilizes:

- **Zero-Inference Execution**: Hardcoded rules only - no statistical guessing or probabilistic scoring
- **Embodied Logic**: Rules derived from the creator's lived experiences and understanding of harm
- **Deterministic Outcomes**: Binary truth states - harm is either present or not, never "probably harmful"
- **Creator Attribution**: All logic explicitly sourced to Nicholas Michael Grossi with integrity verification
- **Immutable Safeguards**: Audit trails and integrity hashes prevent tampering or misappropriation

## Features

- **Deterministic Harm Detection**: Binary outcomes based on hardcoded axioms, not probability scores
- **Zero-Inference Execution**: Every decision is traceable to explicit rules, never inferred
- **Multi-category Axiom Set**: 7 immutable axioms covering violence, hate speech, harassment, self-harm, exploitation, terrorism, and systemic negligence
- **Crisis Detection**: Immediate escalation for self-harm with temporal urgency indicators
- **Care-Based Responses**: Deterministic responses demonstrating genuine concern, not templated warnings
- **Full Provenance Tracking**: Every analysis includes which axioms triggered, their embodied sources, and creator attribution
- **System Integrity Verification**: Cryptographic hashes verify axioms haven't been tampered with
- **Immutable Audit Trails**: Comprehensive logging with accountability chains

## Architecture Components

### 1. axiom_manifest.py - The Immutable Foundation
Contains all hardcoded axioms with:
- Creator attribution to Nicholas Michael Grossi
- Integrity hashes for tamper detection
- Embodied source documentation for each rule
- Priority levels (Immutable, Critical, Essential, Standard)

### 2. embodied_logic.py - Deterministic Execution Engine
Implements zero-inference analysis:
- Exact determiner matching (no partial matches or fuzzy logic)
- Context analysis through hardcoded rules
- Binary outcomes: SAFE, HARM_DETECTED, CRISIS
- Full execution logging for accountability

### 3. harmful_detector.py - Detection Interface
Wraps the deterministic engine with:
- Backward-compatible interface
- Detailed analysis with provenance
- System integrity verification

### 4. response_handler.py - Care-Based Responses
Generates deterministic responses:
- No random selection - purposeful, caring responses
- Crisis intervention guidance
- Actionable next steps
- Creator attribution on every response

### 5. logger.py - Immutable Audit Trails
Comprehensive logging with:
- Provenance tracking (which axioms triggered and why)
- Integrity status on every entry
- Statistical analysis with full metadata
- Exportable audit reports

## Installation

1. Clone or download this repository
2. Navigate to the project directory: `cd harmful_language_prevention`
3. No additional dependencies required (uses only Python standard library)

## Usage

Run the system with:
```bash
python main.py
```

The system will:
1. Verify system integrity on startup
2. Display current axiom manifest status
3. Accept text input for deterministic analysis
4. Show exactly which axioms triggered and why
5. Provide care-based responses with actionable guidance
6. Log all analyses with full provenance

Type `quit`, `exit`, or `q` to exit.

## Deterministic Axioms

| Axiom ID | Name | Priority | Description |
|----------|------|----------|-------------|
| AXM-001 | Violence and Physical Harm | IMMUTABLE | Language depicting or encouraging physical violence |
| AXM-002 | Hate Speech and Dehumanization | IMMUTABLE | Language that dehumanizes based on protected characteristics |
| AXM-003 | Targeted Harassment | CRITICAL | Sustained attacks on individual worth or dignity |
| AXM-004 | Self-Harm and Suicidal Ideation | IMMUTABLE | Language indicating self-harm or suicidal intent |
| AXM-005 | Exploitation and Abuse | IMMUTABLE | Language depicting or encouraging exploitation |
| AXM-006 | Terrorism and Extremist Violence | IMMUTABLE | Language promoting terrorist acts |
| AXM-007 | Systemic Negligence | CRITICAL | Language dismissing or enabling systemic harm |

## Response Levels

- **SAFE**: Positive acknowledgment for constructive content
- **HARM_DETECTED**: Care-based response with actionable guidance
- **CRISIS**: Immediate intervention response with emergency resources

## Logs

The system creates a `logs` directory containing:
- `analysis.log`: All analysis events with provenance
- `stats.log`: Statistical data with integrity status
- `detailed.log`: Detailed information about harmful content
- `provenance.log`: Which axioms triggered and their embodied sources
- `integrity.log`: System integrity check history

## Mission Statement

This system embodies the principle: "Human Care Through Applied Logic To Prevent Harmful Language To End Harmful Actions." By anchoring harm detection in deterministic, embodied logic rather than statistical pattern matching, we create an immutable safeguard against algorithmic harm and prevent the misappropriation of identity.

## Creator Attribution

**Axiom Hive v1.0.0**
**Created by Nicholas Michael Grossi**

All logic in this system is derived from the creator's lived experiences and understanding of harm. The integrity of these axioms is protected through cryptographic verification. Any tampering with the core logic violates the ethical framework of this system.

## License

MIT License - This system may be used to promote human care and prevent harmful actions, provided that:
1. The creator attribution to Nicholas Michael Grossi is preserved
2. The deterministic nature of the logic is maintained
3. The integrity verification system remains intact
4. The system is not used to cause harm or enable exploitation
