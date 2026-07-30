"""
AI Query Service - HBntory Inventory Management Platform
Receives natural language questions and answers using the Product MCP tools.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

sys.path.append(
    os.path.join(os.path.dirname(__file__), "..", "product_mcp_server")
)
sys.path.append(
    os.path.join(os.path.dirname(__file__), "..")
)
from product_tools import list_products, get_product_details

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


BACKOFFICE_DB_PATH = os.path.join(
    os.path.dirname(__file__), "..", "inventory.db"
)
engine = create_engine(f"sqlite:///{BACKOFFICE_DB_PATH}")
SessionLocal = sessionmaker(bind=engine)


def get_stock_for_product(product_id: str) -> list:
    """Read-only query: stock entries for a product across all branches."""
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


@app.post("/ask")
def ask(payload: Question):
    question = payload.question.lower()
    words = payload.question.upper().split()

    product_codes = [w for w in words if w.startswith("HB-")]

    # Shopping list — several products mentioned at once
    if len(product_codes) > 1:
        results = []
        for code in product_codes:
            stock = get_stock_for_product(code)
            if not stock:
                results.append(f"{code} : information de stock introuvable")
                continue
            total = sum(s["quantity"] for s in stock)
            if total > 0:
                details = ", ".join(f"{s['branch']} ({s['quantity']} unités)" for s in stock)
                results.append(f"{code} : disponible — {details}")
            else:
                results.append(f"{code} : rupture de stock partout")
        return {
            "success": True,
            "answer": "Voici la disponibilité de votre liste d'achats :\n" + "\n".join(results),
        }

    product_code = product_codes[0] if product_codes else None

    # "list all products" question — no product code needed
    if not product_code or ("quels produits" in question or "liste des produits" in question or "produits disponibles" in question):
        result = list_products()
        if result["success"]:
            names = ", ".join(p["name"] for p in result["products"][:10])
            return {
                "success": True,
                "answer": f"Voici quelques produits disponibles : {names}.",
            }
        else:
            return {"success": False, "answer": "Impossible de récupérer la liste des produits."}

    if not product_code:
        return {
            "success": False,
            "answer": "Je ne comprends pas encore ce type de question.",
        }

    # Stock question
    if "stock" in question or "où" in question or "trouver" in question or "disponible" in question:
        stock = get_stock_for_product(product_code)
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
