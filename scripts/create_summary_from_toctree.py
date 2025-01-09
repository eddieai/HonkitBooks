"""
Convert a Sphinx toctree index file to a markdown SUMMARY.md format.

This script takes a Sphinx-style index file (typically index.rst or index.md) containing a toctree
directive and converts it to a markdown summary format suitable for GitBook or similar documentation
systems. It handles nested index files recursively.

Example input (index.md):
# Main Title
.. toctree::
   chapter1/index
   chapter2/page1
   chapter2/page2

Example output (SUMMARY.md):
# Main Title
* [Chapter 1](./chapter1/index.md)
* [Page 1](./chapter2/page1.md)
* [Page 2](./chapter2/page2.md)

Usage:
python toctree_to_summary.py path/to/index.md
"""
from pathlib import Path
from typing import Optional
import argparse


def toctree_to_summary(index_path: Path) -> str:
    """
    Convert a toctree index file to a markdown summary.
    
    Args:
        index_path: Path to the index file (with or without .md extension)
        
    Returns:
        Formatted markdown summary with nested structure
    """
    # Ensure we have .md extension
    index_path = index_path.with_suffix('.md') if index_path.suffix != '.md' else index_path
    
    # Read and parse the index file
    with index_path.open('r', encoding='utf-8') as index:
        index_lines = index.readlines()
    
    # Extract title from first line
    title = f"#{index_lines[0].strip()}"
    
    # Process each content line
    summary = ""
    for line in index_lines[3:-1]:  # Skip header and footer lines
        line = line.strip()
        if not line:  # Skip empty lines
            continue
            
        # Handle nested index files recursively
        if line.endswith("index"):
            summary += toctree_to_summary(index_path.parent / line)
        else:
            # Create markdown link with spaces replaced by hyphens
            relative_path = (index_path.parent / line).relative_to(Path.cwd())
            summary += f"* [{line}]({relative_path.with_suffix('.md')})\n"
    
    return f"{title}\n{summary}"


def main():
    """Command line interface for generating summary from index."""
    parser = argparse.ArgumentParser(
        description="Convert a toctree index file to markdown summary"
    )
    parser.add_argument(
        "index_path",
        type=Path,
        help="Path to the index file (with or without .md extension)"
    )
    args = parser.parse_args()
    
    print(toctree_to_summary(args.index_path))


if __name__ == "__main__":
    main()
