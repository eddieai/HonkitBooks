"""Add python language specifier to markdown code blocks."""

from pathlib import Path
import re
import argparse

def add_python_to_code_blocks(directory: Path) -> None:
    """
    Process all markdown files in directory, adding python language specifier to code blocks.
    
    Args:
        directory: Directory containing markdown files to process
    """
    # Recursively find all .md files in directory
    md_files = list(directory.rglob("*.md"))

    if not md_files:
        print(f"No markdown files found in {directory}")
        return

    # Process each markdown file
    for md_file in md_files:
        print(f"Processing {md_file.relative_to(directory)}...")

        # Read file content
        content = md_file.read_text()

        # Check if specific code block languages exist
        if re.search(r"```(py|python|sh|bash|js|javascript)", content):
            # If ```py exists, replace it with ```python
            if "```py" in content:
                modified_content = content.replace("```py", "```python")
                md_file.write_text(modified_content)
                print(
                    f"Replaced '```py' with '```python' in {md_file.relative_to(directory)}"
                )
            else:
                print(
                    f"Skipping {md_file.relative_to(directory)} as it contains a recognized code block language."
                )
        else:
            # Apply the current logic if no recognized code block languages are found
            pattern = re.compile(r"```\n(.*?)```", re.DOTALL)
            modified_content = pattern.sub(r"```python\n\1```", content)
            md_file.write_text(modified_content)
            print(f"Added 'python' to code blocks in {md_file.relative_to(directory)}")


def main() -> None:
    """Main function to handle CLI arguments and execute commands."""
    parser = argparse.ArgumentParser(
        description="Add python language specifier to markdown code blocks"
    )
    parser.add_argument(
        "directory",
        type=Path,
        help="Directory containing markdown files to process"
    )
    
    args = parser.parse_args()
    
    try:
        add_python_to_code_blocks(args.directory)
        print("Processing complete!")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
