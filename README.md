Here is a complete and concise README.md file for your Adobe_Round_1b submission, fully aligned with the required deliverables, execution expectations, and scoring criteria you just shared:

⸻


# Adobe Round 1B – Intelligent Document Section Extractor

## 📝 Overview

This project addresses **Challenge 1B** of the Adobe Document Intelligence task. The goal is to automatically extract the most **relevant sections and sub-sections** from a set of input documents (PDFs) based on a provided **persona** and **job-to-be-done (JTBD)** description. The output is a structured JSON containing metadata, ranked sections, and refined sub-section analysis.

---

## 📂 Directory Structure

Adobe_Round_1b/
├── input/                      # Folder for input PDFs and persona
│   ├── *.pdf
│   ├── persona.json
│   └── job_description.json
├── output/
│   └── challenge1b_output.json
├── models/                    # Pre-downloaded FLAN-T5/MT5 model files
├── main.py                    # Entry-point script for processing
├── utils/                     # Helper modules
│   └── *.py
├── Dockerfile
├── requirements.txt
├── approach_explanation.md
└── README.md

---

## ⚙️ Execution Instructions (Docker)

### 🔧 1. Build Docker Image

```bash
docker build -t adobe_round_1b .

🚀 2. Run the Container

Assuming your inputs are in input/ folder:

docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  adobe_round_1b

This will generate challenge1b_output.json in the output/ folder.

⸻

📤 Output Format

The generated JSON includes the following:

1. Metadata

{
  "input_documents": [...],
  "persona": "...",
  "job_to_be_done": "...",
  "processing_timestamp": "..."
}

2. Extracted Sections

[
  {
    "document": "doc1.pdf",
    "page_number": 3,
    "section_title": "Experience Overview",
    "importance_rank": 1
  },
  ...
]

3. Sub-section Analysis

[
  {
    "document": "doc1.pdf",
    "refined_text": "Detailed sub-section relevant to job",
    "page_number": 3
  },
  ...
]

✅ Output JSON is aligned with challenge1b_output.json sample format.

⸻

📦 Deliverables
	•	approach_explanation.md: Methodology and model design (300–500 words).
	•	Dockerfile: Containerized setup for offline, CPU-only execution.
	•	README.md: This file with setup, usage, and references.
	•	challenge1b_output.json: Output from sample test documents (placed in /output).

⸻

⚖️ Evaluation Criteria Mapping

Criteria	Points	Project Alignment
Section Relevance	60	Uses embedding + persona/job scoring with ranking logic
Sub-Section Relevance	40	Granular sub-section analysis using semantic refinement
Execution Constraints	—	✅ CPU-only✅ Model ≤ 1GB✅ Offline inference
Output Format	—	✅ Structured JSON output


⸻

📄 Refer to
	•	approach_explanation.md for details on methodology and implementation logic.

⸻

❗ Notes
	•	Please ensure model files are placed in models/ before building the Docker image.
	•	Internet access is not required for Docker runtime.

---

Let me know if you'd like a version tailored to a different model or structure (e.g., if `main.py` takes args like `--input` and `--output`).