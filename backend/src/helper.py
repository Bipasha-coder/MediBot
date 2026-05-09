from flask import jsonify
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.prompt import *
import re


def load_pdf_file(data):
    loader= DirectoryLoader(data,
                            glob="*.pdf",
                            loader_cls=PyPDFLoader)
    documents= loader.load()
    filtered_documents = [
        Document(
            page_content=doc.page_content,  # Keep only the text
            metadata={
                "page": doc.metadata.get("page"),
                "source": doc.metadata.get("source")  # Keep only required fields
            }
        )
        for doc in documents
    ]
    return filtered_documents


def text_split(extracted_data):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks=text_splitter.split_documents(extracted_data)
    return text_chunks

def download_hugging_face_embeddings():
    embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2') #384 dimention data
    return embeddings

def query_openai(client, user_input, context=""):
    """
    Queries OpenAI using the provided client, user input, and context.
    """
    try:
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": user_input},
                    {"role": "system", "content": SYSTEM_PROMPT.format(context=context)},
                ],
            )
            return jsonify({"response": completion.choices[0].message.content})

    except Exception as e:
            print("Error querying OpenAI:", e)  # Debugging

            # Handle OpenAI API errors
            if hasattr(e, "response") and e.response is not None:
                try:
                    error_data = e.response.json()  # Extract JSON response
                    print(error_data.get("error", "Unknown API error"))
                    return jsonify({"error": error_data.get("error", "Unknown API error")})
                except Exception:
                    return jsonify({"error": "Unexpected error from OpenAI API"})

            # Generic error handling
            return jsonify({"error": str(e)})

def custom_question_answer_chain(client, input_text, retrieved_docs):
    """
    Processes retrieved documents and queries OpenAI for a response.
    """
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)
    return query_openai(client, input_text, context)

def rag_pipeline(client, input_text, retriever):
    """
    Handles the full RAG pipeline:
    - Retrieves relevant documents using the retriever
    - Feeds them to OpenAI via `custom_question_answer_chain`
    """
    input_text = re.sub(r"[^\w\s]", "", input_text).strip()
    retrieved_docs = retriever.invoke(input_text)
    return custom_question_answer_chain(client, input_text, retrieved_docs)
