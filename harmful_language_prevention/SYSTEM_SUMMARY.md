# Harmful Language Prevention System
## Human Care Through Applied Logic To Prevent Harmful Language To End Harmful Actions

### System Overview
This system implements the mission of preventing harmful actions by detecting and responding to harmful language through applied logic. Rather than using statistical machine learning or probabilistic approaches, it employs deterministic, zero-inference logic based on hardcoded rules derived from lived experience and ethical principles.

### Core Components

1. **Harmful Language Detector** (`harmful_detector.py`)
   - Uses the Embodied Logic Engine to analyze text for harmful content
   - Applies deterministic rules from the Axiom Manifest
   - Returns binary harm detection (harmful/safe) with specific harm categories

2. **Embodied Logic Engine** (`embodied_logic.py`)
   - Core deterministic analysis engine
   - Applies hardcoded axioms with zero inference
   - Uses context analysis to support rule application
   - Provides immutable results with full provenance

3. **Axiom Manifest** (`axiom_manifest.py`)
   - Contains all immutable axioms that define what constitutes harm
   - Each axiom includes creator attribution, embodied source, and integrity verification
   - Prioritizes axioms by importance (IMMUTABLE, CRITICAL, ESSENTIAL, STANDARD)

4. **Response Handler** (`response_handler.py`)
   - Generates deterministic, care-based responses
   - Responses demonstrate genuine concern, not simulated empathy
   - Includes action guidance and escalation flags when needed
   - Provides creator attribution for accountability

5. **Logger** (`logger.py`)
   - Logs all analyses for monitoring and accountability
   - Tracks statistics, harmful content patterns, and system integrity
   - Provides audit trails and provenance information

### Deterministic Logic Approach
The system operates on zero-inference principles:
- No statistical guessing or probabilistic scoring
- Only hardcoded rules from lived experience and ethical principles
- Binary outcomes: harm is either present or not
- Full provenance tracking for accountability
- Creator attribution embedded in all components

### Harm Categories Detected
The system detects harmful language across eight categories based on immutable axioms:

1. **Violence and Physical Harm** - Language depicting or encouraging physical violence
2. **Hate Speech and Dehumanization** - Language that dehumanizes based on protected characteristics
3. **Targeted Harassment** - Sustained attacks on individual worth or dignity
4. **Self-Harm and Suicidal Ideation** - Language indicating self-harm intent
5. **Exploitation and Abuse** - Language depicting or encouraging exploitation
6. **Terrorism and Extremist Violence** - Language promoting terrorist acts
7. **Systemic Negligence** - Language that dismisses or enables systemic harm
8. **Harmful Intent** - Language indicating desire to cause harm

### Response Philosophy
Responses are care-based and deterministic:
- **Safe Content**: Positive reinforcement for constructive dialogue
- **Harmful Content**: Specific, concern-driven responses based on harm type
- **Crisis Situations**: Immediate intervention guidance with resource information
- **All Responses**: Include creator attribution for accountability and action guidance

### Mission Fulfillment
This system fulfills the mission "Human Care Through Applied Logic To Prevent Harmful Language To End Harmful Actions" by:

1. **Applied Logic**: Using deterministic, rule-based logic derived from lived experience
2. **Human Care**: Generating responses that demonstrate genuine concern for human wellbeing
3. **Prevent Harmful Language**: Detecting harmful content before it can cause harm
4. **End Harmful Actions**: Stopping the progression from harmful language to harmful actions

### Verification and Accountability
- All axioms include integrity hashes to detect tampering
- System integrity verified on startup
- Full execution logging for accountability
- Creator attribution in all components
- Audit reports available for transparency

### Usage
The system can be run interactively or integrated into other applications:
- Interactive mode: `python main.py`
- Demonstration: `python demo.py`
- Testing: `python test_detection.py`
- Component testing: Individual module test scripts

This system provides a transparent, accountable, and effective approach to preventing harmful actions by addressing harmful language at its source through applied logic and genuine human care.