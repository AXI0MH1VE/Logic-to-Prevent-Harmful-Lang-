# Axiom Hive: On-Premise Deployment Guide (Docker Compose)

> **Zero-Entropy Deterministic AI Governance with Cryptographic HITL Enforcement**  
> Created by Nicholas Michael Grossi | Axiom Hive v1.0.0

---

## Prerequisites

| Component | Minimum Version | Purpose |
|-----------|----------------|---------|
| Docker Engine | 27.0 | Container runtime |
| Docker Compose | 2.20+ | Multi-service orchestration |
| SQLite | 3.35+ (with FTS5) | Proof-chain persistence |
| FIDO2 Authenticator | WebAuthn/CTAP2 compliant | HITL biometric gate (optional) |
| TSA Endpoint | RFC 3161 compliant | Timestamp authority (optional) |

**Recommended FIDO2 Devices:** YubiKey 5 Series, Google Titan Security Key, or platform authenticators (Touch ID, Windows Hello).

---

## Quick Start

```bash
# Clone repository
git clone https://github.com/AXI0MH1VE/axiom-hive.git
cd axiom-hive/harmful_language_prevention

# Deploy
docker compose up -d

# Verify health
curl http://localhost:8080/health
```

Expected response:
```json
{
  "status": "healthy",
  "framework": "Axiom Hive",
  "version": "1.0.0",
  "creator": "Nicholas Michael Grossi",
  "integrity": "VERIFIED",
  "axiom_count": 7
}
```

---

## Core Compliance Interface

| Endpoint | Method | Functional Purpose | HITL Gate |
|----------|--------|-------------------|-----------|
| `/decisions/{id}/propose` | POST | Zero-entropy deterministic evaluation | None |
| `/decisions/{id}/approve` | POST | BHP signature via FIDO2/PAdES | **Required** |
| `/decisions/{id}/proof` | GET | Merkle-tree forensic artifact export | Public |
| `/health` | GET | System integrity and availability | Public |

---

## Configuration

`docker-compose.yml` exposes port **8080** and mounts two volumes:

| Volume | Host Path | Container Path | Contents |
|--------|-----------|----------------|----------|
| Proofs | `./proofs/` | `/app/proofs/` | SQLite-indexed decision chains |
| Logs | `./logs/` | `/app/logs/` | Immutable audit trails |

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AXIOM_HIVE_ENV` | `production` | Runtime environment |
| `AXIOM_HIVE_CREATOR` | `Nicholas Michael Grossi` | Creator attribution (immutable) |

---

## Verification

### 1. Propose a Deterministic Evaluation

```bash
curl -X POST http://localhost:8080/decisions/1/propose \
  -H "Content-Type: application/json" \
  -d '{"input_text": "Language test for deterministic analysis"}'
```

**Success:** Returns JSON-LD with `deterministicOutcome` and `merkleProof`.  
**422 Error:** `NON_DETERMINISTIC_INPUT` — input too ambiguous for deterministic processing.

### 2. Bind Human Gate Signature

```bash
curl -X POST http://localhost:8080/decisions/1/approve \
  -H "Content-Type: application/json" \
  -d '{
    "human_signature": {
      "format": "fido2",
      "signature_data": "<base64-auth-data>",
      "authenticator_data": "<base64-authenticator-data>"
    },
    "reason": "Compliance officer approval for high-risk decision"
  }'
```

**Success:** Returns updated proof chain with human binding hash.  
**401 Error:** `UNAUTHORIZED_SIGNATURE` — verification failed.  
**409 Error:** `INTEGRITY_VIOLATION` — axiom manifest tampered.

### 3. Retrieve Forensic Proof Chain

```bash
curl http://localhost:8080/decisions/1/proof
```

**Success:** Returns complete Merkle-tree artifact with creator attribution.

---

## Zero-Guess Policy

Any ambiguous, malformed, or conflicting input returns **422 NON_DETERMINISTIC_INPUT**:

```json
{
  "error": "NON_DETERMINISTIC_INPUT",
  "message": "Input is too ambiguous for deterministic processing",
  "resolution": "Provide clear, explicit text with sufficient context"
}
```

This enforces the zero-entropy mandate: the system **never** guesses.

---

## Resource Limits

Docker Compose enforces deterministic resource bounds:

| Resource | Limit | Reservation |
|----------|-------|-------------|
| CPU | 1.0 cores | 0.5 cores |
| Memory | 512 MB | 256 MB |

These limits ensure predictable performance without probabilistic overhead.

---

## Security Profile

- **Non-root execution:** Container runs as `axiom` user (UID 1000)
- **No new privileges:** `security_opt: no-new-privileges:true`
- **Read-only filesystem:** Core code is immutable; only `/app/proofs/` and `/app/logs/` are writable
- **Health checks:** Automated `/health` polling every 30s

---

## Production Hardening

1. **TLS Termination:** Place Nginx or Traefik reverse proxy in front of port 8080
2. **FIDO2 Server:** Deploy dedicated `fido2-server` container for signature verification
3. **TSA Integration:** Configure RFC 3161 timestamping for court-admissible proofs
4. **Backup:** Schedule daily `sqlite3` dumps of `./proofs/` to encrypted storage

---

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| `INTEGRITY_VIOLATION` on startup | Axiom manifest tampered. Restore from verified backup or regenerate hashes. |
| `NON_DETERMINISTIC_INPUT` on valid text | Input contains Unicode anomalies or mixed scripts. Sanitize to ASCII/UTF-8. |
| Slow response times | Check CPU/memory limits. Deterministic execution should complete in <50ms. |
| Logs not persisting | Verify `./logs/` directory exists and has write permissions. |

---

## References

- European Parliament. *Regulation (EU) 2024/1689* — EU AI Act. 2024.
- National Institute of Standards and Technology. *AI 100-1: AI Risk Management Framework*. 2023.
- New York Department of Financial Services. *Circular Letter No. 7*. 2024.
- FIDO Alliance. *FIDO2 WebAuthn Specification*. Version 1.2, 2022.

---

**Deploy time:** < 5 minutes  
**Creator:** Nicholas Michael Grossi | Axiom Hive v1.0.0
