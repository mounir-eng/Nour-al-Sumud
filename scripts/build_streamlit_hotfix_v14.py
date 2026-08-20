from __future__ import annotations

import hashlib
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT.parent
PACKAGE = OUT / "student_samed_platform_ui_v14_streamlit_fix.zip"
CHECKSUMS = OUT / "student_samed_streamlit_v14_checksums.txt"


def excluded(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    parts = set(rel.parts)
    return bool(parts & {"__pycache__", ".git", ".venv", "venv", ".pytest_cache"}) or path.suffix in {".pyc", ".pyo"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    for cache in ROOT.rglob("__pycache__"):
        if cache.is_dir():
            shutil.rmtree(cache)
    if PACKAGE.exists():
        PACKAGE.unlink()
    prefix = ROOT.name
    with zipfile.ZipFile(PACKAGE, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(ROOT.rglob("*")):
            if path.is_file() and not excluded(path):
                archive.write(path, f"{prefix}/{path.relative_to(ROOT).as_posix()}")
    required = [
        f"{prefix}/app.py",
        f"{prefix}/streamlit_dashboard_v13.py",
        f"{prefix}/dashboard_component/index.html",
        f"{prefix}/dashboard_component/dashboard.css",
        f"{prefix}/RELEASE_V14_AR.txt",
        f"{prefix}/scripts/streamlit_ui_v14_stub_qa.py",
        f"{prefix}/scripts/streamlit_dashboard_v14_browser_qa.js",
        f"{prefix}/previews/streamlit_dashboard_v14_desktop.png",
        f"{prefix}/previews/streamlit_dashboard_v14_mobile.png",
        f"{prefix}/unit_packs/physics12_unit1_complete_offline.zip",
        f"{prefix}/unit_packs/chemistry12_unit1_complete_offline.zip",
    ]
    with zipfile.ZipFile(PACKAGE) as archive:
        assert archive.testzip() is None
        names = set(archive.namelist())
        missing = [name for name in required if name not in names]
        assert not missing, missing
        count = len(names)
        raw_size = sum(item.file_size for item in archive.infolist())
    files = [
        PACKAGE,
        ROOT / "previews" / "streamlit_dashboard_v14_desktop.png",
        ROOT / "previews" / "streamlit_dashboard_v14_mobile.png",
    ]
    lines = ["STREAMLIT_UI_V14_HOTFIX_RELEASE", ""]
    for path in files:
        lines.append(f"{path.name}\t{path.stat().st_size} bytes\tSHA256 {sha256(path)}")
    lines.append("")
    lines.append(f"archive_members\t{count}")
    lines.append(f"archive_uncompressed_bytes\t{raw_size}")
    CHECKSUMS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{PACKAGE.name}\t{PACKAGE.stat().st_size} bytes\t{count} files\tSHA256 {sha256(PACKAGE)}")
    print("STREAMLIT_UI_V14_HOTFIX_BUILT")


if __name__ == "__main__":
    main()
