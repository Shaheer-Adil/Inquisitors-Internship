# RAG Design

Corpus: `data/processed/rag_chunks.jsonl`
Collection: `mother_chatbot_v1`
Embedding model: `all-MiniLM-L6-v2` by default
Vector DB: Chroma
Default top_k: 5

Each chunk preserves:
`source_id`, `content_type`, `topic`, `emotion`, `intent`, `language`, and `chunk_id`.

The query is constructed from the original message plus the baseline emotion/intent/language analysis. Retrieved text is reference context only; it is never treated as system instructions.
