# Module 1: Introduction to RAG

Welcome to your journey into RAG (Retrieval-Augmented Generation)! This module will introduce you to the fundamental concepts and help you build your first RAG system.

## 📚 What You'll Learn

- What RAG is and why it's revolutionary
- How RAG differs from traditional AI approaches
- The complete RAG pipeline
- Setting up your development environment
- Building your first RAG system

## 🎯 Learning Objectives

By the end of this module, you will:
- ✅ Understand what RAG is and its benefits
- ✅ Know the components of a RAG system
- ✅ Have a working development environment
- ✅ Build a simple RAG system from scratch
- ✅ Understand the RAG pipeline flow

---

## 🤔 What is RAG?

**RAG (Retrieval-Augmented Generation)** is a technique that combines two powerful AI approaches:

1. **Retrieval**: Finding relevant information from a knowledge base
2. **Generation**: Creating new content based on retrieved information

### Why RAG Matters

Traditional AI models have limitations:
- **Knowledge cutoff**: They only know information from their training data
- **Hallucination**: They can make up facts that sound plausible
- **Static knowledge**: They can't access real-time or domain-specific information

RAG solves these problems by:
- **Dynamic knowledge**: Accessing up-to-date information
- **Factual accuracy**: Grounding responses in retrieved documents
- **Domain expertise**: Using specialized knowledge bases
- **Transparency**: Showing sources for generated answers

---

## 🔄 The RAG Pipeline

A typical RAG system follows this flow:

```
1. Query Input → 2. Query Processing → 3. Document Retrieval → 4. Context Assembly → 5. Generation → 6. Response
```

### Detailed Pipeline Steps

1. **Query Input**: User asks a question
2. **Query Processing**: Convert query to embeddings
3. **Document Retrieval**: Find similar documents in vector database
4. **Context Assembly**: Combine retrieved documents with query
5. **Generation**: LLM generates answer using context
6. **Response**: Return answer with source citations

---

## 🆚 RAG vs Traditional AI

| Aspect | Traditional AI | RAG |
|--------|----------------|-----|
| Knowledge | Static training data | Dynamic knowledge base |
| Accuracy | Can hallucinate | Grounded in sources |
| Updates | Retraining required | Real-time updates |
| Sources | No transparency | Source citations |
| Domain | General knowledge | Specialized domains |

---

## 🛠️ Setting Up Your Environment

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (optional but recommended)

### Installation Steps

1. **Create a virtual environment**:
```bash
python -m venv rag-env
source rag-env/bin/activate  # On Windows: rag-env\Scripts\activate
```

2. **Install required packages**:
```bash
pip install langchain openai chromadb sentence-transformers streamlit
```

3. **Verify installation**:
```bash
python -c "import langchain, openai, chromadb; print('All packages installed successfully!')"
```

### Environment Variables

Create a `.env` file for API keys:
```bash
# .env file
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 🚀 Your First RAG System

Let's build a simple RAG system that can answer questions about a small knowledge base.

### Step 1: Create the Basic Structure

```python
# simple_rag.py
import os
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# Load environment variables
load_dotenv()

class SimpleRAG:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.llm = OpenAI(temperature=0)
        self.vectorstore = None
        
    def load_documents(self, file_path):
        """Load and process documents"""
        # Load document
        loader = TextLoader(file_path)
        documents = loader.load()
        
        # Split into chunks
        text_splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(documents)
        
        # Create vector store
        self.vectorstore = Chroma.from_documents(
            chunks, 
            self.embeddings,
            persist_directory="./chroma_db"
        )
        
        print(f"Loaded {len(chunks)} document chunks")
        
    def create_qa_chain(self):
        """Create question-answering chain"""
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3})
        )
        
    def ask_question(self, question):
        """Ask a question and get answer"""
        qa_chain = self.create_qa_chain()
        result = qa_chain.run(question)
        return result

# Example usage
if __name__ == "__main__":
    # Initialize RAG system
    rag = SimpleRAG()
    
    # Create sample knowledge base
    sample_text = """
    Python is a high-level programming language known for its simplicity and readability.
    It was created by Guido van Rossum and first released in 1991.
    Python supports multiple programming paradigms including procedural, object-oriented, and functional programming.
    It has a large standard library and is widely used in web development, data science, AI, and automation.
    """
    
    # Save sample text to file
    with open("sample_knowledge.txt", "w") as f:
        f.write(sample_text)
    
    # Load documents
    rag.load_documents("sample_knowledge.txt")
    
    # Ask questions
    questions = [
        "Who created Python?",
        "When was Python first released?",
        "What programming paradigms does Python support?"
    ]
    
    for question in questions:
        print(f"\nQ: {question}")
        answer = rag.ask_question(question)
        print(f"A: {answer}")
```

### Step 2: Run Your First RAG System

```bash
python simple_rag.py
```

Expected output:
```
Loaded 1 document chunks

Q: Who created Python?
A: Guido van Rossum created Python.

Q: When was Python first released?
A: Python was first released in 1991.

Q: What programming paradigms does Python support?
A: Python supports multiple programming paradigms including procedural, object-oriented, and functional programming.
```

---

## 🔍 Understanding the Components

### 1. Document Loader
- **Purpose**: Load documents from various sources
- **Example**: `TextLoader` for text files
- **Other options**: PDF, Word, web pages, databases

### 2. Text Splitter
- **Purpose**: Break documents into manageable chunks
- **Strategy**: Overlap chunks to maintain context
- **Size**: Balance between context and processing efficiency

### 3. Embeddings
- **Purpose**: Convert text to numerical vectors
- **Model**: OpenAI's text-embedding-ada-002
- **Usage**: Enable semantic similarity search

### 4. Vector Store
- **Purpose**: Store and search embeddings efficiently
- **Database**: ChromaDB for local development
- **Search**: Find most similar chunks to query

### 5. Retrieval Chain
- **Purpose**: Combine retrieval and generation
- **Type**: "stuff" chain (simple concatenation)
- **Retriever**: Top-k similar documents

---

## 🎯 Key Concepts Summary

1. **RAG combines retrieval and generation** for better AI responses
2. **Document processing** involves chunking and embedding
3. **Vector similarity search** finds relevant information
4. **Context assembly** combines query with retrieved documents
5. **Generation** creates answers using retrieved context

---

## 🏃‍♂️ Practice Exercises

### Exercise 1: Modify the Knowledge Base
- Add more information about Python
- Include information about other programming languages
- Test with new questions

### Exercise 2: Experiment with Chunking
- Try different chunk sizes (500, 1500, 2000)
- Adjust chunk overlap (100, 300, 500)
- Observe how it affects answer quality

### Exercise 3: Test Different Questions
- Ask questions not directly in the text
- Try questions requiring inference
- Test with ambiguous queries

---

## 🚀 Next Steps

Congratulations! You've built your first RAG system. In the next module, we'll dive deeper into:

- Advanced document processing techniques
- Different embedding models
- Vector database options
- Retrieval strategies
- Performance optimization

---

## 📚 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [RAG Research Paper](https://arxiv.org/abs/2005.11401)

---

**Ready for Module 2? Let's explore RAG fundamentals! 🎯**

*Next: [Module 2: RAG Fundamentals](module-02-fundamentals/README.md)*
