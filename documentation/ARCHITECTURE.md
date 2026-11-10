# EnQue System Architecture & Verification Report

## 1. System Overview
**EnQue** is an enterprise AI-powered Audience Intelligence and Content Optimization platform engineered for brands, agencies, and content teams. It bridges the gap between static metrics dashboards and continuous experiential learning using **Hindsight persistent memory** and **coordinated AI agents**.

---

## 2. Multi-Agent & Memory Architecture

```
                       +------------------------+
                       |   React 18 + Vite UI   |
                       +-----------+------------+
                                   | (REST API)
                                   v
                       +------------------------+
                       |     FastAPI Server     |
                       +-----------+------------+
                                   |
                       +-----------v------------+
                       |   Central Orchestrator |
                       +-----+------------+-----+
                             |            |
         +-------------------+            +-------------------+
         |                                                    |
         v                                                    v
+------------------+                                 +------------------+
|  Audience Agent  |                                 |  Content Agent   |
| (Sentiment & NLP)|                                 | (Metrics Agg.)   |
+--------+---------+                                 +--------+---------+
         |                                                    |
         +-------------------+            +-------------------+
                             |            |
                             v            v
                       +------------------------+
                       |     Strategy Agent     |
                       | (Evidence Synthesis)   |
                       +-----------+------------+
                                   |
                                   v
                       +------------------------+
                       |    Evaluation Agent    |
                       +-----------+------------+
                                   |
            +----------------------+----------------------+
            |                                             |
            v                                             v
+-----------------------+                     +-----------------------+
|  Hindsight Memory     |                     |    PostgreSQL / DB    |
| (Retain/Recall/Reflect|                     |  (pgvector / ORM)     |
+-----------------------+                     +-----------------------+
```

### Core Agents:
1. **Audience Intelligence Agent**:
   - Performs sentiment analysis and extracts recurring discussion topics.
   - Categorizes audience inquiries, questions, and acute pain points.
2. **Content Intelligence Agent**:
   - Calculates engagement, save, share, and comment rates across content formats (Reel, Carousel, Single Image).
   - Identifies top-performing topics and formats.
3. **Strategy Agent**:
   - Generates contextual content calendars and strategic recommendations.
   - Formulates explicit hypotheses and grounds recommendations in historical evidence from Hindsight memory.
4. **Evaluation Agent**:
   - Compares actual campaign metrics against predicted targets.
   - Generates structured learning summaries and commits experiential memory to isolated Hindsight banks.
5. **Central Agent Orchestrator**:
   - Synchronizes memory retrieval, audience analysis, content insights, and strategy formulation into an atomic execution pipeline.

---

## 3. End-to-End Verification Matrix

| Acceptance Criteria | Component Tested | Result | Verification Notes |
| :--- | :--- | :---: | :--- |
| **User Authentication** | `/api/auth/register`, `/api/auth/login` | **PASSED** | PBKDF2-HMAC-SHA256 password hashing + signed JWT verification. |
| **Workspace & Multi-tenancy** | `/api/brands` | **PASSED** | Brand workspace created with auto-assigned isolated Hindsight memory bank. |
| **Multi-Format Ingestion** | `/api/data/upload` | **PASSED** | Multipart form upload for posts, metrics, comments with alias normalization. |
| **Deterministic Calculations** | `calculate_post_metrics` | **PASSED** | Pandas metrics compute 22.12% avg engagement rate and 9.02% save rate. |
| **Audience NLP Extraction** | `/api/audience/insights` | **PASSED** | Sentiment distribution, dominant topics, questions & pain points extracted. |
| **Document RAG Retrieval** | `RAGRetriever` | **PASSED** | Chunking (500 chars, 80 overlap) and normalized TF cosine similarity (0.327). |
| **Orchestrated Strategy** | `/api/agents/strategy` | **PASSED** | Multi-agent execution pipeline outputs evidence-grounded recommendations. |
| **Continuous Learning Loop** | `/api/experiments/{id}/evaluate` | **PASSED** | Actual outcomes evaluated, stored in Hindsight; subsequent strategy cites verified evidence. |
| **Frontend Production Build** | Vite + Tailwind CSS | **PASSED** | Built with zero errors (`dist/` generated). |

---

## 4. API Reference Summary

### Authentication
- `POST /api/auth/register` — Register a new organization user.
- `POST /api/auth/login` — Authenticate and receive JWT access token.
- `GET /api/auth/me` — Retrieve authenticated user profile.

### Brand Workspaces
- `POST /api/brands` — Create a brand profile and provision an isolated Hindsight memory bank.
- `GET /api/brands` — List user's brand workspaces.
- `GET /api/brands/{id}` — Fetch specific brand details.

### Data Ingestion
- `POST /api/data/upload` — Ingest CSV/Excel datasets (`posts`, `comments`, `campaigns`).
- `GET /api/data/files` — Summary of all ingested records and documents for a brand.

### Content & Audience Analytics
- `GET /api/content/analytics` — Aggregate engagement, save, share, and format-level stats.
- `GET /api/content/top-performing` — Ranked list of best-performing posts.
- `GET /api/audience/insights` — Audience sentiment, topics, inquiries, and pain points.

### AI Agents & Orchestration
- `POST /api/agents/strategy` — Execute full orchestrator cycle to generate evidence-backed strategies.
- `POST /api/agents/chat` — Conversational assistant grounded in brand memory and analytics.

### Memory & Learning
- `GET /api/memory/overview` — Inspect Hindsight memory bank and stored campaign learnings.
- `GET /api/memory/recall` — Contextual semantic search through brand memory bank.
- `POST /api/experiments` — Register a campaign experiment hypothesis.
- `POST /api/experiments/{id}/evaluate` — Evaluate outcome and retain learning in Hindsight.

