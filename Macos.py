import os
import sys
from pathlib import Path

# --- MODIFIED FOR MACOS ---
# The script now automatically finds your user's home directory.
# It assumes your OneDrive folder is named "OneDrive" and is located there.
# This is the standard location (e.g., /Users/YourUsername/OneDrive).
# If your folder has a different name (e.g., "OneDrive - CompanyName"),
# just change the string "OneDrive" below.
TARGET_FOLDER = Path.home() / "Documents" / "Data & AI Services - Documents"

def generate_tree(directory, output_file, prefix=""):
    """
    Generate a tree-like representation of the directory structure.
    (This function remains unchanged)
    """
    # Using Path objects for robustness, converting to string for os.listdir
    directory_path = Path(directory)
    try:
        # Get all items in the directory, sorted by name
        items = sorted(os.listdir(directory_path))
    except FileNotFoundError:
        # This can happen with OneDrive's online-only files that look like folders
        output_file.write(f"{prefix}└── [Could not access folder - may be online-only]\n")
        return
    except PermissionError:
        output_file.write(f"{prefix}└── [Permission Denied]\n")
        return

    files = [item for item in items if (directory_path / item).is_file()]
    dirs = [item for item in items if (directory_path / item).is_dir()]

    # Process directories first
    for i, dir_name in enumerate(dirs):
        is_last_dir = (i == len(dirs) - 1 and not files)
        connector = "└── " if is_last_dir else "├── "
        output_file.write(f"{prefix}{connector}{dir_name}/\n")

        new_prefix = prefix + ("    " if is_last_dir else "│   ")
        generate_tree(directory_path / dir_name, output_file, new_prefix)

    # Process files
    for i, file_name in enumerate(files):
        is_last_file = (i == len(files) - 1)
        connector = "└── " if is_last_file else "├── "
        output_file.write(f"{prefix}{connector}{file_name}\n")

def main():
    # --- MODIFIED FOR MACOS ---
    # The script now uses the modern `pathlib` for path operations.
    if not TARGET_FOLDER.exists() or not TARGET_FOLDER.is_dir():
        print(f"Error: The folder '{TARGET_FOLDER}' does not exist or is not a directory.")
        print("Please check the TARGET_FOLDER variable in the script.")
        sys.exit(1)

    # --- MODIFIED FOR MACOS ---
    # The output file will be saved directly to your Desktop for easy access.
    output_path = Path(__file__).parent / "folder_tree.txt"

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(f"Directory Tree for: {TARGET_FOLDER}\n")
        output_file.write("=" * 50 + "\n\n")

        output_file.write(f"{TARGET_FOLDER.name}/\n")
        generate_tree(TARGET_FOLDER, output_file)

        output_file.write("\n" + "=" * 50 + "\n")

    print(f"Tree structure generated successfully!")
    print(f"File saved to your Desktop: {output_path}")

if __name__ == "__main__":
    main()