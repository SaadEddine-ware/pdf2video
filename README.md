# pdf2video

Convert any PDF course into an animated educational video. Uses Manim under the hood
to generate real motion graphics -- text writes itself in, bullets slide, elements animate.

## Install

```bash
pip install pdf2video
```

Or one-liner (installs everything including ffmpeg, tesseract):

```bash
curl -sSf https://raw.githubusercontent.com/SaadEddine-ware/pdf2video/main/install.sh | bash
```

## Usage

```bash
pdf2video /path/to/course.pdf
pdf2video /path/to/course.pdf -o output.mp4
pdf2video /path/to/course.pdf --quality qh
pdf2video /path/to/course.pdf --code-only
```

## Quality Flags

| Flag | Resolution | FPS | Use case         |
|------|-----------|-----|------------------|
| ql   | 480p      | 15  | Quick preview    |
| qm   | 720p      | 30  | Standard quality |
| qh   | 1080p     | 60  | High quality     |
| qk   | 2160p     | 60  | 4K (slow)        |

## Requirements

- Python 3.10+
- ffmpeg, tesseract-ocr (installed automatically by install.sh)
- System libraries: `libpango1.0-dev libcairo2-dev pkg-config` (Linux only)

## Docker

```bash
docker run --rm -v $(pwd):/data theakumaa/pdf2video /data/course.pdf -o /data/output.mp4
```

## Project Structure

```
pdf2video/
    __init__.py
    cli.py              CLI and orchestration
    extractor.py        PDF text extraction (with OCR)
    codegen.py          Manim scene code generation
    renderer.py         Manim rendering + ffmpeg concat
```

## How It Works

1. **Extract** -- pdfplumber reads the PDF. Scanned PDFs use PyMuPDF + Tesseract OCR.
2. **Generate** -- Content is converted into Manim Python code with animated scenes.
3. **Render** -- Manim renders each scene, ffmpeg concatenates into a single MP4.

## Customizing Animations

```bash
# Generate code without rendering
pdf2video course.pdf --code-only

# Edit the generated file
nano output/course_manim.py

# Render manually
manim render -qh output/course_manim.py
```

## License

MIT
