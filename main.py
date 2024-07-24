from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain_community.vectorstores.faiss import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv
from io import BytesIO

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

# Function to extract text from PDF
def get_text(file):
    text = ""
    pdf_reader = PdfReader(file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to split text into chunks
def get_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000,
        chunk_overlap=0
    )
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create and save vector index
def get_vector(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectors = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    vectors.save_local("faiss_index")
    return vectors

# Function to create a conversation chain
def conversation_chain():
    prompt_template = '''
    You are a knowledgeable chatbot designed to provide insightful answers based on the context extracted from a PDF document.

    Context: {context}

    Question: {question}

    Instructions:
    - Use the provided context to answer the question accurately.
    - If the question cannot be answered based on the context, politely inform the user.
    - Provide clear and concise answers.
    - Ensure your responses are directly related to the content of the PDF.
    '''
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

# Function to handle user questions
def get_answer(question, vectors):
    doc = vectors.similarity_search(question)
    chain = conversation_chain()
    response = chain({
        "input_documents": doc,
        "question": question,
        "return_only_outputs": True
    })
    return response["output_text"]

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        content = await file.read()
        file_bytes = BytesIO(content)
        text = get_text(file_bytes)
        chunks = get_chunks(text)
        vectors = get_vector(chunks)
        return JSONResponse(content={"message": "PDF processed successfully. You can now ask questions."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ask_question/")
async def ask_question(question: str = Query(...)):
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vectors = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        answer = get_answer(question, vectors)
        return JSONResponse(content={"answer": answer})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

