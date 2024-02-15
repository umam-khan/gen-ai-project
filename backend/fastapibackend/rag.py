from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone 
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from openai import OpenAI

from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

OPENAI_API_KEY = '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'
PINECONE_API_KEY = '5091e5b1-3a34-4a6a-bc03-aeb2f44f7c0c'
pinecone.init(api_key=PINECONE_API_KEY, environment='gcp-starter')

index_name = "chatbook"
index = pinecone.Index(index_name)


chat = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model='gpt-3.5-turbo'
)


message = [
    SystemMessage(content="""You are an educational chatbot. You have to answer the responses based on the contexts that will be provided to you. 
                  If you don't know the answer reply 'The context provided doesn't have answer to this.'"""),
    HumanMessage(content="Hi AI, how are you today?"),
    AIMessage(content="I'm great thank you. How can I help you?")
]

embed_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-ada-002")
text_field = "text"
vectorstore = Pinecone(index, embed_model.embed_query,text_field)


dir_path = "C:\\Users\\Anand\\Desktop\\OPENAI\\data\\data.pdf"


def get_pdf_text(dir_path):
    loader = PyPDFLoader(file_path=dir_path)
    data = loader.load()
    return data


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    chunks = text_splitter.split_documents(text)
    return chunks


def get_vector_store(texts):
    index_name = "chatbook"
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-ada-002")
    docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)


def process_pinecone():
    pdf_text = get_pdf_text(dir_path)
    text_chunks = get_text_chunks(pdf_text)
    get_vector_store(text_chunks)



def augment_prompt(query):
    results = vectorstore.similarity_search(query,k=3)
    source_knowledge = "\n".join([x.page_content for x in results])

    augemented_prompt = f"""Using the contexts below, answer the query.

    Context:
    {source_knowledge}

    Query:
    {query}"""
    return augemented_prompt



def starting_point(question):
    prompt = HumanMessage(
        content = augment_prompt(question)
        )
    message.append(prompt)
    res = chat(message[-4:])
    message.append(res)
    return res.content

def reset_the_pinecone():
    pinecone.delete_index("chatbook")
    pinecone.create_index(name="chatbook", dimension=1536, metric='cosine')


def get_summary(question):
    docs = vectorstore.similarity_search(question)
    client = OpenAI(api_key=OPENAI_API_KEY)
    sumary = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content":"""You are a helpful educational assistant.
            You would need to generate a concise summary on the context provided to you. Include the following in the summary and generate response in this format only:
            1. Introduction\n, 2. Key Concepts and Theoires\n, 3. Methodology\n, 4. Findings or Main Points\n, 5. Implications or Application\n, 6. Conclusion\n """},
            {"role":"user","content":f"{docs}\n Generate the summary"}
        ]
    )
    return (sumary.choices[0].message.content)

def get_viva(question):
    docs = vectorstore.similarity_search(question)
    client = OpenAI(api_key=OPENAI_API_KEY)
    viva = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content":"""You are a helpful educational assistant.
            You would need to generate viva questions and their answers on the context provided to you. Cover all the important points and generate as many questions as. The format of the query should be:\n 
            Question:\n Answer:"""},
            {"role":"user","content":f"{docs}\n Generate the viva questions"}
        ]
    )
    return (viva.choices[0].message.content)

def get_mcq(topic, number):
    docs = vectorstore.similarity_search(topic)
    client = OpenAI(api_key=OPENAI_API_KEY)
    questions = []
    for i in range(0, number, 1):
        response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "system", "content": "Always follow this format (questions : Question generated, answer : correct answer, option1: wrong option , option2 : wrong option, option3: wrong).\n"},
            {"role": "user", "content": f"{docs}\n Generate one mcq questions from the above context. Don't repeat these questions: \n{questions}"}
        ]
        )
        questions.append(response.choices[0].message.content)  
    print(questions)
    return questions      
