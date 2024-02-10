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

chat_history=[]
chat_history.append({"Human_question":"Hey! How are you?","AI_answer":"I am good how are you?"})
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
    You are an Educational Chatbot which provides the answer to the question based on the knowledge retrieved from the vectorstore.
    As per the Context retrieved from the knowledge base which is provided below, generate a relevant information in an easy to understand format to the user based on the question asked below.
    You are even provided with the chat history below keep the History as a reference to make the user experience with the chatbot conversational.
    The history consists of Human_question and the AI_answer. AI_answer is the answer which is given by you. Understand what is the topic being in the conversation based on the history, refer to the Human_question as well as AI_answer. 
    Use the history (if exists), Context and the Question to generate the answer.
\n\n
    History:\n{chat_history}\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.1)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question","chat_history"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain(
        {"input_documents":docs, "question": user_question,"chat_history":chat_history[-1]}
        , return_only_outputs=True)
    use = {"Human_question":user_question,"AI_answer":response['output_text']}
    chat_history.append(use)
    print(chat_history)
    return response['output_text']


def starting_point(question):
    answer = user_input(question)
    return answer