import os
import requests
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


# # -----------------------------
# # 3. Process documents
# # -----------------------------
# def embed_all_spell_descriptions(batch_size=50):
#     docs = collection.find(
#         {"desc": {"$exists": True}, "desc_embedding": {"$exists": False}},
#         {"_id": 1, "desc": 1},
#         batch_size=batch_size
#     )

#     count = 0

#     for doc in docs:
#         spell_id = doc["_id"]
#         desc_text = doc["desc"]

#         if not desc_text.strip():
#             continue

#         print(f"Embedding spell {_id}...")

#         # ---- Embed text ----
#         embedding = get_embedding(desc_text)

#         # ---- Store back into Mongo ----
#         collection.update_one(
#             {"_id": spell_id},
#             {"$set": {"desc_embedding": embedding}}
#         )

#         count += 1
#         time.sleep(0.1)  # gentle rate-limiting

#     print(f"Done. Embedded {count} documents.")


# if __name__ == "__main__":
#     embed_all_spell_descriptions()
