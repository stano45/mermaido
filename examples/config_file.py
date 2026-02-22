"""Use a Mermaid JSON config file for advanced customisation."""

import json
from pathlib import Path

import mermaido

diagram = """
sequenceDiagram
    Alice->>Bob: Hello Bob!
    Bob-->>Alice: Hi Alice!
"""

# Write a mermaid config (same format as mermaid's initialize() options)
config = {"sequence": {"mirrorActors": False, "actorMargin": 120}}
config_path = Path("mermaid-config.json")
config_path.write_text(json.dumps(config))

mermaido.render(diagram, "with_config.png", config_file=config_path)
print("wrote with_config.png")

config_path.unlink()
