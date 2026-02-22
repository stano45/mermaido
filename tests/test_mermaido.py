import pytest
import mermaido

DIAGRAM = "graph TD; A-->B;"


def test_not_installed_error(tmp_path, monkeypatch):
    monkeypatch.setattr(mermaido, "_MMDC", tmp_path / "nonexistent" / "mmdc")
    with pytest.raises(mermaido.MermaidoNotInstalledError, match="mermaido install"):
        mermaido.render(DIAGRAM, tmp_path / "out.png")


def test_not_installed_is_mermaido_error(tmp_path, monkeypatch):
    monkeypatch.setattr(mermaido, "_MMDC", tmp_path / "nonexistent" / "mmdc")
    with pytest.raises(mermaido.MermaidoError):
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


def test_invalid_diagram_raises_mermaido_error(tmp_path):
    with pytest.raises(mermaido.MermaidoError) as exc_info:
        mermaido.render("graph TDf; fdsA-->dfB;", tmp_path / "out.png")
    assert "Error" in str(exc_info.value)


def test_render_to_string_invalid_diagram():
    with pytest.raises(mermaido.MermaidoError):
        mermaido.render_to_string("graph TDf; fdsA-->dfB;")


def test_render_theme(tmp_path):
    for theme in ("default", "forest", "dark", "neutral"):
        out = tmp_path / f"{theme}.png"
        mermaido.render(DIAGRAM, out, theme=theme)
        assert out.stat().st_size > 0


def test_render_background_color(tmp_path):
    out = tmp_path / "transparent.png"
    mermaido.render(DIAGRAM, out, background_color="transparent")
    assert out.stat().st_size > 0


def test_render_dimensions(tmp_path):
    out = tmp_path / "wide.png"
    mermaido.render(DIAGRAM, out, width=1200, height=400)
    assert out.stat().st_size > 0


def test_render_scale(tmp_path):
    normal = tmp_path / "normal.png"
    scaled = tmp_path / "scaled.png"
    mermaido.render(DIAGRAM, normal)
    mermaido.render(DIAGRAM, scaled, scale=2)
    assert scaled.stat().st_size > normal.stat().st_size


def test_render_config_file(tmp_path):
    cfg = tmp_path / "config.json"
    cfg.write_text('{"theme": "forest"}')
    out = tmp_path / "out.png"
    mermaido.render(DIAGRAM, out, config_file=cfg)
    assert out.stat().st_size > 0


def test_render_css_file(tmp_path):
    css = tmp_path / "custom.css"
    css.write_text("body { background: red; }")
    out = tmp_path / "out.png"
    mermaido.render(DIAGRAM, out, css_file=css)
    assert out.stat().st_size > 0


def test_render_pdf_fit(tmp_path):
    out = tmp_path / "out.pdf"
    mermaido.render(DIAGRAM, out, pdf_fit=True)
    assert out.stat().st_size > 0


def test_render_to_string_with_options():
    svg = mermaido.render_to_string(DIAGRAM, theme="dark", background_color="transparent")
    assert "<svg" in svg
