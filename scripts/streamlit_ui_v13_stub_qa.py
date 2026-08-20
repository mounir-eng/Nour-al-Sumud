from __future__ import annotations

import importlib
import sys
import types

rendered: list[str] = []
buttons: list[str] = []


class Context:
    def __enter__(self):
        return fake

    def __exit__(self, exc_type, exc, tb):
        return False


def markdown(body, **kwargs):
    rendered.append(str(body))


def columns(spec, **kwargs):
    count = spec if isinstance(spec, int) else len(spec)
    return [Context() for _ in range(count)]


def tabs(labels):
    return [Context() for _ in labels]


def button(label, **kwargs):
    buttons.append(str(label))
    return False


def download_button(label, *args, **kwargs):
    buttons.append(str(label))
    return False


fake = types.ModuleType("streamlit")
fake.markdown = markdown
fake.columns = columns
fake.tabs = tabs
fake.button = button
fake.download_button = download_button
fake.popover = lambda *args, **kwargs: Context()
fake.expander = lambda *args, **kwargs: Context()
fake.caption = lambda *args, **kwargs: None
fake.info = lambda *args, **kwargs: None
fake.link_button = lambda label, *args, **kwargs: buttons.append(str(label))
sys.modules["streamlit"] = fake

module = importlib.import_module("streamlit_dashboard_v13")
assert module.DASHBOARD_UI_VERSION == "final-ui-v13-figma-rtl"
result = module.render_dashboard_v13(
    profile={"name": "منير", "grade": 12, "subjects": ["phys", "chem"]},
    safe_name="منير",
    grade_label="الثاني عشر",
    overall_pct=30,
    done=12,
    selected_total=40,
    xp=1250,
    allowed=["phys", "chem"],
    physics_live=True,
    chemistry_live=True,
    stage_progress={"phys": [100, 40, 0, 0], "chem": [0, 0, 0, 0]},
    unit_progress={"phys": 30, "chem": 0},
    unit_bytes=lambda name: b"PK\x03\x04",
)
assert result is None
joined = "\n".join(rendered)
for token in [
    "dashboard-final-ui-v13", "مرحبًا منير", "30%", "مسارك المتدرج",
    "مدخل تأسيسي", "مراجعة الوحدة", "تمارين الكتاب", "تدريب إضافي",
    "الزخم الخطي والدفع", "الكهرباء الساكنة", "البناء الإلكتروني للذرة",
    "#f8fafc", "linear-gradient",
]:
    assert token in joined, token
assert "تابع التعلّم ←" in buttons
assert "⚙ الإعدادات" not in buttons  # popover trigger is rendered by Streamlit itself.
assert len(buttons) >= 9, buttons

app_source = open("app.py", encoding="utf-8").read()
assert 'DASHBOARD_UX_VERSION = "final-ui-v13-figma-rtl"' in app_source
assert "render_dashboard_v13(" in app_source
assert '"phys_1": ("physics_review"' in app_source
assert '"chem_3": ("chem_app"' in app_source
print("STREAMLIT_UI_V13_STUB_QA_OK")
