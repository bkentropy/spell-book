import os
import pymongo
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


    def embed_all_spell_descriptions(self, collection, batch_size=10):
        """
        Process and embed spell descriptions in batches.
        
        Args:
            collection: MongoDB collection
            batch_size: Number of documents to process in each batch
        """
        # First, count total documents to process
        total = collection.count_documents({
            "desc": {"$exists": True},
            "desc_embedding": {"$exists": False},
            "resource_type": "spells"
        })
        
        if total == 0:
            print("No documents to process.")
            return
            
        print(f"Found {total} documents to process in batches of {batch_size}...")
        
        processed = 0
        batch = []
        
        cursor = collection.find(
            {
                "desc": {"$exists": True},
                "desc_embedding": {"$exists": False},
                "resource_type": "spells"
            },
            {"_id": 1, "desc": 1},
            batch_size=batch_size
        )

        for doc in cursor:
            try:
                spell_id = doc["_id"]
                desc_text = doc["desc"]
                
                # Handle both string and array types for desc_text
                if isinstance(desc_text, list):
                    desc_text = ' '.join(str(p) for p in desc_text if p)
                
                desc_text = str(desc_text).strip()
                
                if not desc_text:
                    continue
                    
                # Get embedding for this document
                embedding = self.get_embedding(desc_text).get("embeddings")[0]
                
                # Add to batch
                batch.append((spell_id, embedding))
                processed += 1
                
                # Process batch if we've reached batch size
                if len(batch) >= batch_size:
                    self._process_batch(collection, batch)
                    print(f"Processed {processed}/{total} documents...")
                    batch = []
                    
            except Exception as e:
                print(f"Error processing document {doc.get('_id', 'unknown')}: {str(e)}")
                continue
        
        # Process any remaining documents in the last partial batch
        if batch:
            self._process_batch(collection, batch)
            
        print(f"Done. Successfully processed {processed} documents.")
        
    def _process_batch(self, collection, batch):
        """Process a batch of spell embeddings and update the database."""
        bulk_operations = []
        
        for spell_id, embedding in batch:
            bulk_operations.append(
                pymongo.UpdateOne(
                    {"_id": spell_id},
                    {"$set": {"desc_embedding": embedding}}
                )
            )
            
        if bulk_operations:
            collection.bulk_write(bulk_operations, ordered=False)

