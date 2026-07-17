from src.loader import load_documents, split_documents

documents = load_documents()

chunks = split_documents(documents)

print(chunks[0].page_content)