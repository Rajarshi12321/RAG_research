from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

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


def get_cleaned_input_docs(pdf_file):
    print(pdf_file)
    loader = PyPDFLoader(pdf_file)
    pages = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    text_chunks = text_splitter.split_documents(pages)

    # Call function
    cleaned_docs = []
    for d in text_chunks:
        cleaned_text = clean_up_text(d.page_content)
        d.page_content = cleaned_text
        cleaned_docs.append(d)

    print(f"Number of chunks: {cleaned_docs}")

    return cleaned_docs


if __name__ == "__main__":
    # docs = get_cleaned_dir_docs("Data\10200221027_Rajarshi Roy_ (1).pdf")
    docs = get_cleaned_input_docs("Data/[Data] Think Like a Data Scientist (2017).pdf")
    print(docs[-1], "\n\nNumber of chunks:", len(docs))
