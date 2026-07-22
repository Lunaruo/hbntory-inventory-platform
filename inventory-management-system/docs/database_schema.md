# Database Schema

## Overview

The Backoffice database stores only local application data.

It manages:

- Users
- Branches
- Stock quantities

Product information is **not stored** locally. The application only stores the external product identifier (`product_id`) returned by the Product API.

---

# Entity Relationship Diagram

```text
                Branches
+--------------------------------------+
| id (PK)                              |
| name                                 |
| created_at                           |
| updated_at                           |
+--------------------------------------+
          | 1
          |
          | N
+--------------------------------------+
| Users                                |
+--------------------------------------+
| id (PK)                              |
| username (unique)                    |
| password_hash                        |
| role                                 |
| branch_id (FK -> branches.id) NULL   |
| is_active                            |
| created_at                           |
| updated_at                           |
+--------------------------------------+

          | 1
          |
          | N
+--------------------------------------+
| Stock                                |
+--------------------------------------+
| id (PK)                              |
| branch_id (FK -> branches.id)         |
| product_id                           |
| quantity                             |
| created_at                           |
| updated_at                           |
+--------------------------------------+
```

---

# Tables

## Users

Stores authenticated Backoffice users.

| Column | Type | Description |
|---------|------|-------------|
| id | Integer | Primary key |
| username | String | Unique username |
| password_hash | String | Secure password hash |
| role | Enum(admin, user) | User role |
| branch_id | Foreign Key | Assigned branch (NULL for admin) |
| is_active | Boolean | Soft delete flag |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### Rules

- Every common user belongs to exactly one branch.
- The administrator has no branch assignment.
- Users are never permanently deleted.
- Passwords are stored as hashes.

---

## Branches

Stores company branches.

| Column | Type | Description |
|---------|------|-------------|
| id | Integer | Primary key |
| name | String | Branch name |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### Rules

- A branch can have multiple users.
- A branch can contain multiple stock entries.

---

## Stock

Stores product quantities available in each branch.

| Column | Type | Description |
|---------|------|-------------|
| id | Integer | Primary key |
| branch_id | Foreign Key | Branch owning the stock |
| product_id | Integer | Product identifier from Product API |
| quantity | Integer | Available quantity |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### Rules

- Product information is never stored locally.
- Only the external product identifier is stored.
- Quantity must never become negative.

---

# Relationships

## Branch → Users

One branch can have many users.

```
Branch 1 ------ N Users
```

---

## Branch → Stock

One branch can contain many stock entries.

```
Branch 1 ------ N Stock
```

---

# Local Data

The following information is stored locally:

- Users
- Password hashes
- Roles
- Branches
- Stock quantities
- Product identifiers

---

# External Data

The following information comes from the Product API:

- Product names
- Product descriptions
- Product prices
- Product images
- Product metadata

The Backoffice database never stores this information.

---

# Validation Rules

The application must enforce the following business rules:

- Stock quantity cannot become negative.
- Stock operations require positive integer quantities.
- Users must belong to an existing branch.
- The administrator is not assigned to a branch.
- Product identifiers must exist in the external Product API before stock is created.

---

# Design Decisions

The database intentionally contains only three tables:

- Users
- Branches
- Stock

This keeps the design simple while satisfying all project requirements.

Product information is intentionally excluded from the database because the external Product API is the single source of truth.
