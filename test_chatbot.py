from src.rag import ask_question

question = "How many vacation days do employees receive?"

answer, sources = ask_question(question)

print("=" * 60)
print("QUESTION:")
print(question)

print("\nANSWER:")
print(answer)

print("\nSOURCES:")
for source in sources:
    print("-", source)

print("=" * 60)