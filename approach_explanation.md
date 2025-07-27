
# Approach Explanation – Challenge 1B: Persona-Driven Document Intelligence

## Overview  
Our system acts as an **offline, CPU-only document analyst** that selects and ranks the most relevant sections across a small collection of PDFs (3–10 docs) for a **given persona** and their **job-to-be-done (JTBD)**. It then **refines** the top sections into concise, readable snippets using a **multilingual, sub-1 GB LLM** (`google/mt5-small`), satisfying the competition’s runtime and size constraints.

## Pipeline (End-to-End)

1. **Input Loader (Phase 0)**  
   Reads `challenge1b_input.json`, extracting:
   - Persona (`role`)
   - Job-to-be-done (`task`)
   - Document list and challenge metadata

2. **PDF Text Extraction (Phase 1 & 2)**  
   We parse PDFs **fully offline** using `PyPDF2`, page by page, and build a lightweight structure:
   ```python
   {
     "document.pdf": {
        page_number: "raw text …"
     }
   }
   ```
   Basic, fast regex heuristics split text into candidate “sections” (titles / headings / short chunks).

3. **Relevance Ranking (Phase 3)**  
   We construct a **semantic query** from persona + JTBD (e.g., `"Travel Planner: Plan a 4-day trip for 10 college friends"`).  
   Each extracted section is embedded and scored for similarity to this query (e.g., using a compact, CPU-friendly local encoder such as `all-MiniLM-L6-v2`, <100 MB). Sections are sorted by similarity (**importance score**) and assigned an **`importance_rank`**.

   To better match the sample ground truths and avoid overfitting to a single PDF, we add a **diversity filter**: select **Top-N (default 10)** while capping **max_per_doc** (e.g., 2–3 per PDF).

4. **LLM Refinement (Phase 4)**  
   The top ranked sections are passed to a **multilingual summarizer** (`google/mt5-small`, ~300 MB) that:
   - Runs **entirely on CPU**
   - Works **offline** (weights are bundled inside the Docker image)
   - Produces short, well-formed “refined_text” snippets

   Prompt style: `summarize: <section text>` (works across languages; future prompts can be language-aware).

5. **Output Writer (Phase 5)**  
   We emit a strict JSON (`challenge1b_output.json`) containing:
   - **metadata** (documents, persona, JTBD, timestamp)
   - **extracted_sections** (document, page, section_title, importance_rank)
   - **subsection_analysis** (document, refined_text, page_number)

## Constraints Compliance
- **CPU-only**: All steps run on CPU.
- **Model size ≤ 1 GB**: `mt5-small` (~300 MB) + MiniLM (~100 MB) + code comfortably fit under 1 GB.
- **≤ 60 seconds** for 3–5 docs: Achieved via lightweight embedding, tight truncation (≤512 tokens), and Top-N limiting.
- **No internet**: Models are **pre-downloaded** and shipped inside the Docker image.

## Future Improvements
- **Language detection** to auto-adapt prompts.
- **Better section boundary detection** using layout cues (font size, boldness, TOC parsing).
- **Faster inference** via ONNX or TorchScript CPU quantization.
- **Task-aware reranking** (e.g., BM25 + semantic fusion).

---

This approach balances **accuracy, speed, multilingual capability, and strict offline/CPU constraints**, while producing outputs that align with the required JSON schema and scoring criteria (section relevance & sub-section refinement).
