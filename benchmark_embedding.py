import time
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "BAAI/bge-m3",
    trust_remote_code=True
)

print("Device:", model.device)

# Warm-up
model.encode("hello", normalize_embeddings=True)

start = time.perf_counter()

for _ in range(10):
    model.encode(
        "What services does NAVSOFT provide?",
        normalize_embeddings=True,
        show_progress_bar=False
    )

end = time.perf_counter()

print("Average encode time:", (end - start) / 10)