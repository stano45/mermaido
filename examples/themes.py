"""Render the same diagram with every built-in theme."""

import mermaido

diagram = """
graph LR
    A[Client] --> B[Load Balancer]
    B --> C[Server 1]
    B --> D[Server 2]
"""

for theme in ("default", "forest", "dark", "neutral"):
    mermaido.render(diagram, f"theme_{theme}.png", theme=theme)
    print(f"wrote theme_{theme}.png")
