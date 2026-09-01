#!/usr/bin/env python3
"""
pdf2video - Convert PDF courses to animated videos.

Usage:
    pdf2video courses/my_course.pdf
    pdf2video courses/my_course.pdf -o output/custom.mp4
    pdf2video courses/my_course.pdf -q -qm
    pdf2video courses/my_course.pdf --code-only
"""

import argparse
import os
import sys

from .extractor import extract_pdf, Section
from .codegen import generate_manim_code
from .renderer import render_video


def _merge_sections(sections: list[Section], max_scenes: int = 12) -> list[Section]:
    """Merge small sections to keep total scene count manageable."""
    if len(sections) <= max_scenes:
        return sections

    # Group sections, combining small ones
    merged = []
    buffer = Section(title="", items=[])

    for sec in sections:
        if len(sec.items) <= 2 and buffer.items:
            # Small section: merge into buffer
            buffer.items.extend(sec.items)
        else:
            if buffer.items:
                merged.append(buffer)
            buffer = Section(title=sec.title, items=list(sec.items))

    if buffer.items:
        merged.append(buffer)

    # If still too many, just take the first N
    if len(merged) > max_scenes:
        merged = merged[:max_scenes]

    return merged


def main():
    parser = argparse.ArgumentParser(
        prog="pdf2video",
        description="Convert any PDF course into an animated Manim video.",
    )
    parser.add_argument("pdf", help="Path to the input PDF file")
    parser.add_argument("-o", "--output", help="Output video path (default: output/<name>.mp4)")
    parser.add_argument(
        "--quality", default="ql",
        choices=["ql", "qm", "qh", "qk"],
        help="Quality: ql=480p, qm=720p, qh=1080p, qk=4K (default: ql)",
    )
    parser.add_argument(
        "--code-only", action="store_true",
        help="Only generate Manim code, skip rendering",
    )
    args = parser.parse_args()

    if not os.path.exists(args.pdf):
        print(f"Error: file not found: {args.pdf}")
        sys.exit(1)

    basename = os.path.splitext(os.path.basename(args.pdf))[0]
    if args.output:
        if os.path.isdir(args.output):
            output_path = os.path.join(args.output, f"{basename}.mp4")
        else:
            output_path = args.output
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    else:
        output_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{basename}.mp4")
    code_path = f"output/{basename}_manim.py"

    os.makedirs("output", exist_ok=True)

    # Step 1: Extract
    print(f"[1/3] Extracting PDF...")
    title, sections = extract_pdf(args.pdf)
    print(f"      {title} -- {len(sections)} raw sections")

    # Merge small sections
    sections = _merge_sections(sections)
    print(f"      Merged to {len(sections)} scenes")

    # Step 2: Generate Manim code
    print(f"[2/3] Generating animation code...")
    sections_dicts = [{"title": s.title, "items": s.items} for s in sections]
    generate_manim_code(sections_dicts, title, code_path)
    print(f"      Saved: {code_path}")

    manim_quality = f"-{args.quality}"

    if args.code_only:
        print(f"\nDone. Render manually with:")
        print(f"  manim render {manim_quality} {code_path}")
        return

    # Step 3: Render
    print(f"[3/3] Rendering video...")
    render_video(code_path, output_path, quality=manim_quality)

    abs_path = os.path.abspath(output_path)
    print(f"\nDone!")
    print(f"  Video: {abs_path}")
    print(f"  Open:  xdg-open '{abs_path}'")


if __name__ == "__main__":
    main()
