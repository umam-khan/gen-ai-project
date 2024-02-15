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
Analyze the provided context below carefully. From your analysis, generate a set of Viva questions along with their corresponding answers. Ensure that these questions:

Cover the main topics, theories, and concepts discussed in the document.
Include definitions, explanations, and illustrations of critical terms and ideas.
Encompass questions on methods, approaches, or experiments described, asking for explanations on how they are conducted or why they are used.
Probe for significant findings, results, and the reasoning behind conclusions drawn in the study.
Test understanding of the implications or applications of the research findings.
Ask for comparisons or contrasts between theories, methods, or results where relevant.
Include a mix of straightforward factual questions, as well as more complex analytical or evaluative questions to assess deeper understanding.
For each question, provide a concise, accurate answer based on the content of the PDF. The answers should be informative and clear enough to stand alone for someone studying the subject. Structure the questions and answers in a logical sequence, mirroring the organization of the document to facilitate an intuitive learning experience."
Context:
{context}
For your example, the generated question and answer should be in this format:

Question: What are amines?
Answer: In chemistry, amines are compounds and functional groups that contain a basic nitrogen atom with a lone pair. Amines are formally derivatives of ammonia, wherein one or more hydrogen atoms have been replaced by a substituent such as an alkyl or aryl group.

Generate Viva Questions keeping:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.4)

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










