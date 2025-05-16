import re
import json
from pathlib import Path
from itertools import combinations

def parse_bibtex_abstracts(path: Path) -> dict:
    """
    Returns a dict: {entry_key: abstract}
    """
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    entries = content.split("\n@")
    abstracts = {}
    for entry in entries:
        key_match = re.match(r"@\w+\{([^,]+),", entry)
        abstract_match = re.search(r"abstract\s*=\s*[{\"](.+?)[}\"]\s*,?", entry, re.IGNORECASE | re.DOTALL)
        if key_match and abstract_match:
            key = key_match.group(1).strip()
            abstract = abstract_match.group(1).replace("\n", " ").lower()
            abstracts[key] = abstract

    return abstracts


def jaccard_similarity(a: str, b: str) -> float:
    """
    Computes Jaccard similarity between two strings using word sets.
    """
    set_a = set(a.split())
    set_b = set(b.split())
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def compute_jaccard_matrix(abstracts: dict, threshold=0.2) -> list[dict]:
    """
    Computes pairwise Jaccard similarities and returns only those >= threshold.
    """
    similar_pairs = []
    keys = list(abstracts.keys())
    for i, j in combinations(range(len(keys)), 2):
        key_i, key_j = keys[i], keys[j]
        sim = jaccard_similarity(abstracts[key_i], abstracts[key_j])
        if sim >= threshold:
            similar_pairs.append({
                "source": key_i,
                "target": key_j,
                "similarity": round(sim, 4)
            })
    return similar_pairs


def run_jaccard_similarity(
    bib_path: Path,
    output_path: Path,
    threshold: float = 0.2
):
    """
    Full pipeline: load abstracts, compute Jaccard similarity, save results.
    """
    print("Loading abstracts...")
    abstracts = parse_bibtex_abstracts(bib_path)

    print("Computing Jaccard similarities...")
    result = compute_jaccard_matrix(abstracts, threshold=threshold)

    print(f"Saving {len(result)} pairs with similarity >= {threshold}")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"✅ Saved to {output_path}")

