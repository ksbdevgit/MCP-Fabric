"""Build a deploy.zip with Unix-style forward slashes for Azure Linux App Service."""
import os
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(ROOT, "deploy_new.zip")

INCLUDE = [
    "fabric_rti_mcp",
    "scripts",
    ".gitignore",
    ".python-version",
    "app.py",
    "requirements.txt",
    "startup.sh",
    "pyproject.toml",
]

EXCLUDE_DIRS = {"__pycache__", ".pytest_cache", ".ruff_cache"}
EXCLUDE_EXTS = {".pyc", ".pyo"}


def should_exclude(name: str) -> bool:
    if name in EXCLUDE_DIRS:
        return True
    _, ext = os.path.splitext(name)
    return ext in EXCLUDE_EXTS


def add_path(zf: zipfile.ZipFile, path: str, arcname: str) -> None:
    if os.path.isfile(path):
        zf.write(path, arcname.replace(os.sep, "/"))
        return
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not should_exclude(d)]
        for f in files:
            if should_exclude(f):
                continue
            full = os.path.join(root, f)
            rel = os.path.relpath(full, ROOT)
            zf.write(full, rel.replace(os.sep, "/"))


def main() -> None:
    if os.path.exists(OUTPUT):
        os.remove(OUTPUT)
    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in INCLUDE:
            path = os.path.join(ROOT, item)
            if not os.path.exists(path):
                print(f"WARN: {item} not found, skipping")
                continue
            add_path(zf, path, item)
    print(f"Created {OUTPUT}")
    with zipfile.ZipFile(OUTPUT) as zf:
        names = zf.namelist()
        print(f"Total files: {len(names)}")
        print("Sample paths:")
        for n in names[:10]:
            print(f"  {n}")


if __name__ == "__main__":
    main()
