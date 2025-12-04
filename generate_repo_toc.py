import os
import re

# -----------------------------
# Config: path to your repo root
# -----------------------------
repo_root = "."  # <-- change to your repo path

REPO_TOC_START = "<!-- REPO_TOC -->"
REPO_TOC_END = "<!-- /REPO_TOC -->"
HEADING_TOC_START = "<!-- TOC -->"
HEADING_TOC_END = "<!-- /TOC -->"

# -----------------------------
# Helper functions
# -----------------------------
def repo_depth(path):
    rel = os.path.relpath(path, repo_root)
    if rel == ".":
        return 0
    return len(rel.split(os.sep))

def relative_link(target_path, current_path):
    """Compute relative link from current folder to target folder"""
    depth = repo_depth(current_path)
    if target_path == repo_root:
        return "/".join([".."] * depth) + "/" if depth > 0 else "./"
    rel = os.path.relpath(target_path, current_path).replace("\\", "/")
    # Replace spaces with %20
    rel = rel.replace(" ", "%20")
    return rel + "/" if rel != "." else "./"


def generate_toc_for_folder(current_folder):
    """Generate full-repo TOC Markdown for a given folder"""
    lines = [REPO_TOC_START]
    lines.append(f"- [FBDD]({relative_link(repo_root, current_folder)})")

    # Walk repo tree and add all directories
    def walk(folder, indent=1):
        items = sorted(
            [i for i in os.listdir(folder) 
            if os.path.isdir(os.path.join(folder, i)) and i != ".git"]
        )
        for item in items:
            item_path = os.path.join(folder, item)
            link = relative_link(item_path, current_folder)
            lines.append("  " * indent + f"- [{item}]({link})")
            walk(item_path, indent + 1)


    walk(repo_root)
    lines.append(REPO_TOC_END)
    return "\n".join(lines)

def insert_or_replace_repo_toc(readme_path, toc_text):
    """Insert or replace the REPO_TOC block in a README.md file"""
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = ""

    # Remove existing REPO_TOC if present
    content = re.sub(f"{REPO_TOC_START}.*?{REPO_TOC_END}\n?", "", content, flags=re.DOTALL)

    # Find headings TOC
    match = re.search(f"{HEADING_TOC_START}.*?{HEADING_TOC_END}", content, flags=re.DOTALL)
    if match:
        # Insert repo TOC just above headings TOC
        start_index = match.start()
        new_content = content[:start_index] + toc_text + "\n\n" + content[start_index:]
    else:
        # Insert at top
        new_content = toc_text + "\n\n" + content

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)

# -----------------------------
# Walk all folders and update README.md
# -----------------------------
for folder_path, _, _ in os.walk(repo_root):
    readme_path = os.path.join(folder_path, "README.md")
    toc = generate_toc_for_folder(folder_path)
    insert_or_replace_repo_toc(readme_path, toc)
    print(f"Updated README.md in: {folder_path}")

print("\nAll README.md files updated with repo navigation TOC (repo TOC before headings TOC).")
