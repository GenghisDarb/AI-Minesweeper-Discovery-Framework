import os
import sys

src_path = os.path.abspath("src/ai_minesweeper")
site_packages_path = os.path.join(
    sys.prefix,
    "lib",
    f"python{sys.version_info.major}.{sys.version_info.minor}",
    "site-packages",
    "ai_minesweeper",
)

if os.path.exists(src_path) and os.path.exists(site_packages_path):
    print("Error: Both 'src/ai_minesweeper' and a site-packages copy exist.")
    sys.exit(1)
