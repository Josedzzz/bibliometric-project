from pathlib import Path
from utils.keyword_analysis import (
    parse_bibtex_abstracts,
    count_keywords,
    build_cooccurrence_graph,
    save_frequencies
)
from utils.keyword_visualization import generate_wordcloud, draw_cooccurrence_graph

# Config
BIB_PATH = Path("data/processed/merged.bib")
OUTPUT_JSON = Path("data/processed/keyword_frequencies.json")
FIGURES_DIR = Path("figures/keywords")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

HABILIDADES = [
    "abstraction", "algorithm", "algorithmic thinking", "coding",
    "collaboration", "cooperation", "creativity", "critical thinking",
    "debug", "decomposition", "evaluation", "generalization",
    "logic", "logical thinking", "modularity", "patterns recognition",
    "problem solving", "programming"
]

def main():
    print("🔍 Extracting abstracts...")
    abstracts = parse_bibtex_abstracts(BIB_PATH)

    print("📊 Counting keyword frequencies...")
    freq_counter = count_keywords(abstracts, HABILIDADES)

    print("💾 Saving frequencies...")
    save_frequencies(freq_counter, OUTPUT_JSON)

    print("☁️ Generating word cloud...")
    generate_wordcloud(freq_counter, FIGURES_DIR / "habilidades_wordcloud.png")

    print("🧠 Building co-occurrence graph...")
    G = build_cooccurrence_graph(abstracts, HABILIDADES)

    print("🖼️ Drawing co-occurrence graph...")
    draw_cooccurrence_graph(G, FIGURES_DIR / "habilidades_cooccurrence.png")

    print("✅ Done.")

if __name__ == "__main__":
    main()

