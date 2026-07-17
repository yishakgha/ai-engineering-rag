import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_db = Chroma(
    persist_directory="vector_db",
    embedding_function=embeddings
)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


def ask_question(question):
    docs = vector_db.similarity_search(question, k=3)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are an HR assistant.

Answer ONLY using the company policies below.

If the answer is not available, say:
"I cannot find that information in the company policies."

Company Policies:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    sources = [doc.metadata.get("source", "Unknown") for doc in docs]

    return response.content, sources