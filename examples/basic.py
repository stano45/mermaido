"""Basic rendering to files and strings."""

import mermaido

diagram = """
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[OK]
    B -->|No| D[Cancel]
"""

# Output format is determined by the file extension
mermaido.render(diagram, "basic.png")
mermaido.render(diagram, "basic.svg")
mermaido.render(diagram, "basic.pdf")

# Render directly to a string (no file needed)
svg = mermaido.render_to_string(diagram)
print(f"SVG length: {len(svg)} chars")

png = mermaido.render_to_string(diagram, fmt="png")
print(f"PNG length: {len(png)} bytes")

pdf = mermaido.render_to_string(diagram, fmt="pdf")
print(f"PDF length: {len(pdf)} bytes")
