# pdf2video

Convert any PDF course into an animated educational video. Uses Manim under the hood
to generate real motion graphics -- text writes itself in, bullets slide, elements animate.

## Quick Start

### Linux

```bash
# Clone or download the project
cd pdf-to-video

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install system dependencies (Ubuntu/Debian/Kali)
sudo apt install ffmpeg libpango1.0-dev libcairo2-dev pkg-config

# Convert a PDF
python run.py courses/client_server.pdf
```

### Windows

```powershell
# Clone or download the project
cd pdf-to-video

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install ffmpeg
# Download from https://ffmpeg.org/download.html
# Add to your system PATH

# Convert a PDF
python run.py courses\client_server.pdf
```

## Usage

```bash
# Activate virtualenv first (every new terminal session)
source venv/bin/activate        # Linux
venv\Scripts\activate           # Windows

# Basic usage (480p, fast render)
python run.py courses/my_course.pdf

# Specify output path
python run.py courses/my_course.pdf -o output/my_video.mp4

# Higher quality
python run.py courses/my_course.pdf --quality qm    # 720p30
python run.py courses/my_course.pdf --quality qh    # 1080p60
python run.py courses/my_course.pdf --quality qk    # 2160p60 (4K)

# Combine flags
python run.py courses/my_course.pdf --quality qh -o output/custom.mp4

# Generate Manim code only (edit before rendering)
python run.py courses/my_course.pdf --code-only
```

## Project Structure

```
pdf-to-video/
    run.py                  Entry point
    requirements.txt        Python dependencies
    pdf2video/
        __init__.py
        cli.py              CLI and orchestration
        extractor.py        PDF text extraction
        codegen.py          Manim scene code generation
        renderer.py         Manim rendering + ffmpeg concat
    courses/                Put your PDF courses here
    output/                 Generated videos and code
    examples/               Sample output videos
```

## How It Works

1. **Extract** -- pdfplumber reads the PDF and detects headings, bullet points,
   and paragraph text.

2. **Generate** -- The extractor output is converted into Manim Python code.
   Each section becomes an animated scene with text writing, colored bullets,
   and smooth transitions.

3. **Render** -- Manim renders each scene individually, then ffmpeg concatenates
   them into a single MP4 video.

## Customizing Animations

Use `--code-only` to generate the Manim file without rendering. Edit the
generated Python file to change colors, timing, fonts, or add custom animations,
then render manually:

```bash
# Generate code
python run.py courses/my_course.pdf --code-only

# Edit the file
nano output/my_course_manim.py

# Render
manim render -qh output/my_course_manim.py
```

## Manim Quality Flags

| Flag | Resolution | FPS  | Use case           |
|------|-----------|------|---------------------|
| ql   | 480p      | 15   | Quick preview       |
| qm   | 720p      | 30   | Standard quality    |
| qh   | 1080p     | 60   | High quality        |
| qk   | 2160p     | 60   | 4K (slow)           |

## Requirements

- Python 3.10+
- ffmpeg
- System libraries for Manim (pango, cairo) -- Linux only
  - `sudo apt install libpango1.0-dev libcairo2-dev pkg-config`

## Troubleshooting

**"No module named manim"**
Make sure the virtualenv is activated:
```bash
source venv/bin/activate
```

**"pangocairo >= 1.30.0 is required"**
Install the pango development headers:
```bash
sudo apt install libpango1.0-dev
```

**"ffmpeg not found"**
Install ffmpeg:
```bash
sudo apt install ffmpeg       # Linux
choco install ffmpeg          # Windows (via Chocolatey)
```

**Rendered video is blank or has errors**
Use `--code-only` to inspect the generated Manim code. Some PDF layouts
may produce sections that Manim cannot render cleanly. Edit the generated
file to fix the issue, then render manually.

## License

MIT
