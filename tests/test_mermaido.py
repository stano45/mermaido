import pytest
import mermaido

DIAGRAM = "graph TD; A-->B;"


def test_not_installed_error(tmp_path, monkeypatch):
    monkeypatch.setattr(mermaido, "_MMDC", tmp_path / "nonexistent" / "mmdc")
    with pytest.raises(mermaido.MermaidoNotInstalledError, match="mermaido install"):
        mermaido.render(DIAGRAM, tmp_path / "out.png")


def test_is_installed():
    assert mermaido.is_installed()


def test_render_png(tmp_path):
    out = tmp_path / "out.png"
    result = mermaido.render(DIAGRAM, out)
    assert result.exists()
    assert result.stat().st_size > 0


def test_render_svg_string():
    svg = mermaido.render_to_string(DIAGRAM, fmt="svg")
    assert "<svg" in svg
