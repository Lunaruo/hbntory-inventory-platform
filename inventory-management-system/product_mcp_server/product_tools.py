"""
Product MCP Server - HBntory Inventory Management Platform
Bridges the AI agent to the external Product API (localhost:5001).
"""

import os

import httpx

PRODUCT_API_BASE_URL = os.environ.get(
    "PRODUCT_API_BASE_URL", "http://localhost:5001"
)


def list_products(limit: int = 20, offset: int = 0) -> dict:
    """
    MCP Tool: list_products
    Calls GET /api/v1/products and returns a clean list of products.
    """
    try:
        response = httpx.get(
            f"{PRODUCT_API_BASE_URL}/api/v1/products",
            params={"limit": limit, "offset": offset},
            timeout=5.0,
        )
        response.raise_for_status()
        data = response.json()

        products = [
            {
                "product_id": item["sku"],
                "name": item["name"],
                "category": item["category"],
                "brand": item["brand"],
                "unit_price": item["unit_price"],
                "currency": item["currency"],
                "discontinued": item["discontinued"],
            }
            for item in data.get("results", [])
        ]

        return {
            "success": True,
            "count": data.get("count", len(products)),
            "products": products,
        }

    except httpx.TimeoutException:
        return {"success": False, "error": "The Product API took too long to respond (timeout)."}
    except httpx.ConnectError:
        return {"success": False, "error": "Could not connect to the Product API. Is it running on localhost:5001?"}
    except httpx.HTTPStatusError as e:
        return {"success": False, "error": f"Product API returned an error: {e.response.status_code}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error while fetching products: {str(e)}"}


def get_product_details(product_id: str) -> dict:
    """
    MCP Tool: get_product_details
    Calls GET /api/v1/products/{product_id} for a single product's details.
    """
    try:
        response = httpx.get(
            f"{PRODUCT_API_BASE_URL}/api/v1/products/{product_id}",
            timeout=5.0,
        )

        if response.status_code == 404:
            return {
                "success": False,
                "error": f"Product '{product_id}' was not found.",
            }

        response.raise_for_status()
        item = response.json()

        return {
            "success": True,
            "product": {
                "product_id": item["sku"],
                "name": item["name"],
                "description": item["description"],
                "category": item["category"],
                "brand": item["brand"],
                "supplier_name": item["supplier_name"],
                "unit_price": item["unit_price"],
                "currency": item["currency"],
                "discontinued": item["discontinued"],
                "tags": item["tags"],
            },
        }

    except httpx.TimeoutException:
        return {"success": False, "error": "The Product API took too long to respond (timeout)."}
    except httpx.ConnectError:
        return {"success": False, "error": "Could not connect to the Product API. Is it running on localhost:5001?"}
    except httpx.HTTPStatusError as e:
        return {"success": False, "error": f"Product API returned an error: {e.response.status_code}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error while fetching product details: {str(e)}"}


if __name__ == "__main__":
    print(list_products())
    print(get_product_details("HB-LAP-1001"))
    print(get_product_details("PRODUIT-INEXISTANT"))
