import os
import shutil

# -----------------------------
# Config
# -----------------------------
repo_root = "."       # Path to your repo root
docs_root = "./docs"  # Docs folder to generate

# -----------------------------
# Helper functions
# -----------------------------
def safe_folder_name(name):
    """Replace spaces for folder names"""
    return name.replace(" ", "_")

def read_readme(folder):
    """Return README.md content if it exists"""
    readme_path = os.path.join(folder, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def create_docs_index(folder_path, rel_path):
    """Create index.md in docs/ corresponding to folder_path"""
    docs_folder = os.path.join(docs_root, rel_path)
    os.makedirs(docs_folder, exist_ok=True)
    index_file = os.path.join(docs_folder, "index.md")

    # Title = last folder name
    title = os.path.basename(folder_path)
    if title == "":
        title = "Home"

    # Read README content if exists
    readme_content = read_readme(folder_path)
    if readme_content:
        body = readme_content
    else:
        body = f"*(Documentation placeholder for {title})*"

    content = f"""---
title: "{title}"
nav_order: 1
---

# {title}

{body}
"""
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(content)

def walk_and_generate_docs(current_folder, rel_path=""):
    """Walk repo and generate docs/index.md for each folder"""

    # Skip the generated docs folder itself
    if os.path.abspath(current_folder).startswith(os.path.abspath(docs_root)):
        return

    # Skip .git completely
    if ".git" in current_folder.split(os.sep):
        return

    create_docs_index(current_folder, rel_path)

    for item in sorted(os.listdir(current_folder)):
        item_path = os.path.join(current_folder, item)

        # Skip hidden folders
        if item.startswith("."):
            continue

        if os.path.isdir(item_path):
            new_rel_path = os.path.join(rel_path, safe_folder_name(item))
            walk_and_generate_docs(item_path, new_rel_path)



# -----------------------------
# Clear and recreate docs folder
# -----------------------------
if os.path.exists(docs_root):
    shutil.rmtree(docs_root)
os.makedirs(docs_root, exist_ok=True)

# -----------------------------
# Generate docs
# -----------------------------
walk_and_generate_docs(repo_root)
print("Docs folder generated successfully!")
