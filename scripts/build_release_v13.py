from __future__ import annotations

import hashlib
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PWA = ROOT / "static" / "pwa"
OUT = ROOT.parent
UNIT_PACKS = ROOT / "unit_packs"

PWA_README = """منصة الطالب الصامد — تشغيل نسخة PWA دون إنترنت
====================================================

الطريقة الأسرع:
1) فك ضغط الملف كاملاً في مجلد واحد.
2) افتح index.html في المتصفح.
3) إذا استخدمت خادماً محلياً أو استضافة، افتح الصفحة مرة واحدة أثناء الاتصال لتثبيت PWA، ثم تعمل دون إنترنت.
4) التقدم محفوظ محلياً على جهاز الطالب.

مهم: لا تنقل ملفاً منفرداً من المجلد؛ يجب إبقاء جميع الملفات معاً.
الإصدار: FINAL_UI_V13
"""

UNIT_README = """حزمة {label} — الصف الثاني عشر
================================

1) فك الضغط كاملاً.
2) افتح index.html.
3) ابدأ من المدخل التأسيسي، ثم مراجعة الوحدة، ثم تمارين الكتاب، ثم التدريب الإضافي.
4) تعمل الملفات مباشرة دون إنترنت، ولا تحتاج إلى خطوط أو مكتبات خارجية.

الإصدار: FINAL_UI_V13
"""

COMMON = [
    "review.js", "foundation.js", "review.css", "unit.js", "styles.css",
    "dashboard-v13.css", "icon-192.png", "icon-512.png",
    "manifest.webmanifest", "offline.html",
]
PHYSICS = COMMON + [
    "physics-hub.html", "physics-foundation.html", "physics-review.html",
    "physics-textbook.html", "unit.html", "unit-physics-foundation-data.js",
    "unit-physics-review-data.js", "unit-physics-textbook-data.js",
    "unit-momentum-data.js",
]
CHEMISTRY = COMMON + [
    "chemistry-hub.html", "chemistry-foundation.html", "chemistry-review.html",
    "chemistry-textbook.html", "chemistry-unit.html", "unit-chemistry-foundation-data.js",
    "unit-chemistry-review-data.js", "unit-chemistry-textbook-data.js",
    "unit-chemistry-data.js",
]


def add_file(zf: zipfile.ZipFile, src: Path, arcname: str) -> None:
    if not src.is_file():
        raise FileNotFoundError(src)
    zf.write(src, arcname)


def build_unit(output: Path, names: list[str], hub_name: str, label: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for name in names:
            add_file(zf, PWA / name, name)
        zf.writestr("index.html", (PWA / hub_name).read_bytes())
        zf.writestr("README_AR.txt", UNIT_README.format(label=label).encode("utf-8"))


def build_pwa(output: Path) -> None:
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(PWA.iterdir()):
            if path.is_file() and not path.name.startswith("."):
                add_file(zf, path, path.name)
        zf.writestr("README_OFFLINE_AR.txt", PWA_README.encode("utf-8"))


def excluded(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    parts = set(rel.parts)
    return bool(parts & {"__pycache__", ".git", ".venv", "venv", ".pytest_cache"}) or path.suffix in {".pyc", ".pyo"}


def build_platform(output: Path) -> None:
    prefix = ROOT.name
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(ROOT.rglob("*")):
            if path.is_file() and not excluded(path):
                add_file(zf, path, f"{prefix}/{path.relative_to(ROOT).as_posix()}")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def validate(path: Path, required: list[str]) -> tuple[int, int]:
    with zipfile.ZipFile(path) as zf:
        assert zf.testzip() is None, f"corrupt member in {path.name}"
        names = set(zf.namelist())
        missing = [name for name in required if name not in names]
        assert not missing, (path.name, missing)
        return len(names), sum(info.file_size for info in zf.infolist())


def main() -> None:
    for cache in ROOT.rglob("__pycache__"):
        if cache.is_dir():
            shutil.rmtree(cache)

    physics = OUT / "physics12_unit1_ui_v13.zip"
    chemistry = OUT / "chemistry12_unit1_ui_v13.zip"
    pwa = OUT / "student_samed_pwa_ui_v13.zip"
    platform = OUT / "student_samed_platform_ui_v13.zip"

    build_unit(physics, PHYSICS, "physics-hub.html", "الفيزياء: الزخم الخطي والدفع")
    build_unit(chemistry, CHEMISTRY, "chemistry-hub.html", "الكيمياء: البناء الإلكتروني للذرة")
    UNIT_PACKS.mkdir(exist_ok=True)
    shutil.copy2(physics, UNIT_PACKS / "physics12_unit1_complete_offline.zip")
    shutil.copy2(chemistry, UNIT_PACKS / "chemistry12_unit1_complete_offline.zip")
    build_pwa(pwa)
    shutil.copy2(pwa, UNIT_PACKS / "student_samed_pwa_offline.zip")
    build_platform(platform)

    checks = {
        platform: [f"{ROOT.name}/app.py", f"{ROOT.name}/streamlit_dashboard_v13.py", f"{ROOT.name}/static/pwa/dashboard-v13.css"],
        pwa: ["index.html", "app.js", "dashboard-v13.css", "service-worker.js", "physics-hub.html", "chemistry-hub.html"],
        physics: ["index.html", "dashboard-v13.css", "physics-hub.html", "physics-foundation.html", "physics-review.html", "physics-textbook.html", "unit.html"],
        chemistry: ["index.html", "dashboard-v13.css", "chemistry-hub.html", "chemistry-foundation.html", "chemistry-review.html", "chemistry-textbook.html", "chemistry-unit.html"],
    }
    lines = ["FINAL_UI_V13_RELEASE", ""]
    for path, required in checks.items():
        count, raw = validate(path, required)
        digest = sha256(path)
        lines.append(f"{path.name}\t{path.stat().st_size}\t{count} files\tSHA256 {digest}")
        print(lines[-1])
    (OUT / "student_samed_ui_v13_checksums.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("RELEASE_UI_V13_BUILT")


if __name__ == "__main__":
    main()
