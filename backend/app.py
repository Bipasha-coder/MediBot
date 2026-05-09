from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from src.helper import download_hugging_face_embeddings, rag_pipeline
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)  # Allow all origins for now

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("BASE_URL")
INDEX_NAME = os.getenv("INDEX_NAME")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["BASE_URL"] = BASE_URL
os.environ["INDEX_NAME"] = INDEX_NAME

embeddings = download_hugging_face_embeddings()
doc = PineconeVectorStore.from_existing_index(index_name=INDEX_NAME, embedding=embeddings)
retriever = doc.as_retriever(search_type="similarity", search_kwargs={"k": 5})

client = OpenAI(api_key=OPENAI_API_KEY, base_url=BASE_URL)

@app.route("/")
def index():
    return "Backend is running fine"

@app.route("/get", methods=["POST"])
def chat():
    try:
        data = request.get_json()  # Get JSON payload
        msg = data.get("msg")  # Extract message
        
        if not msg:
            return jsonify({"error": "Message is required"}), 400

        response = rag_pipeline(client, msg, retriever)  # Call RAG pipeline
        response_json = response.get_json()  # Convert Flask response to JSON

        if "error" in response_json:
            return jsonify({"error": response_json["error"]}), 500

        return jsonify(response_json), 200  # Send successful response

    except Exception as e:
        print("Error handling /get request:", e)  # Debugging
        return jsonify({"error": "Internal Server Error"}), 500

# for local development
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080, debug=True)
