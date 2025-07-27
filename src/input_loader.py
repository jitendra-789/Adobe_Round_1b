import os
import json
from datetime import datetime

class InputLoader:
    def __init__(self, collection_path: str):
        self.collection_path = collection_path
        self.input_path = os.path.join(self.collection_path, "challenge1b_input.json")  # ✅ Fixed path
        self.input_data = self._load_json()

    def _load_json(self):
        with open(self.input_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_documents(self):
        return self.input_data["documents"]

    def get_persona(self):
        return self.input_data["persona"]

    def get_job_to_be_done(self):
        return self.input_data["job_to_be_done"]

    def get_challenge_info(self):
        return self.input_data.get("challenge_info", {})

    def get_metadata(self):
        return {
            "input_documents": [doc["filename"] for doc in self.input_data["documents"]],
            "persona": self.input_data["persona"]["role"],
            "job_to_be_done": self.input_data["job_to_be_done"]["task"],
            "processing_timestamp": datetime.now().isoformat()
        }


if __name__ == "__main__":
    loader = InputLoader("Collection_1")  # Replace with any collection folder name
    print("Documents:", loader.get_documents())
    print("Persona:", loader.get_persona())
    print("Job To Be Done:", loader.get_job_to_be_done())
    print("Metadata:", loader.get_metadata())