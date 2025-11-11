# Meet-Kant: Kantian Philosophy Knowledge System

A multi-language knowledge graph + RAG (Retrieval-Augmented Generation) system focused on Immanuel Kant's philosophy, with visualization frontend. The system enables users to ask questions about Kant's philosophy and receive answers with traceable evidence from original works.

## 🎯 Features

- **Multi-language support**: Query in Chinese, English, and German
- **Knowledge Graph**: Neo4j-based graph of Kant's philosophy with entities and relationships
- **RAG System**: Retrieval-Augmented Generation for accurate answers with evidence tracing
- **Visualization**: Interactive frontend to explore concepts and relationships
- **Evidence Tracking**: All answers include references to original texts (work_id, para_id, language)

## 🏗️ Architecture

```
meet-kant/
├── backend/
│   ├── app.py                 # FastAPI main application
│   ├── .env.example           # Environment variables example
│   ├── graph/
│   │   ├── neo4j_loader.py    # CSV-to-Neo4j loader
│   │   └── schema.cypher      # Neo4j schema and constraints
│   ├── rag/
│   │   ├── embedding.py       # Embedding model
│   │   ├── retriever.py       # Vector retrieval system
│   │   └── prompt_templates.py # Prompt templates
│   └── api/
│       └── routes_qa.py       # QA API routes
├── frontend/
│   ├── index.html             # Main HTML file
│   └── src/
│       ├── main.ts            # Main JS file
│       └── App.vue            # Vue component
├── resource/kant/
│   ├── persons.csv            # Person entities
│   ├── works.csv              # Work entities
│   ├── concepts.csv           # Concept entities
│   ├── relations.csv          # Relationships
│   └── texts/                 # Text data in JSONL format
├── scripts/
│   └── bootstrap_data.py      # Data bootstrap script
├── config/
├── docs/                      # Documentation
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── LICENSE                    # GPL-3.0 License
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Neo4j (Community Edition) or NetworkX as alternative
- Node.js (for frontend, optional)

### Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/meet-kant.git
    cd meet-kant
    ```

2. **Create virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    ```bash
    cp backend/.env.example backend/.env
    # Edit backend/.env with your Neo4j credentials and other settings
    ```

5. **Start Neo4j (using Docker)**:
    ```bash
    docker run -d --name neo4j -p 7687:7687 -p 7474:7474 -e NEO4J_AUTH=neo4j/password neo4j:latest
    # Default credentials: neo4j/password
    ```

6. **Load knowledge graph data**:
    ```bash
    python scripts/bootstrap_data.py
    ```

7. **Start the backend API**:
    ```bash
    cd backend
    uvicorn app:app --reload --port 8000
    ```

8. **Access the frontend**:
    Open `frontend/index.html` in your browser, or if using Vite:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

## 🔧 API Endpoints

### RAG Question Answering
- `POST /qa/rag`
  - Request body: `{"question": "string", "lang": "string"}`
  - Response: `{"answer": "string", "evidence": [], "graph_hits": []}`

### Graph Neighbor Lookup
- `GET /graph/neighbor?id=kant&k=5`
  - Returns neighbors of specified entity within K hops

### Concept Details (Optional)
- `GET /concept/{id}`
  - Returns details about a specific concept

## 📚 Sample Queries

1. **Simple query**:
    ```bash
    curl -s http://127.0.0.1:8000/qa/rag \
      -H "content-type: application/json" \
      -d '{"question":"什么是定言令式？","lang":"zh"}' | jq .
    ```

2. **English query**:
    ```bash
    curl -s http://127.0.0.1:8000/qa/rag \
      -H "content-type: application/json" \
      -d '{"question":"What is the categorical imperative?","lang":"en"}' | jq .
    ```

## 🗺️ Knowledge Graph Schema

### Entity Types
- `Person`: Philosophers (e.g., Kant, Hume, Leibniz)
- `Work`: Philosophical works (e.g., Critique of Pure Reason)
- `Concept`: Philosophical concepts (e.g., Categorical Imperative, Noumenon)
- `Term`: Technical terms
- `Place`: Locations
- `Event`: Historical events
- `School`: Philosophical schools

### Relationship Types
- `INFLUENCED_BY(Person→Person)`: Influence relationship
- `AUTHORED(Person→Work)`: Authorship
- `DEFINES(Person/Work→Concept/Term)`: Definition relationship
- `RELATES_TO(Concept↔Concept)`: Concept-to-concept relationship
- `OCCURS_IN(Work/Concept→Place/Event)`: Occurrence in location or event
- `HAS_EDITION(Work→Work)`: Different editions of works

## 🌐 Multi-language Support

The system supports indexing and retrieval in Chinese, English, and German:
- Original German texts from Kant's works
- Chinese and English translations
- Cross-language retrieval capabilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by philosophical knowledge systems and the need to make Kant's complex philosophy more accessible
- Built with FastAPI, Neo4j, sentence-transformers, and Vue.js
- Following principles of open knowledge and accessible philosophy