import os

EXTENSIONS = {".py", ".json", ".cfg", ".txt", ".md"}

def snapshot(root_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(f"# SNAPSHOT DU REPO : {os.path.abspath(root_dir)}\n\n")
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Ignorer les dossiers inutiles
            dirnames[:] = [d for d in dirnames if d not in {"__pycache__", ".git", "results"}]
            for filename in sorted(filenames):
                if os.path.splitext(filename)[1] in EXTENSIONS:
                    filepath = os.path.join(dirpath, filename)
                    rel_path = os.path.relpath(filepath, root_dir)
                    out.write("=" * 60 + "\n")
                    out.write(f"FILE: {rel_path}\n")
                    out.write("=" * 60 + "\n\n")
                    with open(filepath, 'r', encoding='utf-8') as f:
                        out.write(f.read())
                    out.write("\n\n")

if __name__ == "__main__":
    snapshot(
        root_dir    = ".",           # répertoire à snapshoter
        output_file = "snapshot.txt"
    )