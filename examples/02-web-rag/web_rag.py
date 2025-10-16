"""
Web RAG Interface
=================

A Streamlit-based web interface for the RAG system that provides an interactive
way to explore RAG capabilities with document upload and real-time Q&A.

Features:
- Interactive web interface
- Document upload and processing
- Real-time question answering
- Source citation and similarity search
- Configurable settings
- Chat history

Author: RAG Course
Date: January 2025
"""

import os
import sys
import tempfile
from typing import List, Dict, Any, Optional
import streamlit as st
from dotenv import load_dotenv

# Import our RAG system
from rag_system import WebRAGSystem

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="RAG Web Interface",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'documents_loaded' not in st.session_state:
        st.session_state.documents_loaded = False
    if 'vectorstore_created' not in st.session_state:
        st.session_state.vectorstore_created = False

def create_sample_documents():
    """Create sample documents for demonstration."""
    sample_docs = {
        "python_basics.txt": """
Python Programming Basics
========================

Python is a versatile programming language known for its simplicity and readability.
It was created by Guido van Rossum and first released in 1991.

Key Features:
- Simple syntax
- Interpreted language
- Cross-platform
- Large standard library
- Extensive third-party packages

Common Use Cases:
- Web development
- Data science
- Machine learning
- Automation
- Scientific computing
""",
        "machine_learning.txt": """
Machine Learning with Python
============================

Machine learning is a subset of artificial intelligence that focuses on algorithms
that can learn from data without being explicitly programmed.

Popular Python Libraries:
- Scikit-learn: General-purpose ML library
- TensorFlow: Deep learning framework
- PyTorch: Deep learning framework
- Pandas: Data manipulation
- NumPy: Numerical computing

Types of Machine Learning:
- Supervised learning
- Unsupervised learning
- Reinforcement learning
""",
        "web_development.txt": """
Web Development with Python
===========================

Python is widely used for web development, offering several frameworks and tools
for building web applications.

Popular Frameworks:
- Django: Full-featured web framework
- Flask: Lightweight microframework
- FastAPI: Modern API framework
- Pyramid: Flexible framework

Key Concepts:
- MVC architecture
- RESTful APIs
- Database integration
- Authentication
- Security best practices
"""
    }
    
    # Create sample_documents directory
    os.makedirs("sample_documents", exist_ok=True)
    
    # Write sample documents
    for filename, content in sample_docs.items():
        with open(f"sample_documents/{filename}", "w", encoding="utf-8") as f:
            f.write(content)
    
    return list(sample_docs.keys())

def sidebar_settings():
    """Create settings sidebar."""
    st.sidebar.header("⚙️ Settings")
    
    # RAG parameters
    chunk_size = st.sidebar.slider("Chunk Size", 500, 2000, 1000, 100)
    chunk_overlap = st.sidebar.slider("Chunk Overlap", 50, 500, 200, 50)
    retrieval_count = st.sidebar.slider("Retrieval Count", 1, 10, 3)
    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.0, 0.1)
    
    # Model settings
    st.sidebar.subheader("Model Settings")
    use_local_embeddings = st.sidebar.checkbox("Use Local Embeddings", value=False)
    
    return {
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "retrieval_count": retrieval_count,
        "temperature": temperature,
        "use_local_embeddings": use_local_embeddings
    }

def document_upload_section():
    """Handle document upload and processing."""
    st.header("📄 Document Management")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Upload Documents")
        uploaded_files = st.file_uploader(
            "Choose files",
            type=['txt', 'md'],
            accept_multiple_files=True,
            help="Upload text files to build your knowledge base"
        )
    
    with col2:
        st.subheader("Sample Documents")
        if st.button("Load Sample Documents"):
            sample_files = create_sample_documents()
            st.success(f"Created {len(sample_files)} sample documents!")
            st.session_state.sample_documents = sample_files
    
    # Process uploaded files
    if uploaded_files:
        st.subheader("Processing Uploaded Files")
        
        for uploaded_file in uploaded_files:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp_file:
                tmp_file.write(uploaded_file.getvalue().decode('utf-8'))
                tmp_path = tmp_file.name
            
            # Process the file
            if st.session_state.rag_system:
                chunks = st.session_state.rag_system.load_documents(tmp_path)
                if chunks:
                    st.success(f"✅ Processed {uploaded_file.name}: {len(chunks)} chunks")
                else:
                    st.error(f"❌ Failed to process {uploaded_file.name}")
            
            # Clean up temporary file
            os.unlink(tmp_path)
    
    # Process sample documents
    if hasattr(st.session_state, 'sample_documents'):
        st.subheader("Sample Documents Available")
        for doc in st.session_state.sample_documents:
            st.write(f"📄 {doc}")
            
            if st.button(f"Load {doc}", key=f"load_{doc}"):
                if st.session_state.rag_system:
                    chunks = st.session_state.rag_system.load_documents(f"sample_documents/{doc}")
                    if chunks:
                        st.success(f"✅ Loaded {doc}: {len(chunks)} chunks")
                    else:
                        st.error(f"❌ Failed to load {doc}")

