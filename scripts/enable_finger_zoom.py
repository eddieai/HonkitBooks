"""Enable finger zoom by modifying viewport meta tags in HTML files."""

from pathlib import Path
import argparse

def enable_finger_zoom(dir: Path) -> None:
    """
    Process all HTML files in directory, enabling user scaling in viewport meta tags.
    
    Args:
        directory: Directory containing HTML files to process
    """
    # Recursively find all .html files in directory
    html_files = list(dir.rglob("*.html"))

    if not html_files:
        print(f"No HTML files found in {dir}")
        return

    # Process each HTML file
    for html_file in html_files:
        # Read file content
        content = html_file.read_text()

        # Find and modify viewport meta tags
        modified_content = content.replace('user-scalable=no', 'user-scalable=yes')

        if modified_content != content:
            html_file.write_text(modified_content)


def main() -> None:
    """Main function to handle CLI arguments and execute commands."""
    parser = argparse.ArgumentParser(
        description="Enable finger zoom by modifying viewport meta tags in HTML files"
    )
    parser.add_argument(
        "directory",
        type=Path,
        help="Directory containing HTML files to process"
    )

    args = parser.parse_args()

    try:
        enable_finger_zoom(args.directory)
        print(f"Run enable_finger_zoom.py on {Path(args.directory).name} complete!")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
