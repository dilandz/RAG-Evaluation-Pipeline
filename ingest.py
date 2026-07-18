import os
import chromadb
from pathlib import Path


def chunk_markdown(content, filename):
    """Split markdown content into chunks by heading sections."""
    chunks = []
    current_chunk = ""
    current_heading = filename

    for line in content.split("\n"):
        if line.startswith("## "):
            if current_chunk.strip():
                chunks.append({
                    "text": current_chunk.strip(),
                    "heading": current_heading,
                    "source": filename
                })
            current_heading = line.strip("# ").strip()
            current_chunk = line + "\n"
        else:
            current_chunk += line + "\n"

    if current_chunk.strip():
        chunks.append({
            "text": current_chunk.strip(),
            "heading": current_heading,
            "source": filename
        })

    return chunks

def ingest_documents():
    """Ingest all markdown files from knowledge_base/ into ChromaDB."""
    kb_path = Path("knowledge_base")
    if not kb_path.exists():
        print("Error: knowledge_base/ folder not found.")
        return

    client = chromadb.PersistentClient(path=".chroma")
    collection = client.get_or_create_collection(name="novatech_docs")

    all_documents = []
    all_ids = []
    all_metadatas = []

    for md_file in sorted(kb_path.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        chunks = chunk_markdown(content, md_file.name)

        for i, chunk in enumerate(chunks):
            doc_id = f"{md_file.stem}_chunk_{i}"
            all_documents.append(chunk["text"])
            all_ids.append(doc_id)
            all_metadatas.append({
                "source": chunk["source"],
                "heading": chunk["heading"],
                "chunk_index": i
            })

        collection.upsert(
        documents=all_documents,
        ids=all_ids,
        metadatas=all_metadatas
    )

    print(f"Ingested {len(all_documents)} chunks from {len(list(kb_path.glob('*.md')))} documents")
    print(f"Collection '{collection.name}' now contains {collection.count()} items")


if __name__ == "__main__":
    ingest_documents()