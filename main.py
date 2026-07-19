import argparse
import sys
from ingest import ingest_documents
from query import query_rag
from evaluate import run_evaluation


def main():
    # Set up the top-level argument parser
    parser = argparse.ArgumentParser(
        description="NovaTech RAG System - Document Q&A with Evaluation"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Ingest subcommand - no extra arguments needed
    subparsers.add_parser("ingest", help="Ingest knowledge base documents into ChromaDB")

    # Query subcommand - takes a question and optional verbose flag
    query_parser = subparsers.add_parser("query", help="Ask a question")
    query_parser.add_argument("question", type=str, help="The question to ask")
    query_parser.add_argument("--verbose", "-v", action="store_true", help="Show retrieved chunks and distances")

    # Evaluate subcommand - runs the full eval suite
    subparsers.add_parser("evaluate", help="Run the full evaluation suite")
    
    # Parse arguments and route to the correct function
    args = parser.parse_args()

    if args.command == "ingest":
        ingest_documents()
    elif args.command == "query":
        query_rag(args.question, verbose=args.verbose)
    elif args.command == "evaluate":
        run_evaluation()
    else:
        # No command provided - show help text
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()