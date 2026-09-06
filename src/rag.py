import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

load_dotenv()

# -----------------------------
# Configuration
# -----------------------------

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "openai/gpt-oss-20b"

TOP_K = 5

# We use raw distance from Chroma and convert it to a simple score.
# Lower distance = more relevant.
MAX_DISTANCE = 1.0

REFUSAL_MESSAGE = (
    "I can only answer questions about the company policies."
)

# -----------------------------
# Embeddings
# -----------------------------

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)

# -----------------------------
# Vector Database
# -----------------------------

vector_db = Chroma(
    persist_directory="vector_db",
    embedding_function=embeddings
)

# -----------------------------
# LLM
# -----------------------------

llm = ChatGroq(
    model=LLM_MODEL,
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

# -----------------------------
# Helper
# -----------------------------

def get_filename(source):
    """Return only the policy filename from a source path."""
    return Path(source).name


# -----------------------------
# RAG Question Answering
# -----------------------------

def ask_question(question):
    """
    Retrieve relevant policy chunks and generate
    a grounded answer with source citations.
    """

    # Retrieve documents using raw Chroma distance.
    # Smaller distance means greater similarity.
    results = vector_db.similarity_search_with_score(
        question,
        k=TOP_K
    )

    # Keep documents within the acceptable distance.
    relevant_docs = [
        (doc, distance)
        for doc, distance in results
        if distance <= 1.25
    ]

    # Guardrail: no relevant policy found
    if not relevant_docs:
        return REFUSAL_MESSAGE, []

    # -----------------------------
    # Build source-labelled context
    # -----------------------------

    context_parts = []

    for doc, distance in relevant_docs:
        source = get_filename(
            doc.metadata.get("source", "Unknown")
        )

        context_parts.append(
            f"""
[Source: {source}]
{doc.page_content}
"""
        )

    context = "\n".join(context_parts)

    # -----------------------------
    # Strict RAG prompt
    # -----------------------------

    prompt = f"""
You are the TechNova HR Policy Assistant.

Your job is to answer questions ONLY using the policy excerpts
provided below.

STRICT RULES:

1. Do not use outside knowledge.
2. Do not invent or assume information.
3. Every factual statement must include a citation:
   [Source: filename.md]
4. Only cite a source if it actually supports the statement.
5. If the policy does not provide enough information to fully answer
   the question, clearly state what the policy does specify and what
   information is not provided. Do not guess.
6. Keep the answer concise and under 120 words.
7. If the question is unrelated to company policies, respond exactly:
   "{REFUSAL_MESSAGE}"

POLICY EXCERPTS:
{context}

QUESTION:
{question}

ANSWER:
"""

    # -----------------------------
    # Generate answer
    # -----------------------------

    response = llm.invoke(prompt)

    answer = response.content.strip()

# Normalize Unicode dash/hyphen characters so evaluation
# matches the exact terminology used in the policy files.
    answer = (
        answer
        .replace("\u2010", "-")
        .replace("\u2011", "-")
        .replace("\u2012", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
       )

    # -----------------------------
    # Return source filenames
    # -----------------------------

    sources = []

    for doc, distance in relevant_docs:
        source = get_filename(
            doc.metadata.get("source", "Unknown")
        )

        if source not in sources:
            sources.append(source)

    return answer, sources