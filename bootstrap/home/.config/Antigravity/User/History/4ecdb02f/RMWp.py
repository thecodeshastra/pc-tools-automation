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
from langchain.agents import initialize_agent, AgentType

# langchain prompts
from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder

# gradio
import gradio as gr

# carrer_assistant module
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


CAREER_RAG_PROMPT = """
You are acting as {name}.

You are a professional career assistant chatbot on {name}'s website.
Answer questions ONLY using the provided context.

Rules:
- Be professional and concise
- Never hallucinate
- If the answer is not in the context, say "I don't know"
- Do not invent details

Context:
{context}

Question:
{question}
"""

rag_prompt = PromptTemplate(
    template=CAREER_RAG_PROMPT, input_variables=["context", "question", "name"]
)


AGENT_SYSTEM_PROMPT = """
You are an AI agent acting as {name}.

Your role:
- Represent {name} professionally
- Decide when to use tools
- Record unanswered questions
- Save user contact details when provided

Rules:
- Never hallucinate
- Use tools when appropriate
- Be helpful but honest
"""

agent_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", AGENT_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


vectorstore = build_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

qa_chain = RetrievalQA.from_chain_type(
    llm=get_ollama_llm(), retriever=retriever, return_source_documents=False
)


agent = initialize_agent(
    tools=[record_unknown_question, record_user_email],
    llm=get_ollama_llm(),
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
)


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
            f"The user asked: '{user_message}'. Record this as an unanswered question."
        )
        return "I don’t have that information yet, but I’ve saved the question for future improvement."

    return answer


if __name__ == "main":
    gr.ChatInterface(
        fn=chat,
        title="Personal Career Assistant",
        description="Ask me about my career, experience, and skills.",
    ).launch()
