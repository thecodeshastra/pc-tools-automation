"""New project or tool initial setup script.
This script is used to set up a new project or tool within the CodiFlowSystems environment
"""

import argparse
import json
import os
import sys


def create_structure(structure: dict, root: str):
    """Recursively create directories and files based on the provided structure.
    
    Args:
        structure (dict): A dictionary representing the project structure.
        root (str): The root directory where the structure will be created.
    """
    for name, content in structure.items():
        path = os.path.join(root, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(content, path)
        else:
            # content is a string (file content)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)


def main():
    """Main function to parse arguments and initialize project structure."""
    parser = argparse.ArgumentParser(
        description="Initialize project structure from a JSON description."
    )
    parser.add_argument(
        "-j",
        "--json_path",
        required=True,
        default="project_structure.json",
        type=str,
        help="Path to project structure JSON file."
    )
    parser.add_argument(
        "-dp",
        "--dest_path",
        required=True,
        default=os.getcwd(),
        type=str,
        help="Destination directory for creating project structure."
    )
    args = parser.parse_args()
    # Ensure JSON file exists
    if not os.path.isfile(args.json_path):
        print(f"JSON file not found: {args.json_path}")
        sys.exit(1)
    # Ensure destination directory exists or create it
    if not os.path.exists(args.dest_path):
        print(f"Destination directory does not exist, creating: {args.dest_path}")
        os.makedirs(args.dest_path, exist_ok=True)
    # Load the JSON structure
    with open(args.json_path, "r", encoding="utf-8") as f:
        structure = json.load(f)
    create_structure(structure, args.dest_path)
    print(f"Project initialized in {args.dest_path}")


if __name__ == "__main__":
    main()
