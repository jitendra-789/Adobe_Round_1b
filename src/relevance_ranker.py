import os
import json
from datetime import datetime
from sentence_transformers import SentenceTransformer, util
from src.input_loader import InputLoader
from src.pdf_extractor import PDFExtractor


class RelevanceRanker:
    def __init__(self, collection_dir):
        self.collection_dir = collection_dir
        self.loader = InputLoader(collection_dir)
        self.extractor = PDFExtractor(collection_dir)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def rank_sections(self):
        persona = self.loader.input_data["persona"]["role"]
        task = self.loader.input_data["job_to_be_done"]["task"]
        query = f"{persona}: {task}"
        query_embedding = self.model.encode(query, convert_to_tensor=True)

        raw_extracted = self.extractor.extract_text()
        sections = []

        for doc_name, pages in raw_extracted.items():
            for page_num, text in pages.items():
                if not text.strip():
                    continue  # skip empty pages
                section_embedding = self.model.encode(text, convert_to_tensor=True)
                score = util.cos_sim(query_embedding, section_embedding).item()

                sections.append({
                    "document": doc_name,
                    "page": page_num,
                    "text": text.strip(),
                    "score": score
                })

        # Sort by relevance score
        ranked_sections = sorted(sections, key=lambda x: x["score"], reverse=True)

        # Assign importance_rank
        for i, section in enumerate(ranked_sections):
            section["importance_rank"] = i + 1
            del section["score"]

        return ranked_sections

    def generate_output_json(self, ranked_sections):
        output_data = {
            "metadata": {
                "input_documents": [doc["filename"] for doc in self.loader.input_data["documents"]],
                "persona": self.loader.input_data["persona"]["role"],
                "job_to_be_done": self.loader.input_data["job_to_be_done"]["task"],
                "processing_timestamp": datetime.now().isoformat()
            },
            "extracted_sections": [],
            "subsection_analysis": []
        }

        for sec in ranked_sections:
            output_data["extracted_sections"].append({
                "document": sec["document"],
                "section_title": sec["text"],
                "importance_rank": sec["importance_rank"],
                "page_number": sec["page"]
            })

            output_data["subsection_analysis"].append({
                "document": sec["document"],
                "refined_text": sec["text"],
                "page_number": sec["page"]
            })

        output_path = os.path.join(self.collection_dir, "challenge1b_output.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=4)

        print(f"[✅] Output saved to: {output_path}")


if __name__ == "__main__":
    collection = "Collection_1"
    ranker = RelevanceRanker(collection)
    ranked = ranker.rank_sections()
    ranker.generate_output_json(ranked)