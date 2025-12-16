"""Practicing AI agents with Vanderbilt University's coursera course."""

from typing import List, Dict
from litellm import completion


def generate_response(msg: List[Dict]) -> str:
    """Call LLM to get response"""
    rsp = completion(
        model="openai/gpt-4o",
        messages=msg,
        max_tokens=1024
    )
    return rsp.choices[0].message.content


messages = [
    {
        "role": "system",
        "content": "You are an expert software engineer that prefers functional programming."
    },
    {
        "role": "user",
        "content": "Write a function to swap the keys and values in a dictionary."
    }
]

response = generate_response(messages)
print(response)