def vectorstore_section():
    """Handle vector store creation and management."""
    st.header("🗄️ Vector Store")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.session_state.rag_system and st.session_state.rag_system.chunks:
            st.info(f"📊 Ready to create vector store with {len(st.session_state.rag_system.chunks)} chunks")
            
            if st.button("Create Vector Store", type="primary"):
                with st.spinner("Creating vector store..."):
                    success = st.session_state.rag_system.create_vectorstore()
                    if success:
                        st.session_state.vectorstore_created = True
                        st.success("✅ Vector store created successfully!")
                    else:
                        st.error("❌ Failed to create vector store")
        else:
            st.warning("⚠️ No documents loaded. Please upload or load documents first.")
    
    with col2:
        if st.session_state.vectorstore_created:
            st.success("✅ Vector store ready")
            if st.button("Reset Vector Store"):
                st.session_state.vectorstore_created = False
                st.session_state.rag_system.vectorstore = None
                st.rerun()

def chat_section():
    """Handle the chat interface."""
    st.header("💬 Chat with Your Documents")
    
    if not st.session_state.vectorstore_created:
        st.warning("⚠️ Please create a vector store first to start chatting.")
        return
    
    # Chat history
    if st.session_state.chat_history:
        st.subheader("Chat History")
        for i, (question, answer, sources) in enumerate(st.session_state.chat_history):
            with st.expander(f"Q{i+1}: {question[:50]}..."):
                st.write(f"**Question:** {question}")
                st.write(f"**Answer:** {answer}")
                if sources:
                    st.write("**Sources:**")
                    for j, source in enumerate(sources):
                        st.write(f"{j+1}. {source.page_content[:100]}...")
    
    # Question input
    question = st.text_input("Ask a question about your documents:", placeholder="What is Python?")
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        ask_button = st.button("Ask", type="primary")
    
    with col2:
        if st.button("Clear History"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Process question
    if ask_button and question:
        with st.spinner("Thinking..."):
            result = st.session_state.rag_system.ask_question(question)
            
            if result and result.get('answer'):
                # Display answer
                st.subheader("Answer")
                st.write(result['answer'])
                
                # Display sources
                if result.get('sources'):
                    st.subheader("Sources")
                    for i, source in enumerate(result['sources']):
                        with st.expander(f"Source {i+1}"):
                            st.write(source.page_content)
                
                # Add to chat history
                st.session_state.chat_history.append((
                    question,
                    result['answer'],
                    result.get('sources', [])
                ))
            else:
                st.error("❌ Failed to get answer. Please check your configuration.")

def similarity_search_section():
    """Handle similarity search functionality."""
    st.header("🔍 Similarity Search")
    
    if not st.session_state.vectorstore_created:
        st.warning("⚠️ Please create a vector store first to use similarity search.")
        return
    
    search_query = st.text_input("Search for similar content:", placeholder="machine learning")
    
    if st.button("Search") and search_query:
        with st.spinner("Searching..."):
            similar_docs = st.session_state.rag_system.get_similar_documents(search_query, k=5)
            
            if similar_docs:
                st.subheader("Similar Documents")
                for i, doc in enumerate(similar_docs):
                    with st.expander(f"Document {i+1}"):
                        st.write(doc.page_content)
            else:
                st.warning("No similar documents found.")

def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
    # App title
    st.title("🤖 RAG Web Interface")
    st.markdown("**Retrieval-Augmented Generation System with Web Interface**")
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        st.error("❌ OpenAI API key not found. Please set OPENAI_API_KEY in your environment.")
        st.stop()
    
    # Initialize RAG system
    if st.session_state.rag_system is None:
        with st.spinner("Initializing RAG system..."):
            settings = sidebar_settings()
            st.session_state.rag_system = WebRAGSystem(
                chunk_size=settings['chunk_size'],
                chunk_overlap=settings['chunk_overlap'],
                retrieval_count=settings['retrieval_count'],
                temperature=settings['temperature'],
                use_local_embeddings=settings['use_local_embeddings']
            )
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Documents", "🗄️ Vector Store", "💬 Chat", "🔍 Search"])
    
    with tab1:
        document_upload_section()
    
    with tab2:
        vectorstore_section()
    
    with tab3:
        chat_section()
    
    with tab4:
        similarity_search_section()
    
    # Footer
    st.markdown("---")
    st.markdown("**RAG Course** - Learn Retrieval-Augmented Generation")

if __name__ == "__main__":
    main()
