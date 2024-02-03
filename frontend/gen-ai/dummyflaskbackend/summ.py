
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS #vector embeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain #for chats and prompts
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv #load all the environment

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_conversational_chain_sum():
    prompt_template = """
    Summarize the main topics covered in the provided context, focusing on the key points and themes. Provide a numbered bulleted list of topics for clarity . If the context is too vague or insufficient for a detailed summary, indicate this by stating, "The context provided does not contain enough information for a detailed summary." \n\n
    Context:\n{context}\n

    Summary of Topics:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "Summarize"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain_sum()

    
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)

    return response["output_text"]

def mainsumm(inp):
    result = user_input(inp)
    return result


