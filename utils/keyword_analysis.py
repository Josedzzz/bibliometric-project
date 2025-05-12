from typing import Union
from pathlib import Path
from .keyword_visualization import generate_wordcloud, draw_cooccurrence_graph
import re
import networkx as nx

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

def parse_keywords(raw_keywords: list[str]) -> dict:
    """
    Parses a list of keywords that may include synonyms separated by a dash.
    Returns a dict mapping canonical keyword -> list of synonyms (including itself).
    """
    keyword_map = {}
    for item in raw_keywords:
        synonyms = [s.strip().lower() for s in item.split(" - ")]
        canonical = synonyms[0]
        keyword_map[canonical] = synonyms
    return keyword_map

def count_keywords_with_synonyms(abstracts: list[str], keyword_map: dict) -> dict:
    """
    Counts occurrences of each canonical keyword, summing all its synonyms.
    """
    counter = {k: 0 for k in keyword_map}
    for abstract in abstracts:
        for canonical, synonyms in keyword_map.items():
            count = sum(abstract.count(s) for s in synonyms)
            counter[canonical] += count
    return counter

def build_graph_with_synonyms(abstracts: list[str], keyword_map: dict):
    """
    Builds co-occurrence graph using canonical keywords, considering synonyms.
    """
    G = nx.Graph()
    for abstract in abstracts:
        present = []
        for canonical, synonyms in keyword_map.items():
            if any(s in abstract for s in synonyms):
                present.append(canonical)
        for i in range(len(present)):
            for j in range(i + 1, len(present)):
                u, v = present[i], present[j]
                if G.has_edge(u, v):
                    G[u][v]['weight'] += 1
                else:
                    G.add_edge(u, v, weight=1)
    return G

def analyze_keyword_category(
    raw_keywords: list[str],
    category_name: str,
    abstracts: list[str],
    json_output_dir: Union[str, Path],
    figure_output_dir: Union[str, Path]
):
    """
    Performs full analysis for a keyword category:
    - Parses synonyms
    - Counts frequencies
    - Builds and draws co-occurrence graph
    - Saves JSON and figures
    """
    category_slug = category_name.lower().replace(" ", "_")
    keyword_map = parse_keywords(raw_keywords)
    freq_counter = count_keywords_with_synonyms(abstracts, keyword_map)
    graph = build_graph_with_synonyms(abstracts, keyword_map)
    json_path = Path(json_output_dir) / f"{category_slug}_frequencies.json"
    wordcloud_path = Path(figure_output_dir) / f"{category_slug}_wordcloud.png"
    graph_path = Path(figure_output_dir) / f"{category_slug}_cooccurrence.png"
    with open(json_path, "w", encoding="utf-8") as f:
        import json
        json.dump(freq_counter, f, indent=2)
    generate_wordcloud(freq_counter, wordcloud_path)
    draw_cooccurrence_graph(graph, graph_path, title=category_name)
    print(f"✅ {category_name} analysis saved in '{figure_output_dir}' and '{json_output_dir}'")

