# mermaido

Render [Mermaid](https://mermaid.js.org/) diagrams from Python — no Node.js required.

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

```python
import mermaido

# Render to a file
mermaido.render("graph TD; A-->B;", "output.png")
mermaido.render("graph TD; A-->B;", "output.svg", fmt="svg")

# Render to a string
svg = mermaido.render_to_string("graph TD; A-->B;")
```

## CLI

`mermaido` is a drop-in replacement for `mmdc`:

```bash
mermaido -i diagram.mmd -o output.svg
mermaido -i diagram.mmd -o output.png -t dark
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
