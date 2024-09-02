# Importing Important libraries

import streamlit as st
from pathlib import Path

import os

import google.generativeai as genai

from langchain_community.chat_message_histories.streamlit import (
    StreamlitChatMessageHistory,
)


from datetime import datetime

from langchain.memory.buffer import ConversationBufferMemory
from langchain.schema.runnable import RunnableMap

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.callbacks.tracers.langchain import wait_for_all_tracers

import streamlit as st

from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings


# from streamlit_feedback import streamlit_feedback


# from langsmith import Client

# from langchain_core.tracers.context import collect_runs


from dotenv import load_dotenv


from QA_app.components.data_ingestion import (
    get_cleaned_input_docs,
)

from QA_app.components.data_querying import user_query
from QA_app.components.data_indexing import store_vectors


from langsmith import Client

from langchain_core.tracers.context import collect_runs


from dotenv import load_dotenv


load_dotenv()
os.getenv("GOOGLE_API_KEY")
gemini_api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


# -----------------------------

# Adding an event loop
# import asyncio

# import aiohttp


# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)


model = ChatGoogleGenerativeAI(
    model="gemini-1.0-pro-latest",
    api_key=gemini_api_key,
    temperature=0.3,
    convert_system_message_to_human=True,
)


# Configuring memory
memory = ConversationBufferMemory(
    chat_memory=StreamlitChatMessageHistory(key="langchain_messages"),
    return_messages=True,
    memory_key="chat_history",
)


# Load Vector DB
new_db = FAISS.load_local(
    "faiss_index", embeddings, allow_dangerous_deserialization=True
)

# Main retriever
retriever = new_db.as_retriever()


# Configuring our runnablemap
ingress = RunnableMap(
    {
        "input": lambda x: x["input"],
        "chat_history": lambda x: memory.load_memory_variables(x)["chat_history"],
        "time": lambda _: str(datetime.now()),
        "context": lambda x: retriever.get_relevant_documents(x["input"]),
    }
)


# Making the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI system assistant to help people chat with their pdf, provided pdf context answer reliably. Be humble, greet users nicely, and answer their queries."
            """
            "Instructions":
            "You can only make conversations based on the provided context. If a response cannot be formed strictly using the context, politely say you dont have knowledge about that topic."
            "Use the Context section to provide accurate answers, as if you knew this information innately."
            "You can also utilize chat history to give better response"
            
            "Context": {context}
            
            """,
            # ----
            # "Examples of Human feedback":
            # {examples},
            # ------
            # "system",
            # "Only and Only talk about games, nothing else, your knowledge is constraint games"
            # "You are a GAME RECOMMENDATION system assistant. You are humble AI. Greet the user nicely and answer their queries"
            # """
            #     Use the information from the Context section to provide accurate answers but act as if you knew this information innately.
            #     If unsure, simply state that you don't know.
            #     Context: {context}
            #     Here are some impressive examples of Human feedback, Do your best to try to generate these type of answer format for the specific format of questions
            #     The examples are listed below :
            #     {examples}""",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

llm = model

# Our final chain
chain = ingress | prompt | llm


# Initialize State
if "trace_link" not in st.session_state:
    st.session_state.trace_link = None
if "run_id" not in st.session_state:
    st.session_state.run_id = None


# Sidebar to give option for Clearing message history
if st.sidebar.button("Clear message history"):
    print("Clearing message history")
    memory.clear()
    st.session_state.trace_link = None
    st.session_state.run_id = None

# When we get response from the Chatbot, then only we can see this Trace link
if st.session_state.trace_link:
    st.sidebar.markdown(
        f'<a href="{st.session_state.trace_link}" target="_blank"><button>Latest Trace: 🛠️</button></a>',
        unsafe_allow_html=True,
    )


# -------------------------------------


# st.set_page_config("Chat With your PDF")

st.header("Your AI assistant here to help💁 (Powered by Gemini)")


File = st.file_uploader(
    "Upload Your new PDF file to store in FAISS", type=("pdf"), key="pdf"
)

if File:  # Save uploaded file to 'Data_final/' folder.
    save_folder = "Data_final"
    save_path = Path(save_folder, File.name)
    with open(save_path, mode="wb") as w:
        w.write(File.getvalue())

    if save_path.exists():
        st.success(f"File {File.name} is successfully saved!")

    file_dir = f"Data_final/{File.name}"

    res = get_cleaned_input_docs(file_dir)

    print(res, "cleaned docs")

    # Storing vectors in FAISS
    vector_store_check = store_vectors(res)

    # print(index_stats, "checking indexes")

    if vector_store_check == "Done":
        st.success(f"File {File.name} chunks are successfully stored in FAISS!")

    user_question_pdf = st.text_input("Ask a Question from the PDF File")

    if user_question_pdf:
        response = user_query(user_question_pdf)

        st.write(response)

    File = None


# user_question = st.text_input(
#     "Chat with existing Pdfs in Pinecone data base or Your added PDF"
# )

# if user_question:
#     response = user_query(user_question)

#     st.write(response)

for msg in st.session_state.langchain_messages:
    avatar = "🤖" if msg.type == "ai" else None
    with st.chat_message(msg.type, avatar=avatar):
        st.markdown(msg.content)


# The main chatbot configuration to get desired out and create runs for Langsmith
if prompt := st.chat_input(placeholder="Ask me a question!"):
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        print("in chat here")

        # Getting the input
        input_dict = {"input": prompt}
        print("in chat here", input_dict)

        # Displaying the response from chatbot and collecting runs
        with collect_runs() as cb:
            # try:
            for chunk in chain.stream(input_dict, config={"tags": ["Streamlit Chat"]}):
                full_response += chunk.content
                message_placeholder.markdown(full_response + "▌")

        # except:
        #     message_placeholder.markdown(
        #         "Sorry getting internal error, Please be more specific" + "▌"
        #     )

        memory.save_context(input_dict, {"output": full_response})

        print(memory.chat_memory)

        # storing the run id in streamlit session
        ## Since the runnable sequence would come after retriever I have chosen `1` instead on `0`
        # run_id = cb.traced_runs[1].id

        # st.session_state.run_id = run_id

        # wait_for_all_tracers()
        # # Requires langsmith >= 0.0.19

        # # Getting the Trace link
        # url = client.share_run(run_id)

        # st.session_state.trace_link = url

        # message_placeholder.markdown(full_response)

# Checking if we have messages in chat
has_chat_messages = len(st.session_state.get("langchain_messages", [])) > 0
