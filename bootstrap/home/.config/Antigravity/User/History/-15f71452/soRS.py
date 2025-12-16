"""RAG module for career assistant."""

from langchain.vectorstores import FAISS
from langchain.document_loaders import load_career_assistant_data
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

from .loader import load_career_assistant_data
from .constants import NAME


def build_vectorstore() -> FAISS:
    """Build a vector store from career assistant data.

    Returns:
        FAISS: The vector store.
    """
    docs = load_career_assistant_data()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    split_docs = splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = FAISS.from_documents(split_docs, embeddings)
    return vectorstore
