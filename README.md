# pdf2video

Convert any PDF course into an animated educational video with one command.

Uses [Manim](https://www.manim.community/) under the hood to generate real motion
graphics -- text writes itself in, bullets slide in, elements animate, and backgrounds
flow. No static slides, no slide transitions. Real animation.

[![PyPI version](https://badge.fury.io/py/pdf2video.svg)](https://pypi.org/project/pdf2video/)
[![Python](https://img.shields.io/pypi/pyversions/pdf2video)](https://pypi.org/project/pdf2video/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Install

```bash
pip install pdf2video
```

That's it. The `pdf2video` command is now available everywhere.

### One-liner (with system dependencies)

If you need ffmpeg, tesseract-ocr, and other system deps installed automatically:

```bash
curl -sSf https://raw.githubusercontent.com/SaadEddine-ware/pdf2video/main/install.sh | bash
```

### System requirements (manual)

If `pip install` works but rendering fails, you may need system libraries:

```bash
# Ubuntu / Debian / Kali
sudo apt install ffmpeg libpango1.0-dev libcairo2-dev pkg-config tesseract-ocr tesseract-ocr-fra tesseract-ocr-eng
```

## Usage

```bash
# Basic -- convert a PDF to video
pdf2video course.pdf

# Specify output path
pdf2video course.pdf -o my_video.mp4

# Higher quality (slower render)
pdf2video course.pdf --quality qm    # 720p30
pdf2video course.pdf --quality qh    # 1080p60
pdf2video course.pdf --quality qk    # 4K60

# Generate Manim code only (edit before rendering)
pdf2video course.pdf --code-only

# Combine flags
pdf2video course.pdf --quality qh -o output/custom.mp4
```

## Examples

```bash
# Quick preview at 480p (fast)
pdf2video courses/algebra.pdf

# High quality render
pdf2video courses/client_server.pdf --quality qh -o videos/client_server.mp4

# Scanned PDF with OCR (works automatically)
pdf2video courses/scanned_handout.pdf

# Edit the animation yourself
pdf2video courses/physics.pdf --code-only
# -> edit output/physics_manim.py
manim render -qh output/physics_manim.py
```

## Quality Flags

| Flag | Resolution | FPS | Render Speed | Best for            |
|------|-----------|-----|-------------|---------------------|
| `ql` | 480p      | 15  | Fast        | Quick preview       |
| `qm` | 720p      | 30  | Medium      | Standard quality    |
| `qh` | 1080p     | 60  | Slow        | YouTube / teaching  |
| `qk` | 2160p     | 60  | Very slow   | 4K displays         |

## Docker

```bash
docker run --rm -v $(pwd):/data theakumaa/pdf2video /data/course.pdf -o /data/output.mp4
```

## How It Works

1. **Extract** -- [pdfplumber](https://github.com/jsvine/pdfplumber) reads digital PDFs.
   Scanned PDFs are detected automatically and processed with PyMuPDF + Tesseract OCR
   (supports French, English, and more).

2. **Generate** -- The extracted content (titles, bullet points, paragraphs) is converted
   into Manim Python code. Each section becomes an animated scene with `Write()`,
   `GrowFromCenter()`, `FadeIn` with shift, colored bullets, and grid backgrounds.

3. **Render** -- Manim renders each scene individually, then `ffmpeg` concatenates
   them into a single MP4 video.

## Project Structure

```
pdf2video/
    __init__.py         Package init (version)
    cli.py              CLI argument parsing, section merging, orchestration
    extractor.py        PDF text extraction (pdfplumber + OCR fallback)
    codegen.py          Manim scene code generation
    renderer.py         Manim rendering + ffmpeg concatenation
```

## Customizing Animations

Use `--code-only` to generate the Manim file without rendering. Edit the
generated Python file to change colors, timing, fonts, or add custom animations,
then render manually:

```bash
# Generate code
pdf2video course.pdf --code-only

# Edit the file
nano output/course_manim.py

# Render
manim render -qh output/course_manim.py
```

## Troubleshooting

**"No module named manim"**
```bash
pip install pdf2video
```

**"pangocairo >= 1.30.0 is required"**
```bash
sudo apt install libpango1.0-dev libcairo2-dev pkg-config
```

**"ffmpeg not found"**
```bash
sudo apt install ffmpeg
```

**"tesseract not found" (for scanned PDFs)**
```bash
sudo apt install tesseract-ocr tesseract-ocr-fra tesseract-ocr-eng
```

**Rendered video is blank or has errors**
Use `--code-only` to inspect the generated Manim code. Some PDF layouts
may produce sections that Manim cannot render cleanly. Edit the generated
file to fix the issue, then render manually.

**OCR is slow on large scanned PDFs**
The tool processes the first 6 pages for OCR by default. For full-document OCR,
edit `extractor.py` and remove the page limit.

## License

MIT
