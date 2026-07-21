Minimum Viable Product (MVP)
Objective

The objective of our Minimum Viable Product (MVP) is to implement all mandatory project requirements while keeping the system as simple, maintainable, and easy to integrate as possible.

The MVP focuses on delivering a complete functional workflow rather than advanced features or user interface improvements.

Features to Implement First

The following features are considered essential and will be implemented first.

Backoffice
User authentication.
Secure password storage using password hashing.
Role-based authorization (Admin and Common User).
Administrator account (admin).
User management:
Create users.
Modify users.
Soft-delete users.
Change passwords.
Assign users to branches.
Branch management.
Stock management:
Add stock.
Remove stock.
View stock.
Prevent negative stock quantities.
Database

The relational database will store:

Users
Password hashes
User roles
Branches
Stock quantities
Product identifiers

The database will not store product information provided by the external Product API.

Product Integration
Connect to the external Product API.
Retrieve product lists.
Retrieve product details.
Use product identifiers to associate stock with products.
Product MCP Server

Implement an MCP server exposing two tools:

list_products
get_product_details

The MCP server will communicate with the external Product API on behalf of the AI service.

AI Query Service

Implement one AI agent capable of:

Receiving a natural language question.
Requesting product information through the Product MCP Server.
Requesting stock information from the database.
Generating a clear response.
Returning a message when requested information is unavailable instead of inventing an answer.
Client Web Interface

Implement a simple public web page containing:

A text input field.
A submit button.
A response area.

Users will be able to ask questions about products and stock without authentication.

Features Deferred Until Later

The following features are not required for the MVP and will only be implemented after all mandatory functionality works correctly.

Improved user interface design.
Advanced search filters.
Product images.
Better formatting of AI responses.
Loading animations.
Input suggestions.
Better error pages.
Optional Features (If Time Allows)

If sufficient development time remains, we may implement:

Multiple specialized AI agents.
Conversation history.
Response streaming using WebSockets.
Dockerized deployment of all services.
Dashboard with stock statistics.
Search history.
Logging and monitoring.
Automated tests.
Advanced AI reasoning for multi-product purchase recommendations.
Development Priorities

Our implementation order will be:

Create the database schema.
Implement user authentication.
Develop the Backoffice.
Connect to the Product API.
Implement the Product MCP Server.
Develop the AI Query Service.
Build the Client Web Interface.
Integrate all services.
Improve usability and add optional features if time permits.
MVP Summary

Our MVP delivers all mandatory project requirements:

Authenticated Backoffice
User and branch management
Stock management
External Product API integration
Product MCP Server
AI-powered query service
Public client interface
Secure authentication
Role-based authorization

Additional features will only be considered after the complete mandatory workflow is fully functional and integrated.
