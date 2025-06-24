import os
import sys
from pathlib import Path

# --- CONFIGURATION ---

# Set the folder path you want to analyze here
TARGET_FOLDER = r"G:\My Drive\A_Capstone Thesis - Sintica\Docs\Annex templates and regulations - KNOW HOW KB"  # Modify this to your folder path

# --- NEW ---
# Add folder names here to prevent the script from scanning deeper into them.
# The script will list the folder itself but will not explore its contents.
STOP_FOLDERS = [
    "poppler-24.08.0",
    "hf_cache",
    "vendor",
    "__pycache__",
    ".git"
]
# --- END NEW ---

# --- END CONFIGURATION ---


def generate_tree(directory, output_file, stop_folders, prefix=""):
    """
    Generate a tree-like representation of the directory structure,
    stopping at specified folders.
    """
    # Get all items in the directory, sorted by name
    try:
        items = sorted(os.listdir(directory))
    except FileNotFoundError:
        return # In case of broken symlinks or permissions issues

    # Count files and directories
    files = [item for item in items if os.path.isfile(os.path.join(directory, item))]
    dirs = [item for item in items if os.path.isdir(os.path.join(directory, item))]

    # Process directories first
    for i, dir_name in enumerate(dirs):
        is_last_dir = (i == len(dirs) - 1 and len(files) == 0)
        current_path = os.path.join(directory, dir_name)

        # Print current directory
        if is_last_dir:
            output_file.write(f"{prefix}└── {dir_name}/\n")
            new_prefix = prefix + "    "
        else:
            output_file.write(f"{prefix}├── {dir_name}/\n")
            new_prefix = prefix + "│   "

        # --- MODIFIED SECTION ---
        # If the directory is in the stop list, do not recurse into it.
        if dir_name in stop_folders:
            continue  # Stop processing this directory and move to the next item
        # --- END MODIFIED SECTION ---

        # Recursively process subdirectory
        generate_tree(current_path, output_file, stop_folders, new_prefix)

    # Process files
    for i, file_name in enumerate(files):
        is_last_file = (i == len(files) - 1)

        if is_last_file:
            output_file.write(f"{prefix}└── {file_name}\n")
        else:
            output_file.write(f"{prefix}├── {file_name}\n")

def main():
    """
    Main function to run the script.
    """
    # Check if the target folder exists
    if not os.path.exists(TARGET_FOLDER):
        print(f"Error: The folder '{TARGET_FOLDER}' does not exist.")
        sys.exit(1)

    # Get the script's directory (handling potential execution from different contexts)
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        script_dir = os.getcwd() # Fallback for interactive interpreters

    # Create output file path
    output_path = os.path.join(script_dir, "folder_tree.txt")

    # Open the output file
    with open(output_path, 'w', encoding='utf-8') as output_file:
        # Write the header
        output_file.write(f"Directory Tree for: {TARGET_FOLDER}\n")
        output_file.write(f"Ignoring contents of folders: {', '.join(STOP_FOLDERS)}\n")
        output_file.write("=" * 50 + "\n\n")

        # Write the folder name as the tree root
        folder_name = os.path.basename(os.path.normpath(TARGET_FOLDER))
        output_file.write(f"{folder_name}/\n")

        # Generate tree structure, passing the stop folders list
        generate_tree(TARGET_FOLDER, output_file, STOP_FOLDERS, prefix="│   ")

        # Write footer
        output_file.write("\n" + "=" * 50 + "\n")

    print(f"Tree structure generated successfully at: {output_path}")

if __name__ == "__main__":
    main()