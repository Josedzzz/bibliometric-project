from pathlib import Path

# define directories for the data
RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def read_bib_files():
    """
    reads all .bib files in the raw data directory and reads it
    returns: the list of all bibtex entries
    """
    bib_entries = []
    for file in RAW_DIR.glob("*.bib"):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            entries = split_bib_entries(content)
            bib_entries.extend(entries)
    return bib_entries

def split_bib_entries(content):
    """
    splits the content of a .bib file into individual entries
    args: the raw content of the .bib file
    returns: a list of individual bibtex entries as a string
    """
    entries = []
    current = []
    inside_entry = False
    for line in content.splitlines():
        if line.strip().startswith("@"):
            if current:
                entries.append("\n".join(current))
                current = []
            inside_entry = True
        if inside_entry:
            current.append(line)
    if current:
        entries.append("\n".join(current))
    return entries

def extract_key(entry):
    """
    extracts the identifier from a entry, it can be the title or DOI
    args: a single bibtex entry
    returns: the DOI or the title in lowercase
    """
    doi = None
    title = None
    for line in entry.splitlines():
        line = line.strip()
        if line.lower().startswith("doi"):
            doi = line.split("=", 1)[-1].strip().strip(",{}").lower()
            break
        elif line.lower().startswith("title") and not title:
            title = line.split("=", 1)[-1].strip().strip(",{}").lower()
    return doi if doi else title

def merge_entries(entries):
    """
    merge entries by removing duplicates based on the DOI or title
    args: a list of bibtex entries
    returns: list of unique entries and list of duplicate entries
    """
    seen = {}
    duplicates = []
    for entry in entries:
        key = extract_key(entry)
        if key in seen:
            duplicates.append(entry)
        else:
            seen[key] = entry
    return list(seen.values()), duplicates

def save_bib_file(entries, path):
    """
    saves a list of bibtex entries to a specified path
    args: the bibtex entries to save and the file path
    """
    with open(path, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(entry + "\n\n")

def main():
    """
    main execution:
    - reads the bibtex files
    - merge entries while removing duplicates
    - saves both, the merged and duplicates
    """
    all_entries = read_bib_files()
    unique_entries, duplicate_entries = merge_entries(all_entries)
    save_bib_file(unique_entries, PROCESSED_DIR / "merged.bib")
    save_bib_file(duplicate_entries, PROCESSED_DIR / "duplicates.bib")
    print(f"Merged: {len(unique_entries)} entries")
    print(f"Duplicates: {len(duplicate_entries)} entries")

if __name__ == "__main__":
    main()

