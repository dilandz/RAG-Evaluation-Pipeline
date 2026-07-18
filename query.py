import os
import sys
import chromadb
from dotenv import load_dotenv
from google import genai

load_dotenv()


def get_gemini_client():
    """Initialize and return a Gemini client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file")
        sys.exit(1)
    return genai.Client(api_key=api_key)


def retrieve_context(question, n_results=3):
    """Query ChromaDB for relevant document chunks."""
    client = chromadb.PersistentClient(path=".chroma")
    collection = client.get_collection(name="novatech_docs")

    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )

    return results

def generate_answer(question, context_results):
    """Generate an answer using Gemini with retrieved context."""
    documents = context_results["documents"][0]
    metadatas = context_results["metadatas"][0]
    distances = context_results["distances"][0]

    context_block = ""
    for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances)):
        context_block += f"\n--- Source: {meta['source']} | Section: {meta['heading']} | Distance: {dist:.4f} ---\n"
        context_block += doc + "\n"

    prompt = f"""You are a helpful assistant for NovaTech Platform. Answer the user's question based ONLY on the provided context. If the context does not contain enough information to answer the question, say "I don't have enough information to answer this question based on the available documentation."

Context:
{context_block}

Question: {question}

Answer:"""

    client = get_gemini_client()
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text

def query_rag(question, verbose=False):
    """Full RAG pipeline: retrieve context and generate answer."""
    context_results = retrieve_context(question)
    answer = generate_answer(question, context_results)

    print(f"\nQuestion: {question}")
    print(f"\nAnswer: {answer}")

    if verbose:
        print("\n--- Retrieved Sources ---")
        for i, (meta, dist) in enumerate(zip(
            context_results["metadatas"][0],
            context_results["distances"][0]
        )):
            print(f"  {i+1}. {meta['source']} > {meta['heading']} (distance: {dist:.4f})")

    return answer


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python query.py \"Your question here\"")
        sys.exit(1)

    question = sys.argv[1]
    query_rag(question, verbose=True)