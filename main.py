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
    """Extract the first meaningful line as the section title."""
    first_line = text.strip().split("\n")[0]
    return re.sub(r"^[•\-\*\s]+", "", first_line).strip()

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

def run_pipeline(collection_path):
    # Phase 0: Load input
    loader = InputLoader(collection_path)
    persona = loader.input_data['persona']['role']
    task = loader.input_data['job_to_be_done']['task']

    # Phase 1 & 2: Extract text from PDFs
    extractor = PDFExtractor(collection_path)
    _ = extractor.extract_text()

    ranker = RelevanceRanker(collection_path)
    all_ranked_sections = ranker.rank_sections()

    top_sections = select_top_sections_diverse(
        all_ranked_sections,
        max_per_doc=3,
        top_n=15
    )
    # Phase 4: Refine selected sections using CPU-based LLM
    llm_refiner = LLMRefiner("models/flan-t5-small")
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

    # Save output JSON
    output_file = os.path.join(collection_path, "challenge1b_output.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4)

    print(f"\n✅ Output saved to: {output_file}")


if __name__ == "__main__":
    collection_name = "Collection_3"  # Change as needed
    run_pipeline(collection_name)