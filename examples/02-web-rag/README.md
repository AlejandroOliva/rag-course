# Web RAG Interface

This example demonstrates a RAG system with a web interface built using Streamlit. It provides an interactive way to explore RAG capabilities.

## 🚀 Quick Start

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set up environment**:
```bash
# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

3. **Run the web interface**:
```bash
streamlit run web_rag.py
```

4. **Open your browser** to `http://localhost:8501`

## 📁 Files

- `web_rag.py` - Streamlit web interface
- `rag_system.py` - RAG system implementation
- `sample_documents/` - Sample knowledge base documents
- `requirements.txt` - Python dependencies
- `README.md` - This file

## 🔧 Features

- **Interactive Web Interface**: User-friendly Streamlit interface
- **Document Upload**: Upload your own documents
- **Real-time Q&A**: Ask questions and get instant answers
- **Source Citations**: See which documents were used
- **Similarity Search**: Explore document similarity
- **Settings Panel**: Configure chunk size, retrieval count, etc.
- **Chat History**: Keep track of your conversation

## 🎯 Learning Objectives

After using this example, you'll understand:
- How to build interactive RAG applications
- Web interface design for AI applications
- Real-time document processing
- User experience considerations
- Error handling in web applications

## 📝 Customization

You can customize this example by:
- Adding more document types (PDF, Word, etc.)
- Implementing different embedding models
- Adding authentication
- Creating different UI layouts
- Adding export functionality
- Implementing conversation memory

## 🐛 Troubleshooting

**Common issues**:
- Streamlit not starting
- Document upload errors
- API rate limits
- Memory issues with large documents

**Solutions**:
- Check port availability (8501)
- Verify file permissions
- Implement rate limiting
- Use document chunking for large files
