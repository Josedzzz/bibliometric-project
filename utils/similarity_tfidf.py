import json
import re
from pathlib import Path
from typing import Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def parse_bibtex_abstracts(path: Path) -> Dict[str, str]:
    """
    Parses a BibTeX file and returns a dictionary of entry keys and corresponding cleaned abstracts
    """
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    entries = re.split(r"\n(?=@\w+\{)", content)
    print(f"Total entries split: {len(entries)}")
    abstracts = {}
    for entry in entries:
        key_match = re.match(r"@\w+\{([^,]+),", entry)
        abstract_match = re.search(
            r"abstract\s*=\s*(\{|\")([\s\S]+?)(\}|\")\s*,?", entry,
            re.IGNORECASE
        )
        if key_match and abstract_match:
            key = key_match.group(1).strip()
            abstract = abstract_match.group(2).strip().replace("\n", " ").lower()
            if len(abstract) > 30:
                abstracts[key] = abstract
    print(f"\nExtracted {len(abstracts)} abstracts with content.")
    print(f"Unique abstracts: {len(set(abstracts.values()))}")
    return abstracts

def run_tfidf_similarity(bib_path: Path, output_path: Path, threshold: float = 0.3):
    """
    Applies TF-IDF vectorization to abstracts and calculates pairwise cosine similarity
    Returns only those pairs with similarity greater than or equal to the specified threshold
    Outputs the result to a JSON file
    """
    print("Loading abstracts...")
    abstracts = parse_bibtex_abstracts(bib_path)
    keys = list(abstracts.keys())
    texts = [abstracts[k] for k in keys]
    print("Vectorizing abstracts with TF-IDF...")
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    print("Computing cosine similarities...")
    cosine_sim = cosine_similarity(tfidf_matrix)
    print(f"Filtering pairs with similarity >= {threshold}...")
    similar_pairs = []
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            sim = cosine_sim[i, j]
            if sim >= threshold:
                similar_pairs.append({
                    "source": keys[i],
                    "target": keys[j],
                    "similarity": round(sim, 4)
                })
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(similar_pairs, f, indent=2)
    print(f"Saved {len(similar_pairs)} similar pairs to {output_path}")
