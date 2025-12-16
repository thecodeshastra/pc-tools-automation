"""
Personal Career Assistant Agent
Tech stack:
- LangChain
- Open-source LLM (Ollama)
- FAISS vector store
- PyPDF
- YAML / Text
- Gradio UI
"""

# =========================
# 1. Imports & Setup
# =========================

import os
import yaml
from typing import List

from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

from langchain.llms import Ollama
from langchain.chains import RetrievalQA

from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType

import gradio as gr


# =========================
# 2. Load Career Data
# =========================

def load_pdf(path: str) -> List[Document]:
    loader = PyPDFLoader(path)
    return loader.load()


def load_text(path: str) -> List[Document]:
    loader = TextLoader(path)
    return loader.load()


def load_yaml_qa(path: str) -> List[Document]:
    if not os.path.exists(path):
        return []

    with open(path, "r") as f:
        data = yaml.safe_load(f) or []

    docs = []
    for item in data:
        content = f"Question: {item['question']}\nAnswer: {item['answer']}"
        docs.append(Document(page_content=content))
    return docs


# =========================
# 3. Build Knowledge Base
# =========================

def build_vectorstore():
    docs = []

    docs += load_pdf("me/linkedin.pdf")
    docs += load_text("me/summary.txt")
    docs += load_yaml_qa("me/qa.yaml")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    split_docs = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(split_docs, embeddings)
    return vectorstore


# =========================
# 4. Open-Source LLM
# =========================

llm = Ollama(
    model="llama3",
    temperature=0.3
)


# =========================
# 5. Tools (Agent Abilities)
# =========================

@tool
def record_unknown_question(question: str) -> str:
    """Store unanswered user questions for later improvement."""
    path = "me/unknown_questions.yaml"

    data = []
    if os.path.exists(path):
        with open(path, "r") as f:
            data = yaml.safe_load(f) or []

    data.append({"question": question})

    with open(path, "w") as f:
        yaml.safe_dump(data, f)

    return "Question recorded for later review."


@tool
def record_user_email(email: str, notes: str = "") -> str:
    """Save user contact information."""
    path = "me/leads.yaml"

    data = []
    if os.path.exists(path):
        with open(path, "r") as f:
            data = yaml.safe_load(f) or []

    data.append({"email": email, "notes": notes})

    with open(path, "w") as f:
        yaml.safe_dump(data, f)

    return "Contact details saved."


# =========================
# 6. RAG Chain
# =========================

vectorstore = build_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=False
)


# =========================
# 7. Agent (Reasoning + Tools)
# =========================

agent = initialize_agent(
    tools=[record_unknown_question, record_user_email],
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)


# =========================
# 8. Chat Logic
# =========================

def chat(user_message, history):
    """
    1. Try to answer using RAG
    2. If answer is weak / unknown → agent records question
    """

    answer = qa_chain.run(user_message)

    if (
        "I don't know" in answer
        or "not sure" in answer.lower()
        or len(answer.strip()) < 30
    ):
        agent.run(
            f"The user asked: '{user_message}'. "
            f"Record this as an unanswered question."
        )
        return "I don’t have that information yet, but I’ve saved the question for future improvement."

    return answer


# =========================
# 9. Gradio UI
# =========================

gr.ChatInterface(
    fn=chat,
    title="Personal Career Assistant",
    description="Ask me about my career, experience, and skills."
).launch()
