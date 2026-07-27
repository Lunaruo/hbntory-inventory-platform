# Communication Strategy

This document records the communication strategy decisions made for the HBntory project, as required by Task 0.2 of the project brief. For each decision: the option chosen, the main benefit, and the main trade-off or limitation.

---

## 1. Client Web Interface <-> AI Query Service

**Decision:** REST API.

**Benefit:** each question asked by a user is independent — there is no requirement to maintain conversation history or an open connection between questions. REST is simpler to implement, test, and debug (a single `curl` command is enough to verify the endpoint works), and requires no additional client-side complexity.

**Trade-off:** no real-time streaming of the answer (the response arrives all at once, not word-by-word), and no persistent connection for future features like live notifications. This is an acceptable trade-off since the project does not require a live-typing effect or real-time updates.

---

## 2. AI Query Service <-> Product MCP Server

**Decision:** direct MCP tool calls (`list_products`, `get_product_details`) over the Model Context Protocol.

**Benefit:** matches the project requirement that the AI agent must access product information exclusively through an MCP server, not by calling the external Product API directly. This creates a clear separation of concerns: the MCP server handles all communication with the external API and its error cases (timeouts, connection failures, product not found), while the AI Query Service only interprets user questions and composes answers.

**Trade-off:** adds one extra layer between the AI agent and the external API, compared to calling it directly. This is intentional and required by the project, not an unplanned cost.

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