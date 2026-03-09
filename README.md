# openclaw-expert-suite

An open-source expert system rule engine and toolkit written in Python.

## Features

- **Forward-chaining inference engine** – evaluates rules in descending priority order and chains them automatically.
- **Fact base** – declare, overwrite, and retract typed facts at runtime.
- **Flexible rules** – attach any Python callable as a condition or action.
- **CLI** – load a fact file and inspect the knowledge base from the terminal.
- **Zero runtime dependencies** – pure Python 3.9+.

## Installation

```bash
pip install openclaw-expert-suite        # from PyPI (future release)
# or from source:
git clone https://github.com/rebootmindful/openclaw-expert-suite.git
cd openclaw-expert-suite
pip install -e ".[dev]"
```

## Quick start

```python
from openclaw import ExpertEngine, Fact, Rule

engine = ExpertEngine()

# Declare facts
engine.declare(Fact("temperature", 42))

# Define rules
engine.add_rule(Rule(
    name="high-temp-alert",
    condition=lambda fb: fb.has("temperature") and fb.get("temperature").value > 40,
    action=lambda fb: fb.declare(Fact("alert", "HIGH TEMPERATURE")),
    priority=10,
))

# Run inference
engine.run()

print(engine.facts.get("alert").value)  # HIGH TEMPERATURE
```

## CLI

```bash
# Print version
openclaw --version

# Load a JSON facts file and inspect facts
openclaw run path/to/facts.json
```

A facts file is a plain JSON object mapping fact names to values:

```json
{
  "temperature": 42,
  "humidity": 80,
  "location": "warehouse-A"
}
```

## Running tests

```bash
pytest
```

## License

MIT
