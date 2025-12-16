"""Loading data module for career assistant."""

# Import necessary libraries
import os
import yaml
# langchain module
from langchain.document_loaders import PyPDFLoader, TextLoader
# career assistant module
from .constants import RESOURCES_DIR

# constants
PDF_FILE = os.path.join(RESOURCES_DIR, "career_data.pdf")
YAML_FILE = os.path.join(RESOURCES_DIR, "extra_knowledge.yaml")
SUMMARY_FILE = os.path.join(RESOURCES_DIR, "summary.txt")

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file.
    Returns:
        str: Extracted text from the PDF."""
    reader = PdfReader(pdf_path)
    pdf_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pdf_text += text
    return text


def load_extra_knowledge(yaml_path: str) -> str:
    """Load extra knowledge from a YAML file.
    
    Args:
        yaml_path (str): Path to the YAML file.
    Returns:
        dict: Loaded extra knowledge."""
    with open(yaml_path, "r") as file:
        data = yaml.safe_load(file)
        data = "\n".join([str(item) for item in data])
    return data


def load_summary(summary_path: str) -> str:
    """Load summary from a text file.
    
    Args:
        summary_path (str): Path to the summary file.
    Returns:
        str: Loaded summary."""
    with open(summary_path, "r") as file:
        summary = file.read()
    return summary


def load_career_assistant_data() -> dict:
    """Load data for the career assistant from PDF and YAML files.
    
    Returns:
        dict: Dictionary containing extracted text and extra knowledge."""
    pdf_text = extract_text_from_pdf(PDF_FILE)
    extra_knowledge = load_extra_knowledge(YAML_FILE)
    summary = load_summary(SUMMARY_FILE)
    return pdf_text, extra_knowledge, summary
