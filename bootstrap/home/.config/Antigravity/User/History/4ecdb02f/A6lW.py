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

# langchain text splitters
from langchain.text_splitter import RecursiveCharacterTextSplitter

# langchain embeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# langchain llms
from langchain.chains import RetrievalQA

# langchain tools
from langchain.agents import create_openai_functions_agent, AgentExecutor

# langchain prompts
from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder

# gradio
import gradio as gr

# carrer_assistant module
from .constants import CAREER_RAG_PROMPT, AGENT_SYSTEM_PROMPT, NAME
from .llm import get_ollama_llm
from .loader import load_career_assistant_data
from .tools import record_unknown_question, record_user_email


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


# prompts
rag_prompt = PromptTemplate(
    template=CAREER_RAG_PROMPT, input_variables=["context", "question", "name"]
)
agent_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", AGENT_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# retrivers
vectorstore = build_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# qa_chain
qa_chain = RetrievalQA.from_chain_type(
    llm=get_ollama_llm(),
    retriever=retriever,
    chain_type_kwargs={"prompt": rag_prompt, "document_variable_name": "context"},
)

# agent
agent = create_openai_functions_agent(
    llm=get_ollama_llm(),
    tools=[record_unknown_question, record_user_email],
    prompt=agent_prompt,
)
agent_executor = AgentExecutor(
    agent=agent, tools=[record_unknown_question, record_user_email], verbose=True
)


# ======================================================
# 9. Chat Logic (Orchestration Layer)
# ======================================================


def chat(user_message, history):
    """
    1. Attempt RAG answer
    2. If weak/unknown → agent records question
    """

    answer = qa_chain.run({"query": user_message, "name": NAME})

    if "I don't know" in answer or len(answer.strip()) < 30:
        agent_executor.run(
            f"The user asked: '{user_message}'. This could not be answered. Record it."
        )
        return (
            "I don’t have that information yet, but I’ve saved the question for review."
        )

    return answer


if __name__ == "main":
    gr.ChatInterface(
        fn=chat,
        title="Personal Career Assistant",
        description="Ask me about my career, experience, and skills.",
    ).launch()
