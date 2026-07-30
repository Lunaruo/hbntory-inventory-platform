# Minimum Viable Product (MVP)

<p align="center">
  <img src="https://img.shields.io/badge/scope-mandatory%20first-blue" alt="scope">
  <img src="https://img.shields.io/badge/status-in%20progress-yellow" alt="status">
</p>

## Objective

The objective of our Minimum Viable Product (MVP) is to implement all mandatory project requirements while keeping the system as simple, maintainable, and easy to integrate as possible.

The MVP focuses on delivering a **complete functional workflow** rather than advanced features or user interface improvements.

---

## Scope by Component

### Backoffice

| Feature | Included in MVP |
|---|---|
| User authentication | Yes |
| Secure password storage (hashing) | Yes |
| Role-based authorization (Admin / Common User) | Yes |
| Administrator account (`admin`) | Yes |
| Create / modify / soft-delete users | Yes |
| Change user passwords | Yes |
| Assign users to branches | Yes |
| Branch management | Yes |
| Add / remove / view stock | Yes |
| Prevent negative stock quantities | Yes |

### Database

The relational database stores:

- Users
- Password hashes
- User roles
- Branches
- Stock quantities
- Product identifiers

It does **not** store product information provided by the external Product API.

### Product Integration

| Feature | Included in MVP |
|---|---|
| Connect to the external Product API | Yes |
| Retrieve product lists | Yes |
| Retrieve product details | Yes |
| Use product identifiers to link stock to products | Yes |

### Product MCP Server

An MCP server exposing two tools:

- `list_products`
- `get_product_details`

The MCP server communicates with the external Product API on behalf of the AI service.

### AI Query Service

One AI agent capable of:

- Receiving a natural-language question.
- Requesting product information through the Product MCP Server.
- Requesting stock information from the database.
- Generating a clear response.
- Returning a message when requested information is unavailable, instead of inventing an answer.

### Client Web Interface

A simple public web page containing:

- A text input field.
- A submit button.
- A response area.

Users can ask questions about products and stock **without authentication**.

---

## Development Priorities

```mermaid
flowchart LR
    A["1. Database schema"] --> B["2. Authentication"]
    B --> C["3. Backoffice"]
    C --> D["4. Product API connection"]
    D --> E["5. Product MCP Server"]
    E --> F["6. AI Query Service"]
    F --> G["7. Client Web Interface"]
    G --> H["8. Integration"]
    H --> I["9. Usability & optional features"]

    style A fill:#0C447C,color:#fff,stroke:#333
    style B fill:#0C447C,color:#fff,stroke:#333
    style C fill:#0C447C,color:#fff,stroke:#333
    style D fill:#7B2FF7,color:#fff,stroke:#333
    style E fill:#7B2FF7,color:#fff,stroke:#333
    style F fill:#7B2FF7,color:#fff,stroke:#333
    style G fill:#F3217C,color:#fff,stroke:#333
    style H fill:#888,color:#fff,stroke:#333
    style I fill:#444,color:#fff,stroke:#333
```

---

## Features Deferred Until Later

Not required for the MVP — implemented only after all mandatory functionality works correctly:

- Improved user interface design
- Advanced search filters
- Product images
- Better formatting of AI responses
- Loading animations
- Input suggestions
- Better error pages

## Optional Features (If Time Allows)

| Feature | Priority |
|---|---|
| Multiple specialized AI agents | Optional |
| Conversation history | Optional |
| Response streaming (WebSockets) | Optional |
| Dockerized deployment of all services | Optional |
| Dashboard with stock statistics | Optional |
| Search history | Optional |
| Logging and monitoring | Optional |
| Automated tests | Optional |
| Advanced AI reasoning for multi-product recommendations | Optional |

---

## MVP Summary

Our MVP delivers **all mandatory project requirements**:

- Authenticated Backoffice
- User and branch management
- Stock management
- External Product API integration
- Product MCP Server
- AI-powered query service
- Public client interface
- Secure authentication
- Role-based authorization

Additional features will only be considered after the complete mandatory workflow is fully functional and integrated.

---

<p align="center"><i>Part of the HBntory Inventory Management Platform — Holberton School, Cohort C#29</i></p>