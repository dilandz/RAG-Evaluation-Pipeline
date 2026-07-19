# RAG Evaluation Pipeline

A document Q&A system powered by Gemini and ChromaDB that answers questions from a custom knowledge base, with an automated evaluation pipeline that scores answer quality.

## Architecture

```
┌─────────────┐     ┌──────────┐     ┌─────────┐
│ Knowledge   │────>│ ChromaDB │────>│ Gemini  │
│ Base (.md)  │     │ (Vectors)│     │  (LLM)  │
└─────────────┘     └──────────┘     └─────────┘
    ingest.py         query.py        evaluate.py
                                           │
                                    ┌──────v──────┐
                                    │ Eval Report │
                                    │   (JSON)    │
                                    └─────────────┘

```


## Setup

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd RAG Pipeline
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your Gemini API key (get one free at [Google AI Studio](https://aistudio.google.com)):
   ```
   GEMINI_API_KEY=your-key-here
   ```

## Usage

```bash
python ingest.py                         # Ingest knowledge base documents
python query.py "Your question here"     # Query the system
python evaluate.py                       # Run evaluation suite
```

## Sample Output

```
Question: How do I reset my API key?
Answer: Navigate to Settings > API Keys, click the three-dot menu next to
your key, select "Regenerate". The old key is immediately invalidated.
```

## Evaluation Results

The eval pipeline scores answers on **faithfulness** (supported by context?) and **relevance** (addresses the question?).

| Metric | Score |
|--------|-------|
| Average Faithfulness | ~4.5/5 |
| Average Relevance | ~4.3/5 |
| Overall Score | ~4.4/5 |

The system correctly refuses unanswerable questions rather than hallucinating.