# Software Requirements Specification: Natural Language to SQL REST API

**Note:** This document was automatically derived (reverse-engineered) using AI based on the app's codebase.

## 1. High-Level Summary

The application is a proof-of-concept REST API service that translates natural language questions into SQL queries. It accepts a question from a user, leverages a Google Vertex AI language model to generate a corresponding SQL query, executes the query against a local SQLite database, and returns the results in JSON format. The primary purpose is to demonstrate the feasibility of using an LLM for natural language database querying.

## 2. Technologies Used

*   **Languages:** Python
*   **Frameworks/Libraries:** Flask, google-cloud-vertexai, google-api-core
*   **Database:** SQLite
*   **Platforms/Infrastructure:** Google Cloud Platform (for Vertex AI)

## 3. Functional Requirements

### 3.1. User Roles

*   **API User:** A human or automated client capable of sending HTTP POST requests to the service. This is the only role identified.

### 3.2. Feature: Natural Language Querying

*   **FR-1.1:** The system **shall** provide a REST API endpoint at `/query`.
*   **FR-1.2:** The `/query` endpoint **shall** accept HTTP POST requests with a JSON payload.
*   **FR-1.3:** The request payload **shall** contain a key named `question` with a string value representing the natural language query.
*   **FR-1.4:** The system **shall** read a set of base instructions from the `natlang_to_sql_prompt_instructions.md` file.
*   **FR-1.5:** The system **shall** read the database schema from the `database_schema.sql` file.
*   **FR-1.6:** The system **shall** construct a prompt for a language model by combining the base instructions, the database schema, and the user's question.
*   **FR-1.7:** The system **shall** send the constructed prompt to the Google Vertex AI (Gemini) model.
*   **FR-1.8:** The system **shall** receive a SQL query string in response from the language model.
*   **FR-1.9:** The system **shall** execute the received SQL query against the `orders.db` SQLite database.
*   **FR-1.10:** The system **shall** return the results of the database query as a JSON array of objects.
*   **FR-1.11:** In case of a database error during query execution, the system **shall** return a JSON error message with a 400 status code.

### 3.3. Feature: Database Setup

*   **FR-2.1:** The system **shall** provide a script (`create_db.py`) to initialize the application's database.
*   **FR-2.2:** The database initialization script **shall** create a SQLite database file named `orders.db`.
*   **FR-2.3:** The script **shall** create the database schema by executing the SQL in `database_schema.sql`.
*   **FR-2.4:** The script **shall** populate the newly created tables with sample data.

## 4. Non-Functional Requirements

*   **NFR-1 (Security):** The system **shall** rely on Google Cloud's Application Default Credentials (ADC) for authentication to the Vertex AI service. The API endpoint itself does not implement authentication.
*   **NFR-2 (Reliability):** The system **shall** implement error handling for API calls to the external Vertex AI service, capturing and logging specific authentication, permission, and precondition errors.
*   **NFR-3 (Maintainability):** The system **shall** be configurable with the Google Cloud Project ID via a command-line argument (`--gcp-project-id`).

## 5. Data Model

The database consists of three tables: `customers`, `products`, and `orders`.

### 5.1. customers

*   `id`: (INTEGER, Primary Key, The unique identifier for a customer)
*   `name`: (VARCHAR, The name of the customer)
*   `email`: (VARCHAR, The email address of the customer)

### 5.2. products

*   `id`: (INTEGER, Primary Key, The unique identifier for a product)
*   `name`: (VARCHAR, The name of the product)
*   `price`: (DECIMAL, The price of the product)

### 5.3. orders

*   `id`: (INTEGER, Primary Key, The unique identifier for an order)
*   `customer_id`: (INTEGER, Foreign Key to `customers.id`)
*   `product_id`: (INTEGER, Foreign Key to `products.id`)
*   `order_date`: (DATE, The date the order was placed)
*   **Relations:**
    *   Has a many-to-one relationship with `customers`.
    *   Has a many-to-one relationship with `products`.

## 6. External Dependencies

*   **Google Vertex AI (Gemini Model):** Used to convert the user's natural language question into a machine-readable SQL query.

---
