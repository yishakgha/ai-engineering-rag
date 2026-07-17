from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import glob


def load_documents():
    documents = []

    for file in glob.glob("data/policies/*.md"):
        loader = TextLoader(file, encoding="utf-8")
        documents.extend(loader.load())

    print(f"Loaded {len(documents)} documents")
    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    return chunks