"""Convert Jupyter notebooks to markdown files."""

from pathlib import Path
import subprocess
from typing import Optional
import argparse

def convert_notebooks(input_dir: Path, output_dir: Optional[Path] = None) -> None:
    """
    Convert all Jupyter notebooks in input_dir to markdown files.
    
    Args:
        input_dir: Directory containing Jupyter notebooks
        output_dir: Directory to save markdown files (defaults to input_dir)
    """
    if output_dir is None:
        output_dir = input_dir
        
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all .ipynb files in input directory using pathlib's glob
    notebooks = list(input_dir.glob("*.ipynb"))
    
    # Early return if no notebooks found
    if not notebooks:
        print(f"No notebooks found in {input_dir}")
        return
        
    # Convert each notebook to markdown using jupyter nbconvert
    for notebook in notebooks:
        print(f"Converting {notebook.name}...")
        cmd = [
            "jupyter", 
            "nbconvert", 
            "--to", 
            "markdown", 
            str(notebook)
        ]
        subprocess.run(cmd, check=True)

def main() -> None:
    """Main function to handle CLI arguments and execute commands."""
    parser = argparse.ArgumentParser(
        description="Convert Jupyter notebooks to markdown files"
    )
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Directory containing Jupyter notebooks to convert"
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=Path,
        help="Directory to save markdown files (defaults to input directory)"
    )
    
    args = parser.parse_args()
    
    try:
        convert_notebooks(args.input_dir, args.output_dir)
        print("Conversion complete!")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
