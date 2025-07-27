import torch
from transformers import AutoTokenizer, MT5ForConditionalGeneration

class LLMRefiner:
    def __init__(self, model_name_or_path="models/flan-t5-small"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        self.model = MT5ForConditionalGeneration.from_pretrained(model_name_or_path).to(self.device)
        self.model.eval()

    def refine_sections(self, extracted_sections):
        refined_results = []

        for sec in extracted_sections:
            raw = sec["text"].strip().replace("\n", " ")
            # The prompt "summarize:" works across languages for mT5
            input_prompt = f"summarize: {raw[:500]}"  # Truncate input for safety

            inputs = self.tokenizer(input_prompt, return_tensors="pt", truncation=True, max_length=512).to(self.device)
            output_ids = self.model.generate(inputs["input_ids"], max_length=100, num_beams=4)

            summary = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

            refined_results.append({
                "document": sec["document"],
                "refined_text": summary.strip(),
                "page_number": sec["page"]
            })

        return refined_results