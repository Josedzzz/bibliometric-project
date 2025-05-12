from pathlib import Path
from utils.keyword_analysis import (
    parse_bibtex_abstracts,
    analyze_keyword_category
)

# routes
BIB_PATH = Path("data/processed/merged.bib")
FIGURES_DIR = Path("figures/keywords")
OUTPUT_DIR = Path("data/processed")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# categories
SKILLS = [
    "abstraction", "algorithm", "algorithmic thinking", "coding",
    "collaboration", "cooperation", "creativity", "critical thinking",
    "debug", "decomposition", "evaluation", "generalization",
    "logic", "logical thinking", "modularity", "patterns recognition",
    "problem solving", "programming"
]

CONCEPTS = [
    "conditionals", "control structures", "directions", "events",
    "functions-funtions", "loops", "modular structure", "parallelism",
    "sequences", "software/hardware", "variables"
]

ATTITUDES = [
    "emotional", "engagement", "motivation", "perceptions",
    "persistence", "self-efficacy", "self-perceived"
]

PROPERTIES = [
    "Classical Test Theory - CTT", "Confirmatory Factor Analysis - CFA",
    "Exploratory Factor Analysis - EFA", "Item Response Theory - IRT",
    "Reliability", "Structural Equation Model - SEM", "Validity"
]

ASSESSMENT = [
    "Beginners Computational Thinking test - BCTt", "Coding Attitudes Survey - ESCAS",
    "Collaborative Computing Observation Instrument", "Competent Computational Thinking test - cCTt",
    "Computational thinking skills test - CTST", "Computational concepts",
    "Computational Thinking Assessment for Chinese Elementary", "Students - CTA - CES",
    "Computational Thinking Challenge - CTC", "Computational Thinking Levels Scale - CTLS",
    "Computational Thinking Scale - CTS", "Computational Thinking Skill Levels Scale - CTS",
    "Computational Thinking Test - CTt", "Computational Thinking Test for Elementary School Students",
    "Computational Thinking Test for Lower Primary - CTtLP", "Computational thinking skill tasks on numbers and arithmetic",
    "Computerized Adaptive Programming Concepts Test - lAPCT", "CT Scale - CTS", 
    "Elementary Student Coding Attitudes Survey - ESCAS", "General self-efficacy scale",
    "ICT competency test", "Instrument of computational identity",
    "KBIT fluid intelligence subtest", "Mastery of computational concepts Test and an Algorithmic Test",
    "Multidimensional 21st Century Skills Scale", "Self-efficacy scale",
    "STEM learning attitude scale", "The computational thinking scale"
]

RESEARCH = [
    "No experimental", "Experimental", "Longitudinal research",
    "Mixed methods", "Post-test", "Pre-test", "Quasi-experiments"
]

EDUCATION = [
    "Upper elementary education - Upper elementary school", "Primary school - Primary education - Elementary school",
    "Early childhood education – Kindergarten - Preschool", "Secondary school - Secondary education",
    "high school - higher education", "University – College"
]

MEDIUM = [
    "Block programming", "Mobile application", "Pair programming",
    "Plugged activities", "Programming", "Robotics", "Spreadsheet",
    "STEM", "Unplugged activities"
]

STRATEGY = [
    "Construct-by-self mind mapping", "Construct-on-scaffold mind mapping",
    "Design-based learning", "Evidence-centred design approach",
    "Gamification", "Reverse engineering pedagogy", "Technology-enhanced learning",
    "Collaborative learning", "Cooperative learning", "Flipped classroom",
    "Game-based learning", "Inquiry-based learning", "Personalized learning",
    "Problem-based learning", "Project-based learning", "Universal design for learning"
]

TOOL = [
    "Alice", "Arduino", "Scratch", "ScratchJr", "Blockly Games", "Code.org",
    "Codecombat", "CSUnplugged", "Robot Turtles", "Hello Ruby", "Kodable",
    "LightbotJr", "KIBO robots", "BEE BOT", "CUBETTO", "Minecraft",
    "Agent Sheets", "Mimo", "Py–Learn", "SpaceChem"
]

def main():
    abstracts = parse_bibtex_abstracts(BIB_PATH)
    analyze_keyword_category(SKILLS, "Skills", abstracts, OUTPUT_DIR, FIGURES_DIR)
    analyze_keyword_category(CONCEPTS, "Computational concepts", abstracts, OUTPUT_DIR, FIGURES_DIR)
    analyze_keyword_category(ATTITUDES, "Attitudes", abstracts, OUTPUT_DIR, FIGURES_DIR)
    analyze_keyword_category(PROPERTIES, "Properties", abstracts, OUTPUT_DIR, FIGURES_DIR)
    analyze_keyword_category(ASSESSMENT, "Assessment", abstracts, OUTPUT_DIR, FIGURES_DIR)
    analyze_keyword_category(RESEARCH, "Research", abstracts, OUTPUT_DIR, FIGURES_DIR)
    analyze_keyword_category(EDUCATION, "Education", abstracts, OUTPUT_DIR, FIGURES_DIR)
    analyze_keyword_category(MEDIUM, "Medium", abstracts, OUTPUT_DIR, FIGURES_DIR)
    analyze_keyword_category(STRATEGY, "Strategy", abstracts, OUTPUT_DIR, FIGURES_DIR)
    analyze_keyword_category(TOOL, "Tool", abstracts, OUTPUT_DIR, FIGURES_DIR)

if __name__ == "__main__":
    main()

