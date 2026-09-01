import json
from backend.retriever import Retriever

chunks=[json.loads(line) for line in open("data/processed/rag_chunks.jsonl",encoding="utf-8") if line.strip()]
r=Retriever()
r.add_chunks(chunks)
print(f"Indexed {len(chunks)} chunks. Collection count: {r.count()}")
