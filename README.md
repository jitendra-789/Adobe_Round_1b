# Adobe Round 1B – Intelligent Document Section Extractor

## 📝 Overview

This project addresses **Challenge 1B** of the Adobe Document Intelligence task. The goal is to automatically extract the most **relevant sections and sub-sections** from a set of input documents (PDFs) based on a provided **persona** and **job-to-be-done (JTBD)** description. The output is a structured JSON containing metadata, ranked sections, and refined sub-section analysis.

---

## 📂 Directory Structure

```
Adobe_Round_1b/
├── input/                     # Folder for input PDFs and persona
│   ├── *.pdf
│   └── challenge1b_input.json
├── output/
│   └── challenge1b_output.json
├── models/                    # Pre-downloaded FLAN-T5/MT5 model files
├── main.py                    # Entry-point script for processing
├── src/                     # Helper modules
│   └── input_loader.py
│   └── pdf_extractor.py
│   └──relevance_ranker.py
│   └──text_refiner_llm.py
├── Dockerfile
├── requirements.txt
├── approach_explanation.md
└── README.md
```
---

## ⚙️ Execution Instructions (Docker)

Here’s your Docker usage instructions formatted and highlighted in Markdown:

⸻

🐳 Docker Instructions

🔧 1. Build the Docker Image
```bash
docker build -t adobe_round_1b .
```
This will build the Docker image using the provided Dockerfile.

⸻

🚀 2. Run the Docker Container

Assuming your input PDFs and JSON are in the **input/** folder, run:
```
Adobe_Round_1b/
├── input/                     # Folder for input PDFs and persona
│   ├── *.pdf
│   └── challenge1b_input.json
```
```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  adobe_round_1b
```
✅ This will mount your local input/ and output/ folders to the container and run the pipeline.

📄 After execution, the output will be saved as:
```
output/challenge1b_output.json
```
Here is a cleanly structured and well-formatted version of your content in Markdown:

⸻

📤 Output Format

The generated output JSON follows the structure outlined below:

1. 🧾 Metadata
```
{
  "input_documents": [...],
  "persona": "...",
  "job_to_be_done": "...",
  "processing_timestamp": "..."
}
```
2. 📚 Extracted Sections
```
[
  {
    "document": "doc1.pdf",
    "page_number": 3,
    "section_title": "Experience Overview",
    "importance_rank": 1
  },
  ...
]
```
3. 🧠 Sub-section Analysis
```
[
  {
    "document": "doc1.pdf",
    "refined_text": "Detailed sub-section relevant to job",
    "page_number": 3
  },
  ...
]
```
✅ The output strictly follows the required format defined in challenge1b_output.json.

⸻

📦 Deliverables
	•	approach_explanation.md – Methodology and model design explanation (300–500 words).
	•	Dockerfile – Container setup for offline, CPU-only execution.
	•	README.md – This file with setup instructions, usage, and references.
	•	output/challenge1b_output.json – Final output generated from sample input documents.

⸻

⚖️ Evaluation Criteria Mapping
	•	Section Relevance (60 points)
→ Uses embedding similarity + persona/job scoring with intelligent ranking.
	•	Sub-section Relevance (40 points)
→ Refined sub-section summaries using local mT5 model.
	•	Execution Constraints
	•	✅ CPU-only
	•	✅ Model size ≤ 1GB
	•	✅ Offline inference using pre-downloaded model weights.
	•	Output Format
	•	✅ Structured JSON output
	•	✅ Includes metadata, extracted sections, and sub-section summaries.

⸻

📄 Refer To
	•	approach_explanation.md for:
	•	Document extraction pipeline
	•	Ranking mechanism
	•	LLM-based sub-section refinement
	•	Offline execution setup with local models

⸻
## 👨‍💻 Authors
👥 TeamIronMan – Adobe Hackathon 2025

This solution was collaboratively built as part of the Adobe Hackathon 2025 by TeamIronMan 🚀:


**Jitendra Kolli**
: [https://github.com/jitendra-789](jitendra-789)

**Prasanth**
: [https://github.com/prasanth1221](prasanth1221)
