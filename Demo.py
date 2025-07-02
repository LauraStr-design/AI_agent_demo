from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.document_loaders import TextLoader
from langchain.schema import Document

import streamlit as st

import os
from langchain import hub

from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
import bs4 

load_dotenv()

token = os.getenv("SECRET")  
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-nano"

st.title("Apie Vilnių ir Gedimino sapną")

input_text = st.text_area("Įvesk klausimą:", placeholder="Įvesk bet kokį klausimą apie Vilniaus istoriją...")

def generate_response(input_text):
    web_urls = [
        "https://lt.wikipedia.org/wiki/Vilnius",
        "https://lt.wikipedia.org/wiki/Vilniaus_istorija"
    ]
    web_docs = []
    for url in web_urls:
        loader = WebBaseLoader(
            web_paths=[url],
            bs_kwargs=dict(parse_only=bs4.SoupStrainer("div", {"class": "mw-parser-output"}))
        )
        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = url
            web_docs.append(doc)

    
     # 2. Įkeliam txt failą
    txt_loader = TextLoader("info.txt", encoding="utf-8")
    txt_docs = txt_loader.load()
    for doc in txt_docs:
        doc.metadata["source"] = "info.txt"

    # 4. Sujungiame visus dokumentus
    all_docs = web_docs + txt_docs

    # 5. Skaidome tekstą
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    splits = text_splitter.split_documents(all_docs)

    # 6. Embedding'ai ir vektorinė saugykla
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        base_url="https://models.inference.ai.azure.com",
        api_key=token
    )
    vectorstore = InMemoryVectorStore(embeddings)
    _ = vectorstore.add_documents(splits)

    # 7. Retriever ir promptas
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})  # Renkame 3 dokumentus pagal užklausą
    prompt = hub.pull("rlm/rag-prompt")

    # 8. Formatuojame dokumentus (pagal užklausą)
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # 9. Kuriame rag grandinę
    llm = ChatOpenAI(base_url=endpoint, temperature=0.7, api_key=token, model=model)

    fetch_docs = retriever.get_relevant_documents(input_text)
    
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    result = rag_chain.invoke(input_text)
    st.info(result)

    st.subheader("📚 Šaltiniai")
    for i, doc in enumerate(fetch_docs, start=1):
        if len(doc.page_content.strip()) < 50:
           continue  # praleisti labai trumpus ar tuščius
        with st.expander(f"Šaltinis {i}"):
            st.write(f"**Ištrauka:** {doc.page_content[:300]}...")
            st.write(f"**Šaltinis:** {doc.metadata.get('source', 'Nenurodyta')}")
            url = doc.metadata.get("source")
            if url and url.startswith("http"):
                st.markdown(f"[🔗 Atidaryti šaltinį]({url})")

if st.button("Užduoti klausimą") and input_text.strip() != "":
    generate_response(input_text)