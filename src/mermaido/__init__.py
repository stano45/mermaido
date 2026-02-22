from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

from nodejs import npm
from platformdirs import user_cache_dir

MMDC_VERSION = os.environ.get("MERMAIDO_MMDC_VERSION", "11.4.0")

_CACHE = Path(user_cache_dir("mermaido"))
_MMDC = _CACHE / "node_modules" / ".bin" / "mmdc"
_PUPPETEER_CFG = _CACHE / "puppeteer-config.json"

_PUPPETEER_ARGS = {"args": ["--no-sandbox", "--disable-setuid-sandbox"]}


class MermaidoNotInstalledError(RuntimeError):
    def __init__(self):
        super().__init__(
            "mermaid-cli is not installed. Run:\n\n    mermaido install\n"
        )


def _require_mmdc():
    if not _MMDC.exists():
        raise MermaidoNotInstalledError()


def is_installed() -> bool:
    """Return True if mermaid-cli and Chromium have been installed via ``mermaido install``."""
    return _MMDC.exists()


def install() -> None:
    """Download mermaid-cli and Chromium (~200 MB). Only needed once."""
    _CACHE.mkdir(parents=True, exist_ok=True)
    _PUPPETEER_CFG.write_text(json.dumps(_PUPPETEER_ARGS))
    npm.call(
        ["install", f"@mermaid-js/mermaid-cli@{MMDC_VERSION}"],
        cwd=str(_CACHE),
    )


def render(diagram: str, output: str | Path, fmt: str = "png") -> Path:
    """Render a Mermaid diagram to a file.

    Args:
        diagram: Mermaid markup, e.g. ``"graph TD; A-->B;"``.
        output: Destination file path.
        fmt: Output format — ``"png"``, ``"svg"``, or ``"pdf"``.

    Returns:
        The output path.

    Raises:
        MermaidoNotInstalledError: If ``mermaido install`` has not been run.
    """
    _require_mmdc()
    output = Path(output)

    tmp = Path(tempfile.mktemp(suffix=".mmd"))
    tmp.write_text(diagram)
    try:
        subprocess.run(
            [str(_MMDC), "-i", str(tmp), "-o", str(output), "-p", str(_PUPPETEER_CFG)],
            check=True,
        )
    finally:
        tmp.unlink(missing_ok=True)
    return output


def render_to_string(diagram: str, fmt: str = "svg") -> str | bytes:
    """Render a Mermaid diagram and return the content directly.

    Returns ``str`` for SVG, ``bytes`` for PNG/PDF.
    """
    tmp_out = Path(tempfile.mktemp(suffix=f".{fmt}"))
    try:
        render(diagram, tmp_out, fmt=fmt)
        return tmp_out.read_text() if fmt == "svg" else tmp_out.read_bytes()
    finally:
        tmp_out.unlink(missing_ok=True)
