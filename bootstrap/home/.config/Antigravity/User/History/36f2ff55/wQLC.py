"""Loading data module for career assistant."""

# Import necessary libraries
import os
import yaml
from typing import List

# langchain module
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.schema import Document

# career assistant module
from .constants import RESOURCES_DIR

# constants
PDF_FILE = os.path.join(RESOURCES_DIR, "career_data.pdf")
YAML_FILE = os.path.join(RESOURCES_DIR, "extra_knowledge.yaml")
SUMMARY_FILE = os.path.join(RESOURCES_DIR, "summary.txt")


def load_text_from_pdf(pdf_path: str) -> List[Document]:
    """Load text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.
    Returns:
        List[Document]: Loaded text from the PDF.
    """
    reader = PyPDFLoader(pdf_path)
    return reader.load()


def load_extra_knowledge(yaml_path: str) -> List[Document]:
    """Load extra knowledge from a YAML file.

    Args:
        yaml_path (str): Path to the YAML file.
    Returns:
        dict: Loaded extra knowledge.
    """
    if not os.path.exists(yaml_path):
        return []

    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f) or []

    docs = []
    for item in data:
        content = f"Question: {item['question']}\nAnswer: {item['answer']}"
        docs.append(Document(page_content=content))
    return docs


def load_summary(summary_path: str) -> List[Document]:
    """Load summary from a text file.

    Args:
        summary_path (str): Path to the summary file.
    Returns:
        List[Document]: Loaded summary.
    """
    loader = TextLoader(summary_path)
    return loader.load()


def load_career_assistant_data() -> dict:
    """Load data for the career assistant from PDF and YAML files.

    Returns:
        dict: Dictionary containing extracted text and extra knowledge."""
    pdf_text = load_text_from_pdf(PDF_FILE)
    extra_knowledge = load_extra_knowledge(YAML_FILE)
    summary = load_summary(SUMMARY_FILE)
    return [pdf_text, extra_knowledge, summary]
