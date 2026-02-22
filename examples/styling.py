"""Background colour, dimensions, and scale."""

import mermaido

diagram = "graph TD; A-->B; B-->C;"

# Transparent background (useful for embedding in dark UIs)
mermaido.render(diagram, "transparent.png", background_color="transparent")
print("wrote transparent.png")

# Custom dimensions and 2x scale for retina-quality output
mermaido.render(diagram, "large.png", width=1920, height=1080, scale=2)
print("wrote large.png")
