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
   git clone [https://github.com/dilandz/RAG-Evaluation-Pipeline.git]
   cd RAG-Evaluation-Pipeline
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

The project features a unified Command Line Interface (CLI) built into `main.py` to manage the entire RAG lifecycle.

### 1. Ingest Data
Parse documents, generate embeddings, and populate your local ChromaDB vector store:
```bash
python main.py ingest
```

### 2. Query the Knowledge Base
Ask questions directly from the terminal. The system retrieves relevant context chunks and passes them to the LLM for generation:
```bash
python main.py query "How do I reset my API key?"
```

#### 🔍 Debugging Retrieval
To inspect exactly what chunks were pulled from ChromaDB and view the raw context being injected into the prompt, append the `--verbose` flag:
```bash
python main.py query "How do I reset my API key?" --verbose
```

### 3. Run the Evaluation Suite
Execute the full automated evaluation pipeline. This launches the LLM-as-a-judge system to score your test dataset on faithfulness and relevance, outputting a structured JSON report:
```bash
python main.py evaluate
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
| Average Faithfulness | ~5/5 |
| Average Relevance | ~4.71/5 |
| Overall Score | ~4.86/5 |

The system correctly refuses unanswerable questions rather than hallucinating.