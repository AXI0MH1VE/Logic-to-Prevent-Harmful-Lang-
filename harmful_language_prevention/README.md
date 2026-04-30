# Human Care Through Applied Logic To Prevent Harmful Language To End Harmful Actions

This project implements a system that uses applied logic to detect and prevent harmful language, with the ultimate goal of ending harmful actions. The system analyzes text input for various types of harmful content and provides appropriate responses to promote positive discourse.

## Features

- **Multi-category Harmful Language Detection**: Identifies violence, hate speech, harassment, self-harm, illegal activities, sexual exploitation, terrorism, and general harmful intent
- **Configurable Sensitivity**: Adjustable thresholds for different response levels
- **Detailed Logging**: Comprehensive logging of all analyses for monitoring and improvement
- **Responsive Feedback System**: Provides appropriate responses based on harm severity
- **Extensible Design**: Modular components for easy maintenance and enhancement

## Components

1. **main.py**: Entry point that orchestrates the harmful language prevention system
2. **harmful_detector.py**: Core detection logic using pattern matching and applied logic
3. **response_handler.py**: Generates appropriate responses based on detection results
4. **logger.py**: Logs all analysis events for monitoring and system improvement
5. **requirements.txt**: Dependencies (currently just Python standard library)

## Installation

1. Clone or download this repository
2. Navigate to the project directory
3. No additional dependencies required (uses only Python standard library)

## Usage

Run the system with:
```bash
python main.py
```

Then enter text to analyze. The system will:
1. Analyze the text for harmful content
2. Log the analysis
3. Provide an appropriate response
4. Continue until you type 'quit', 'exit', or 'q'

## Harmful Categories Detected

- **Violence**: Language depicting or encouraging physical violence
- **Hate Speech**: Explicit hate speech targeting protected characteristics
- **Harassment**: Personal attacks and harassment
- **Self-harm**: Language indicating self-harm or suicidal ideation
- **Illegal Activities**: Language promoting or depicting illegal activities
- **Sexual Exploitation**: Language depicting sexual exploitation or abuse
- **Terrorism**: Language promoting terrorism or extremist ideology
- **Harmful Intent**: Language indicating harmful intent or desire for retaliation

## Response Levels

- **Safe**: Positive reinforcement for constructive content
- **Warning**: Gentle reminders for borderline content
- **Intervention**: Clear guidance for moderate harmful content
- **Blocking**: Firm rejection for severe harmful content

## Customization

Adjust sensitivity thresholds in `ResponseHandler` class:
- `warning_threshold`: Lower bound for warning responses (default: 0.3)
- `intervention_threshold`: Lower bound for intervention responses (default: 0.6)
- `blocking_threshold`: Lower bound for blocking responses (default: 0.8)

Modify patterns in `HarmfulLanguageDetector` class to add or refine detection logic.

## Logs

The system creates a `logs` directory containing:
- `analysis.log`: All analysis events
- `stats.log`: Statistical data for monitoring
- `detailed.log`: Detailed information about harmful content

## Mission Statement

This system embodies the principle: "Human Care Through Applied Logic To Prevent Harmful Language To End Harmful Actions." By detecting harmful language early and responding appropriately, we aim to prevent harmful actions before they occur, fostering safer and more respectful digital environments.

## License

MIT License - Feel free to use, modify, and distribute this system to promote human care and prevent harmful actions.