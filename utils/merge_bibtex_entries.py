from pathlib import Path

# define directories for the data
RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def read_bib_files():
    """
    Loads all .bib files from 'data/raw' and extracts their content
    Returns:
        list[str]: All raw BibTeX entries
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
    Splits the raw BibTeX content into individual entries
    Args:
        content (str): Raw content from a .bib file
    Returns:
        list[str]: List of individual BibTeX entries
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
    Extracts a unique key from a BibTeX entry (DOI if available, otherwise title)
    Args:
        entry (str): A single BibTeX entry
    Returns:
        str: Unique key for deduplication
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
    Removes duplicate entries based on DOI or title
    Args:
        entries (list[str]): All BibTeX entries
    Returns:
        tuple: (unique_entries, duplicate_entries)
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
    Saves a list of BibTeX entries to a file
    Args:
        entries (list[str]): BibTeX entries to save
        path (Path): Destination file path
    """
    with open(path, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(entry + "\n\n")

def main():
    """
    Main function to:
    - Load all raw BibTeX files
    - Merge and deduplicate entries
    - Save merged and duplicate results
    """
    all_entries = read_bib_files()
    unique_entries, duplicate_entries = merge_entries(all_entries)
    save_bib_file(unique_entries, PROCESSED_DIR / "merged.bib")
    save_bib_file(duplicate_entries, PROCESSED_DIR / "duplicates.bib")
    print(f"Merged: {len(unique_entries)} entries")
    print(f"Duplicates: {len(duplicate_entries)} entries")

if __name__ == "__main__":
    main()
