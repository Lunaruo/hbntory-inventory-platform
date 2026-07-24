# AI Query Service — HBntory

Independent backend service that receives natural language questions about products and stock, and returns clear answers based on real data (never invented).

## Role

This service:
- Receives a question via the `POST /ask` endpoint
- Uses the Product MCP Server to get product information (name, price, description...)
- Checks stock data (currently temporary placeholder data, until the connection to the Backoffice database is ready)
- Generates a clear answer, or clearly states when the requested information is unavailable

## Supported Question Types

- Product details: *"give me the details for product HB-LAP-1001"*
- Stock availability: *"where can I find product HB-LAP-1001"*
- List of available products: *"what products are available?"*

## Installation

```bash
cd inventory-management-system/ai_service
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn httpx
```

## Running the service

Make sure the external Product API is running (see `product_mcp_server/README.md`), then:

```bash
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

The service is available at `http://localhost:8000`.

## Usage

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "give me the details for product HB-LAP-1001"}'
```

Response:
```json
{
  "success": true,
  "answer": "Product Holberton Student Laptop 14 is priced at 799.0 USD. ..."
}
```

If the information is not available:
```json
{
  "success": false,
  "answer": "Product not found."
}
```

## Current Limitations

- Stock data is temporarily simulated (`FAKE_STOCK` in `main.py`) until the Backoffice database is ready. This must be replaced with a real database query as soon as possible.
- Question understanding is based on simple keyword matching, not a true language model.
- Multi-product shopping list questions are not supported yet (coming soon).

## Communication with the Client Web Interface

This service exposes a REST API (justification: each question is independent, no need to maintain a session or an open connection).