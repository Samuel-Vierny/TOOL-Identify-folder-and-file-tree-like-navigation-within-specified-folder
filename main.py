import os
import sys
from pathlib import Path

# Set the folder path you want to analyze here
TARGET_FOLDER = r"C:\Your\Folder\Path\Here"  # Modify this to your folder path

def generate_tree(directory, output_file, prefix=""):
    """
    Generate a tree-like representation of the directory structure.
    """
    # Get all items in the directory, sorted by name
    items = sorted(os.listdir(directory))
    
    # Count files and directories
    files = [item for item in items if os.path.isfile(os.path.join(directory, item))]
    dirs = [item for item in items if os.path.isdir(os.path.join(directory, item))]
    
    # Process directories first
    for i, dir_name in enumerate(dirs):
        is_last_dir = (i == len(dirs) - 1 and len(files) == 0)
        
        # Print current directory
        if is_last_dir:
            output_file.write(f"{prefix}└── {dir_name}/\n")
            new_prefix = prefix + "    "
        else:
            output_file.write(f"{prefix}├── {dir_name}/\n")
            new_prefix = prefix + "│   "
        
        # Recursively process subdirectory
        generate_tree(os.path.join(directory, dir_name), output_file, new_prefix)
    
    # Process files
    for i, file_name in enumerate(files):
        is_last_file = (i == len(files) - 1)
        
        if is_last_file:
            output_file.write(f"{prefix}└── {file_name}\n")
        else:
            output_file.write(f"{prefix}├── {file_name}\n")

def main():
    # Check if the target folder exists
    if not os.path.exists(TARGET_FOLDER):
        print(f"Error: The folder '{TARGET_FOLDER}' does not exist.")
        sys.exit(1)
    
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create output file path
    output_path = os.path.join(script_dir, "folder_tree.txt")
    
    # Open the output file
    with open(output_path, 'w', encoding='utf-8') as output_file:
        # Write the header
        output_file.write(f"Directory Tree for: {TARGET_FOLDER}\n")
        output_file.write("=" * 50 + "\n\n")
        
        # Write the folder name as the tree root
        folder_name = os.path.basename(TARGET_FOLDER)
        output_file.write(f"{folder_name}/\n")
        
        # Generate tree structure
        generate_tree(TARGET_FOLDER, output_file)
        
        # Write footer
        output_file.write("\n" + "=" * 50 + "\n")
        
    print(f"Tree structure generated successfully at: {output_path}")

if __name__ == "__main__":
    main()