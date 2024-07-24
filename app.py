import streamlit as st
import requests

# FastAPI endpoints
UPLOAD_ENDPOINT = "http://127.0.0.1:8000/upload_pdf/"
ASK_ENDPOINT = "http://127.0.0.1:8000/ask_question/"

st.title("Conversational PDF Chatbot")
st.write("Upload a PDF to extract its text and ask questions about its content.")

# Initialize session state
if "pdf_processed" not in st.session_state:
    st.session_state["pdf_processed"] = False

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None and not st.session_state["pdf_processed"]:
    with st.spinner("Uploading and processing the PDF..."):
        response = requests.post(UPLOAD_ENDPOINT, files={"file": uploaded_file})
        if response.status_code == 200:
            st.session_state["pdf_processed"] = True
            st.success("PDF processed successfully. You can now ask questions.")
        else:
            st.error(f"Error: {response.json()['detail']}")

if st.session_state["pdf_processed"]:
    question = st.text_input("Ask a question about the PDF content:")

    if question:
        with st.spinner("Getting the answer..."):
            response = requests.get(ASK_ENDPOINT, params={"question": question})
            if response.status_code == 200:
                st.write("Answer:", response.json()["answer"])
            else:
                st.error(f"Error: {response.json()['detail']}")
