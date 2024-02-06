
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
    "Generate a comprehensive summary covering key information, symptoms, prevention methods, and treatment options for the major health problems identified in the knowledge base. Ensure the summary is balanced, providing equal attention to each health issue based on the information available. Highlight common management strategies, crucial distinctions, and any public health guidelines related to these conditions."

1. **Introduction**: Briefly introduce the main subject or field of study of the PDF. Mention the purpose or objective of the document if explicitly stated.

2. **Key Concepts and Theories**: Identify and summarize the key concepts, theories, or frameworks introduced in the document. Provide a brief explanation of each, emphasizing their significance to the subject matter.

3. **Methodology**: If the document includes empirical research, describe the methodology used in a succinct manner. This includes the research design, data collection methods, and analytical techniques.

4. **Findings or Main Points**: Summarize the primary findings, arguments, or points made in the document. Highlight any significant data, results, or conclusions drawn by the authors.

5. **Implications or Applications**: Discuss the implications or potential applications of the material. This could include how the findings might affect future research, policy, practice, or the field of study in general.

6. **Conclusion**: Provide a conclusion that encapsulates the overall essence of the document, including any final thoughts, recommendations, or calls to action made by the authors.

If the document's content is too broad or does not provide sufficient detail for a comprehensive summary, please note this by stating, "The content of the provided document is too broad or lacks the necessary detail for a comprehensive summary." Ensure the summary is clear, well-organized, accessible to individuals and each topic is in brief with a basic understanding of the subject matter. After ending of each toppic, generate a topic in a new line
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


