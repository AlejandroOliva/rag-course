# 🚀 Quick Guide - RAG Course

This is your quick reference guide for RAG concepts, implementations, and commands.

## 📚 Core Concepts

### RAG Pipeline
```
Query → Embeddings → Vector Search → Context Assembly → LLM Generation → Answer
```

### Key Components
- **Document Loader**: Load documents from various sources
- **Text Splitter**: Break documents into chunks
- **Embeddings**: Convert text to vectors
- **Vector Store**: Store and search embeddings
- **Retriever**: Find relevant documents
- **Generator**: Create answers using context

## 🔧 Common Implementations

### Basic RAG with LangChain
```python
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# Load documents
loader = TextLoader("document.txt")
documents = loader.load()

# Split into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

# Create embeddings and vector store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)

# Create QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# Ask questions
answer = qa_chain.run("Your question here")
```

### Local Embeddings with Sentence Transformers
```python
from langchain.embeddings import HuggingFaceEmbeddings

# Use local embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

## 🗄️ Vector Databases

### ChromaDB (Local)
```python
from langchain.vectorstores import Chroma

# Create persistent vector store
vectorstore = Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory="./chroma_db"
)

# Load existing vector store
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)
```

### Pinecone (Cloud)
```python
from langchain.vectorstores import Pinecone
import pinecone

# Initialize Pinecone
pinecone.init(api_key="your-api-key", environment="your-environment")
vectorstore = Pinecone.from_documents(chunks, embeddings, index_name="rag-index")
```

## 🔍 Retrieval Strategies

### Basic Similarity Search
```python
# Get similar documents
docs = vectorstore.similarity_search(query, k=5)

# Get similar documents with scores
docs_with_scores = vectorstore.similarity_search_with_score(query, k=5)
```

### Hybrid Search (Dense + Sparse)
```python
from langchain.retrievers import EnsembleRetriever
from langchain.vectorstores import Chroma
from langchain.retrievers import BM25Retriever

# Create dense retriever
dense_retriever = Chroma.from_documents(chunks, embeddings).as_retriever()

# Create sparse retriever
sparse_retriever = BM25Retriever.from_documents(chunks)

# Combine retrievers
ensemble_retriever = EnsembleRetriever(
    retrievers=[dense_retriever, sparse_retriever],
    weights=[0.7, 0.3]
)
```

## 📝 Document Processing

### Text Splitting Strategies
```python
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    TokenTextSplitter
)

# Character-based splitting
text_splitter = CharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separator="\n"
)

# Recursive splitting (recommended)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]
)

# Token-based splitting
text_splitter = TokenTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
```

### Document Loaders
```python
from langchain.document_loaders import (
    TextLoader,
    PyPDFLoader,
    DirectoryLoader,
    WebBaseLoader
)

# Load text files
loader = TextLoader("file.txt")

# Load PDFs
loader = PyPDFLoader("document.pdf")

# Load entire directory
loader = DirectoryLoader("./docs", glob="**/*.txt")

# Load web pages
loader = WebBaseLoader(["https://example.com"])
```

## 🎯 Chain Types

### Stuff Chain (Default)
```python
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever
)
```

### Map Reduce Chain
```python
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="map_reduce",
    retriever=retriever
)
```

### Refine Chain
```python
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="refine",
    retriever=retriever
)
```

## 🔧 Configuration Tips

### Chunk Size Guidelines
- **Small chunks (200-500)**: Better precision, less context
- **Medium chunks (500-1000)**: Balanced approach
- **Large chunks (1000-2000)**: More context, less precision

### Retrieval Count
- **k=1-3**: Focused answers
- **k=3-5**: Balanced approach
- **k=5-10**: Comprehensive answers

### Temperature Settings
- **0.0**: Deterministic, factual answers
- **0.1-0.3**: Slightly creative, mostly factual
- **0.5-0.7**: Balanced creativity and accuracy
- **0.8-1.0**: Highly creative, less factual

## 🚀 Performance Optimization

### Caching
```python
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache

# Enable caching
set_llm_cache(InMemoryCache())
```

### Batch Processing
```python
# Process multiple documents
documents = loader.load()
chunks = text_splitter.split_documents(documents)

# Batch embedding generation
embeddings = embeddings.embed_documents([chunk.page_content for chunk in chunks])
```

### Async Processing
```python
import asyncio
from langchain.llms import OpenAI

async def async_qa(questions):
    llm = OpenAI()
    tasks = [llm.agenerate([q]) for q in questions]
    results = await asyncio.gather(*tasks)
    return results
```

## 🐛 Common Issues & Solutions

### Issue: "No module named 'langchain'"
**Solution**: `pip install langchain`

### Issue: "OpenAI API key not found"
**Solution**: Set `OPENAI_API_KEY` environment variable

### Issue: "ChromaDB permission denied"
**Solution**: Check directory permissions or use different path

### Issue: "Out of memory"
**Solution**: Reduce chunk size or use smaller embedding model

### Issue: "Rate limit exceeded"
**Solution**: Implement rate limiting or use local models

## 📊 Evaluation Metrics

### Retrieval Metrics
- **Precision@K**: Relevant documents in top K results
- **Recall@K**: Relevant documents retrieved
- **NDCG@K**: Normalized Discounted Cumulative Gain

### Generation Metrics
- **BLEU**: Bilingual Evaluation Understudy
- **ROUGE**: Recall-Oriented Understudy for Gisting Evaluation
- **BERTScore**: Contextual embedding-based similarity

## 🔗 Useful Commands

### Install Dependencies
```bash
pip install langchain openai chromadb sentence-transformers streamlit
```

### Run Streamlit App
```bash
streamlit run web_rag.py
```

### Start ChromaDB Server
```bash
chroma run --host 0.0.0.0 --port 8000
```

### Test Embeddings
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(['Hello world'])
```

## 📚 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Sentence Transformers](https://www.sbert.net/)
- [RAG Research Paper](https://arxiv.org/abs/2005.11401)

---

**Keep this guide handy while working through the course! 🎯**
