"""
AI Query Service - HBntory Inventory Management Platform
A real AI agent: Ollama decides which tool to call (product info via
a real MCP client, or stock via direct read-only DB access), then
writes the final natural-language answer.
"""

import os
import re
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import ollama
from fastmcp import Client as MCPClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backoffice.models.stock import Stock
from backoffice.models.branch import Branch

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    question: str


_default_path = os.path.join(os.path.dirname(__file__), "..", "inventory.db")
_same_dir_path = os.path.join(os.path.dirname(__file__), "inventory.db")
BACKOFFICE_DB_PATH = _default_path if os.path.exists(_default_path) else _same_dir_path

engine = create_engine(f"sqlite:///{BACKOFFICE_DB_PATH}")
SessionLocal = sessionmaker(bind=engine)


def get_stock_for_product(product_id: str) -> list:
    session = SessionLocal()
    try:
        results = (
            session.query(Stock, Branch)
            .join(Branch, Stock.branch_id == Branch.id)
            .filter(Stock.product_id == product_id)
            .all()
        )
        return [
            {"branch": branch.name, "quantity": stock.quantity}
            for stock, branch in results
        ]
    finally:
        session.close()


MCP_SERVER_URL = os.environ.get(
    "MCP_SERVER_URL", "http://127.0.0.1:8001/mcp"
)
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://host.docker.internal:11434")

ollama_client = ollama.Client(host=OLLAMA_HOST)


def extract_message(response):
    """Handle both dict-style and object-style Ollama responses."""
    if isinstance(response, dict):
        return response["message"]
    return response.message


def get_message_content(message):
    if isinstance(message, dict):
        return message.get("content", "")
    return getattr(message, "content", "") or ""


def get_tool_calls(message):
    if isinstance(message, dict):
        return message.get("tool_calls")
    return getattr(message, "tool_calls", None)


def get_call_name(call):
    if isinstance(call, dict):
        return call["function"]["name"]
    return call.function.name


def get_call_arguments(call):
    if isinstance(call, dict):
        return call["function"]["arguments"]
    args = call.function.arguments
    return dict(args) if not isinstance(args, dict) else args


async def call_mcp_tool(name: str, arguments: dict) -> dict:
    async with MCPClient(MCP_SERVER_URL) as client:
        result = await client.call_tool(name, arguments)
        text = result.content[0].text
        return json.loads(text)


def get_stock_tool(product_id: str) -> dict:
    stock = get_stock_for_product(product_id)
    if not stock:
        return {"success": False, "message": f"No stock found for {product_id}"}
    return {"success": True, "product_id": product_id, "stock": stock}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_products",
            "description": "List available products from the external Product API.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Max products to return"}
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_product_details",
            "description": "Get details (name, price, description) for a product given its product_id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "string", "description": "e.g. HB-LAP-1001"}
                },
                "required": ["product_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock",
            "description": "Get stock availability (quantity per branch) for a product given its product_id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "string", "description": "e.g. HB-LAP-1001"}
                },
                "required": ["product_id"],
            },
        },
    },
]

SYSTEM_PROMPT = (
    "You are the HBntory inventory assistant. You have access to real tools "
    "and must use them for any question about products or stock.\n\n"
    "Rules:\n"
    "- ALWAYS call the appropriate tool when the question is about a product, "
    "its price, its description, or its stock.\n"
    "- NEVER answer from your own knowledge or guess a value.\n"
    "- NEVER invent a product name, price, category, or stock quantity.\n"
    "- The tool results are the only source of truth.\n"
    "- If a tool call fails or returns no result, say so honestly instead "
    "of making something up.\n\n"
    "Product identifiers always look like HB-XXX-NNNN (e.g. HB-LAP-1001). "
    "If the user names a product in plain language without giving a valid "
    "product_id in that exact format, do not guess which product they mean "
    "— ask them to provide the exact code.\n\n"
    "Reply in French, concisely, in plain text (not JSON or code), based "
    "only on the tool's result."

)

PRODUCT_ID_PATTERN = re.compile(r"HB-[A-Z]{2,4}-\d{3,5}", re.IGNORECASE)


def looks_like_product_question(question: str) -> bool:
    q = question.lower()
    if PRODUCT_ID_PATTERN.search(question):
        return True
    keywords = ["produit", "produits", "liste", "disponible", "catalogue", "stock"]
    return any(k in q for k in keywords)


def is_empty_or_json_like(text: str) -> bool:
    stripped = text.strip().strip(".").strip()
    return not stripped or stripped in ("{}", "{ }", "{} {}", "{{}}")


async def execute_tool_call(name: str, arguments: dict) -> dict:
    if name == "list_products":
        return await call_mcp_tool(
            "list_products_tool", {"limit": arguments.get("limit", 20)}
        )
    if name == "get_product_details":
        product_id = arguments.get("product_id")
        if not product_id:
            return {"success": False, "message": "Missing product_id"}
        return await call_mcp_tool(
            "get_product_details_tool", {"product_id": product_id}
        )
    if name == "get_stock":
        product_id = arguments.get("product_id")
        if not product_id:
            return {"success": False, "message": "Missing product_id"}
        return get_stock_tool(product_id)
    return {"success": False, "message": f"Unknown tool: {name}"}


async def run_agent(question: str) -> str:
    if not looks_like_product_question(question):
        return (
            "Bonjour ! Je peux vous renseigner sur nos produits et leur "
            "stock. Donnez-moi un code produit (ex: HB-LAP-1001) ou "
            "demandez la liste des produits disponibles."
        )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    response = ollama_client.chat(model=OLLAMA_MODEL, messages=messages, tools=TOOLS)
    message = extract_message(response)
    tool_calls = get_tool_calls(message)

    if not tool_calls:
        answer = get_message_content(message).strip()
        if is_empty_or_json_like(answer):
            return (
                "Bonjour ! Posez-moi une question sur un produit (donnez "
                "son code, ex: HB-LAP-1001) ou son stock."
            )
        return answer

    messages.append({
        "role": "assistant",
        "content": get_message_content(message),
        "tool_calls": [
            {"function": {"name": get_call_name(c), "arguments": get_call_arguments(c)}}
            for c in tool_calls
        ],
    })

    for call in tool_calls:
        tool_name = get_call_name(call)
        arguments = get_call_arguments(call)
        result = await execute_tool_call(tool_name, arguments)
        messages.append({"role": "tool", "content": json.dumps(result)})

    final_response = ollama_client.chat(model=OLLAMA_MODEL, messages=messages, tools=TOOLS)
    final_message = extract_message(final_response)
    answer = get_message_content(final_message).strip()
    if is_empty_or_json_like(answer):
        return (
            "Je n'ai pas bien compris votre question. Pouvez-vous préciser "
            "un code produit (ex: HB-LAP-1001) ?"
        )
    return answer


@app.post("/ask")
async def ask(payload: Question):
    try:
        answer = await run_agent(payload.question)
        return {"success": True, "answer": answer}
    except Exception as e:
        return {"success": False, "answer": f"Une erreur est survenue: {str(e)}"}