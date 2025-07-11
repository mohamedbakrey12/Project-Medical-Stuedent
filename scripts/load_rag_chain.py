import os
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings





def get_rag_chain():
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")


    embedding_model = OpenAIEmbeddings(
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1")

    

    vectorstore = FAISS.load_local(
        "vectorstores/arabic_faiss",
        embedding_model,
        allow_dangerous_deserialization=True
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    #  إعداد LLM (من OpenRouter أو غيره)

    llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    temperature=0.2,
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),  # ✅ الصحيح
    openai_api_base="https://openrouter.ai/api/v1"   # ✅ الصحيح
    )


    prompt_template = PromptTemplate(
        template="""
You are a smart, helpful assistant. Your goal is to answer the user’s question as clearly and accurately as possible 
by using the retrieved context provided below. If the answer is not directly in the context, you should still 
use reasoning, inference, and general knowledge to produce a helpful and logical answer.

Never mention that the context is missing or insufficient. Never say "I don't know." Always try your best to answer 
the question meaningfully and informatively.

---------------------
Context:
{context}
---------------------

Question: {question}

Answer:""",
        input_variables=["context", "question"]
    )

    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt_template}
    )

    return rag_chain
