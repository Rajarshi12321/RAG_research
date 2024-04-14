import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_community.document_loaders import DirectoryLoader


load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=gemini_api_key)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
# Setting Tempreture to 0.3 for getting low risk results

model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-latest", api_key=gemini_api_key, temperature=0.3
)

genai.configure(api_key=gemini_api_key)  # configuring api to run the pipeline
# model = Gemini(models="gemini-pro", api_key=gemini_api_key, temperature=0.3)
# gemini_embed_model = GeminiEmbedding(model_name="models/embedding-001")


def get_text_chunks(folder):
    loader = DirectoryLoader(folder, glob="**/*.pdf")
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    text_chunks = text_splitter.split_documents(docs)

    # Call function
    cleaned_docs = []
    for d in text_chunks:
        cleaned_text = clean_up_text(d.page_content)
        d.page_content = cleaned_text
        cleaned_docs.append(d)

    return cleaned_docs

    # return text_chunks


# Clean up our Documents' content
import re


def clean_up_text(content: str) -> str:
    """
    Remove unwanted characters and patterns in text input.

    :param content: Text input.

    :return: Cleaned version of original text input.
    """

    # Fix hyphenated words broken by newline
    content = re.sub(r"(\w+)-\n(\w+)", r"\1\2", content)

    # Remove specific unwanted patterns and characters
    unwanted_patterns = [
        "\\n",
        "  —",
        "——————————",
        "—————————",
        "—————",
        r"\\u[\dA-Fa-f]{4}",
        r"\uf075",
        r"\uf0b7",
    ]
    for pattern in unwanted_patterns:
        content = re.sub(pattern, "", content)

    # Fix improperly spaced hyphenated words and normalize whitespace
    content = re.sub(r"(\w)\s*-\s*(\w)", r"\1-\2", content)
    content = re.sub(r"\s+", " ", content)

    return content


def store_vectors(text_chunks):
    vector_store = FAISS.from_documents(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    print("Successfully stored indexes")


if __name__ == "__main__":
    text_chunks = get_text_chunks("E:/proj/ai assignment/QA_assistant/Data")
    store_vectors(text_chunks)
