import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores.faiss import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain_community.callbacks import get_openai_callback
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class Chatbot:
    def __init__(self, model_name, api_key, file_path, chain_type):
        """
        Initializes the Chatbot class.

        Args:
            model_name (str): Name of the language model to use.
            api_key (str): API key for the OpenAI service.
            file_path (str): Path to the PDF file for context.
            chain_type (str): Type of chat chain ('RAG' or 'conversation').
        """
        self.file_path = file_path
        self.chain_type = chain_type
        self.file_name = os.path.splitext(os.path.basename(file_path))[0]
        self.chat_history = []

        # Initialize core components
        self.embeddings = OpenAIEmbeddings(api_key=api_key)
        self.llm = ChatOpenAI(model_name=model_name, api_key=api_key)
        self.chain = self._initialize_chain()

    def _initialize_chain(self):
        """Initialize the appropriate chain based on the selected chain type."""
        retriever = self._load_vector_store_as_retriever()
        if self.chain_type == 'RAG':
            return self._create_RAG_chain(retriever)
        return ConversationalRetrievalChain.from_llm(
            llm=self.llm, retriever=retriever, return_source_documents=True
        )

    def _file_load_and_split(self):
        """Load and split PDF document into chunks."""
        loader = PyPDFLoader(file_path=self.file_path, extract_images=True)
        return loader.load_and_split()

    def _load_vector_store_as_retriever(self):
        """Load or create a vector store, and return it as a retriever."""
        index_path = f"./faiss_db/{self.file_name}.faiss"
        if os.path.exists(index_path):
            vector_store = FAISS.load_local(folder_path="./faiss_db", index_name=self.file_name,
                                            embeddings=self.embeddings,allow_dangerous_deserialization=True)
        else:
            doc_chunks = self._file_load_and_split()
            vector_store = FAISS.from_documents(documents=doc_chunks, embedding=self.embeddings)
            vector_store.save_local(folder_path="./faiss_db", index_name=self.file_name)
        return vector_store.as_retriever()

    def _create_RAG_chain(self, retriever):
        """Create a RAG-based conversational chain."""
        template = (
            "You are a chatbot where the user asks questions. "
            "Answer those questions based only on the following context: {context}\n"
            "Question: {question}"
        )
        prompt = ChatPromptTemplate.from_template(template)
        chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | self.llm | StrOutputParser()
        return chain

    def invoke(self, query):
        """Invoke the chain based on the selected chain type."""
        return self._invoke_without_history(query) if self.chain_type == 'RAG' else self._invoke_with_history(query)

    def _invoke_without_history(self, query):
        """Invoke the chain without chat history for RAG-based responses."""
        with get_openai_callback() as cb:
            response = self.chain.invoke(query)
            print(cb)
        return response

    def _invoke_with_history(self, query):
        """Invoke the chain with chat history for conversational responses."""
        with get_openai_callback() as cb:
            response = self.chain.invoke({"question": query, "chat_history": self.chat_history})
            print(cb)
            self.chat_history.append((query, response["answer"]))
        return response["answer"]