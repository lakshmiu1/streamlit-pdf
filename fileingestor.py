import streamlit as st
from langchain_community.document_loaders import PyMuPDFLoader
from loadllm import Loadllm
from streamlit_chat import message
import tempfile
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

DB_FAISS_PATH = 'vectorstore/db_faiss'


class FileIngestor:
    def __init__(self, uploaded_file):
        self.uploaded_file = uploaded_file

    def handlefileandingest(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(self.uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        loader = PyMuPDFLoader(file_path=tmp_file_path)
        data = loader.load()

        # Create embeddings
        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

        # Create FAISS vector store
        db = FAISS.from_documents(data, embeddings)
        db.save_local(DB_FAISS_PATH)

        # Load LLM
        llm = Loadllm.load_llm()

        # Prompt that incorporates chat history
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Use the context below to answer the question.\n\nContext: {context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ])

        # Build the chain
        combine_docs_chain = create_stuff_documents_chain(llm, prompt)
        chain = create_retrieval_chain(db.as_retriever(), combine_docs_chain)

        # Conversational chat function
        def conversational_chat(query):
            # Convert history to LangChain message objects
            chat_history = []
            for human, ai in st.session_state['history']:
                chat_history.append(HumanMessage(content=human))
                chat_history.append(AIMessage(content=ai))

            result = chain.invoke({
                "input": query,
                "chat_history": chat_history
            })
            st.session_state['history'].append((query, result["answer"]))
            return result["answer"]

        # Initialize session state
        if 'history' not in st.session_state:
            st.session_state['history'] = []
        if 'generated' not in st.session_state:
            st.session_state['generated'] = ["Hello! Ask me (LLAMA2) about " + self.uploaded_file.name + " 🤗"]
        if 'past' not in st.session_state:
            st.session_state['past'] = ["Hey! 👋"]

        # UI
        response_container = st.container()
        container = st.container()

        with container:
            with st.form(key='my_form', clear_on_submit=True):
                user_input = st.text_input("Query:", placeholder="Talk to PDF data 🧮", key='input')
                submit_button = st.form_submit_button(label='Send')

            if submit_button and user_input:
                output = conversational_chat(user_input)
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)

        if st.session_state['generated']:
            with response_container:
                for i in range(len(st.session_state['generated'])):
                    message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                    message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")
