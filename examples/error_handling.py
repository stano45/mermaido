"""Graceful error handling for invalid diagrams."""

import mermaido

try:
    mermaido.render("graph TDf; fdsA-->dfB;", "bad.png")
except mermaido.MermaidoError as exc:
    print("Caught MermaidoError:")
    print(exc)
