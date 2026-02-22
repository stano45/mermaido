from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

from nodejs_wheel import npm
from platformdirs import user_cache_dir

MMDC_VERSION = os.environ.get("MERMAIDO_MMDC_VERSION", "11.4.2")

_CACHE = Path(user_cache_dir("mermaido"))
_MMDC = _CACHE / "node_modules" / ".bin" / "mmdc"
_PUPPETEER_CFG = _CACHE / "puppeteer-config.json"

_PUPPETEER_ARGS = {"args": ["--no-sandbox", "--disable-setuid-sandbox"]}


class MermaidoError(RuntimeError):
    """Base exception for all mermaido errors."""


class MermaidoNotInstalledError(MermaidoError):
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
    npm(
        ["install", f"@mermaid-js/mermaid-cli@{MMDC_VERSION}"],
        cwd=str(_CACHE),
        check=True,
    )


def _build_cmd(
    input_path: str,
    output_path: str,
    *,
    theme: str | None,
    background_color: str | None,
    width: int | None,
    height: int | None,
    scale: int | None,
    config_file: str | Path | None,
    css_file: str | Path | None,
    pdf_fit: bool,
) -> list[str]:
    cmd = [str(_MMDC), "-i", input_path, "-o", output_path, "-p", str(_PUPPETEER_CFG)]
    if theme is not None:
        cmd += ["-t", theme]
    if background_color is not None:
        cmd += ["-b", background_color]
    if width is not None:
        cmd += ["-w", str(width)]
    if height is not None:
        cmd += ["-H", str(height)]
    if scale is not None:
        cmd += ["-s", str(scale)]
    if config_file is not None:
        cmd += ["-c", str(config_file)]
    if css_file is not None:
        cmd += ["-C", str(css_file)]
    if pdf_fit:
        cmd += ["-f"]
    return cmd


def render(
    diagram: str,
    output: str | Path,
    *,
    theme: str | None = None,
    background_color: str | None = None,
    width: int | None = None,
    height: int | None = None,
    scale: int | None = None,
    config_file: str | Path | None = None,
    css_file: str | Path | None = None,
    pdf_fit: bool = False,
) -> Path:
    """Render a Mermaid diagram to a file.

    The output format is determined by the file extension of *output*
    (``.png``, ``.svg``, or ``.pdf``).

    Args:
        diagram: Mermaid markup, e.g. ``"graph TD; A-->B;"``.
        output: Destination file path.
        theme: ``"default"``, ``"forest"``, ``"dark"``, or ``"neutral"``.
        background_color: CSS color for the background (e.g. ``"transparent"``).
        width: Page width in pixels.
        height: Page height in pixels.
        scale: Puppeteer device scale factor.
        config_file: Path to a Mermaid JSON config file.
        css_file: Path to a custom CSS file.
        pdf_fit: Scale the PDF to fit the chart.

    Returns:
        The output path.

    Raises:
        MermaidoNotInstalledError: If ``mermaido install`` has not been run.
        MermaidoError: If rendering fails for any reason.
    """
    _require_mmdc()
    output = Path(output)

    tmp = Path(tempfile.mktemp(suffix=".mmd"))
    tmp.write_text(diagram)
    try:
        proc = subprocess.run(
            _build_cmd(
                str(tmp), str(output),
                theme=theme,
                background_color=background_color,
                width=width,
                height=height,
                scale=scale,
                config_file=config_file,
                css_file=css_file,
                pdf_fit=pdf_fit,
            ),
            capture_output=True,
            text=True,
        )
    finally:
        tmp.unlink(missing_ok=True)

    if proc.returncode != 0:
        raise MermaidoError(proc.stderr)

    return output


def render_to_string(
    diagram: str,
    fmt: str = "svg",
    *,
    theme: str | None = None,
    background_color: str | None = None,
    width: int | None = None,
    height: int | None = None,
    scale: int | None = None,
    config_file: str | Path | None = None,
    css_file: str | Path | None = None,
    pdf_fit: bool = False,
) -> str | bytes:
    """Render a Mermaid diagram and return the content directly.

    Args:
        diagram: Mermaid markup.
        fmt: Output format, ``"png"``, ``"svg"``, or ``"pdf"``.
        theme: ``"default"``, ``"forest"``, ``"dark"``, or ``"neutral"``.
        background_color: CSS color for the background.
        width: Page width in pixels.
        height: Page height in pixels.
        scale: Puppeteer device scale factor.
        config_file: Path to a Mermaid JSON config file.
        css_file: Path to a custom CSS file.
        pdf_fit: Scale the PDF to fit the chart.

    Returns:
        ``str`` for SVG, ``bytes`` for PNG/PDF.
    """
    tmp_out = Path(tempfile.mktemp(suffix=f".{fmt}"))
    try:
        render(
            diagram, tmp_out,
            theme=theme,
            background_color=background_color,
            width=width,
            height=height,
            scale=scale,
            config_file=config_file,
            css_file=css_file,
            pdf_fit=pdf_fit,
        )
        return tmp_out.read_text() if fmt == "svg" else tmp_out.read_bytes()
    finally:
        tmp_out.unlink(missing_ok=True)
