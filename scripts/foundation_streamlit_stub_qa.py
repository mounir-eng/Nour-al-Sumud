"""Runtime smoke test for the Streamlit foundation renderer without installing Streamlit."""
from __future__ import annotations

import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class Session(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name, value):
        self[name] = value


class Context:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class FakeStreamlit(types.ModuleType):
    def __init__(self):
        super().__init__("streamlit")
        self.session_state = Session()
        self.target_lesson = 0
        self.markups: list[str] = []
        self.text_inputs: list[tuple[str, dict]] = []

    def set_page_config(self, *args, **kwargs):
        return None

    def markdown(self, body, **kwargs):
        self.markups.append(str(body))

    def write(self, *args, **kwargs):
        return None

    def columns(self, spec, **kwargs):
        count = spec if isinstance(spec, int) else len(spec)
        return [Context() for _ in range(count)]

    def form(self, *args, **kwargs):
        return Context()

    def expander(self, *args, **kwargs):
        return Context()

    def container(self, *args, **kwargs):
        return Context()

    def spinner(self, *args, **kwargs):
        return Context()

    def selectbox(self, label, options, index=0, **kwargs):
        if len(options) == 8:
            return options[self.target_lesson]
        return options[index]

    def text_input(self, label, **kwargs):
        self.text_inputs.append((str(label), dict(kwargs)))
        return ""

    def form_submit_button(self, *args, **kwargs):
        return False

    def button(self, *args, **kwargs):
        return False

    def success(self, *args, **kwargs):
        return None

    def warning(self, *args, **kwargs):
        return None

    def info(self, *args, **kwargs):
        return None

    def error(self, *args, **kwargs):
        return None

    def rerun(self):
        raise AssertionError("Unexpected rerun during smoke test")

    def switch_page(self, *args, **kwargs):
        raise AssertionError("Unexpected page switch during smoke test")


fake = FakeStreamlit()
sys.modules["streamlit"] = fake

from foundation_content import FOUNDATION_COURSES  # noqa: E402
from foundation_renderer import render_foundation_course  # noqa: E402

lesson_count = 0
for course in FOUNDATION_COURSES:
    for index, lesson in enumerate(course["lessons"]):
        fake.session_state.clear()
        fake.markups.clear()
        fake.text_inputs.clear()
        fake.target_lesson = index
        render_foundation_course(course)
        rendered = "\n".join(fake.markups)
        expected_inputs = len(lesson["example"]["fields"]) + 1
        assert len(fake.text_inputs) == expected_inputs, (lesson["id"], len(fake.text_inputs), expected_inputs)
        assert all(call[1].get("label_visibility") == "collapsed" for call in fake.text_inputs), lesson["id"]
        assert "rv-simple-sentence" in rendered, lesson["id"]
        assert "rv-inline-guide" in rendered, lesson["id"]
        assert "rv-inline-token" in rendered, lesson["id"]
        assert lesson["example"]["inline_template"].count("[[") == len(lesson["example"]["fields"])
        if "→" in lesson["formula"]:
            formula_blocks = [x for x in fake.markups if "rv-equation" in x or "rv-substitution" in x]
            assert any("→" in x for x in formula_blocks), lesson["id"]
            assert all("⃗" not in x for x in formula_blocks), lesson["id"]
        lesson_count += 1

assert lesson_count == 16
print(f"STREAMLIT_FOUNDATION_V12_OK {lesson_count} lessons")
