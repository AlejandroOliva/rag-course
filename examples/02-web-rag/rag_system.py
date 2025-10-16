"""
Web RAG System Implementation
============================

Enhanced RAG system designed for web applications with additional features
like local embeddings support and improved error handling.

Author: RAG Course
Date: January 2025
"""

import os
import sys
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# LangChain imports
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.schema import Document

# Load environment variables
load_dotenv()

class WebRAGSystem:
    """
    Enhanced RAG system for web applications.
    
    Features:
    - Support for both OpenAI and local embeddings
    - Configurable parameters
    - Better error handling
    - Web-friendly interface
    """
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        retrieval_count: int = 3,
        temperature: float = 0.0,
        use_local_embeddings: bool = False,
        persist_directory: str = "./chroma_db"
    ):
        """
        Initialize the web RAG system.
        
        Args:
            chunk_size: Size of document chunks
            chunk_overlap: Overlap between chunks
            retrieval_count: Number of documents to retrieve
            temperature: LLM temperature
            use_local_embeddings: Whether to use local embeddings
            persist_directory: Directory to persist vector database
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.retrieval_count = retrieval_count
        self.temperature = temperature
        self.use_local_embeddings = use_local_embeddings
        self.persist_directory = persist_directory
        
        # Initialize components
        self.embeddings = None
        self.llm = None
        self.vectorstore = None
        self.qa_chain = None
        self.chunks = []
        
        # Initialize components
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize the core RAG components."""
        try:
            # Initialize embeddings
            if self.use_local_embeddings:
                self.embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2"
                )
            else:
                if not os.getenv("OPENAI_API_KEY"):
                    raise ValueError("OPENAI_API_KEY not found in environment variables")
                self.embeddings = OpenAIEmbeddings()
            
            # Initialize LLM
            if not os.getenv("OPENAI_API_KEY"):
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            
            self.llm = OpenAI(
                temperature=self.temperature,
                max_tokens=500
            )
            
        except Exception as e:
            raise Exception(f"Error initializing components: {e}")
    
    def load_documents(self, file_path: str) -> List[Document]:
        """
        Load and process documents.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            List of processed document chunks
        """
        try:
            # Load document
            loader = TextLoader(file_path, encoding='utf-8')
            documents = loader.load()
            
            # Split into chunks
            text_splitter = CharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                separator="\n"
            )
            chunks = text_splitter.split_documents(documents)
            
            # Add to existing chunks
            self.chunks.extend(chunks)
            
            return chunks
            
        except Exception as e:
            raise Exception(f"Error loading documents: {e}")
    
    def create_vectorstore(self) -> bool:
        """
        Create vector store from loaded chunks.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.chunks:
                raise ValueError("No chunks available. Please load documents first.")
            
            # Create vector store
            self.vectorstore = Chroma.from_documents(
                self.chunks,
                self.embeddings,
                persist_directory=self.persist_directory
            )
            
            return True
            
        except Exception as e:
            raise Exception(f"Error creating vector store: {e}")
    
    def create_qa_chain(self) -> bool:
        """
        Create question-answering chain.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.vectorstore:
                raise ValueError("Vector store not initialized")
            
            # Create QA chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(
                    search_kwargs={"k": self.retrieval_count}
                ),
                return_source_documents=True
            )
            
            return True
            
        except Exception as e:
            raise Exception(f"Error creating QA chain: {e}")
    
    def ask_question(self, question: str) -> Dict[str, Any]:
        """
        Ask a question and get answer with sources.
        
        Args:
            question: The question to ask
            
        Returns:
            Dictionary containing answer and source documents
        """
        try:
            if not self.qa_chain:
                # Create QA chain if not exists
                if not self.create_qa_chain():
                    raise ValueError("Failed to create QA chain")
            
            # Get answer with sources
            result = self.qa_chain({"query": question})
            
            return {
                "question": question,
                "answer": result["result"],
                "sources": result["source_documents"]
            }
            
        except Exception as e:
            return {
                "question": question,
                "answer": f"Error: {e}",
                "sources": []
            }
    
    def get_similar_documents(self, query: str, k: int = 5) -> List[Document]:
        """
        Get similar documents for a query.
        
        Args:
            query: The query string
            k: Number of documents to retrieve
            
        Returns:
            List of similar documents
        """
        try:
            if not self.vectorstore:
                raise ValueError("Vector store not initialized")
            
            # Get similar documents
            docs = self.vectorstore.similarity_search(query, k=k)
            return docs
            
        except Exception as e:
            raise Exception(f"Error getting similar documents: {e}")
    
    def get_vectorstore_info(self) -> Dict[str, Any]:
        """
        Get information about the vector store.
        
        Returns:
            Dictionary with vector store information
        """
        try:
            if not self.vectorstore:
                return {"status": "not_created", "chunk_count": len(self.chunks)}
            
            # Get collection info
            collection = self.vectorstore._collection
            count = collection.count()
            
            return {
                "status": "created",
                "chunk_count": count,
                "persist_directory": self.persist_directory
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def reset_system(self):
        """Reset the RAG system to initial state."""
        self.vectorstore = None
        self.qa_chain = None
        self.chunks = []
        
        # Clean up vector store directory
        if os.path.exists(self.persist_directory):
            import shutil
            shutil.rmtree(self.persist_directory)
    
    def update_settings(
        self,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
        retrieval_count: Optional[int] = None,
        temperature: Optional[float] = None
    ):
        """
        Update system settings.
        
        Args:
            chunk_size: New chunk size
            chunk_overlap: New chunk overlap
            retrieval_count: New retrieval count
            temperature: New temperature
        """
        if chunk_size is not None:
            self.chunk_size = chunk_size
        if chunk_overlap is not None:
            self.chunk_overlap = chunk_overlap
        if retrieval_count is not None:
            self.retrieval_count = retrieval_count
        if temperature is not None:
            self.temperature = temperature
            # Update LLM temperature
            if self.llm:
                self.llm.temperature = temperature
