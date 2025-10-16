# RAG Course Containers

This directory contains Docker/Podman containers for easy deployment of RAG systems.

## 🐳 Available Containers

### 1. RAG Development Environment
- **File**: `Dockerfile.rag-dev`
- **Purpose**: Complete development environment for RAG
- **Includes**: Python, LangChain, ChromaDB, Jupyter, VS Code Server
- **Usage**: `podman build -f Dockerfile.rag-dev -t rag-dev .`

### 2. RAG Web Application
- **File**: `Dockerfile.rag-web`
- **Purpose**: Production-ready web RAG application
- **Includes**: Streamlit app, optimized Python environment
- **Usage**: `podman build -f Dockerfile.rag-web -t rag-web .`

### 3. Vector Database Services
- **File**: `docker-compose.yml`
- **Purpose**: Multi-service setup with ChromaDB and Redis
- **Includes**: ChromaDB, Redis, monitoring
- **Usage**: `podman-compose up -d`

## 🚀 Quick Start

1. **Build development environment**:
```bash
podman build -f Dockerfile.rag-dev -t rag-dev .
```

2. **Run development container**:
```bash
podman run -it --rm -p 8888:8888 -p 8080:8080 rag-dev
```

3. **Access services**:
- Jupyter: http://localhost:8888
- VS Code Server: http://localhost:8080

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `CHROMA_PERSIST_DIR`: ChromaDB persistence directory
- `STREAMLIT_PORT`: Streamlit port (default: 8501)

### Volume Mounts
- `./examples:/app/examples`: Mount examples directory
- `./data:/app/data`: Mount data directory
- `./models:/app/models`: Mount models directory

## 📝 Usage Examples

### Development Mode
```bash
# Start development container
podman run -it --rm \
  -p 8888:8888 \
  -p 8080:8080 \
  -v $(pwd)/examples:/app/examples \
  -e OPENAI_API_KEY=your_key_here \
  rag-dev
```

### Production Mode
```bash
# Start web application
podman run -d \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -e OPENAI_API_KEY=your_key_here \
  rag-web
```

### Multi-Service Setup
```bash
# Start all services
podman-compose up -d

# View logs
podman-compose logs -f

# Stop services
podman-compose down
```

## 🛠️ Customization

You can customize the containers by:
- Modifying the Dockerfiles
- Adding additional Python packages
- Changing port configurations
- Adding volume mounts
- Setting environment variables

## 🐛 Troubleshooting

**Common issues**:
- Port conflicts
- Permission issues
- API key not set
- Memory limitations

**Solutions**:
- Check port availability
- Use appropriate user permissions
- Set environment variables
- Increase container memory limits
