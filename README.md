# mermaido

Render [Mermaid](https://mermaid.js.org/) diagrams from Python, no Node.js required.

`mermaido` bundles Node.js via [`nodejs-bin`](https://pypi.org/project/nodejs-bin/) and wraps [`mermaid-cli`](https://github.com/mermaid-js/mermaid-cli) so you can generate diagrams without managing any JavaScript tooling yourself.

## Install

```bash
pip install mermaido
mermaido install
```

or with [uv](https://docs.astral.sh/uv/):

```bash
uv add mermaido
uv run mermaido install
```

The `mermaido install` step downloads mermaid-cli and Chromium (~200 MB) into a local cache. You only need to run it once.

## Python API

### Render to a file

The output format is determined by the file extension (`.png`, `.svg`, or `.pdf`):

```python
import mermaido

mermaido.render("graph TD; A-->B;", "output.png")
mermaido.render("graph TD; A-->B;", "output.svg")
mermaido.render("graph TD; A-->B;", "output.pdf")
```

### Render to a string

```python
svg = mermaido.render_to_string("graph TD; A-->B;")              # str
png = mermaido.render_to_string("graph TD; A-->B;", fmt="png")   # bytes
pdf = mermaido.render_to_string("graph TD; A-->B;", fmt="pdf")   # bytes
```

### Themes

Four built-in themes: `default`, `forest`, `dark`, `neutral`.

```python
mermaido.render(diagram, "dark.png", theme="dark")
mermaido.render(diagram, "forest.svg", theme="forest")
```

### Background colour

Any CSS colour value. Use `"transparent"` for no background:

```python
mermaido.render(diagram, "out.png", background_color="transparent")
mermaido.render(diagram, "out.png", background_color="#1a1a2e")
```

### Dimensions and scale

```python
mermaido.render(diagram, "out.png", width=1920, height=1080)
mermaido.render(diagram, "retina.png", scale=2)
```

### Mermaid config file

Pass a JSON config file with [Mermaid configuration options](https://mermaid.js.org/config/schema-docs/config.html):

```python
mermaido.render(diagram, "out.png", config_file="mermaid-config.json")
```

### Custom CSS

```python
mermaido.render(diagram, "out.png", css_file="custom.css")
```

### PDF fit

Scale the PDF to fit the chart:

```python
mermaido.render(diagram, "out.pdf", pdf_fit=True)
```

### All options at a glance

Both `render()` and `render_to_string()` accept these keyword arguments:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `theme` | `str` | mmdc default (`"default"`) | `"default"`, `"forest"`, `"dark"`, or `"neutral"` |
| `background_color` | `str` | mmdc default (`"white"`) | Any CSS colour value |
| `width` | `int` | mmdc default (`800`) | Page width in pixels |
| `height` | `int` | mmdc default (`600`) | Page height in pixels |
| `scale` | `int` | mmdc default (`1`) | Puppeteer device scale factor |
| `config_file` | `str \| Path` | `None` | Path to a Mermaid JSON config file |
| `css_file` | `str \| Path` | `None` | Path to a custom CSS file |
| `pdf_fit` | `bool` | `False` | Scale PDF to fit the chart |

### Error handling

Invalid diagrams raise `MermaidoError` instead of exposing raw subprocess internals:

```python
try:
    mermaido.render("graph TDf; oops;", "out.png")
except mermaido.MermaidoError as e:
    print(e)
```

## CLI

`mermaido` is a drop-in replacement for `mmdc`:

```bash
mermaido -i diagram.mmd -o output.svg
mermaido -i diagram.mmd -o output.png -t dark -b transparent
mermaido -i diagram.mmd -o output.pdf -f
mermaido --help
```

## Configuration

| Environment variable | Default | Description |
|---|---|---|
| `MERMAIDO_MMDC_VERSION` | `11.4.2` | mermaid-cli version to install |

## How it works

1. `pip install mermaido` installs the Python package and a bundled Node.js binary (via `nodejs-bin`).
2. `mermaido install` uses that bundled Node.js to `npm install` mermaid-cli and Chromium into a cache directory (`~/.cache/mermaido` on Linux, platform-appropriate elsewhere).
3. `mermaido.render()` or the `mermaido` CLI invokes `mmdc` from that cache.

No system-wide Node.js or npm installation is needed.

## License

MIT
