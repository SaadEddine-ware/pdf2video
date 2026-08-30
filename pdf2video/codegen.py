"""Manim scene code generator - rich animations."""

import re
import textwrap


def _clean(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def _make_title_scene(cls: str, title: str) -> str:
    return (
        f'class {cls}(Scene):\n'
        f'    def construct(self):\n'
        f'        self.camera.background_color = "#0f172a"\n'
        f'\n'
        f'        grid = VGroup()\n'
        f'        for x in range(-8, 9):\n'
        f'            for y in range(-5, 6):\n'
        f'                sq = Square(side_length=0.5, stroke_color=WHITE, stroke_width=0.5, stroke_opacity=0.08)\n'
        f'                sq.move_to([x * 0.5, y * 0.5, 0])\n'
        f'                grid.add(sq)\n'
        f'        self.play(FadeIn(grid, run_time=1))\n'
        f'\n'
        f'        title = Text("{_clean(title)}", font_size=52, color=WHITE, weight=BOLD)\n'
        f'        title.move_to(ORIGIN)\n'
        f'        self.play(Write(title, run_time=3))\n'
        f'        self.wait(0.5)\n'
        f'\n'
        f'        line = Line(LEFT * 4, RIGHT * 4, color=BLUE, stroke_width=4)\n'
        f'        line.move_to(DOWN * 1.0)\n'
        f'        self.play(Create(line, run_time=1))\n'
        f'\n'
        f'        sub = Text("Cours interactif", font_size=28, color=TEAL)\n'
        f'        sub.move_to(DOWN * 1.5)\n'
        f'        self.play(FadeIn(sub, shift=UP * 0.5), run_time=1)\n'
        f'        self.wait(2)\n'
        f'\n'
        f'        self.play(\n'
        f'            FadeOut(title, shift=UP * 0.5),\n'
        f'            FadeOut(line, shift=UP * 0.5),\n'
        f'            FadeOut(sub, shift=UP * 0.5),\n'
        f'            FadeOut(grid, shift=UP * 0.5),\n'
        f'            run_time=1.5\n'
        f'        )\n'
    )


def _make_bullets_scene(cls: str, title: str, items: list[str]) -> str:
    lines = []
    lines.append(f'class {cls}(Scene):')
    lines.append(f'    def construct(self):')
    lines.append(f'        self.camera.background_color = "#0f172a"')
    lines.append(f'')
    lines.append(f'        title = Text("{_clean(title)}", font_size=38, color=WHITE, weight=BOLD)')
    lines.append(f'        title.to_edge(UP, buff=0.6)')
    lines.append(f'        self.play(FadeIn(title, shift=LEFT * 2), run_time=1)')
    lines.append(f'')
    lines.append(f'        line = Line(title.get_left(), title.get_right(), color=BLUE, stroke_width=3)')
    lines.append(f'        line.move_to(title.get_bottom() + DOWN * 0.15)')
    lines.append(f'        self.play(Create(line, run_time=0.8))')
    lines.append(f'')
    lines.append(f'        colors = [TEAL, BLUE, PURPLE, GREEN, ORANGE, PINK]')

    for i, item in enumerate(items[:6]):
        lines.append(f'')
        lines.append(f'        dot_{i} = Dot(color=colors[{i}], radius=0.12)')
        lines.append(f'        dot_{i}.move_to(LEFT * 5.5 + DOWN * ({i} * 0.8))')
        lines.append(f'        txt_{i} = Text("{_clean(item)}", font_size=22, color=WHITE)')
        lines.append(f'        txt_{i}.next_to(dot_{i}, RIGHT, buff=0.3)')
        lines.append(f'        self.play(')
        lines.append(f'            GrowFromCenter(dot_{i}, run_time=0.3),')
        lines.append(f'            FadeIn(txt_{i}, shift=LEFT * 0.3, run_time=0.4),')
        lines.append(f'        )')
        lines.append(f'        self.wait(0.3)')

    lines.append(f'')
    lines.append(f'        self.wait(2)')
    lines.append(f'        self.play(')
    lines.append(f'            *[FadeOut(m, shift=RIGHT * 2) for m in self.mobjects],')
    lines.append(f'            run_time=1')
    lines.append(f'        )')

    return "\n".join(lines) + "\n"


def _make_summary_scene(cls: str, items: list[str]) -> str:
    lines = []
    lines.append(f'class {cls}(Scene):')
    lines.append(f'    def construct(self):')
    lines.append(f'        self.camera.background_color = "#0f172a"')
    lines.append(f'')
    lines.append(f'        title = Text("Points Cles a Retenir", font_size=42, color=WHITE, weight=BOLD)')
    lines.append(f'        title.to_edge(UP, buff=0.5)')
    lines.append(f'        self.play(Write(title, run_time=2))')
    lines.append(f'')
    lines.append(f'        line = Line(LEFT * 3, RIGHT * 3, color=TEAL, stroke_width=3)')
    lines.append(f'        line.next_to(title, DOWN, buff=0.2)')
    lines.append(f'        self.play(Create(line), run_time=0.5)')

    for i, item in enumerate(items[:6]):
        lines.append(f'')
        lines.append(f'        check_{i} = Text(">>", font_size=24, color=GREEN)')
        lines.append(f'        txt_{i} = Text("{_clean(item)}", font_size=22, color=WHITE)')
        lines.append(f'        row_{i} = VGroup(check_{i}, txt_{i}).arrange(RIGHT, buff=0.2)')
        lines.append(f'        row_{i}.move_to(UP * (2 - {i} * 0.8))')
        lines.append(f'        self.play(')
        lines.append(f'            FadeIn(check_{i}, shift=LEFT * 0.5, run_time=0.3),')
        lines.append(f'            Write(txt_{i}, run_time=0.8),')
        lines.append(f'        )')
        lines.append(f'        self.wait(0.4)')

    lines.append(f'')
    lines.append(f'        self.wait(3)')
    lines.append(f'        self.play(')
    lines.append(f'            *[m.animate.scale(0.3).set_opacity(0) for m in self.mobjects],')
    lines.append(f'            run_time=2')
    lines.append(f'        )')
    lines.append(f'')
    lines.append(f'        thanks = Text("Merci!", font_size=56, color=TEAL, weight=BOLD)')
    lines.append(f'        thanks.move_to(ORIGIN)')
    lines.append(f'        self.play(Write(thanks, run_time=1.5))')
    lines.append(f'        self.wait(2)')
    lines.append(f'        self.play(FadeOut(thanks), run_time=1)')

    return "\n".join(lines) + "\n"


def generate_manim_code(sections: list[dict], course_title: str, output_path: str) -> str:
    """Generate Manim code with rich animations from extracted sections."""
    class_name = re.sub(r"[^a-zA-Z0-9]", "", course_title.title().replace(" ", "")) or "Course"

    header = 'from manim import *\n\nconfig.media_dir = "media"\n\n'
    scenes = []
    scenes.append(_make_title_scene(f"{class_name}Title", course_title))

    for i, section in enumerate(sections):
        name = f"{class_name}S{i+1:02d}"
        scenes.append(_make_bullets_scene(name, section["title"], section["items"]))

    all_items = []
    for s in sections[:6]:
        all_items.extend(s["items"][:3])
    scenes.append(_make_summary_scene(f"{class_name}Summary", all_items[:6]))

    full_code = header + "\n".join(scenes)

    with open(output_path, "w") as f:
        f.write(full_code)

    return output_path
