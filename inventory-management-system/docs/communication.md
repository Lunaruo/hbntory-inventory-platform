# Communication Strategy

This document records the communication strategy decisions made for the HBntory project, as required by Task 0.2 of the project brief. For each decision: the option chosen, the main benefit, and the main trade-off or limitation.

---

## 1. Client Web Interface <-> AI Query Service

**Decision:** REST API.

**Benefit:** each question asked by a user is independent — there is no requirement to maintain conversation history or an open connection between questions. REST is simpler to implement, test, and debug (a single `curl` command is enough to verify the endpoint works), and requires no additional client-side complexity.

**Trade-off:** no real-time streaming of the answer (the response arrives all at once, not word-by-word), and no persistent connection for future features like live notifications. This is an acceptable trade-off since the project does not require a live-typing effect or real-time updates.

---

## 2. AI Query Service <-> Product MCP Server

**Decision:** the AI agent (Ollama) decides autonomously whether to call `list_products_tool` or `get_product_details_tool`, via a real MCP client (`fastmcp.Client`) connecting to the Product MCP Server over HTTP (`streamable-http` transport).

**Benefit:** matches the project requirement that the AI agent must access product information exclusively through an MCP server, not by calling the external Product API directly — and goes further by having a genuine AI model decide when to use each tool, rather than hardcoded keyword matching. This creates a clear separation of concerns: the MCP server handles all communication with the external API and its error cases, the AI model decides intent, and the AI Query Service only orchestrates the exchange.

**Trade-off:** small local models can occasionally misformat a tool call response; this is mitigated with response format normalization and honest fallback messages rather than invented answers.

---

## 3. AI Query Service <-> Relational Database (stock information)

**Decision:** direct read-only SQL query (via SQLAlchemy), joining the `stock` and `branches` tables, instead of a database MCP tool.

**Benefit:** simpler to implement given the small, well-defined read-only need (looking up stock quantities per product and branch). No additional MCP server or tool layer is required for this specific access pattern.

**Trade-off:** the AI Query Service depends on the Backoffice's database schema (table and column names). If the Backoffice's schema changes, this query needs to be updated accordingly. This is considered acceptable since both services are part of the same project and schema changes are expected to be communicated between the team.

---

## 4. Backoffice <-> Relational Database / Product API

*(To be completed by the Backoffice team member.)*

**Decision:**

**Benefit:**

**Trade-off:**

---

## 5. Backoffice Interface (REST + HTML/CSS/JS vs Server-Side Rendering)

*(To be completed by the Backoffice team member.)*

**Decision:**

**Benefit:**

**Trade-off:**