"""
Simple RAG Implementation
========================

This is a basic RAG (Retrieval-Augmented Generation) system that demonstrates
the core concepts covered in Module 1 of the RAG course.

Features:
- Document loading and chunking
- Vector embedding generation
- Similarity search with ChromaDB
- Question-answering with OpenAI
- Source citation

Author: RAG Course
Date: January 2025
"""

import os
import sys
from typing import List, Dict, Any
from dotenv import load_dotenv

# LangChain imports
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.schema import Document

# Load environment variables
load_dotenv()

class SimpleRAG:
    """
    A simple RAG implementation for educational purposes.
    
    This class demonstrates the basic RAG pipeline:
    1. Load and process documents
    2. Create embeddings and store in vector database
    3. Retrieve relevant documents for queries
    4. Generate answers using retrieved context
    """
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Initialize the RAG system.
        
        Args:
            persist_directory: Directory to persist the vector database
        """
        self.persist_directory = persist_directory
        self.embeddings = None
        self.llm = None
        self.vectorstore = None
        self.qa_chain = None
        
        # Initialize components
        self._initialize_components()
        
    def _initialize_components(self):
        """Initialize the core RAG components."""
        try:
            # Check for OpenAI API key
            if not os.getenv("OPENAI_API_KEY"):
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            
            # Initialize embeddings
            self.embeddings = OpenAIEmbeddings()
            
            # Initialize LLM
            self.llm = OpenAI(temperature=0, max_tokens=500)
            
            print("✅ Components initialized successfully")
            
        except Exception as e:
            print(f"❌ Error initializing components: {e}")
            sys.exit(1)
    
    def load_documents(self, file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
        """
        Load and process documents.
        
        Args:
            file_path: Path to the document file
            chunk_size: Size of each text chunk
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of processed document chunks
        """
        try:
            # Load document
            loader = TextLoader(file_path, encoding='utf-8')
            documents = loader.load()
            
            # Split into chunks
            text_splitter = CharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separator="\n"
            )
            chunks = text_splitter.split_documents(documents)
            
            print(f"📄 Loaded {len(documents)} document(s)")
            print(f"✂️ Split into {len(chunks)} chunks")
            
            return chunks
            
        except Exception as e:
            print(f"❌ Error loading documents: {e}")
            return []
    
    def create_vectorstore(self, chunks: List[Document]) -> bool:
        """
        Create vector store from document chunks.
        
        Args:
            chunks: List of document chunks
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create vector store
            self.vectorstore = Chroma.from_documents(
                chunks,
                self.embeddings,
                persist_directory=self.persist_directory
            )
            
            print(f"🗄️ Created vector store with {len(chunks)} chunks")
            return True
            
        except Exception as e:
            print(f"❌ Error creating vector store: {e}")
            return False
    
    def create_qa_chain(self, k: int = 3) -> bool:
        """
        Create question-answering chain.
        
        Args:
            k: Number of documents to retrieve
            
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
                retriever=self.vectorstore.as_retriever(search_kwargs={"k": k}),
                return_source_documents=True
            )
            
            print(f"🔗 Created QA chain with k={k}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating QA chain: {e}")
            return False
    
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
                raise ValueError("QA chain not initialized")
            
            # Get answer with sources
            result = self.qa_chain({"query": question})
            
            return {
                "question": question,
                "answer": result["result"],
                "sources": result["source_documents"]
            }
            
        except Exception as e:
            print(f"❌ Error asking question: {e}")
            return {
                "question": question,
                "answer": f"Error: {e}",
                "sources": []
            }
    
    def get_similar_documents(self, query: str, k: int = 3) -> List[Document]:
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
            print(f"❌ Error getting similar documents: {e}")
            return []

def create_sample_knowledge():
    """Create a sample knowledge base file."""
    sample_content = """
Python Programming Language
==========================

Python is a high-level, interpreted programming language known for its simplicity and readability. 
It was created by Guido van Rossum and first released in 1991. Python's design philosophy emphasizes 
code readability with its notable use of significant whitespace.

Key Features:
- Simple and easy to learn syntax
- Interpreted language (no compilation needed)
- Cross-platform compatibility
- Large standard library
- Extensive third-party libraries
- Object-oriented programming support
- Functional programming capabilities

Popular Use Cases:
- Web development (Django, Flask)
- Data science and analytics (Pandas, NumPy)
- Machine learning (TensorFlow, PyTorch)
- Automation and scripting
- Scientific computing
- Game development

Python Versions:
- Python 2.x (legacy, no longer supported)
- Python 3.x (current version)
- Latest stable version: Python 3.12

Installation:
Python can be installed from python.org or using package managers like pip, conda, or homebrew.

Development Environment:
Popular IDEs and editors for Python development include:
- PyCharm
- Visual Studio Code
- Jupyter Notebook
- Sublime Text
- Vim/Neovim

Best Practices:
- Follow PEP 8 style guide
- Use virtual environments
- Write comprehensive tests
- Document your code
- Use type hints
- Follow DRY principle (Don't Repeat Yourself)
"""
    
    with open("sample_knowledge.txt", "w", encoding="utf-8") as f:
        f.write(sample_content)
    
    print("📝 Created sample knowledge base")

def main():
    """Main function to demonstrate the RAG system."""
    print("🚀 Starting Simple RAG Demo")
    print("=" * 50)
    
    # Create sample knowledge base
    create_sample_knowledge()
    
    # Initialize RAG system
    rag = SimpleRAG()
    
    # Load documents
    chunks = rag.load_documents("sample_knowledge.txt")
    if not chunks:
        print("❌ Failed to load documents")
        return
    
    # Create vector store
    if not rag.create_vectorstore(chunks):
        print("❌ Failed to create vector store")
        return
    
    # Create QA chain
    if not rag.create_qa_chain(k=3):
        print("❌ Failed to create QA chain")
        return
    
    print("\n" + "=" * 50)
    print("🎯 Ready to answer questions!")
    print("=" * 50)
    
    # Sample questions
    questions = [
        "Who created Python and when?",
        "What are the key features of Python?",
        "What are some popular use cases for Python?",
        "What is the latest stable version of Python?",
        "What are some best practices for Python development?"
    ]
    
    # Ask questions
    for i, question in enumerate(questions, 1):
        print(f"\n📝 Question {i}: {question}")
        print("-" * 40)
        
        result = rag.ask_question(question)
        
        print(f"💡 Answer: {result['answer']}")
        
        if result['sources']:
            print(f"📚 Sources ({len(result['sources'])} documents):")
            for j, source in enumerate(result['sources'], 1):
                print(f"  {j}. {source.page_content[:100]}...")
        
        print("-" * 40)
    
    print("\n🎉 Demo completed successfully!")
    print("\n💡 Try asking your own questions by modifying the questions list!")

if __name__ == "__main__":
    main()
