# 🏬 HBntory — Inventory Management Platform

<p align="center">
  <img src="https://img.shields.io/badge/status-in%20progress-blue" alt="status">
  <img src="https://img.shields.io/badge/python-3.11+-yellow?logo=python" alt="python">
  <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" alt="fastapi">
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white" alt="sqlalchemy">
  <img src="https://img.shields.io/badge/MCP-enabled-8A2BE2" alt="mcp">
  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" alt="docker">
</p>

<p align="center">
  An inventory management system for a fictional multi-branch retail company,
  combining a secure Backoffice, an external product catalog, an MCP-powered
  AI agent, and a natural-language client interface.
</p>

---

## 📐 Architecture overview

```mermaid
flowchart TB
    subgraph Public["🌐 Public"]
        Client["Client Web Interface<br/><i>chat-style, no login</i>"]
    end

    subgraph Internal["🔒 Internal"]
        Backoffice["Backoffice Service<br/><i>auth, users, stock</i>"]
        DB[("Relational Database<br/>users · branches · stock")]
    end

    subgraph AI["🤖 AI Layer"]
        AIService["AI Query Service<br/><i>independent backend</i>"]
        MCP["Product MCP Server<br/><i>list_products · get_product_details</i>"]
    end

    subgraph External["☁️ External"]
        ProductAPI["External Product API<br/><i>Docker, read-only</i>"]
    end

    Client -->|"POST /ask (REST)"| AIService
    AIService -->|"MCP tools"| MCP
    MCP -->|"HTTP"| ProductAPI
    AIService -.->|"reads stock"| DB
    Backoffice -->|"SQLAlchemy"| DB

    style Client fill:#F3217C,color:#fff,stroke:#333
    style AIService fill:#7B2FF7,color:#fff,stroke:#333
    style MCP fill:#7B2FF7,color:#fff,stroke:#333
    style Backoffice fill:#0C447C,color:#fff,stroke:#333
    style ProductAPI fill:#888,color:#fff,stroke:#333
    style DB fill:#0C447C,color:#fff,stroke:#333
```

**Data boundary:** product catalog data (names, prices, descriptions) always comes from the external Product API. The local database never duplicates it — it only stores the external `product_id` (the API's `sku` field) alongside branch and quantity information.

---

## 🧩 Components

| Component | Owner | Responsibility |
|---|---|---|
| **Backoffice Service** | Léo | Authenticated internal app — user & branch management, stock operations |
| **Relational Database** | Léo | Stores users, branches, stock quantities (never product details) |
| **External Product API** | Provided by school | Read-only product catalog (Docker container) |
| **Product MCP Server** | Ouarda | Bridges the AI agent to the external Product API |
| **AI Query Service** | Ouarda | Independent backend answering natural-language questions |
| **Client Web Interface** | Ouarda/Léo | Public chat page, no authentication required |

---

## 🔄 Request flow example

```mermaid
sequenceDiagram
    actor U as User
    participant C as Client Web
    participant AI as AI Query Service
    participant MCP as Product MCP Server
    participant API as External Product API

    U->>C: "Where can I find HB-LAP-1001?"
    C->>AI: POST /ask
    AI->>MCP: get_product_details("HB-LAP-1001")
    MCP->>API: GET /api/v1/products/HB-LAP-1001
    API-->>MCP: product data
    MCP-->>AI: clean product info
    AI-->>C: "Available in Lille (5) and Paris (2)"
    C-->>U: displays answer
```

---

## 🛠️ Tech stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,fastapi,sqlite,docker,html,css,js,git,github" />
</p>

- **Backend:** Python, FastAPI, SQLAlchemy
- **AI / Agent layer:** Model Context Protocol (MCP)
- **Database:** relational (SQLite/PostgreSQL via SQLAlchemy)
- **Frontend:** vanilla HTML/CSS/JS (chat-style interface)
- **Infrastructure:** Docker for the external Product API

---

## 🚀 Getting started

### 1. Clone the repository
```bash
git clone https://github.com/Lunaruo/hbntory-inventory-platform.git
cd hbntory-inventory-platform/inventory-management-system
```

### 2. Start the external Product API
```bash
cd ../../hbntory-products-api
docker compose up --build
```

### 3. Start the Product MCP Server
```bash
cd inventory-management-system/product_mcp_server
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 server.py
```

### 4. Start the AI Query Service
```bash
cd ../ai_service
python3 -m venv venv && source venv/bin/activate
pip install fastapi uvicorn httpx
uvicorn main:app --reload --port 8000
```

### 5. Open the Client Web Interface
```bash
open ../client_web/index.html
```

### 6. Start the Backoffice
See [`backoffice/README.md`](inventory-management-system/backoffice/README.md) for setup instructions.

---

## 📋 Project structure

inventory-management-system/
├── backoffice/ # Internal app — auth, users, stock (Léo)
├── ai_service/ # AI Query Service (Ouarda)
├── product_mcp_server/ # MCP bridge to the Product API (Ouarda)
├── client_web/ # Public chat interface (Ouarda)
├── docs/ # Architecture & decision documents
└── docker-compose.yml


---

## 📖 Documentation

- [AI Query Service — architecture & technical decisions](inventory-management-system/ai_service/README.md)
- [Product MCP Server](inventory-management-system/product_mcp_server/README.md)
- [Database schema](inventory-management-system/docs/database_schema.md)
- [MVP definition](inventory-management-system/docs/mvp.md)

---

## 👥 Team

| | |
|---|---|
| **Léo Lebtahi** | Backoffice — database, authentication, stock management, Client Web Interface |
| **Ouarda Bouchema** | AI/MCP layer — Product MCP Server, AI Query Service, Client Web Interface |

---

<p align="center"><i>HBntory — Holberton School project, Cohort C#29</i></p>