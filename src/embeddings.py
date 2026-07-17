from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


def create_vector_db(chunks):
    """
    Create and save the Chroma vector database.
    """

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="vector_db"
    )

    print("✅ Vector database created successfully!")

    return vector_db