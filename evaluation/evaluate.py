import json
from pathlib import Path
from src.rag import ask_question


BASE_DIR = Path(__file__).resolve().parent.parent
QUESTIONS_FILE = BASE_DIR / "evaluation" / "test_questions.json"


with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
    questions = json.load(f)


passed = 0
failed = 0


for i, item in enumerate(questions, 1):

    question = item["question"]
    expected_source = item["expected_source"]
    expected_answer = item["expected_answer_contains"]

    answer, sources = ask_question(question)

    source_ok = expected_source in sources
    answer_ok = expected_answer.lower().replace(" ", "") in answer.lower().replace(" ", "").replace("\u202f", "")

    if source_ok and answer_ok:
        status = "PASS"
        passed += 1
    else:
        status = "FAIL"
        failed += 1

    print(f"\n[{status}] Test {i}")
    print(f"Question: {question}")
    print(f"Answer: {answer}")
    print(f"Sources: {sources}")


print("\n" + "=" * 50)
print("EVALUATION SUMMARY")
print("=" * 50)
print(f"Total tests : {len(questions)}")
print(f"Passed      : {passed}")
print(f"Failed      : {failed}")
print(f"Accuracy    : {(passed / len(questions)) * 100:.1f}%")