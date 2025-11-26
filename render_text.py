from pathlib import Path
import argparse
from PIL import Image

DIR = Path(__file__).parent
EXAMPLES = DIR / "examples"
SCALE, MARGIN, SPACER = 10, 3, 1


def load_glyphs_from_bin(path=DIR / "glyph_matrices.bin"):
    if not path.exists():
        return {}
    data = path.read_bytes()
    if len(data) < 4 or data[:3] != b"3X3":
        raise ValueError("Invalid font binary (bad magic).")
    version = data[3]
    if version != 2:
        raise ValueError(f"Unsupported font version: {version}")

    bits = []
    for byte in data[4:]:
        bits.extend((byte >> i) & 1 for i in range(8))

    needed = 26 * 9
    if len(bits) < needed:
        raise ValueError("Incomplete font binary (not enough bits).")
    bits = bits[:needed]

    g = {}
    idx = 0
    for letter in (chr(i) for i in range(ord("a"), ord("z") + 1)):
        mat = [[0] * 3 for _ in range(3)]
        for r in range(3):
            for c in range(3):
                mat[r][c] = bits[idx]
                idx += 1
        g[letter] = mat
    return g


def render(text, glyphs):
    blank = [[0] * 3 for _ in range(3)]
    seq = [blank if c == " " else glyphs.get(c.lower(), blank) for c in text] or [blank]
    w = len(seq) * 3 + max(0, len(seq) - 1) * SPACER
    canvas = Image.new("RGBA", (w, 3), (0, 0, 0, 0))
    x = 0
    for i, g in enumerate(seq):
        for y, row in enumerate(g):
            for dx, v in enumerate(row):
                if v:
                    canvas.putpixel((x + dx, y), (0, 0, 0, 255))
        x += 3 + (SPACER if i < len(seq) - 1 else 0)
    bg = Image.new("RGBA", (canvas.width + 2 * MARGIN, canvas.height + 2 * MARGIN), (255, 255, 255, 255))
    bg.alpha_composite(canvas, dest=(MARGIN, MARGIN))
    return bg.resize((bg.width * SCALE, bg.height * SCALE), Image.NEAREST)


def slug_to_text(path: Path):
    stem = path.stem.replace("-", " ").strip()
    return stem or "rendered"


def render_to_file(text, glyphs, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    render(text, glyphs).save(out_path)
    print(f"Saved {out_path.resolve()}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text")
    ap.add_argument("--output", type=Path, default=EXAMPLES / "rendered.png")
    ap.add_argument(
        "--use-examples",
        action="store_true",
        help="Regenerate every PNG in examples/ using the text inferred from its filename.",
    )
    args = ap.parse_args()

    glyphs = load_glyphs_from_bin()
    if not glyphs:
        raise SystemExit("No glyphs found (expected glyph_matrices.bin).")

    if args.use_examples:
        paths = sorted(EXAMPLES.glob("*.png"))
        if not paths:
            raise SystemExit("No example PNGs found in examples/.")
        for p in paths:
            render_to_file(slug_to_text(p), glyphs, p)
        return

    text = args.text or input("Enter text to render: ")
    slug = "-".join("".join(ch for ch in w.lower() if ch.isalnum()) for w in text.split()) or "rendered"
    out = args.output if args.output != EXAMPLES / "rendered.png" else EXAMPLES / f"{slug}.png"
    render_to_file(text, glyphs, out)


if __name__ == "__main__":
    main()
