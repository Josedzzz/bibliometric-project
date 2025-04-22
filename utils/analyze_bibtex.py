from pathlib import Path
from collections import Counter, defaultdict
import re
import json

# Path to the merged BibTeX file
MERGED_PATH = Path("data/processed/merged.bib")
STATS_OUTPUT_PATH = Path("data/processed/stats.json")

def parse_bibtex_entries(path):
    """
    Parses a .bib file and returns a list of entries (as raw strings)
    """
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    entries = content.split("\n@")
    entries = ["@" + e.strip() for e in entries if e.strip()]
    return entries

def extract_field(entry, field_name):
    """
    Extracts a specific field from a BibTeX entry using regex
    """
    pattern = re.compile(rf"{field_name}\s*=\s*{{(.*?)}}", re.IGNORECASE | re.DOTALL)
    match = pattern.search(entry)
    return match.group(1).strip() if match else None

def analyze_entries(entries):
    """
    Extracts statistics from a list of BibTeX entries.
    """
    author_counter = Counter()
    year_type_counter = defaultdict(Counter)
    type_counter = Counter()
    journal_counter = Counter()
    publisher_counter = Counter()
    for entry in entries:
        entry_type = entry.split("{", 1)[0].replace("@", "").strip().lower()
        year = extract_field(entry, "year")
        authors_raw = extract_field(entry, "author")
        journal = extract_field(entry, "journal")
        publisher = extract_field(entry, "publisher")
        # Process authors
        if authors_raw:
            authors = [a.strip() for a in authors_raw.split(" and ")]
            if authors:
                author_counter[authors[0]] += 1  # first author only
        # Year by type
        if year:
            year_type_counter[entry_type][year] += 1
        # Product type
        type_counter[entry_type] += 1
        # Journal
        if journal:
            journal_counter[journal] += 1
        # Publisher
        if publisher:
            publisher_counter[publisher] += 1
    return {
        "top_authors": author_counter.most_common(15),
        "year_by_type": dict(year_type_counter),
        "types": type_counter,
        "top_journals": journal_counter.most_common(15),
        "top_publishers": publisher_counter.most_common(15),
    }

def print_statistics(stats):
    """
    Prints the analysis results in a readable format.
    """
    print("\nTop 15 First Authors:")
    for author, count in stats["top_authors"]:
        print(f"  {author}: {count}")
    print("\nPublication Year by Product Type:")
    for t, years in stats["year_by_type"].items():
        print(f"  {t}:")
        for year, count in sorted(years.items()):
            print(f"    {year}: {count}")
    print("\nProduct Types:")
    for t, count in stats["types"].items():
        print(f"  {t}: {count}")
    print("\nTop 15 Journals:")
    for j, count in stats["top_journals"]:
        print(f"  {j}: {count}")
    print("\nTop 15 Publishers:")
    for p, count in stats["top_publishers"]:
        print(f"  {p}: {count}")

def save_statistics(stats):
    """
    Saves stats to a JSON file for further processing.
    """
    # Transform Counter and defaultdict to regular dicts
    serializable_stats = {
        "top_authors": dict(stats["top_authors"]),
        "publication_year_by_type": {
            t: dict(y) for t, y in stats["year_by_type"].items()
        },
        "product_type_counts": dict(stats["types"]),
        "top_journals": dict(stats["top_journals"]),
        "top_publishers": dict(stats["top_publishers"]),
    }
    with open(STATS_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(serializable_stats, f, indent=2)

def run_analysis():
    """
    Entry point to parse and analyze the merged BibTeX file.
    """
    entries = parse_bibtex_entries(MERGED_PATH)
    stats = analyze_entries(entries)
    print_statistics(stats)
    save_statistics(stats)

if __name__ == "__main__":
    run_analysis()

