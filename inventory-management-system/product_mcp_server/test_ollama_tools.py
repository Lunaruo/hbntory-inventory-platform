#!/usr/bin/env python3
"""
Simple test: does this Ollama model support tool calling?
"""

import ollama

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The city name"}
                },
                "required": ["city"],
            },
        },
    }
]

response = ollama.chat(
    model="qwen2.5:0.5b",
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
    tools=tools,
)

print("Full response message:")
print(response["message"])
print()

tool_calls = response["message"].get("tool_calls")
if tool_calls:
    print("Tool calls detected:")
    for call in tool_calls:
        print(f"  Function: {call['function']['name']}")
        print(f"  Arguments: {call['function']['arguments']}")
else:
    print("No tool calls detected — model answered directly instead.")
    