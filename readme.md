# 📚 Bibliometric Analysis Tool

This is a Python-based command-line application designed to support bibliometric analysis of scientific publications. It allows you to merge BibTeX data from multiple sources, detect duplicates, extract statistics, analyze keyword frequencies, compute similarity between abstracts, and even scrape papers directly from the ACM Digital Library.

## 🚀 Features

- Merge `.bib` files and detect duplicate entries
- Generate statistics for authors, journals, years, and publishers
- Analyze keyword frequency by category (skills, tools, strategies, etc.)
- Generate word clouds and co-occurrence graphs
- Compute abstract similarity using:
  - Jaccard Similarity
  - TF-IDF + Cosine Similarity
- Scrape BibTeX entries from ACM Digital Library using Selenium

## 🛠 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/bibliometric-project.git
cd bibliometric-project
```

### 2. Set up a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install the required dependencies

```bash
pip install -r requirements.txt
```
