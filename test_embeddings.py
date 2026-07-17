from src.loader import load_documents, split_documents
from src.embeddings import create_vector_db

documents = load_documents()

chunks = split_documents(documents)

vector_db = create_vector_db(chunks)

print("Done!")