import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain 
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv 

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_conversational_chain():
    prompt_template = """
Given the medical content provided, your task is to generate a set of questions along with their answers on the important aspects.

Focus on creating questions that:
- Encourage detailed explanations, requiring the user to elaborate on concepts, processes, theories, or methodologies.
- If a question requires a solution provide it.

Your questions should span the entirety of the provided content, ensuring a comprehensive assessment of the user's knowledge and understanding. 

Context:
{context}

Generate Viva Questions:
    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain



def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs}, return_only_outputs=True)
    return response["output_text"]  

def main_viva(inp):
    result = user_input(inp)
    return result










