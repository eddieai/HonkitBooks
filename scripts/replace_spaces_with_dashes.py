"""
Replace spaces with dashes in markdown filenames within a documentation folder structure.

This script recursively processes a directory tree, renaming all markdown files that contain spaces
in their names, replacing spaces with dashes. This is useful for preparing documentation files for
web publishing where spaces in URLs are problematic.

Example before:
docs/
├── chapter 1/
│   ├── page one.md
│   └── page two.md
└── chapter 2/
    └── page three.md

Example after:
docs/
├── chapter-1/
│   ├── page-one.md
│   └── page-two.md
└── chapter-2/
    └── page-three.md

Usage:
python replace_spaces_with_dashes.py [docs_folder]
"""
from pathlib import Path
import argparse


def replace_spaces_with_dashes(dir: Path) -> None:
    """
    Replace spaces with dashes in markdown filenames within a directory tree.
    
    Args:
        root_dir: Root directory to process recursively
    """
    md_files = list(dir.rglob("*.md"))
    for file in md_files:
        # Skip if filename doesn't contain spaces
        if " " not in file.name:
            continue

        # Create new path with spaces replaced by dashes
        new_name = file.with_name(file.name.replace(" ", "-"))

        # Rename the file
        file.rename(new_name)
        print(f"Renamed: {file} -> {new_name}")


def main():
    """Command line interface for replacing spaces with dashes in filenames."""
    parser = argparse.ArgumentParser(
        description="Replace spaces with dashes in markdown filenames"
    )
    parser.add_argument(
        "directory",
        type=Path,
        default=Path("./docs"),
        nargs="?",
        help="Root directory to process (default: ./docs)"
    )
    args = parser.parse_args()
    
    replace_spaces_with_dashes(args.directory)


if __name__ == "__main__":
    main()
