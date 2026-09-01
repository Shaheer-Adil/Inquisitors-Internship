import os
import chromadb
from sentence_transformers import SentenceTransformer
from .config import settings

class Retriever:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.chroma_path)
        self.collection = self.client.get_or_create_collection(
            name=settings.chroma_collection,
            metadata={"hnsw:space":"cosine","corpus_version":"mother_chatbot_day2_v1"}
        )
        self.embedder = SentenceTransformer(settings.embedding_model)

    def add_chunks(self, chunks):
        ids=[c["chunk_id"] for c in chunks]
        docs=[c["text"] for c in chunks]
        metas=[c["metadata"] for c in chunks]
        vectors=self.embedder.encode(docs, normalize_embeddings=True).tolist()
        self.collection.upsert(ids=ids, documents=docs, metadatas=metas, embeddings=vectors)

    def search(self, query, top_k=None):
        k=top_k or settings.top_k
        vector=self.embedder.encode([query], normalize_embeddings=True).tolist()
        result=self.collection.query(query_embeddings=vector,n_results=k,include=["documents","metadatas","distances"])
        rows=[]
        for i,cid in enumerate(result["ids"][0]):
            rows.append({"chunk_id":cid,"text":result["documents"][0][i],
                         "metadata":result["metadatas"][0][i],"distance":result["distances"][0][i]})
        return rows

    def count(self):
        return self.collection.count()
