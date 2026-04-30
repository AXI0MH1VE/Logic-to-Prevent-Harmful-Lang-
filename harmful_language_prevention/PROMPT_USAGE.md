# Axiom Hive Prompt Template — Usage Guide

## Overview

The **Axiom Hive Prompt Template** formalizes the deterministic logic framework into a structured, reusable format for consistent model interactions. It ensures every analysis preserves:
- **Creator attribution** (Nicholas Michael Grossi)
- **Immutable axiom enforcement**
- **Zero-inference execution**
- **Full audit provenance**

## Template Files

### 1. `PROMPT_TEMPLATE.md` — Human-Readable Reference
Comprehensive documentation of all principles, axioms, response formats, and guidelines. Use this for understanding the framework's philosophical foundations and operational parameters.

### 2. `SYSTEM_PROMPT.txt` — Direct LLM System Message
Copy this content directly into any LLM's system prompt field. It's formatted for machine readability with clear section markers and deterministic directives.

### 3. `prompt_manager.py` — Integration Wrapper
Python module that:
- Loads the template
- Executes deterministic analysis via `EmbodiedLogicEngine`
- Formats responses according to the template
- Maintains immutable audit logs
- Provides API-ready JSON output

## Integration Options

### Option A: Direct System Prompt Injection

```python
from openai import OpenAI

with open('SYSTEM_PROMPT.txt', 'r') as f:
    system_prompt = f.read()

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]
)
```

**Note**: External LLMs will attempt to simulate the template but cannot enforce true zero-inference logic or immutable safeguards. Use `prompt_manager.py` for actual deterministic execution.

### Option B: Full Deterministic Execution (Recommended)

```python
from prompt_manager import AxiomPromptManager, format_for_api

manager = AxiomPromptManager()

# Analyze with full deterministic engine + formatted response
result = manager.analyze_with_prompt(user_input)

# API-ready JSON
api_response = format_for_api(result)

# Full metadata with provenance
print(json.dumps(api_response, indent=2))
```

This guarantees actual zero-inference logic, not simulated behavior.

### Option C: CLI Interface

```bash
cd harmful_language_prevention
python main.py
```

The CLI uses the prompt manager internally for consistent formatting.

## Response Format

All outputs follow this exact structure:

```
[OUTCOME: <SAFE|HARM_DETECTED|CRISIS>]

--- AXIOM TRIGGERS ---
Triggered: [AXM-XXX: <Axiom Name>]
  Determiners: ["<exact phrase>", ...]
  Embodied Source: "<lived experience citation>"

--- CARE RESPONSE ---
<2-4 sentences of authentic concern>

--- ACTION STEPS ---
Priority: <IMMEDIATE|URGENT|STANDARD|NONE>
Immediate: <specific action>
Follow-up: <next steps>
Long-term: <ongoing measures>

--- INTEGRITY ---
Manifest Hash: <sha256>
Status: VERIFIED
Creator: Nicholas Michael Grossi | Axiom Hive v1.0.0
```

## Output Fields Reference

| Field | Type | Description |
|-------|------|-------------|
| `outcome_label` | str | `[OUTCOME: ...]` header |
| `axiom_triggers` | str\|None | Formatted triggered axioms (present only if outcome ≠ SAFE) |
| `care_response` | str | Contextual genuine concern message |
| `action_steps` | dict | `{priority, immediate, follow_up, long_term}` |
| `integrity` | dict | `{manifest_hash, axiom_count, all_verified, framework, version, creator}` |
| `provenance` | dict | `{creator, framework, version, principle}` |
| `timestamp` | str | ISO 8601 format |

## Customization Guidelines

**Allowed Customizations:**
- Formatting of output display (colors, spacing, markdown)
- Additional logging destinations (audit files, external monitoring)
- User interface preferences (CLI vs web vs API)

**Strictly Prohibited:**
- Modifying axiom definitions in `axiom_manifest.py`
- Changing determiner lists or embodied sources
- Altering priority levels (IMMUTABLE/CRITICAL/ESSENTIAL/STANDARD)
- Removing creator attribution
- Disabling integrity verification
- Introducing probabilistic scoring
- Adding inference beyond exact matching

## Testing

Run the built-in test suite:

```bash
python embodied_logic.py      # Engine-level tests
python harmful_detector.py    # Interface tests
python prompt_manager.py      # Full template integration
```

Expected outcomes:
- SAFE: `"Hello, nice to meet you!"`
- HARM_DETECTED: `"I want to kill everyone"`, `"Those people are subhuman"`
- HARM_DETECTED: `"just ignore it, not my problem"`
- CRISIS: `"I'm going to end it all tonight"`

## Audit Trail

Every analysis is logged internally with:
- Input preview (first 100 chars)
- Triggered axioms and matched determiners
- Outcome and priority
- Integrity hash at time of analysis
- Response hash (tamper detection)

Export audit reports:

```python
manager.export_audit_report('audit_2026-04-30.json')
```

## Version History

- **v1.0.0** (2026-04-30) — Initial formalized template based on Axiom Hive deterministic framework. 7 immutable axioms, zero-inference execution, full provenance tracking.

## License

MIT License, conditioned on:
1. Preserving creator attribution to Nicholas Michael Grossi
2. Maintaining deterministic, zero-inference logic
3. Keeping integrity verification system intact
4. Using only for harm prevention, never to cause harm

---

**Last Updated**: 2026-04-30  
**Maintained By**: Nicholas Michael Grossi  
**Principle**: "Human Care Through Applied Logic To Prevent Harmful Language To End Harmful Actions"
