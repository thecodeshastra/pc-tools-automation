"""Tools for the career assistant."""

# python module
import os
import yaml

# langchain module
from langchain.tools import tool


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
