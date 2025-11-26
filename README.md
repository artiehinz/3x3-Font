# 3x3 Font Renderer

Render text using a custom 3x3 pixel alphabet stored in a tiny binary font and scale the output for readability while keeping the footprint minimal.

## Setup
- Requires Python 3 and Pillow (`pip install pillow`).
- Font data comes from `glyph_matrices.bin` (bundled). Rendering is binary-only—no PNG glyphs are read.

## Usage
- Render text (saves to `examples/<slug>.png` by default):
  ```bash
  python render_text.py --text "hello world"
  ```
- Choose a custom output path:
  ```bash
  python render_text.py --text "abc" --output out.png
  ```
- Run without `--text` to be prompted interactively.
- Refresh the sample outputs in `examples/` based on their filenames (hyphens become spaces):
  ```bash
  python render_text.py --use-examples
  ```

## Examples
- `examples/demo.png` -> "demo"
- `examples/test.png` -> "test"
- `examples/thank-you.png` -> "thank you"

## Details
- Letters are 3x3 pixels each and loaded as binary masks (black pixels = 1, others = 0).
- Output uses a white background, 1px spacer between letters, 3px margin, and 10x nearest-neighbor upscaling.
- Minimal-memory font format: `glyph_matrices.bin` packs every letter into 9 bits (3x3), so the full 26-letter alphabet lives in well under 40 bytes (magic `3X3`, version 2 header included). The renderer reads this binary exclusively—no PNG fallback.

## Repo Hygiene
- Generated outputs live in `examples/` (ignored by `.gitignore` alongside `__pycache__/` and any scratch assets).
