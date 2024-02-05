from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS #vector embeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain #for chats and prompts
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv #load all the api key
import pdfplumber

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def read_pdfs_in_directory(directory_path):
    text=""
    for filename in os.listdir(directory_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory_path, filename)
            print(f"Reading {filename}...")
            text += get_pdf_text(file_path)
    return text


def get_pdf_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() if page.extract_text() else ""
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index") 


def get_conversational_chain():

    prompt_template = """
    Retrieve the most relevant information from the provided knowledge base related to the query. Synthesize the information to generate a comprehensive yet concise response. 
    The answer should fully address the user's query without introducing any inaccuracies or speculative details not supported by the knowledge base.
    Ensure the response is neither too brief nor too lengthy. If the query encompasses multiple facets or requires clarification on different aspects, structure the response in 
    a logical, cohesive manner, addressing each point succinctly. Avoid technical jargon unless it is necessary to accurately answer the question. When technical terms are used, provide clear 
    definitions or explanations to ensure the response is accessible to a general audience. Do not fabricate information or provide speculative answers. If the information is not available in 
    the knowledge base, indicate clearly that the answer is based on the available data and suggest a general direction for further inquiry or research if applicable."Based on the latest 
    updates in the provided knowledge base, {question}. It is mandatory for the response to be in less than 500 characters, reflecting the most recent information available, and framed in a manner that is 
    easy to understand for someone unfamiliar with the topic."
\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.2)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)
    return response["output_text"]


def starting_point(question):
    answer = user_input(question)
    return answer
