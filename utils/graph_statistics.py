import json
import matplotlib.pyplot as plt
from pathlib import Path

# Paths
STATS_PATH = Path("data/processed/stats.json")
FIGURES_DIR = Path("figures")
FIGURES_DIR.mkdir(exist_ok=True)

def load_stats():
    """
    Loads precomputed statistics from the `stats.json` file
    Returns a dictionary with all required metrics for plotting
    """
    with open(STATS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def plot_bar_chart(data, title, xlabel, ylabel, filename):
    """
    Creates and saves a bar chart given a dictionary of data
    Args:
    - data: dictionary {label: value}
    - title: chart title
    - xlabel: label for the x-axis
    - ylabel: label for the y-axis
    - filename: name of the file to save the plot
    """
    labels = list(data.keys())
    values = list(data.values())
    plt.figure(figsize=(12, 6))
    bars = plt.bar(labels, values, color="skyblue")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{int(height)}', ha='center', va='bottom')
    plt.savefig(FIGURES_DIR / filename)
    plt.close()

def main():
    """
    Main function to generate all statistical plots
    Produces bar charts for:
    - Top authors
    - Product types
    - Top journals and publishers
    - Publication year distribution per product type
    """
    stats = load_stats()
    plot_bar_chart(
        stats["top_authors"],
        "Top 15 Authors by Number of Products",
        "Author",
        "Number of Products",
        "top_authors.png"
    )
    plot_bar_chart(
        stats["product_type_counts"],
        "Count by Product Type",
        "Product Type",
        "Count",
        "product_types.png"
    )
    plot_bar_chart(
        stats["top_journals"],
        "Top 15 Journals",
        "Journal",
        "Number of Products",
        "top_journals.png"
    )
    plot_bar_chart(
        stats["top_publishers"],
        "Top 15 Publishers",
        "Publisher",
        "Number of Products",
        "top_publishers.png"
    )
    for product_type, year_data in stats["publication_year_by_type"].items():
        plot_bar_chart(
            year_data,
            f"Publication Year Distribution - {product_type}",
            "Year",
            "Count",
            f"years_{product_type.lower().replace(' ', '_')}.png"
        )
    print("All plots generated in the 'figures/' directory.")

if __name__ == "__main__":
    main()
