"""
Module for generating documentation for Python files in a given directory.
The documentation is generated using pydoc.
"""

import os
import subprocess

from config.settings_paths import current_dir


def generate_docs(root_directory, save_directory = None):
    """
    :param root_directory: The base directory from which to gather .py files and generate documentation.
    :param save_directory: The  directory where save generated documentation.
    :return: None. Generates documentation files.
    """
    if save_directory is None:
        # Create a "docs" directory in the root directory if it does not exist
        save_directory = os.path.join(root_directory, "docs")
        os.makedirs(save_directory, exist_ok=True)

    for root, dirs, files in os.walk(root_directory):
        # Ignore directories starting with a dot (e.g., .git, .vscode)
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        for file in files:
            if file.endswith(".py"):
                # Get the relative path from the base directory
                relative_path = os.path.relpath(os.path.join(root, file), root_directory)

                # Replace OS-specific path separators with dots and remove the .py extension
                module_name = os.path.splitext(relative_path)[0].replace(os.sep, ".")

                # Exclude __init__ files if you don't want docs for them
                if module_name.endswith(".__init__"):
                    continue

                print(f"Generating docs for: {module_name}")

                # Generate the documentation file and save it in the desired directory
                output_file = os.path.join(save_directory, f"{module_name}.html")
                subprocess.run(["python", "-m", "pydoc", "-w", module_name], check=True)
                # Move the generated .html file to the save_directory
                generated_file = f"{module_name}.html"
                if os.path.exists(generated_file):
                    os.rename(generated_file, output_file)

if __name__ == "__main__":
    parent_dir = os.path.dirname(current_dir)
    generate_docs(parent_dir)
