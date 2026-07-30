"""
Product MCP Server - HBntory Inventory Management Platform
Exposes list_products and get_product_details as MCP tools.
"""

from mcp.server.fastmcp import FastMCP
from product_tools import list_products, get_product_details

mcp = FastMCP("hbntory-product-server")


@mcp.tool()
def list_products_tool(limit: int = 20, offset: int = 0) -> dict:
    """List available products from the external Product API."""
    return list_products(limit=limit, offset=offset)


@mcp.tool()
def get_product_details_tool(product_id: str) -> dict:
    """Get details for a single product by its product_id (sku)."""
    return get_product_details(product_id)


if __name__ == "__main__":
    mcp.run()
