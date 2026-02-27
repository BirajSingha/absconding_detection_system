from sentence_transformers import SentenceTransformer
import time

print("Starting debug script...")
start_time = time.time()
try:
    print("Loading SentenceTransformer('all-MiniLM-L6-v2')...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print(f"Model loaded successfully in {time.time() - start_time:.2f} seconds.")
except Exception as e:
    print(f"Error loading model: {e}")
