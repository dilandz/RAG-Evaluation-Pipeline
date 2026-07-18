import os
import sys
import json
import time
from dotenv import load_dotenv
from google import genai
from query import retrieve_context, generate_answer

load_dotenv()


def get_gemini_client():
    """Initialize and return a Gemini client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file")
        sys.exit(1)
    return genai.Client(api_key=api_key)

def judge_answer(question, answer, context_docs, expected_answer, category):
    """Use Gemini as a judge to score the answer on faithfulness and relevance."""
    context_text = "\n".join(context_docs)

    prompt = f"""You are an evaluation judge for a RAG (Retrieval-Augmented Generation) system. Score the following answer on two dimensions.

Question: {question}
Expected Answer: {expected_answer}
Category: {category} (if "unanswerable", the system should refuse to answer rather than hallucinate)

Retrieved Context:
{context_text}

System Answer: {answer}

Score on these dimensions (1-5 each):

1. FAITHFULNESS: Is the answer supported by the retrieved context? (5 = fully supported, 1 = contradicts or fabricates information not in context)
2. RELEVANCE: Does the answer address the question? For "unanswerable" questions, does it correctly refuse? (5 = perfectly addresses the question or correctly refuses, 1 = completely off-topic or hallucinates when should refuse)

Respond in this exact JSON format:
{{"faithfulness": <score>, "faithfulness_reason": "<brief reason>", "relevance": <score>, "relevance_reason": "<brief reason>"}}"""

    client = get_gemini_client()
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    try:
        response_text = response.text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("\n", 1)[1].rsplit("```", 1)[0]
        scores = json.loads(response_text)
        return scores
    except (json.JSONDecodeError, IndexError):
        return {
            "faithfulness": 0,
            "faithfulness_reason": "Failed to parse judge response",
            "relevance": 0,
            "relevance_reason": "Failed to parse judge response"
        }
    
def run_evaluation():
    """Run the full evaluation pipeline."""
    with open("test_questions.json", "r") as f:
        test_cases = json.load(f)

    results = []
    total_faithfulness = 0
    total_relevance = 0

    print("=" * 60)
    print("RAG EVALUATION REPORT")
    print("=" * 60)

    for i, test in enumerate(test_cases):
        print(f"\n[{i+1}/{len(test_cases)}] {test['question']}")

        context_results = retrieve_context(test["question"])
        answer = generate_answer(test["question"], context_results)
        scores = judge_answer(
            test["question"],
            answer,
            context_results["documents"][0],
            test["expected_answer"],
            test["category"]
        )

        total_faithfulness += scores.get("faithfulness", 0)
        total_relevance += scores.get("relevance", 0)

        result = {
            "question": test["question"],
            "category": test["category"],
            "answer": answer,
            "scores": scores
        }
        results.append(result)

        print(f"  Faithfulness: {scores.get('faithfulness', 0)}/5 - {scores.get('faithfulness_reason', 'N/A')}")
        print(f"  Relevance:    {scores.get('relevance', 0)}/5 - {scores.get('relevance_reason', 'N/A')}")
        print("Waiting 15 seconds to respect free tier API rate limits...")
        time.sleep(30)

    num_tests = len(test_cases)
    avg_faithfulness = total_faithfulness / num_tests if num_tests > 0 else 0
    avg_relevance = total_relevance / num_tests if num_tests > 0 else 0

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total questions evaluated: {num_tests}")
    print(f"Average Faithfulness: {avg_faithfulness:.2f}/5")
    print(f"Average Relevance:    {avg_relevance:.2f}/5")
    print(f"Overall Score:        {((avg_faithfulness + avg_relevance) / 2):.2f}/5")


if __name__ == "__main__":
    run_evaluation()