"""
AI Query Service - HBntory Inventory Management Platform
Receives natural language questions and answers using the Product MCP tools.
"""

from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# Allows importing product_tools.py from the MCP server folder
sys.path.append(
    os.path.join(os.path.dirname(__file__), "..", "product_mcp_server")
)
from product_tools import list_products, get_product_details

app = FastAPI()


class Question(BaseModel):
    question: str


# Temporary fake stock data (until Léo's real database is ready)
FAKE_STOCK = {
    "HB-LAP-1001": [
        {"branch": "Lille", "quantity": 5},
        {"branch": "Paris", "quantity": 2},
    ],
    "HB-MON-2102": [
        {"branch": "Lille", "quantity": 0},
        {"branch": "Paris", "quantity": 8},
    ],
}


@app.post("/ask")
def ask(payload: Question):
    question = payload.question.lower()
    words = payload.question.upper().split()

    product_code = None
    for word in words:
        if word.startswith("HB-"):
            product_code = word
            break

    if not product_code:
        return {
            "success": False,
            "answer": "Je ne comprends pas encore ce type de question.",
        }

    # Stock question
    if "stock" in question or "où" in question or "trouver" in question or "disponible" in question:
        stock = FAKE_STOCK.get(product_code)
        if not stock:
            return {
                "success": False,
                "answer": f"Aucune information de stock pour {product_code}.",
            }

        details = ", ".join(f"{s['branch']} ({s['quantity']} unités)" for s in stock)
        return {
            "success": True,
            "answer": f"Le produit {product_code} est disponible : {details}.",
        }

    # Product details question (default)
    result = get_product_details(product_code)
    if result["success"]:
        p = result["product"]
        return {
            "success": True,
            "answer": f"Le produit {p['name']} est proposé à {p['unit_price']} {p['currency']}. {p['description']}",
        }
    else:
        return {
            "success": False,
            "answer": "Je n'ai pas trouvé ce produit.",
        }
