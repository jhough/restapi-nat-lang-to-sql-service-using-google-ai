# Python REST API Natural Language to SQL App - Using Google Cloud Vertex AI with Google Gemini LLM

This is a Proof of Concept REST API app that accepts a natural language question, uses AI to generate a SQL query statement from the question, and queries a local database for the results.

Author: Jim Hough

- [Requirements (AI reverse-engineered)](docs/ai_derived_requirements.md)
- [Architecture Design (AI reverse-engineered)](docs/ai_derived_architecture.md)

## Python packages required (imports)

* Flask
* sqlite3
* google-cloud-vertexai
* google-api-core 

To install the packages listed in the requirements.txt file, run the following command in your terminal:

`pip install -r requirements.txt`

This command tells pip (the Python package installer) to read the requirements.txt file and install all the packages listed in it.

## Create local SQLite database

`python create_db.py`

This will create a database file named, `orders.db`, if it does not exist. It will execute the schema (database_schema.sql) to create the tables. It will insert some sample data.

## Usage

To call the API with a question:

1. Run the REST API app:

`python restapi_service.py --gcp-project-id YOUR-GCP-PROJECT-ID`

2. Authenticate to Google Cloud

`gcloud auth login --update-adc`

3. In a separate terminal, use the following curl command to send a question to the API:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the names of the customers?"}' \
  http://127.0.0.1:5000/query
```

Replace "What are the names of the customers?" with your own natural language question.

## Troubleshooting

If get a server side authentication error attempting to access the Gemini API: stop the restapi service, reauthenticate using the Google Cloud authentication command, above. Restart the restapi service. 

Reminder that this is a proof of concept app to prove that the AI model can convert natural language to SQL which can be used to query a database. Not to prove authentication. Your production app may use an alternate form of authentication.


## FYI: This is the prompt used to create the initial version of this application

```
# Persona:
You are an expert Python software engineer.

# Task:
Write a Python function that accepts a natural language question and returns the results from a database.

# Instructions:
* Provide a REST API interface.
* Accept a natural language question as input.
* Then make an LLM prompt by combining the content from a file named natlang_to_sql_prompt_instructions.md and a file named database_schema.sql and the question.
* Send this prompt to the Google Gemini LLM API using the Python  google-cloud-aiplatform package.
* Receive a SQL query statement back from the API call.
* Use the SQL to query a local SQLite database file named orders.db.
* Return the results of that query in JSON format.
```