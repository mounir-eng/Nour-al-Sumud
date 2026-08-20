from __future__ import annotations

import hashlib
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PWA = ROOT / "static" / "pwa"
PACKS = ROOT / "unit_packs"
OUT = ROOT.parent

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
    "chemistry-textbook.html", "chemistry-unit.html",
    "unit-chemistry-foundation-data.js", "unit-chemistry-review-data.js",
    "unit-chemistry-textbook-data.js", "unit-chemistry-data.js",
]

PWA_README = """منصة الطالب الصامد — تشغيل أونلاين وأوفلاين
================================================

تشغيل مباشر دون إنترنت:
1) فك ضغط الملف كاملًا في مجلد واحد.
2) افتح index.html في المتصفح.
3) لا تنقل ملفًا منفردًا؛ أبقِ جميع الملفات معًا.

تشغيل محلي عبر بايثون (أنسب للتثبيت كتطبيق):
1) افتح نافذة الأوامر داخل المجلد.
2) شغّل: python -m http.server 8000
3) افتح: http://localhost:8000
4) افتح المنصة مرة واحدة، ثم يمكن متابعتها عند انقطاع الإنترنت.

تعمل على سطح المكتب واللوحات والهاتف، ويحفظ التقدم على جهاز الطالب.
الإصدار: UI v16
"""

UNIT_README = """حزمة {label} — الصف الثاني عشر
================================

1) فك الضغط كاملًا في مجلد واحد.
2) افتح index.html.
3) اتبع المسار: تأسيس ← مراجعة الدرس ← تمارين الكتاب ← تدريب إضافي.
4) تعمل الملفات مباشرة دون إنترنت، ولا تحتاج إلى خطوط أو مكتبات خارجية.

الإصدار: UI v16
"""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def add_file(archive: zipfile.ZipFile, source: Path, name: str) -> None:
    if not source.is_file():
        raise FileNotFoundError(source)
    archive.write(source, name)


def build_unit(output: Path, names: list[str], hub: str, label: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in names:
            add_file(archive, PWA / name, name)
        archive.writestr("index.html", (PWA / hub).read_bytes())
        archive.writestr("README_AR.txt", UNIT_README.format(label=label).encode("utf-8"))


def build_pwa(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source in sorted(PWA.iterdir()):
            if source.is_file() and not source.name.startswith("."):
                add_file(archive, source, source.name)
        archive.writestr("README_OFFLINE_AR.txt", PWA_README.encode("utf-8"))


def validate(path: Path, required: list[str]) -> tuple[int, int]:
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None, path
        names = set(archive.namelist())
        missing = [name for name in required if name not in names]
        assert not missing, (path.name, missing)
        return len(names), sum(item.file_size for item in archive.infolist())


def main() -> None:
    PACKS.mkdir(parents=True, exist_ok=True)
    physics = OUT / "physics12_unit1_offline_v16.zip"
    chemistry = OUT / "chemistry12_unit1_offline_v16.zip"
    pwa = OUT / "student_samed_pwa_offline_v16.zip"

    build_unit(physics, PHYSICS, "physics-hub.html", "الفيزياء: الزخم الخطي والدفع")
    build_unit(chemistry, CHEMISTRY, "chemistry-hub.html", "الكيمياء: البناء الإلكتروني للذرة")
    build_pwa(pwa)

    canonical = {
        physics: PACKS / "physics12_unit1_complete_offline.zip",
        chemistry: PACKS / "chemistry12_unit1_complete_offline.zip",
        pwa: PACKS / "student_samed_pwa_offline.zip",
    }
    for source, target in canonical.items():
        shutil.copy2(source, target)

    checks = {
        physics: ["index.html", "physics-foundation.html", "physics-review.html", "physics-textbook.html", "unit.html", "README_AR.txt"],
        chemistry: ["index.html", "chemistry-foundation.html", "chemistry-review.html", "chemistry-textbook.html", "chemistry-unit.html", "README_AR.txt"],
        pwa: ["index.html", "app.js", "dashboard-v13.css", "service-worker.js", "manifest.webmanifest", "physics-hub.html", "chemistry-hub.html", "README_OFFLINE_AR.txt"],
    }
    lines = ["OFFLINE_PACKS_UI_V16", ""]
    for path, required in checks.items():
        count, raw = validate(path, required)
        line = f"{path.name}\t{path.stat().st_size} bytes\t{count} files\t{raw} uncompressed bytes\tSHA256 {sha256(path)}"
        lines.append(line)
        print(line)
    (PACKS / "OFFLINE_PACKS_V16_SHA256.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("OFFLINE_PACKS_V16_BUILT")


if __name__ == "__main__":
    main()
