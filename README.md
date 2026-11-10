# EnQue — AI-Powered Audience Intelligence & Content Optimization Platform

> **Understand your audience. Remember what works. Make smarter content decisions.**

EnQue is a specialized B2B marketing intelligence platform built for brands, agencies, and social media managers. Unlike standard analytics tools that display static engagement metrics, EnQue features **continuous experiential memory (powered by Hindsight)** and **four specialized AI agents** that learn from past campaign outcomes to generate increasingly effective future content strategies.

---

## 🌟 Key Features

1. **Brand-Isolated Multi-Tenancy**: Every brand workspace maintains its own isolated database scope and isolated Hindsight memory bank (`bank_<id>_<slug>`).
2. **Robust Data Ingestion**: Processes multi-format marketing data (`posts.csv`, `comments.csv`, `campaigns.csv`, brand guidelines) with column alias normalization and duplicate detection.
3. **Deterministic Pandas Analytics**: Accurate engagement rate, save rate, share rate, and format-level aggregation calculated directly on data before AI interpretation.
4. **Four Specialized AI Agents**:
   - **Audience Intelligence Agent**: Sentiment breakdown, recurring topics, common customer inquiries, and pain points.
   - **Content Intelligence Agent**: Format and topic performance rankings, viral drivers, and underperforming format analysis.
   - **Strategy Agent**: Formulates high-impact content plans grounded in audience pain points and verified Hindsight memory.
   - **Evaluation Agent**: Compares actual campaign outcomes vs. expected goals, extracts actionable learnings, and retains them in Hindsight.
5. **Persistent Memory & Learning Loop (Hindsight)**: Demonstrates clear evolution from a cold-start hypothesis (Confidence: Medium) to an experiential, evidence-backed strategy (Confidence: High).
6. **RAG Document Retrieval**: Retrieval-Augmented Generation for brand guidelines and voice consistency.
7. **Full-Featured React Dashboard**: Overview, Audience Insights, Content Analytics, AI Strategy Planner with interactive chat, AI Memory explorer, Experiment tracker, and Data ingestion manager.

---

## 🏗️ System Architecture

```text
                           EnQue
                             |
                      REACT FRONTEND (Vite + Tailwind CSS)
                             |
                      FASTAPI BACKEND
                             |
                     AGENT ORCHESTRATOR
                             |
          +------------------+------------------+
          |                  |                  |
          v                  v                  v
   AUDIENCE AGENT      CONTENT AGENT      STRATEGY AGENT
          |                  |                  |
          +------------------+------------------+
                             |
                             v
                     EVALUATION AGENT
                             |
             +---------------+---------------+
             |                               |
             v                               v
         HINDSIGHT                          RAG
     PERSISTENT MEMORY               DOCUMENT RETRIEVAL
             |                               |
             +---------------+---------------+
                             |
                             v
                        POSTGRESQL
                        (or SQLite)
                             |
                             v
                      DATA PROCESSING
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ and npm
- (Optional) Docker & Docker Compose

### 2. Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Fill in your API keys:
- `GROQ_API_KEY`: Groq API key for LLM inference (e.g. `openai/gpt-oss-120b`).
- `HINDSIGHT_API_KEY`: Hindsight persistent memory key (falls back gracefully if not configured).
- `DATABASE_URL`: PostgreSQL connection string (defaults to SQLite for instant local runs).

### 3. Backend Setup & Startup
```powershell
# Set Python path
$env:PYTHONPATH="."

# Install dependencies
pip install -r backend/requirements.txt

# Start FastAPI server
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
Swagger UI will be available at: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Frontend Setup & Startup
```powershell
cd frontend
npm install
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🧪 Verifying the Continuous Learning Cycle

Run the end-to-end learning cycle verification test:
```powershell
$env:PYTHONPATH="."
python backend/tests/test_sync_learning_cycle.py
```
This verifies:
1. User registration & JWT authentication
2. Brand workspace creation with isolated memory bank
3. Demo dataset ingestion (25 posts, 30 audience comments)
4. Deterministic Pandas calculation (22.12% avg engagement, 9.02% avg save rate)
5. RAG chunking and semantic cosine similarity retrieval
6. Cold-start strategy formulation (Confidence: Medium)
7. Campaign outcome evaluation & Hindsight memory retention
8. Memory-informed second strategy (Confidence: High with cited historical proof)

---

## 🐳 Docker Deployment

To launch the complete application stack (PostgreSQL + pgvector, FastAPI, Nginx React frontend):
```bash
docker-compose up --build
```
- Frontend: `http://localhost:3000`
- API Backend: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

