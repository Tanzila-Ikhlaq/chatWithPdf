# Conversational PDF Chatbot

This project is a Conversational PDF Chatbot that allows users to upload a PDF document, extract its text, and ask questions about its content. The application leverages FastAPI for the backend and Streamlit for the frontend.

## Features

- Upload and process PDF files.
- Extract text from PDF documents.
- Split extracted text into manageable chunks.
- Create and save vector indexes of text chunks using embeddings.
- Handle user questions and provide insightful answers based on the PDF content.

## Tech Stack

- **FastAPI**: Backend API for handling PDF uploads and question answering.
- **Streamlit**: Frontend for user interactions and visualizations.
- **PyPDF2**: Extract text from PDF files.
- **LangChain**: Text splitting and vector storage.
- **Google Generative AI**: For generating embeddings and providing conversational responses.
- **FAISS**: Vector search and similarity matching.
- **dotenv**: For managing environment variables.

### Run the Application

1. Start the FastAPI server:
    ```sh
    uvicorn main:app --reload
    ```

2. Start the Streamlit application:
    ```sh
    streamlit run app.py
    ```

## Usage

1. Open the Streamlit application in your browser.
2. Upload a PDF file using the file uploader.
3. Once the PDF is processed, ask questions about its content using the text input field.
4. The chatbot will provide answers based on the context extracted from the PDF.

## Screenshot

![Screenshot 2024-07-24 073346](https://github.com/user-attachments/assets/702b6755-ad57-42b9-90f4-1f0e2e45a43d)
