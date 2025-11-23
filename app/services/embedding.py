import os
import requests
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class EmbeddingClient:
    def __init__(self):
        self.url = os.getenv("EMBEDDING_SERVICE_URL", "http://10.13.13.6:8001")
        if not self.url:
            raise ValueError("EMBEDDING_SERVICE_URL environment variable not set")

    def get_embedding(self, text: str):
        response = requests.post(
            f"{self.url}/embed",
            json={"texts": text}
        )
        return response.json()


    def embed_all_spell_descriptions(self, collection, batch_size=50):
        docs = collection.find(
            {
                "desc": {"$exists": True},
                "desc_embedding": {"$exists": False},
                "resource_type": "spells"
            },
            {"_id": 1, "desc": 1},
            batch_size=batch_size
        )

        count = 0

        for doc in docs:
            spell_id = doc["_id"]
            desc_text = doc["desc"]
            
            # Handle both string and array types for desc_text
            if isinstance(desc_text, list):
                # Join list of strings with spaces if it's an array
                desc_text = ' '.join(str(p) for p in desc_text if p)
            
            # Convert to string and strip whitespace
            desc_text = str(desc_text).strip()
            
            if not desc_text:
                continue

            print(f"Embedding spell {spell_id}...")

            # ---- Embed text ----
            embedding = self.get_embedding(desc_text).get("embeddings")

            # ---- Store back into Mongo ----
            collection.update_one(
                {"_id": spell_id},
                {"$set": {"desc_embedding": embedding}}
            )

            count += 1
            time.sleep(0.1)  # gentle rate-limiting

        print(f"Done. Embedded {count} documents.")

