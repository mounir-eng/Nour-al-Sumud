from __future__ import annotations

import hashlib
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT.parent
PACKAGE = OUT / "student_samed_platform_ui_v16_navigation_account.zip"
CHECKSUMS = OUT / "student_samed_streamlit_v16_checksums.txt"
PREVIEWS = [
    "landing_v16_desktop.png", "landing_v16_mobile.png",
    "account_v16_desktop.png", "account_v16_mobile.png",
    "dashboard_v16_desktop.png", "dashboard_v16_mobile.png",
    "how_it_works_v16.png",
]


def excluded(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if set(rel.parts) & {"__pycache__", ".git", ".venv", "venv", ".pytest_cache", ".mypy_cache"}:
        return True
    if path.suffix in {".pyc", ".pyo"}:
        return True
    return path.name in {
        ".DS_Store",
        "streamlit_ui_v14_stub_qa.py",
        "streamlit_ui_v15_stub_qa.py",
        "apply_ui_v16_notes.py",
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_nested(path: Path, required: list[str]) -> None:
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None, path
        names = set(archive.namelist())
        missing = [name for name in required if name not in names]
        assert not missing, (path.name, missing)


def main() -> None:
    for cache in ROOT.rglob("__pycache__"):
        if cache.is_dir():
            shutil.rmtree(cache)
    nested = {
        ROOT / "unit_packs" / "physics12_unit1_complete_offline.zip": ["index.html", "physics-foundation.html", "physics-review.html", "physics-textbook.html"],
        ROOT / "unit_packs" / "chemistry12_unit1_complete_offline.zip": ["index.html", "chemistry-foundation.html", "chemistry-review.html", "chemistry-textbook.html"],
        ROOT / "unit_packs" / "student_samed_pwa_offline.zip": ["index.html", "app.js", "service-worker.js", "manifest.webmanifest"],
    }
    for path, required in nested.items():
        validate_nested(path, required)

    if PACKAGE.exists():
        PACKAGE.unlink()
    prefix = ROOT.name
    with zipfile.ZipFile(PACKAGE, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(ROOT.rglob("*")):
            if path.is_file() and not excluded(path):
                archive.write(path, f"{prefix}/{path.relative_to(ROOT).as_posix()}")

    required = [
        f"{prefix}/app.py", f"{prefix}/streamlit_dashboard_v13.py",
        f"{prefix}/landing_component/index.html",
        f"{prefix}/onboarding_component/index.html",
        f"{prefix}/dashboard_component/index.html",
        f"{prefix}/dashboard_component/dashboard.css",
        f"{prefix}/static/pwa/index.html", f"{prefix}/static/pwa/app.js",
        f"{prefix}/static/pwa/service-worker.js",
        f"{prefix}/RELEASE_V16_AR.txt", f"{prefix}/README_AR.md",
        f"{prefix}/scripts/streamlit_ui_v16_stub_qa.py",
        f"{prefix}/scripts/ui_v16_browser_qa.js",
        f"{prefix}/scripts/pwa_v16_browser_qa.js",
        f"{prefix}/scripts/package_unit_offline_qa.js",
        f"{prefix}/scripts/build_offline_packs_v16.py",
        f"{prefix}/unit_packs/physics12_unit1_complete_offline.zip",
        f"{prefix}/unit_packs/chemistry12_unit1_complete_offline.zip",
        f"{prefix}/unit_packs/student_samed_pwa_offline.zip",
    ] + [f"{prefix}/previews/{name}" for name in PREVIEWS]
    with zipfile.ZipFile(PACKAGE) as archive:
        assert archive.testzip() is None
        names = set(archive.namelist())
        missing = [name for name in required if name not in names]
        assert not missing, missing
        count = len(names)
        raw_size = sum(item.file_size for item in archive.infolist())

    files = [PACKAGE, OUT / "student_samed_pwa_offline_v16.zip"] + [ROOT / "previews" / name for name in PREVIEWS]
    lines = ["STREAMLIT_UI_V16_NAVIGATION_ACCOUNT_RELEASE", ""]
    for path in files:
        assert path.is_file(), path
        lines.append(f"{path.name}\t{path.stat().st_size} bytes\tSHA256 {sha256(path)}")
    lines.extend(["", f"archive_members\t{count}", f"archive_uncompressed_bytes\t{raw_size}"])
    CHECKSUMS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{PACKAGE.name}\t{PACKAGE.stat().st_size} bytes\t{count} files\tSHA256 {sha256(PACKAGE)}")
    print("STREAMLIT_UI_V16_NAVIGATION_ACCOUNT_BUILT")


if __name__ == "__main__":
    main()
