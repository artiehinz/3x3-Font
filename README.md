# 3x3 Font Renderer

Render text using a custom 3×3 pixel alphabet (PNG glyphs) and scale the output for readability.

## Setup
- Requires Python 3 and Pillow (`pip install pillow`).
- Place 3×3 RGBA glyphs in `letters/` (one PNG per letter, named like `a.png`, `b.png`, etc.).

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

## Details
- Letters are loaded as 3×3 binary masks (black pixels = 1, others = 0).
- Output uses a white background, 1×3 spacer between letters, 3px margin, and 10× nearest-neighbor upscaling.
- A compact binary font dump is written to `glyph_matrices.bin` (magic `3X3`, version 2, bit-packed 26-letter masks).

## Repo Hygiene
- Generated outputs live in `examples/` (ignored by `.gitignore` alongside `letters/`, PNGs, binaries, and `__pycache__/`).
