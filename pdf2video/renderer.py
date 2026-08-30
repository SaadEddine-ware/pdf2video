"""Manim rendering and video assembly."""

import os
import re
import subprocess
import tempfile


QUALITY_DIRS = {
    "-ql": "480p15",
    "-qm": "720p30",
    "-qh": "1080p60",
    "-qk": "2160p60",
}


def render_video(manim_file: str, output_path: str, quality: str = "-ql") -> str:
    """Render all Manim scenes and concatenate into final video.

    Args:
        manim_file: Path to the generated Manim Python file.
        output_path: Path for the final output MP4.
        quality: Manim quality flag (-ql, -qm, -qh, -qk).
    """
    abs_manim = os.path.abspath(manim_file)
    work_dir = os.path.dirname(abs_manim)
    manim_base = os.path.splitext(os.path.basename(manim_file))[0]

    with open(manim_file) as f:
        code = f.read()
    scene_names = re.findall(r"^class (\w+)\(Scene\):", code, re.MULTILINE)

    if not scene_names:
        raise ValueError("No scenes found in the Manim file")

    print(f"  Found {len(scene_names)} scenes")

    rendered = []
    for name in scene_names:
        print(f"  Rendering {name}...")
        cmd = ["manim", "render", quality, abs_manim, name]
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=work_dir, timeout=300
        )
        if result.returncode != 0:
            err = result.stderr[-200:] if result.stderr else "unknown error"
            print(f"  WARNING: {name} failed: {err}")
            continue

        qdir = QUALITY_DIRS.get(quality, "480p15")
        mp4 = os.path.join(work_dir, "media", "videos", manim_base, qdir, f"{name}.mp4")
        if os.path.exists(mp4):
            rendered.append(mp4)
            print(f"    OK")

    if not rendered:
        raise RuntimeError("No scenes rendered successfully")

    # Concatenate with ffmpeg
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    concat = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
    for p in rendered:
        concat.write(f"file '{os.path.abspath(p)}'\n")
    concat.close()

    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat.name,
        "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-pix_fmt", "yuv420p",
        output_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    os.unlink(concat.name)

    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {result.stderr[-300:]}")

    return output_path
