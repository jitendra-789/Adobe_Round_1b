import os
from PyPDF2 import PdfReader

class PDFExtractor:
    def __init__(self, collection_path: str):
        self.collection_path = collection_path
        self.pdf_folder = os.path.join(collection_path, "PDFs")  # ✅ fixed here
        self.extracted_text = {}  # {filename: {page_num: text}}

    def extract_text(self):
        for pdf_file in os.listdir(self.pdf_folder):
            if not pdf_file.endswith(".pdf"):
                continue
            full_path = os.path.join(self.pdf_folder, pdf_file)
            reader = PdfReader(full_path)
            self.extracted_text[pdf_file] = {}

            for i, page in enumerate(reader.pages):
                try:
                    text = page.extract_text() or ""
                except Exception as e:
                    text = f"ERROR: {e}"
                self.extracted_text[pdf_file][i + 1] = text.strip()

        return self.extracted_text


if __name__ == "__main__":
    from input_loader import InputLoader

    loader = InputLoader("Collection_1")
    extractor = PDFExtractor("Collection_1")

    all_text = extractor.extract_text()

    for pdf_name, pages in all_text.items():
        print(f"\n📄 {pdf_name}")
        for page, text in pages.items():
            print(f"  Page {page}:\n{text[:200]}...\n")