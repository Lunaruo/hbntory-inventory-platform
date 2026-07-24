The AI Query Service is intentionally kept as an independent service, separate from the Backoffice, as required by the project. It does not share a database connection or codebase with the Backoffice — it only consumes the Product MCP Server tools and (soon) the stock data exposed by the Backoffice database.

## Technical Decisions and Justifications

### 1. Why REST instead of WebSockets

We chose REST for communication between the Client Web Interface and this service.

**Justification:**
- Each question asked by a user is independent — there is no requirement to maintain conversation history or an open connection between questions.
- REST is simpler to implement, test, and debug (a single `curl` command is enough to verify the endpoint works).
- WebSockets would add complexity (connection lifecycle, reconnection handling) with no corresponding functional benefit for this use case.

**Trade-off accepted:** no real-time streaming of the answer (the response arrives all at once, not word-by-word). We consider this an acceptable trade-off since the project does not require a live typing effect.

### 2. Why the Product MCP Server is a separate component

Rather than calling the external Product API directly from this service, we built a dedicated MCP server (`product_mcp_server/`) that exposes two tools: `list_products` and `get_product_details`.

**Justification:**
- This matches the project requirement: the AI agent must access product information exclusively through an MCP server, not by calling the external API directly.
- It creates a clear separation of concerns: the MCP server is responsible for talking to the external Product API and handling its errors (timeouts, connection failures, product not found), while this service focuses only on interpreting the user's question and composing an answer.
- If the external Product API ever changes its format, only `product_mcp_server/product_tools.py` needs to be updated — this service does not need to change.

### 3. How the agent accesses stock information

The project allows two options: extending the MCP server with stock tools, or reading stock data through another means (e.g. a direct database connection or an internal API).

**Current implementation:** temporary in-memory data (`FAKE_STOCK` dictionary in `main.py`).

**Justification for this temporary choice:** the Backoffice database (owned by our teammate) was not yet available with real data when this service was built. Rather than blocking progress on the AI Query Service until the database was ready, we simulated the expected shape of the stock data so the question-answering logic could be built and tested independently.

**Planned final implementation:** once the Backoffice database is ready, this service will query it directly (read-only) for stock quantities per branch and product, using the `product_id` (matching the external API's `sku` field, a string) as the join key between stock records and product information. This keeps the same separation of concerns: the Backoffice owns and writes stock data, this service only reads it to answer questions.

### 4. Why product identifiers use the external API's `sku` field

The external Product API returns two identifiers per product: a numeric internal `id` and an alphanumeric `sku` (e.g. `HB-LAP-1001`).

**Justification:** the `sku` is the stable, human-readable identifier used throughout the API's documentation and search functionality. Using it as the shared `product_id` between the Backoffice stock table and this service avoids ambiguity and matches the identifier format users are likely to reference when asking questions.

### 5. Why question understanding uses keyword matching, not a full language model

The current implementation looks for a product code pattern (`HB-...`) and specific keywords (e.g. "stock", "où", "trouver", "disponible") in the question text, rather than using a large language model to interpret free-form questions.

**Justification:** this keeps the service simple, fast, fully predictable, and free of external API costs or dependencies, while still satisfying the mandatory question types defined in the project (product details, stock availability, product listing). We consider this the right trade-off for the MVP; a true language-understanding layer is listed as a possible improvement if time allows.

## Supported Question Types

- Product details: *"give me the details for product HB-LAP-1001"*
- Stock availability: *"where can I find product HB-LAP-1001"*
- List of available products: *"what products are available?"*

Not yet supported (planned next): multi-product shopping list questions (e.g. *"I want 3 units of X and 2 units of Y, which branch should I visit?"*).

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

## CORS

CORS is enabled (`allow_origins=["*"]`) so that the Client Web Interface, opened directly as a local HTML file, can call this service from the browser. In a production deployment this would be restricted to the actual client domain.

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

This service exposes a REST API (justification detailed above in Technical Decisions, section 1).