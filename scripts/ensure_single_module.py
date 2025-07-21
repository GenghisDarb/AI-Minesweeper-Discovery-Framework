#!/usr/bin/env python3
"""
Fail fast if both editable-install AND src-path copies of ai_minesweeper are present.

Usage:  python scripts/ensure_single_module.py
Returns exit-status 1 (and prints an error) if duplication is detected.
"""

import importlib.util as _ilu
import pathlib
import sys

pkg = "ai_minesweeper"


def _location(modname: str) -> pathlib.Path | None:
    spec = _ilu.find_spec(modname)
    return pathlib.Path(spec.origin).resolve().parent if spec else None


site_pkg = _location(pkg)
src_pkg = pathlib.Path("src", pkg).resolve()
if site_pkg and site_pkg != src_pkg and src_pkg.exists():
    sys.stderr.write(
        f"[ensure_single_module] duplicate {pkg} detected:\n"
        f"  • site-packages → {site_pkg}\n"
        f"  • src path      → {src_pkg}\n"
        "Remove one of these paths or adjust PYTHONPATH.\n"
    )
    sys.exit(1)

sys.exit(0)
