import streamlit as st
from pathlib import Path

import os

import google.generativeai as genai

from QA_app.components.data_ingestion import (
    get_cleaned_input_docs,
)

# from QA_app.components.data_querying import user_query
# from QA_app.components.data_indexing import run_indexing_pipeline

# name =

file_dir = f"Data/[Data] Think Like a Data Scientist (2017).pdf"

res = get_cleaned_input_docs(file_dir)

print(res[-1], "\ncleaned docs")
