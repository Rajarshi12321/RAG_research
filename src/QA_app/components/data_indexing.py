from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from QA_app.components.data_ingestion import (
    get_cleaned_input_docs,
)


load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=gemini_api_key)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
# Setting Tempreture to 0.3 for getting low risk results

model = ChatGoogleGenerativeAI(
    model="gemini-1.0-pro-latest", api_key=gemini_api_key, temperature=0.3
)

genai.configure(api_key=gemini_api_key)  # configuring api to run the pipeline
# model = Gemini(models="gemini-pro", api_key=gemini_api_key, temperature=0.3)
# gemini_embed_model = GeminiEmbedding(model_name="models/embedding-001")


def store_vectors(text_chunks):
    vector_store = FAISS.from_documents(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    print("Successfully stored indexes")

    return "Done"


if __name__ == "__main__":
    file_dir = f"Data/[Data] Think Like a Data Scientist (2017).pdf"

    res = get_cleaned_input_docs(file_dir)
    store_vectors(res)
