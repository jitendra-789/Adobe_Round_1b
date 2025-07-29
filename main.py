import os
import json
import re
from datetime import datetime
from collections import defaultdict

from src.input_loader import InputLoader
from src.pdf_extractor import PDFExtractor
from src.relevance_ranker import RelevanceRanker
from src.text_refiner_llm import LLMRefiner


def clean_title(text):
    """
    Extracts an intelligent section title by analyzing the first few lines.
    It avoids generic titles (e.g., 'Conclusion') and prefers informative ones.
    """
    lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
    
    # If no lines, return a fallback
    if not lines:
        return "Untitled Section"

    # Filter candidates: avoid lines that are too short or purely numeric/bullet-like
    candidates = []
    for line in lines[:10]:  # Check top 10 lines only
        # Skip lines with fewer than 3 words or purely numeric
        if len(line.split()) < 3:
            continue
        if re.match(r"^[\d\W_]+$", line):
            continue
        candidates.append(line)

    # Prefer the longest candidate line that seems like a title
    if candidates:
        best = sorted(candidates, key=lambda x: len(x), reverse=True)[0]
        return best.strip(":-–. ")

    # Fallback to first non-empty line
    return lines[0].strip(":-–. ")

def select_top_sections_diverse(all_sections, max_per_doc=2, top_n=10):
    doc_counter = defaultdict(int)
    selected = []

    # Sort all by original importance_rank first
    for sec in sorted(all_sections, key=lambda x: x["importance_rank"]):
        doc = sec["document"]
        if doc_counter[doc] < max_per_doc:
            selected.append(sec)
            doc_counter[doc] += 1
        if len(selected) == top_n:
            break

    # Renumber importance_rank from 1 to len(selected)
    for idx, sec in enumerate(selected, start=1):
        sec["importance_rank"] = idx

    return selected

def run_pipeline(input_dir="input", output_dir="output"):
    # Phase 0: Load input
    loader = InputLoader(input_dir)
    persona = loader.input_data['persona']['role']
    task = loader.input_data['job_to_be_done']['task']

    # Phase 1 & 2: Extract text from PDFs
    extractor = PDFExtractor(input_dir)
    _ = extractor.extract_text()

    ranker = RelevanceRanker(input_dir)
    all_ranked_sections = ranker.rank_sections()

    top_sections = select_top_sections_diverse(
        all_ranked_sections,
        max_per_doc=3,
        top_n=20
    )

    # Phase 4: Refine selected sections using CPU-based LLM
    llm_refiner = LLMRefiner("models/all-MiniLM-L6-v2")
    subsection_analysis = llm_refiner.refine_sections(top_sections)

    # Phase 5: Combine and export results
    output_data = {
        "metadata": {
            "input_documents": [doc["filename"] for doc in loader.input_data["documents"]],
            "persona": persona,
            "job_to_be_done": task,
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [
            {
                "document": sec["document"],
                "section_title": clean_title(sec["text"]),
                "importance_rank": sec["importance_rank"],
                "page_number": sec["page"]
            } for sec in top_sections
        ],
        "subsection_analysis": subsection_analysis
    }

    # Ensure output folder exists
    os.makedirs(output_dir, exist_ok=True)

    # Save output JSON
    output_file = os.path.join(output_dir, "challenge1b_output.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)

    print(f"\n✅ Output saved to: {output_file}")


if __name__ == "__main__":
    run_pipeline()