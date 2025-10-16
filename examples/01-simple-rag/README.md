# Simple RAG Example

This is a basic RAG implementation that demonstrates the core concepts covered in Module 1.

## 🚀 Quick Start

1. **Install dependencies**:
```bash
pip install langchain openai chromadb sentence-transformers python-dotenv
```

2. **Set up environment**:
```bash
# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

3. **Run the example**:
```bash
python simple_rag.py
```

## 📁 Files

- `simple_rag.py` - Main RAG implementation
- `sample_knowledge.txt` - Sample knowledge base
- `requirements.txt` - Python dependencies
- `README.md` - This file

## 🔧 Features

- Document loading and chunking
- Vector embedding generation
- Similarity search with ChromaDB
- Question-answering with OpenAI
- Source citation

## 🎯 Learning Objectives

After running this example, you'll understand:
- How to set up a basic RAG pipeline
- Document processing workflow
- Vector similarity search
- Context-aware generation
- Error handling basics

## 📝 Customization

You can easily customize this example by:
- Changing the knowledge base content
- Adjusting chunk size and overlap
- Modifying the number of retrieved documents
- Using different embedding models
- Adding more sophisticated retrieval strategies

## 🐛 Troubleshooting

**Common issues**:
- Missing OpenAI API key
- ChromaDB permission errors
- Memory issues with large documents
- Network connectivity problems

**Solutions**:
- Check your `.env` file
- Run with appropriate permissions
- Reduce chunk size for large documents
- Verify internet connection
