from src.rag import search

query = "How many vacation days do employees receive?"

results = search(query)

print("\nQuestion:")
print(query)

print("\nTop Results:\n")

for i, doc in enumerate(results, start=1):
    print(f"Result {i}")
    print("-" * 40)
    print(doc.page_content)
    print("\nSource:", doc.metadata.get("source"))
    print()