"""
Generate a markdown SUMMARY.md from a folder structure of markdown files with YAML front matter.

This script processes a documentation folder structure where each markdown file contains YAML front
matter with metadata like title and nav_order. It generates a hierarchical SUMMARY.md file suitable
for GitBook or similar documentation systems.

Example folder structure:
docs/
├── README.md
├── chapter1/
│   ├── README.md
│   ├── page1.md
│   └── page2.md
└── chapter2/
    ├── README.md
    └── page3.md

Example output (SUMMARY.md):
# Summary
### Main Title
* [Main Title](./README.md)

### Chapter 1
* [Page 1](./chapter1/page1.md)
* [Page 2](./chapter1/page2.md)

### Chapter 2
* [Page 3](./chapter2/page3.md)

Usage:
python template_to_summary.py [docs_folder]
"""
from pathlib import Path
import re
from typing import Optional, Dict, List
import argparse
from dataclasses import dataclass, field


@dataclass
class Page:
    """Represents a markdown page with its metadata and content structure."""
    title: Optional[str] = None
    nav_order: Optional[float] = None
    parent: Optional['Page'] = None
    has_children: bool = False
    path: Optional[Path] = None
    children: List['Page'] = field(default_factory=list)


def read_markdown_front_matter(md_file_path: Path) -> Optional[Page]:
    """
    Parse markdown file's front matter and return Page object.
    
    Args:
        md_file_path: Path to the markdown file
        
    Returns:
        Page object with parsed metadata, or None if no front matter found
    """
    with md_file_path.open('r', encoding='utf-8') as file:
        content = file.read()

    # Extract YAML front matter between --- markers
    front_matter_match = re.search(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not front_matter_match:
        return None

    # Parse front matter key-value pairs
    attributes: Dict[str, str | float | bool] = {}
    for line in front_matter_match.group(1).split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            # Convert specific fields to appropriate types
            if key == "nav_order":
                attributes[key] = float(value)
            elif key == "has_children":
                attributes[key] = value.lower() == "true"
            else:
                attributes[key] = value

    # Fallback to first H1 if title not in front matter
    if "title" not in attributes:
        with md_file_path.open('r', encoding='utf-8') as file:
            for line in file:
                if line.lstrip().startswith('# '):
                    attributes["title"] = line[2:].strip()
                    break

    attributes["path"] = md_file_path
    return Page(**attributes)


def generate_summary(dir: Path) -> str:
    """
    Generate markdown summary from a folder structure.
    
    Args:
        folder: Root directory containing markdown files
        
    Returns:
        Formatted markdown summary string
    """
    def add_page_recursively(current_dir: Path) -> Page:
        """Recursively build page hierarchy from folder structure."""
        readme_path = current_dir / "README.md"
        readme = read_markdown_front_matter(readme_path)
        
        if not readme:
            return Page()

        # Process all items in current folder
        for item in current_dir.glob("*"):
            if item.is_dir():
                readme.children.append(add_page_recursively(item))
            elif item.suffix == ".md" and item.stem != "README":
                page = read_markdown_front_matter(item)
                if page:
                    readme.children.append(page)

        # Sort children by nav_order
        readme.children.sort(key=lambda x: x.nav_order or float('inf'))
        return readme

    # Build the index tree
    index = add_page_recursively(dir)
    
    # Generate summary markdown
    summary = ["# Summary"]
    summary.append(f"\n### {index.title}")
    summary.append(f"* [{index.title}](./README.md)")

    # Add chapters and pages
    for chapter in index.children:
        summary.append(f"\n### {chapter.title}")
        for page in chapter.children:
            relative_path = page.path.relative_to(dir).as_posix()
            summary.append(f"* [{page.title}]({relative_path})")
        summary.append("")

    return "\n".join(summary)


def main():
    """Command line interface for generating documentation summary."""
    parser = argparse.ArgumentParser(
        description="Generate markdown summary from documentation folder structure"
    )
    parser.add_argument(
        "folder",
        type=Path,
        default=Path("./docs"),
        nargs="?",
        help="Path to documentation root folder (default: ./docs)"
    )
    args = parser.parse_args()
    
    print(generate_summary(args.folder))


if __name__ == "__main__":
    main()
