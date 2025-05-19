from wordcloud import WordCloud
import matplotlib.pyplot as plt
import networkx as nx
from typing import Union
from pathlib import Path

def generate_wordcloud(counter, output_path: Union[str, Path]):
    """
    Generates and saves a word cloud from keyword frequency data
    """
    filtered = {k: v for k, v in counter.items() if v > 0}
    if not filtered:
        print("X Skipping word cloud: no keywords with frequency > 0")
        return
    wc = WordCloud(width=1000, height=600, background_color="white")
    wc.generate_from_frequencies(counter)
    wc.to_file(str(output_path))

def draw_cooccurrence_graph(G: nx.Graph, output_path: Union[str, Path], title: str = "Keyword Co-occurrence Network"):
    """
    Draws and saves a co-occurrence network graph of keywords
    """
    if G.number_of_edges() == 0:
        print("X Skipping co-occurrence graph: no edges found")
        return
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=0.5, seed=42)
    edges = list(G.edges(data=True))
    edgelist = [(u, v) for u, v, _ in edges]
    weights = [float(data.get("weight", 1)) for _, _, data in edges]
    max_w = max(weights) if weights else 1
    weights = [w / max_w * 3 for w in weights]
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=700)
    nx.draw_networkx_edges(G, pos, edgelist=edgelist, width=weights) #type: ignore
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
    plt.title(f"Keyword Co-occurrence Network - {title}")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(str(output_path))
    plt.close()

