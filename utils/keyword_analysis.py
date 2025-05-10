from pathlib import Path
from collections import Counter
import re
import json

def parse_bibtex_abstracts(path: Path) -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    entries = content.split("\n@")
    abstracts = []
    for entry in entries:
        match = re.search(r"abstract\s*=\s*[{\"](.+?)[}\"]\s*,?", entry, re.IGNORECASE | re.DOTALL)
        if match:
            abstract = match.group(1).replace("\n", " ").lower()
            abstracts.append(abstract)
    return abstracts

def count_keywords(abstracts: list[str], keywords: list[str]) -> Counter:
    counter = Counter()
    for abstract in abstracts:
        for keyword in keywords:
            count = abstract.count(keyword.lower())
            if count > 0:
                counter[keyword.lower()] += count
    return counter

def build_cooccurrence_graph(abstracts: list[str], keywords: list[str]):
    import networkx as nx
    G = nx.Graph()
    keywords = [k.lower() for k in keywords]
    for abstract in abstracts:
        present = [k for k in keywords if k in abstract]
        for i in range(len(present)):
            for j in range(i + 1, len(present)):
                u, v = present[i], present[j]
                if G.has_edge(u, v):
                    G[u][v]['weight'] += 1
                else:
                    G.add_edge(u, v, weight=1)
    return G

def save_frequencies(counter: Counter, output_path: Path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(counter, f, indent=4)

