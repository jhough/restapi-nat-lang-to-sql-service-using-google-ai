import os
import sqlite3
from flask import Flask, request, jsonify
import vertexai
from vertexai.generative_models import GenerativeModel
from google.api_core import exceptions as google_exceptions
import argparse


# Get the Google Cloud project ID from the command line argument
if True:
    parser = argparse.ArgumentParser(
        description="A REST API for Natural Language to SQL queries.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Example usage:
  python app.py --gcp-project-id YOUR-GCP-PROJECT-ID
"""
    )
    parser.add_argument(
        '--gcp-project-id',
        help='The Google Cloud Project ID to use for Vertex AI API calls.'
    )

    args = parser.parse_args()

    project_id = args.gcp_project_id


# Initialize Flask app
app = Flask(__name__)


def get_llm_response(prompt_text, project_id):
    """Sends a prompt to the Vertex AI API and returns the response text."""

    print("Calling Vertex AI API . . .")

    try:
        if not project_id:
            print("ERROR: Google Cloud Project ID is not provided.")
            return None

        # Vertex AI SDK uses Application Default Credentials (ADC) by default.
        # Ensure you have run 'gcloud auth application-default login'
        # Initialize Vertex AI with your project and a region.
        vertexai.init(project=project_id, location="us-central1")

        model = GenerativeModel("gemini-2.5-flash")
        
        response = model.generate_content(prompt_text)

        print("-----------------")
        print("Result SQL Query  = ", response.text)
        print("-----------------")

        return response.text

    except ImportError:
        print("ERROR: The 'google-cloud-aiplatform' library is not installed. Please run: pip install google-cloud-aiplatform")
        return None
    except google_exceptions.Unauthenticated as e:
        print(f"ERROR: Unauthenticated. The credentials could not be found or are invalid. Please run 'gcloud auth application-default login' again. Details: {e}")
        return None
    except google_exceptions.PermissionDenied as e:
        print(f"ERROR: Permission Denied. The account does not have the required IAM permissions (e.g., 'Vertex AI User') on project '{project_id}'. Details: {e}")
        return None
    except google_exceptions.FailedPrecondition as e:
        # This often indicates the API is not enabled.
        print(f"ERROR: Failed Precondition. This often means the Vertex AI API (aiplatform.googleapis.com) is not enabled for project '{project_id}'. Please check the Google Cloud Console. Details: {e}")
        return None
    except Exception as e:
        # Catching the generic exception for other potential issues like the 503 you saw.
        print(f"ERROR: An unexpected error occurred while calling the Vertex AI API: {e}")
        print("This could be a temporary network issue or a problem with credentials. Please try the troubleshooting steps.")
        return None


@app.route("/query", methods=["POST"])
def query_database():

    # Get the natural language question from the request
    question = request.json.get("question")

    print("-----------------")
    print("Nat Lang Question = ", question)
    print("-----------------")

    # Read the prompt instructions and database schema
    with open("natlang_to_sql_prompt_instructions.md", "r") as f:
        prompt_instructions = f.read()
    with open("database_schema.sql", "r") as f:
        database_schema = f.read()

    # Construct the prompt for the LLM
    prompt = f"{prompt_instructions}\n\nDatabase Schema:\n{database_schema}\n\nQuestion: {question}"

    # Get the SQL query from the LLM
    sql_query = get_llm_response(prompt, project_id)

    # Connect to the SQLite database
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    # Execute the SQL query
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        json_results = [dict(zip(column_names, row)) for row in results]
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

    # Return the results in JSON format
    return jsonify(json_results)

if __name__ == "__main__":
    # For production, use a proper WSGI server like Gunicorn or Waitress.
    # Running on port 5000.
    app.run(host='0.0.0.0', port=5000, debug=False)
