import streamlit as st
from PyPDF2 import PdfReader
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain.prompts.chat import ChatPromptTemplate


load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=gemini_api_key)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
# Setting Tempreture to 0.3 for getting low risk results

model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-latest", api_key=gemini_api_key, temperature=0.3
)

genai.configure(api_key=gemini_api_key)


def my_prompt():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    print(prompt)
    qa_prompt = ChatPromptTemplate.from_messages([("human", prompt_template)])
    print("checking promt")

    return qa_prompt


# return chain


def my_query(qa_prompt, user_question):

    # qa_prompt = ChatPromptTemplate.from_messages([("human", prompt_template)])

    chain = load_qa_chain(llm=model, chain_type="stuff", verbose=True, prompt=qa_prompt)
    new_db = FAISS.load_local(
        "faiss_index", embeddings, allow_dangerous_deserialization=True
    )
    docs = new_db.similarity_search(user_question)

    response = chain(
        {"input_documents": docs, "question": user_question}, return_only_outputs=True
    )

    return response


def user_query(user_question):
    prompt_template = my_prompt()

    response = my_query(prompt_template, user_question)

    return response["output_text"]


if __name__ == "__main__":
    user_question = "What happened in the deadly mongoose story"
    print(user_question)
    # prompt_template = my_prompt()

    response = user_query(user_question)

    print(response)
