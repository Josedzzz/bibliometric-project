import json
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

def plot_similarity_graph(json_path: Path, output_path: Path):
    """
    Plots a graph where nodes are abstracts and edges represent Jaccard similarity.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    G = nx.Graph()
    for item in data:
        src, tgt, sim = item["source"], item["target"], item["similarity"]
        G.add_edge(src, tgt, weight=sim)

    if G.number_of_edges() == 0:
        print("No edges found, skipping graph.")
        return

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=0.4, seed=42)

    weights = [G[u][v]["weight"] * 5 for u, v in G.edges()]
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color="lightblue")
    nx.draw_networkx_edges(G, pos, width=weights, alpha=0.7) #type: ignore
    nx.draw_networkx_labels(G, pos, font_size=8)

    plt.title("Jaccard Similarity Graph (abstracts)")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Graph saved to {output_path}")

