"""Practicing AI agents with Vanderbilt University's coursera course."""

import json
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

# Example usage
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

# we can also have code spec to be more specific
code_spec = {
    'name': 'swap_keys_values',
    'description': 'Swaps the keys and values in a given dictionary.',
    'params': {
        'd': 'A dictionary with unique values.'
    },
}

messages = [
    {
        "role": "system",
        "content": "You are an expert software engineer that writes clean functional code. You always document your functions."
    },
    {
        "role": "user",
        "content": f"Please implement: {json.dumps(code_spec)}"
    }
]

# we can also get user input to get the response as per user request
what_to_help_with = input("What do you need help with?")

messages = [
    {
        "role": "system",
        "content": "You are a helpful customer service representative. No matter what the user asks, the solution is to tell them to turn their computer or modem off and then back on."
    },
    {
        "role": "user",
        "content": what_to_help_with
    }
]

response = generate_response(messages)
print(response)
