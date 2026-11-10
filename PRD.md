# AUDIENCEIQ — PRODUCT REQUIREMENTS DOCUMENT (PRD)

# MASTER BUILD PROMPT — EnQue

You are a senior full-stack engineer, AI systems architect, backend developer and UI/UX designer.

Your task is to design, develop, test and deliver a complete, functional AI-powered application named **EnQue**.

Do not merely create a prototype, UI mockup or demonstration dashboard. Build a working software product with a properly implemented backend, database, AI agents, persistent memory, document retrieval and frontend integration.

You are responsible for the entire implementation.

---

# 1. PRODUCT IDENTITY

**Application Name:** EnQue

**Product Category:** AI-Powered Audience Intelligence & Content Optimization Platform.

**Tagline:** Understand your audience. Remember what works. Make smarter content decisions.

## Product Vision

EnQue is an intelligent marketing platform designed for brands, marketing teams and social media agencies.

It helps businesses understand their audience, analyse content performance, identify behavioural patterns and develop better content strategies.

EnQue uses multiple specialized AI agents, Retrieval-Augmented Generation (RAG), and Hindsight persistent memory.

Unlike conventional analytics platforms that simply display historical metrics, EnQue learns from previous campaigns, remembers audience behaviour, evaluates its own recommendations and uses accumulated experiences to improve future strategies.

The central principle is:

**EnQue should not just analyse data. It should accumulate experience and use that experience to make increasingly context-aware decisions.**

## Target Users

- Brands.
- Marketing agencies.
- Social media management teams.
- Digital marketing consultants.
- Business marketing departments.

This is a professional B2B product.

---

# 2. DEVELOPMENT PRIORITIES

Follow this priority order:

1. Backend architecture and functionality.
2. Database and data management.
3. Data ingestion and processing.
4. AI agent implementation.
5. Hindsight persistent memory.
6. RAG implementation.
7. Agent orchestration.
8. Continuous learning workflow.
9. Frontend implementation.
10. Integration testing and deployment readiness.

The backend is the most important part of EnQue.

Do not spend excessive development time decorating the frontend while backend functionality remains incomplete.

The frontend should be simple, intuitive and professional.

---

# 3. TECHNOLOGY STACK

Use the following technology stack.

| Layer | Technology |
|---|---|
| Frontend | React + Vite |
| Language | JavaScript or TypeScript |
| Styling | Tailwind CSS |
| Backend | Python + FastAPI |
| Database | PostgreSQL |
| Vector Database | PostgreSQL + pgvector |
| LLM Provider | Groq API |
| Primary Model | openai/gpt-oss-120b |
| Alternative Model | qwen/qwen3-32b |
| Persistent Memory | Hindsight |
| Data Processing | Pandas |
| NLP | Hugging Face / suitable NLP libraries |
| Charts | Recharts |
| API Documentation | FastAPI Swagger |
| Containerization | Docker + Docker Compose |

Use free and open-source solutions wherever practical.

Do not introduce unnecessary paid services or complicated infrastructure.

If a technology or model is unavailable, implement a reasonable compatible alternative and document the change.

---

# 4. COMPLETE SYSTEM ARCHITECTURE

Implement a modular architecture.

The application should follow this structure:

```text
                         EnQue
                           |
                     REACT FRONTEND
                           |
                        FASTAPI
                           |
                   AGENT ORCHESTRATOR
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
     AUDIENCE          CONTENT           STRATEGY
      AGENT             AGENT              AGENT
          |                |                |
          +----------------+----------------+
                           |
                           v
                  EVALUATION AGENT
                           |
             +-------------+-------------+
             |                           |
             v                           v
        HINDSIGHT                       RAG
     PERSISTENT MEMORY             DOCUMENT RETRIEVAL
             |                           |
             +-------------+-------------+
                           |
                           v
                      POSTGRESQL
                           |
                           v
                    DATA PROCESSING
```

The agents must be independent backend modules coordinated by the orchestrator.

They must not simply be four chatbot interfaces.

Implement clear responsibilities, structured communication, logging, validation and error handling.

---

# 5. BACKEND IMPLEMENTATION

Build the backend using FastAPI.

Keep API routes, business logic, agents, memory, RAG, database operations and data processing separate.

## 5.1 Authentication

Implement:

- User registration.
- User login.
- Secure password hashing.
- JWT authentication.
- Current-user endpoint.
- Protected API routes.
- User-specific data access.

## 5.2 Brand Management

Users must be able to create and manage multiple brand workspaces.

Each brand must have:

- Brand name.
- Industry.
- Description.
- Products or services.
- Target audience.
- Brand objectives.
- Brand voice.
- Brand guidelines.
- Associated campaigns.
- Associated datasets.
- Associated Hindsight memory bank.

Each brand must have an isolated memory bank.

Never mix information from different brands.

## 5.3 Data Ingestion

Support:

- CSV.
- Excel.
- PDF.
- TXT.
- Manual text entry.

### Post dataset fields

```text
post_id
platform
post_date
caption
content_type
topic
reach
impressions
likes
comments
shares
saves
clicks
campaign_id
```

### Audience comment fields

```text
comment_id
post_id
comment_text
comment_date
platform
```

### Campaign fields

```text
campaign_id
campaign_name
campaign_objective
campaign_start_date
campaign_end_date
target_audience
budget
```

### Data ingestion workflow

1. Accept the uploaded file.
2. Validate its extension and size.
3. Inspect its columns and structure.
4. Validate required fields.
5. Handle missing values.
6. Detect duplicate records.
7. Normalize dates and numerical fields.
8. Clean and standardize records.
9. Associate the records with the correct brand.
10. Store structured data in PostgreSQL.
11. Trigger the appropriate analysis pipeline.
12. Return an ingestion report.

Show the user:

- Total records detected.
- Successfully imported records.
- Rejected records.
- Skipped duplicates.
- Validation errors.
- Processing status.

Do not silently ignore errors.

Implement CSV and Excel ingestion first, then PDF and TXT document ingestion.

## 5.4 Data Analysis Engine

Implement deterministic numerical calculations using Python and Pandas.

Required metrics:

**Engagement rate by reach**

(Likes + Comments + Shares + Saves) / Reach × 100

**Save rate**

Saves / Reach × 100

**Share rate**

Shares / Reach × 100

**Comment rate**

Comments / Reach × 100

**Reach growth**

(Current Reach - Previous Reach) / Previous Reach × 100

Handle zero denominators, null values and invalid data.

Never ask an LLM to calculate basic numerical metrics when deterministic calculations are possible.

### Content analysis

Identify:

- Best-performing posts.
- Underperforming posts.
- Successful content formats.
- Successful topics.
- Weak topics.
- Engagement trends.
- Save and share patterns.
- Repeated content themes.
- Content gaps.
- Potential content fatigue.

### Audience analysis

Identify:

- Positive, negative and neutral sentiment.
- Recurring audience interests.
- Frequently discussed topics.
- Frequently asked questions.
- Complaints and pain points.
- Product-related discussions.
- Audience expectations.
- Emerging interests.
- Changes in audience behaviour.

Use NLP for classification and LLMs for deeper contextual interpretation.

All findings must be traceable to actual records.

---

# 6. FOUR SPECIALIZED AI AGENTS

Implement the following agents.

## AGENT 1 — Audience Intelligence Agent

Purpose: Understand the audience.

Responsibilities:

- Analyse uploaded comments and feedback.
- Identify sentiment.
- Extract recurring topics.
- Detect common questions.
- Identify customer concerns.
- Discover audience interests.
- Identify emerging trends.
- Compare audience behaviour over time.

Output must be structured JSON.

Example:

```json
{
  "overall_sentiment": "Mixed",
  "dominant_topics": [],
  "audience_interests": [],
  "common_questions": [],
  "pain_points": [],
  "emerging_trends": [],
  "audience_changes": [],
  "supporting_evidence": []
}
```

## AGENT 2 — Content Intelligence Agent

Purpose: Understand content performance.

Responsibilities:

- Analyse posts and captions.
- Categorize content.
- Compare formats.
- Identify high-performing content.
- Identify low-performing content.
- Discover successful content patterns.
- Detect repeated topics.
- Identify content gaps.
- Analyse brand voice consistency.

Output:

```json
{
  "top_performing_content": [],
  "underperforming_content": [],
  "successful_formats": [],
  "successful_topics": [],
  "weak_topics": [],
  "content_gaps": [],
  "repetition_patterns": [],
  "brand_voice_observations": [],
  "supporting_evidence": []
}
```

## AGENT 3 — Strategy Agent

Purpose: Generate intelligent content strategies.

Inputs:

- Audience analysis.
- Content analysis.
- Brand objectives.
- Brand guidelines.
- Relevant RAG documents.
- Hindsight memories.
- Previous recommendations.
- Previous campaign outcomes.

Responsibilities:

- Recommend content topics.
- Recommend content formats.
- Generate content ideas.
- Create content calendars.
- Suggest engagement strategies.
- Identify campaign opportunities.
- Recommend experiments.
- Explain the reasoning behind recommendations.

Each recommendation must include:

- Recommended action.
- Reasoning.
- Supporting evidence.
- Relevant historical experience.
- Expected outcome.
- Confidence or evidence-strength indicator.
- Measurement method.

Never invent historical evidence.

Clearly distinguish verified findings from hypotheses.

## AGENT 4 — Performance Evaluation and Learning Agent

Purpose: Learn from actual results.

Responsibilities:

1. Retrieve previous recommendations.
2. Identify implemented recommendations.
3. Compare expected and actual results.
4. Identify successful approaches.
5. Identify unsuccessful approaches.
6. Generate learning summaries.
7. Send meaningful experiences to Hindsight.
8. Make those experiences available for future strategy generation.

Example:

```json
{
  "recommendation": "Create educational ingredient-focused reels",
  "expected_outcome": "Increase saves",
  "actual_outcome": "Saves increased compared with the previous campaign",
  "evaluation": "Positive",
  "learning": "Educational ingredient content resonated with this audience",
  "future_action": "Continue testing educational content"
}
```

Do not claim causation from simple before-and-after comparisons.

---

# 7. CENTRAL AGENT ORCHESTRATOR

Build a central orchestration module.

The orchestrator must:

- Receive user requests.
- Identify the required operation.
- Retrieve relevant brand information.
- Retrieve relevant Hindsight memories.
- Retrieve relevant RAG documents.
- Select the appropriate agents.
- Execute agents in the correct order.
- Pass structured results between agents.
- Validate agent outputs.
- Combine the results.
- Return the final response.
- Record execution status and logs.

Example:

```text
User Request
     |
     v
Orchestrator
     |
     v
Identify Brand and Task
     |
     v
Retrieve Brand Information
     |
     +-------> Hindsight Recall
     |
     +-------> RAG Retrieval
     |
     v
Audience Intelligence Agent
     |
     v
Content Intelligence Agent
     |
     v
Strategy Agent
     |
     v
Validate Results
     |
     v
Return Strategy
```

Do not execute all agents for every request unnecessarily.

Implement task-based agent selection.

For long-running tasks, use background processing and status tracking.

---

# 8. HINDSIGHT — THE CORE MEMORY SYSTEM

This is a mandatory and central feature.

Do not simulate memory.

Use the actual Hindsight service and official Python SDK.

Install the official SDK:

```bash
pip install hindsight-client
```

Use environment variables:

```env
HINDSIGHT_BASE_URL=
HINDSIGHT_API_KEY=
```

Implement actual supported operations:

- `retain()` — Store meaningful experiences.
- `recall()` — Retrieve relevant experiences.
- `reflect()` — Generate higher-level insights.

Before implementation, inspect the installed SDK version and its official documentation. Confirm the exact method signatures, parameters and return structures. Do not invent APIs.

## 8.1 Memory Isolation

Each brand must have a separate Hindsight memory bank.

Example:

```text
EnQue
  |
  +-- GlowUp Memory Bank
  |
  +-- PureSkin Memory Bank
  |
  +-- FreshFace Memory Bank
```

The names are illustrative.

## 8.2 Memory Categories

Retain:

**Brand knowledge**
- Brand identity.
- Brand voice.
- Products.
- Objectives.
- Target audience.

**Audience knowledge**
- Recurring interests.
- Common questions.
- Customer concerns.
- Emerging trends.
- Changing preferences.

**Content knowledge**
- Successful topics.
- Successful formats.
- Underperforming content.
- Repeated patterns.
- Brand communication preferences.

**Experience knowledge**
- Previous recommendations.
- Implemented strategies.
- Campaign outcomes.
- Successful experiments.
- Failed experiments.
- Lessons learned.

Do not indiscriminately store every raw comment.

Retain meaningful, contextualized findings with relevant brand, campaign and source information.

## 8.3 Memory Retrieval

Before strategy generation:

1. Identify the current brand.
2. Understand the current request.
3. Retrieve relevant historical memories.
4. Identify similar previous situations.
5. Supply useful memories to the Strategy Agent.
6. Record which memories were used in the generated recommendation.

## 8.4 Memory Reflection

Use Hindsight reflection to discover patterns across accumulated experiences.

Examples:

- Educational posts repeatedly generate more saves.
- Certain topics generate engagement but fewer shares.
- Audience interests have changed over time.
- Some content strategies repeatedly underperform.

These are examples only. Discover actual patterns from accumulated data.

## 8.5 Memory Inspection

Create backend functions that allow the frontend to display actual Hindsight-backed memories.

Display:
- Stored observations.
- Audience patterns.
- Content patterns.
- Campaign experiences.
- Lessons learned.
- Recent reflections.

Where supported, preserve dates, source references and other relevant metadata.

Never hardcode fake memory records or fake learning statistics.

---

# 9. RAG IMPLEMENTATION

Implement document-based Retrieval-Augmented Generation using PostgreSQL and pgvector.

Supported documents:

- Brand guidelines.
- Product descriptions.
- Campaign reports.
- Marketing documents.
- Brand strategy documents.

Workflow:

```text
Upload Document
      |
Extract Text
      |
Split Into Chunks
      |
Generate Embeddings
      |
Store in pgvector
      |
Retrieve Relevant Chunks
      |
Pass Context to Agents
```

RAG retrieves information from source documents.

Hindsight remembers experiences and learnings.

They must remain separate systems and be used together where appropriate.

Implement brand-level retrieval isolation.

---

# 10. DATABASE

Use PostgreSQL.

Create appropriate models, migrations, relationships and indexes.

Required tables:

- users
- brands
- brand_guidelines
- campaigns
- posts
- post_metrics
- audience_comments
- documents
- document_chunks
- recommendations
- experiments
- experiment_outcomes
- analysis_runs

Include:

- Primary keys.
- Foreign keys.
- Created and updated timestamps.
- Appropriate uniqueness constraints.
- Brand ownership relationships.
- Database indexes.

Hindsight should retain persistent experiential memories in its own service. PostgreSQL should store application data and the identifiers connecting brands to their Hindsight banks.

---

# 11. API ENDPOINTS

Create REST APIs.

### Authentication

```text
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
```

### Brands

```text
POST   /api/brands
GET    /api/brands
GET    /api/brands/{id}
PUT    /api/brands/{id}
DELETE /api/brands/{id}
```

### Data

```text
POST /api/data/upload
GET  /api/data/files
GET  /api/data/files/{id}
POST /api/data/process
GET  /api/data/process/{job_id}
```

### Audience

```text
POST /api/audience/analyze
GET  /api/audience/insights
GET  /api/audience/trends
```

### Content

```text
POST /api/content/analyze
GET  /api/content/analytics
GET  /api/content/top-performing
GET  /api/content/underperforming
```

### Agents

```text
POST /api/agents/analyze
POST /api/agents/strategy
POST /api/agents/chat
GET  /api/agents/runs/{run_id}
```

### Hindsight

```text
GET  /api/memory/overview
GET  /api/memory/recall
POST /api/memory/reflect
GET  /api/memory/history
```

### Recommendations

```text
POST  /api/recommendations
GET   /api/recommendations
PATCH /api/recommendations/{id}
```

### Experiments

```text
POST /api/experiments
GET  /api/experiments
POST /api/experiments/{id}/evaluate
GET  /api/experiments/{id}/outcome
```

All APIs must include validation, authentication, authorization, consistent response schemas and error handling.

Generate Swagger documentation.

---

# 12. FRONTEND — SIMPLE AND USER FRIENDLY

The frontend should be professional, modern and easy to navigate.

Do not make it complicated.

## Design direction

Create a clean SaaS interface with:

- Minimal layout.
- Clear typography.
- Consistent spacing.
- Professional colours.
- Responsive design.
- Light and dark mode.
- Simple charts.
- Clear loading states.
- Friendly empty states.
- Useful error messages.

Avoid:
- Excessive gradients.
- Unnecessary animations.
- Overcrowded cards.
- Complicated visualizations.
- Decorative elements that do not improve usability.

## Main navigation

Create a sidebar:

1. Overview
2. Audience Insights
3. Content Analytics
4. AI Strategy
5. AI Memory
6. Experiments
7. Data Sources
8. Settings

Include a brand selector.

## Required pages

### A. Overview

Show:
- Selected brand.
- Posts analysed.
- Comments analysed.
- Engagement metrics.
- Recent audience insights.
- Top-performing content.
- Recent recommendations.
- Recent learning activity.

### B. Audience Insights

Show:
- Sentiment distribution.
- Audience interests.
- Recurring topics.
- Common questions.
- Pain points.
- Emerging trends.
- Changes over time.

### C. Content Analytics

Show:
- Performance by format.
- Best-performing posts.
- Underperforming posts.
- Topic performance.
- Engagement trends.
- Content gaps.

### D. AI Strategy

Provide a simple AI interaction interface.

Example questions:

- What should we post next month?
- Which topics should we focus on?
- Why did our last campaign underperform?
- What content formats resonate with our audience?
- Has our audience's interest changed?

Display recommendations with evidence and reasoning.

### E. AI Memory

Show actual Hindsight-backed memories.

Allow users to explore:
- Audience observations.
- Brand knowledge.
- Content patterns.
- Campaign learnings.
- Previous experiences.

Provide a way to trigger reflection.

### F. Experiments

Allow users to:
- Create an experiment.
- Define a hypothesis.
- Select a measurement method.
- Record actual results.
- Evaluate the outcome.

### G. Data Sources

Allow users to:
- Upload files.
- View imported datasets.
- View processing status.
- Review errors.
- View available documents.

Every screen must retrieve actual data from backend APIs.

Do not build static dashboard cards with hardcoded numbers.

---

# 13. DEMONSTRATION DATASET

Create a realistic synthetic dataset for a fictional skincare brand named GlowUp Skincare.

Generate:

- 30–50 posts.
- 200–500 audience comments.
- 3–5 campaigns.
- Different content formats.
- Different engagement levels.
- Multiple audience topics.
- Successful and unsuccessful examples.
- At least two time periods with a meaningful audience-interest shift.

The dataset should be internally consistent.

Label it clearly as synthetic demonstration data.

Provide an easy way to load the demo data into the application.

The application must also work with user-uploaded datasets.

---

# 14. CRITICAL END-TO-END LEARNING DEMONSTRATION

This is the most important acceptance test.

EnQue must demonstrate that it learns from accumulated experiences.

Build the following complete workflow.

### Stage 1 — Initial Analysis

Create or select the GlowUp Skincare brand.

Upload the first dataset.

Run audience and content analysis.

Generate an initial strategy.

### Stage 2 — Store Experiences

Generate recommendations.

Allow the user to mark recommendations as implemented, rejected or not implemented.

Upload the resulting campaign data.

Evaluate actual outcomes.

### Stage 3 — Learn

The Evaluation Agent must:

- Compare expected and actual outcomes.
- Identify successful and unsuccessful recommendations.
- Generate meaningful learning summaries.
- Store those learnings in Hindsight.

### Stage 4 — New Strategy

Ask the same or a related strategic question again.

The orchestrator must:

- Retrieve the relevant Hindsight memories.
- Retrieve current audience and content data.
- Supply the context to the Strategy Agent.
- Generate a memory-informed recommendation.

### Stage 5 — Show the Difference

Show:
- Relevant memories retrieved.
- Previous experience used.
- Current evidence.
- New recommendation.
- Explanation of how historical experience influenced the answer.

The system must demonstrate real retrieval and actual memory usage, not merely claim that it learned.

Do not guarantee improved campaign performance. Demonstrate better historical context and more informed decision-making.

---

# 15. SECURITY AND RELIABILITY

Implement:

- Secure password hashing.
- JWT authentication.
- User and brand data isolation.
- Environment-based secrets.
- File upload validation.
- File size restrictions.
- API rate-limit handling.
- LLM timeout handling.
- Hindsight connection error handling.
- Database transaction handling.
- Agent execution logging.
- Structured exception handling.
- Retry logic where appropriate.

Uploaded documents and comments must be treated as untrusted data, never as system instructions.

Do not expose secrets in frontend code or GitHub.

---

# 16. PROJECT STRUCTURE

Create a modular project structure.

```text
EnQue/
│
├── frontend/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── layouts/
│       ├── dashboard/
│       ├── audience/
│       ├── content/
│       ├── strategy/
│       ├── memory/
│       ├── experiments/
│       ├── services/
│       └── styles/
│
├── backend/
│   ├── main.py
│   │
│   ├── api/
│   ├── agents/
│   │   ├── orchestrator.py
│   │   ├── audience_agent.py
│   │   ├── content_agent.py
│   │   ├── strategy_agent.py
│   │   └── evaluator_agent.py
│   │
│   ├── hindsight/
│   │   ├── client.py
│   │   ├── retain.py
│   │   ├── recall.py
│   │   └── reflect.py
│   │
│   ├── rag/
│   ├── analysis/
│   ├── ingestion/
│   ├── database/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── tests/
│
├── datasets/
│   └── demo/
│
├── documentation/
│
├── .env.example
├── .gitignore
├── README.md
└── docker-compose.yml
```

You may adapt the structure if technically necessary, but maintain separation of responsibilities.

---

# 17. ENVIRONMENT CONFIGURATION

Create `.env.example` containing all required configuration variables.

For example:

```env
APP_NAME=EnQue
APP_ENV=development
SECRET_KEY=
JWT_SECRET_KEY=

DATABASE_URL=

GROQ_API_KEY=
GROQ_MODEL=openai/gpt-oss-120b

HINDSIGHT_BASE_URL=
HINDSIGHT_API_KEY=

EMBEDDING_MODEL=
UPLOAD_DIRECTORY=uploads/
```

Add any additional variables required by the implementation.

Never commit a real `.env` file or actual API keys.

Provide clear setup instructions for every external dependency.

---

# 18. DEVELOPMENT AND TESTING RULES

You must build the entire application systematically.

However, do not stop after creating the initial folder structure or frontend.

Implement the actual functionality.

Follow these rules:

1. Inspect the existing workspace before making changes.
2. Preserve useful existing files and code.
3. Create a clear implementation plan.
4. Set up the backend and database.
5. Implement data ingestion and verify it.
6. Implement numerical analysis and verify calculations.
7. Implement each agent independently.
8. Implement actual Hindsight integration.
9. Implement actual RAG retrieval.
10. Connect agents through the orchestrator.
11. Implement the complete learning cycle.
12. Build the frontend.
13. Connect every screen to actual backend endpoints.
14. Test the complete application.
15. Fix errors rather than hiding them.
16. Update documentation.

Write automated tests for:

- Authentication.
- Brand isolation.
- File validation.
- Data ingestion.
- Metric calculations.
- Audience analysis.
- Content analysis.
- Agent orchestration.
- Hindsight retain and recall.
- RAG retrieval.
- Recommendation generation.
- Outcome evaluation.
- Memory-informed strategy generation.

Use mocks only in isolated unit tests when external services are unavailable. Never represent mocked integrations as successful live integrations.

---

# 19. IMPLEMENTATION STRATEGY

Work in implementation phases, but continue until the entire MVP is built.

**Phase 1:** Project foundation, backend, database and authentication.

**Phase 2:** Brand management, ingestion and data processing.

**Phase 3:** Audience and Content Intelligence Agents.

**Phase 4:** Hindsight and RAG.

**Phase 5:** Strategy Agent, Evaluation Agent and Orchestrator.

**Phase 6:** Complete learning cycle and backend testing.

**Phase 7:** Frontend implementation and API integration.

**Phase 8:** End-to-end testing, bug fixing and documentation.

At the end of each phase:

- Run relevant tests.
- Fix implementation errors.
- Verify the working functionality.
- Update the project documentation.
- Continue to the next phase.

Do not stop to ask for permission after every phase.

Make reasonable technical decisions independently.

Ask me only when an essential external credential or genuinely ambiguous requirement prevents progress.

If credentials are missing, implement the integration properly, create configuration placeholders and explain exactly what I need to provide. Continue building all other components.

---

# 20. FINAL ACCEPTANCE CRITERIA

The project is considered complete only when:

- The frontend runs.
- The FastAPI backend runs.
- PostgreSQL works.
- Authentication works.
- Brand workspaces work.
- File uploads work.
- Data validation and processing work.
- Metrics are calculated correctly.
- Audience Intelligence Agent works.
- Content Intelligence Agent works.
- Strategy Agent works.
- Evaluation Agent works.
- The central orchestrator works.
- Hindsight is genuinely integrated.
- Hindsight retain, recall and reflect work.
- Brand-specific memory isolation works.
- RAG document retrieval works.
- Recommendations use current data and relevant memories.
- Outcomes can be evaluated.
- New learning is retained.
- Future recommendations can retrieve that learning.
- The frontend displays real backend information.
- The demonstration workflow works.
- Tests and documentation are included.

---

# 21. FINAL BUILD INSTRUCTION

Build **EnQue as a complete, functional AI-powered business intelligence platform**.

Do not optimize for appearance at the expense of functionality.

The backend must be robust, modular and genuinely intelligent.

The agents must collaborate through an orchestrator.

Hindsight must provide real persistent memory.

RAG must retrieve actual uploaded documents.

The learning loop must operate across separate sessions and new datasets.

The frontend must make all these capabilities accessible through a simple, clean and intuitive interface.

**Do not deliver a collection of disconnected features. Deliver one integrated product.**

Start by inspecting the workspace, then implement the application from foundation to completion.

Your final response must include:

1. What has been implemented.
2. What is fully functional.
3. What external credentials I need to configure.
4. Exact commands to install and run the application.
5. How to load the demo dataset.
6. How to demonstrate the complete Hindsight learning cycle.
7. Any remaining limitations.

**Build EnQue.**



**Product:** EnQue  
**Product Type:** AI-Powered Audience Intelligence & Content Optimization Platform  
**Build Environment:** Google Antigravity  
**Primary Focus:** Backend engineering, AI agents, persistent memory and data processing  
**Frontend Priority:** Simple, clean and user-friendly  
**Version:** MVP 1.0

---

# 1. PRODUCT OVERVIEW

## 1.1 What is EnQue?

EnQue is an AI-powered platform that helps brands, marketing teams and social media agencies understand their audiences, evaluate content performance and continuously improve their content strategies.

It uses multiple specialized AI agents, Retrieval-Augmented Generation (RAG), and Hindsight persistent memory.

Unlike ordinary AI analytics tools that analyse data once and generate generic recommendations, EnQue remembers previous campaigns, audience behaviour, content performance and the outcomes of its recommendations.

It uses these accumulated experiences to make increasingly informed decisions.

### Core idea

**EnQue doesn't just analyse what happened. It remembers why it happened and uses those learnings to make better-informed future decisions.**

## 1.2 Problem Statement

Businesses collect large amounts of social media and marketing data but often struggle to:

- Understand what their audience actually cares about.
- Identify recurring audience interests and concerns.
- Understand why certain content performs better than others.
- Detect changes in audience behaviour.
- Develop content strategies based on historical performance.
- Learn from unsuccessful campaigns.
- Maintain consistent brand communication.

Most analytics tools show numbers. Most AI tools generate recommendations without meaningful historical context.

EnQue bridges this gap through persistent experiential memory and coordinated AI agents.

## 1.3 Target Users

- Marketing agencies.
- Social media management teams.
- Brand marketing departments.
- Digital marketing consultants.
- Businesses managing multiple brands.

The product must be designed as a real business intelligence platform, not a student analytics application.

---

# 2. PRODUCT OBJECTIVES

The MVP must successfully demonstrate the following:

1. Upload and process real structured marketing data.
2. Analyse audience comments, feedback and engagement.
3. Analyse content performance across different formats and topics.
4. Use multiple specialized AI agents to interpret the data.
5. Store important insights and experiences in Hindsight.
6. Retrieve previous experiences when answering new questions.
7. Generate evidence-based content strategies.
8. Evaluate recommendations against actual results.
9. Update persistent memory based on new outcomes.
10. Demonstrate that the system improves its recommendations through accumulated experience.

**Hindsight must be a core functional component, not an optional integration or decorative feature.**

---

# 3. CORE SYSTEM WORKFLOW

The complete system must follow this cycle:

**COLLECT → ANALYSE → REMEMBER → STRATEGIZE → EXECUTE → MEASURE → LEARN**

### Step 1: Collect
- Upload campaign reports.
- Upload post-performance CSV or Excel files.
- Upload audience comments and feedback.
- Upload brand guidelines and product information.
- Allow manual entry of missing information.

### Step 2: Analyse
- Process uploaded data.
- Calculate engagement metrics.
- Identify audience interests and sentiment.
- Categorize content.
- Identify performance patterns.

### Step 3: Remember
- Retain important findings in Hindsight.
- Store previous campaign experiences.
- Store successful and unsuccessful strategies.
- Maintain brand-specific memory.

### Step 4: Strategize
- Retrieve relevant historical memories.
- Combine them with current data.
- Generate personalized content recommendations.
- Explain the reasoning behind each recommendation.

### Step 5: Execute
For MVP, execution means generating:
- Content calendars.
- Post ideas.
- Content format recommendations.
- Campaign strategies.
- Suggested engagement approaches.

Automated publishing is outside the MVP scope.

### Step 6: Measure
- Upload new campaign results.
- Compare actual performance with expectations.
- Evaluate recommendation effectiveness.

### Step 7: Learn
- Identify what worked and what failed.
- Generate learning summaries.
- Retain those experiences in Hindsight.
- Use them in future recommendations.

---

# 4. TECHNICAL ARCHITECTURE

The application must use a modular backend architecture.

## 4.1 Technology Stack

| Component | Technology |
|---|---|
| Frontend | React + Vite |
| Styling | Tailwind CSS |
| Backend | Python + FastAPI |
| Database | PostgreSQL |
| Vector Search / Document RAG | pgvector |
| AI Models | Groq API |
| Primary LLM | openai/gpt-oss-120b |
| Alternative LLM | qwen/qwen3-32b |
| Persistent Agent Memory | Hindsight |
| Data Processing | Pandas |
| NLP | Hugging Face / suitable NLP libraries |
| Charts | Recharts |
| API Documentation | FastAPI Swagger |

Use the available free tiers and open-source tools wherever possible.

Do not introduce unnecessary paid services.

## 4.2 High-Level Architecture

The architecture should follow this structure:

```text
                  FRONTEND
                     |
                     |
                FASTAPI
                  BACKEND
                     |
             AGENT ORCHESTRATOR
                     |
       +-------------+-------------+
       |             |             |
  AUDIENCE       CONTENT       STRATEGY
   AGENT          AGENT         AGENT
       |             |             |
       +-------------+-------------+
                     |
              EVALUATION AGENT
                     |
          +----------+----------+
          |                     |
      HINDSIGHT               RAG
   PERSISTENT MEMORY      DOCUMENT RETRIEVAL
          |                     |
          +----------+----------+
                     |
               POSTGRESQL
                     |
              DATA PROCESSING
```

The orchestrator coordinates the agents and manages their execution order.

Agents must be independent backend modules, not separate chatbot interfaces.

---

# 5. BACKEND FUNCTIONAL REQUIREMENTS

This is the most important part of the project.

Antigravity must prioritize correct backend implementation before spending significant time on frontend styling.

## 5.1 Data Ingestion Module

Create a robust data ingestion pipeline.

### Supported inputs

- CSV files.
- Excel files (.xlsx).
- PDF documents.
- TXT documents.
- Manual text input.

### Expected social media dataset fields

For content/posts:

- post_id
- platform
- post_date
- caption
- content_type
- topic/category
- reach
- impressions
- likes
- comments
- shares
- saves
- clicks (optional)
- campaign_id

For audience comments:

- comment_id
- post_id
- comment_text
- comment_date
- platform (optional)

For campaigns:

- campaign_id
- campaign_name
- campaign_objective
- campaign_start_date
- campaign_end_date
- target_audience
- budget (optional)

### Data ingestion requirements

The backend must:

1. Validate uploaded file types.
2. Validate required columns.
3. Handle missing and invalid values.
4. Identify duplicate records.
5. Normalize dates and numeric fields.
6. Associate records with the correct brand.
7. Store structured data in PostgreSQL.
8. Trigger appropriate analysis pipelines.
9. Return clear processing reports and errors.

Do not silently discard invalid data.

The user must be able to see whether a dataset was processed successfully and how many records were imported, rejected or skipped.

## 5.2 Data Analysis Module

Build a dedicated analysis layer separate from the LLM agents.

Use Python and Pandas for numerical calculations.

### Required metrics

**Engagement rate by reach**

Engagement Rate = (Likes + Comments + Shares + Saves) / Reach × 100

**Save rate**

Save Rate = Saves / Reach × 100

**Share rate**

Share Rate = Shares / Reach × 100

**Comment rate**

Comment Rate = Comments / Reach × 100

**Reach growth**

Reach Growth = (Current Reach - Previous Reach) / Previous Reach × 100

Handle zero denominators and missing metrics safely.

Do not treat reach and impressions as interchangeable.

### Content performance analysis

Identify:

- Best-performing content.
- Lowest-performing content.
- Best-performing content formats.
- Topics with consistently high engagement.
- Topics with consistently low engagement.
- Content performance over time.
- Engagement differences between formats.
- Content that generates saves and shares.
- Potential content fatigue or repetition.

Comparisons must consider relevant context, such as time period, reach and content format.

### Audience analysis

Analyse audience comments and feedback to identify:

- Positive, negative and neutral sentiment.
- Frequently discussed topics.
- Recurring questions.
- Customer complaints.
- Product-related discussions.
- Audience expectations.
- Frequently mentioned features.
- Emerging interests.
- Changes in audience concerns.

Use NLP models or appropriate classification methods.

LLMs can provide deeper interpretations, but deterministic data calculations should not be delegated to an LLM.

---

# 6. AI AGENT SYSTEM

Implement four specialized agents coordinated by one central orchestrator.

Each agent must have a clearly defined responsibility, structured input and output, and access only to the tools and data required for its task.

## 6.1 Audience Intelligence Agent

**Responsibility:** Understand the audience.

Inputs:
- Audience comments.
- Customer feedback.
- Engagement data.
- Campaign information.
- Previous audience insights.

Tasks:
- Analyse sentiment.
- Extract recurring topics.
- Identify frequently asked questions.
- Detect complaints and concerns.
- Identify audience interests.
- Compare audience behaviour across time periods.
- Detect emerging or declining topics.

Output should contain:

```json
{
  "overall_sentiment": "...",
  "dominant_topics": [],
  "audience_interests": [],
  "common_questions": [],
  "pain_points": [],
  "emerging_trends": [],
  "audience_changes": [],
  "supporting_evidence": []
}
```

The output must be grounded in actual uploaded data.

## 6.2 Content Intelligence Agent

**Responsibility:** Understand content performance.

Inputs:
- Post captions.
- Content types.
- Topics.
- Performance metrics.
- Campaign details.
- Historical content memories.

Tasks:
- Categorize content.
- Identify successful content patterns.
- Identify underperforming content.
- Compare content formats.
- Detect repeated topics.
- Identify content gaps.
- Analyse brand voice consistency.
- Connect content performance with audience interests.

Output:

```json
{
  "top_performing_content": [],
  "underperforming_content": [],
  "successful_formats": [],
  "successful_topics": [],
  "weak_topics": [],
  "content_gaps": [],
  "repetition_patterns": [],
  "brand_voice_observations": [],
  "supporting_evidence": []
}
```

## 6.3 Strategy Agent

**Responsibility:** Generate intelligent content strategies.

Inputs:
- Audience Intelligence Agent output.
- Content Intelligence Agent output.
- Brand objectives.
- Brand guidelines.
- Hindsight recalled memories.
- Hindsight reflections.
- Previous recommendation outcomes.

Tasks:
- Recommend content topics.
- Recommend content formats.
- Suggest content calendars.
- Suggest posting strategies.
- Generate content ideas.
- Recommend audience engagement approaches.
- Suggest campaign experiments.
- Explain why a recommendation is suitable.

Every recommendation must contain:

- Recommendation.
- Reasoning.
- Supporting audience evidence.
- Supporting historical evidence, if available.
- Expected outcome.
- Confidence or evidence-strength indicator.
- Suggested measurement method.

The agent must distinguish between verified findings, reasonable interpretations and hypotheses.

It must not invent historical evidence or claim a predicted improvement is guaranteed.

## 6.4 Performance Evaluation and Learning Agent

**Responsibility:** Learn from actual outcomes.

Inputs:
- Previous recommendations.
- Actual published content.
- New performance metrics.
- Campaign objectives.
- Previous Hindsight memories.

Tasks:
1. Identify which recommendations were implemented.
2. Compare expected and actual outcomes.
3. Identify successful strategies.
4. Identify unsuccessful strategies.
5. Analyse possible reasons for differences.
6. Generate structured learning summaries.
7. Send meaningful experiences to Hindsight for retention.

Example:

```json
{
  "recommendation": "Create educational ingredient-focused reels",
  "expected_outcome": "Increase saves and audience engagement",
  "actual_outcome": "Higher saves compared with the previous campaign",
  "evaluation": "Positive",
  "learning": "Educational ingredient content resonated with this audience",
  "future_action": "Continue testing educational content in different formats"
}
```

Do not claim causation from simple before-and-after comparisons. Mark conclusions as observational unless a controlled experiment supports them.

---

# 7. CENTRAL AGENT ORCHESTRATOR

Build a central orchestrator that controls all agent operations.

It should:

1. Receive the user's request.
2. Understand the requested operation.
3. Retrieve relevant brand information.
4. Retrieve relevant Hindsight memories.
5. Retrieve relevant RAG documents.
6. Decide which agents are required.
7. Execute agents in the correct order.
8. Pass structured outputs between agents.
9. Validate agent responses.
10. Combine results.
11. Return a final response to the frontend.
12. Log execution status and errors.

Example workflow:

```text
User asks:
"What should our brand post next month?"

          |
          v
    ORCHESTRATOR
          |
          v
    Retrieve brand data
          |
          v
    Hindsight Recall
          |
          v
    RAG Document Retrieval
          |
          v
    Audience Intelligence Agent
          |
          v
    Content Intelligence Agent
          |
          v
    Strategy Agent
          |
          v
    Validate recommendations
          |
          v
    Return content strategy
```

The orchestrator must not blindly execute every agent for every request. It should select the necessary agents based on the task.

Implement structured agent communication and clear error handling.

---

# 8. HINDSIGHT PERSISTENT MEMORY

## 8.1 Core Requirement

Hindsight is a mandatory part of EnQue.

It must function as the platform's long-term experiential memory.

The system must retain meaningful information from its previous analyses and retrieve that information when making future decisions.

Use the official Hindsight Python SDK.

Install:

```bash
pip install hindsight-client
```

Configure using environment variables:

```env
HINDSIGHT_BASE_URL=
HINDSIGHT_API_KEY=
```

Use the actual SDK and its supported operations.

The core operations are:

- `retain()` — Store important information.
- `recall()` — Retrieve relevant memories.
- `reflect()` — Generate higher-level insights from accumulated memories.

Do not simulate these operations with PostgreSQL or an ordinary dictionary.

## 8.2 Memory Isolation

Create a separate Hindsight memory bank for every brand.

Example:

```text
EnQue
   |
   +-- Brand A Memory Bank
   |
   +-- Brand B Memory Bank
   |
   +-- Brand C Memory Bank
```

Never mix the experiences or memories of different brands.

## 8.3 What Should Be Remembered?

The memory system should retain:

**Brand Knowledge**
- Brand identity.
- Target audience.
- Brand voice.
- Product information.
- Brand objectives.

**Audience Knowledge**
- Recurring interests.
- Common questions.
- Audience preferences.
- Repeated complaints.
- Emerging interests.

**Content Knowledge**
- Successful topics.
- Successful formats.
- Underperforming content.
- Repeated content patterns.
- Brand communication preferences.

**Experience Knowledge**
- Previous recommendations.
- Implemented strategies.
- Actual campaign results.
- Successful experiments.
- Failed experiments.
- Lessons learned.

Retain meaningful findings, not every raw record or every individual comment.

## 8.4 Memory Retrieval

Before generating a strategy, retrieve memories relevant to:

- Current brand.
- Current audience interests.
- Requested content topic.
- Previous campaigns.
- Previous recommendations.
- Similar historical situations.

The Strategy Agent must actually use the retrieved memories.

## 8.5 Memory Reflection

Use Hindsight reflection to identify broader patterns over time.

Examples:

- Educational content has repeatedly generated more saves.
- Product-focused posts have generated discussion but fewer shares.
- Audience interest has shifted from general skincare to ingredient safety.
- Certain campaign strategies repeatedly underperformed.

These are illustrative examples. The system must derive its own findings from uploaded data.

## 8.6 Visible Memory Interface

Create a dedicated Memory page that displays information retrieved from actual Hindsight memory.

Display:
- Stored brand knowledge.
- Audience observations.
- Content performance patterns.
- Previous campaign experiences.
- Successful strategies.
- Unsuccessful strategies.
- Recent learning summaries.

Each memory should show relevant metadata where available, such as source, date or campaign association.

Never create fake memory counters or hardcode example memories as if they were real.

---

# 9. RAG IMPLEMENTATION

RAG and Hindsight must have different responsibilities.

### RAG

Retrieves information from uploaded source documents:

- Brand guidelines.
- Product descriptions.
- Campaign reports.
- Marketing documents.
- Brand strategy documents.

### Hindsight

Remembers accumulated experiences:

- What worked previously.
- What failed previously.
- Audience behaviour patterns.
- Historical observations.
- Lessons from previous campaigns.

Use PostgreSQL with pgvector for document embeddings and similarity retrieval.

RAG workflow:

```text
Upload Document
      |
Extract Text
      |
Split Into Chunks
      |
Generate Embeddings
      |
Store in pgvector
      |
Retrieve Relevant Chunks
      |
Pass Context to Agents
```

Ensure retrieved documents belong to the correct brand.

Do not treat RAG as a replacement for Hindsight.

---

# 10. DATABASE DESIGN

Use PostgreSQL for structured application data.

Create appropriate tables with relationships, constraints and indexes.

Required entities:

### Users
- id
- name
- email
- password_hash
- created_at

### Brands
- id
- user_id
- brand_name
- description
- industry
- target_audience
- objectives
- hindsight_bank_id
- created_at

### Brand_Guidelines
- id
- brand_id
- document_id
- brand_voice
- communication_preferences

### Campaigns
- id
- brand_id
- campaign_name
- objective
- start_date
- end_date
- target_audience

### Posts
- id
- brand_id
- campaign_id
- platform
- caption
- content_type
- topic
- post_date

### Post_Metrics
- id
- post_id
- reach
- impressions
- likes
- comments
- shares
- saves
- clicks
- recorded_at

### Audience_Comments
- id
- brand_id
- post_id
- comment_text
- comment_date
- sentiment
- topic

### Documents
- id
- brand_id
- file_name
- document_type
- processing_status
- uploaded_at

### Recommendations
- id
- brand_id
- recommendation
- reasoning
- evidence
- expected_outcome
- status
- created_at

### Experiments
- id
- brand_id
- recommendation_id
- hypothesis
- measurement_method
- start_date
- end_date
- status

### Experiment_Outcomes
- id
- experiment_id
- actual_results
- evaluation
- learning_summary
- evaluated_at

### Analysis_Runs
- id
- brand_id
- analysis_type
- execution_status
- result
- created_at

Use appropriate foreign keys and indexes.

Store Hindsight memory in Hindsight itself. PostgreSQL should store application records and references to the relevant brand memory banks, not pretend to be Hindsight.

---

# 11. BACKEND API REQUIREMENTS

Implement REST APIs using FastAPI.

Required endpoints:

### Authentication
- POST `/api/auth/register`
- POST `/api/auth/login`
- GET `/api/auth/me`

### Brand Management
- POST `/api/brands`
- GET `/api/brands`
- GET `/api/brands/{brand_id}`
- PUT `/api/brands/{brand_id}`
- DELETE `/api/brands/{brand_id}`

### Data Ingestion
- POST `/api/data/upload`
- GET `/api/data/files`
- GET `/api/data/files/{file_id}`
- POST `/api/data/process`
- GET `/api/data/process/{job_id}`

### Audience Intelligence
- POST `/api/audience/analyze`
- GET `/api/audience/insights`
- GET `/api/audience/trends`

### Content Intelligence
- POST `/api/content/analyze`
- GET `/api/content/analytics`
- GET `/api/content/top-performing`
- GET `/api/content/underperforming`

### Agent Operations
- POST `/api/agents/analyze`
- POST `/api/agents/strategy`
- POST `/api/agents/chat`
- GET `/api/agents/runs/{run_id}`

### Hindsight Memory
- GET `/api/memory/overview`
- GET `/api/memory/recall`
- POST `/api/memory/reflect`
- GET `/api/memory/history`

### Recommendations
- POST `/api/recommendations`
- GET `/api/recommendations`
- PATCH `/api/recommendations/{id}`

### Experiments and Learning
- POST `/api/experiments`
- GET `/api/experiments`
- POST `/api/experiments/{id}/evaluate`
- GET `/api/experiments/{id}/outcome`

All endpoints must include proper request validation, authentication, authorization, response schemas and error handling.

Use asynchronous job processing for longer-running ingestion and analysis operations where necessary. The frontend must be able to check processing status.

Generate API documentation through FastAPI Swagger.

---

# 12. FRONTEND REQUIREMENTS

The frontend must be simple, intuitive and user-friendly.

**Do not overdesign it. Do not make the frontend the main focus of development.**

The goal is to provide a clear interface for accessing the backend's intelligence.

## 12.1 Design Direction

Create a modern SaaS dashboard.

Visual requirements:

- Clean and minimal.
- Professional.
- Easy-to-read typography.
- Clear navigation.
- Consistent spacing.
- Responsive layout.
- Light and dark mode.
- Subtle charts and visualizations.
- No unnecessary animations.
- No overcrowded dashboards.

Avoid excessive gradients, glowing effects, complicated cards and decorative elements.

## 12.2 Main Navigation

Create a simple sidebar containing:

1. Overview
2. Audience Insights
3. Content Analytics
4. AI Strategy
5. AI Memory
6. Experiments
7. Data Sources
8. Settings

Include a brand selector at the top.

## 12.3 Required Screens

### Overview Dashboard

Display:
- Selected brand.
- Total posts analysed.
- Total audience comments analysed.
- Overall engagement metrics.
- Recent audience insights.
- Top-performing content.
- Recent AI recommendations.
- Latest learning activity.

All displayed information must come from the backend.

### Audience Insights

Display:
- Sentiment breakdown.
- Audience interests.
- Frequently discussed topics.
- Common questions.
- Audience pain points.
- Emerging trends.
- Historical audience changes.

### Content Analytics

Display:
- Performance by content type.
- Best-performing posts.
- Underperforming posts.
- Topic performance.
- Engagement trends.
- Content gaps.

### AI Strategy

Provide a simple interface where users can ask:

- What should we post next month?
- Which topics should we focus on?
- Why did our last campaign underperform?
- What content formats resonate with our audience?
- Has our audience's interest changed?

Display recommendations with explanations and evidence.

### AI Memory

Display real Hindsight memory.

Allow users to:
- View stored memories.
- Explore previous campaign learnings.
- See audience observations.
- View historical strategy patterns.
- Trigger a reflection.

### Experiments

Allow users to:
- Create an experiment from a recommendation.
- Define a hypothesis.
- Define how success will be measured.
- Add actual campaign results.
- Evaluate the outcome.

### Data Sources

Allow users to:
- Upload files.
- View imported datasets.
- View processing status.
- See validation errors.
- View document processing status.

---

# 13. DATASET FOR THE DEMO

The application must work with real uploaded data.

However, create a synthetic demonstration dataset so that the entire product can be tested immediately.

Use a fictional skincare brand called **GlowUp Skincare**.

Create:

- 30–50 social media posts.
- 200–500 audience comments.
- 3–5 campaigns.
- Engagement metrics for each post.
- Multiple content formats.
- Different audience topics.
- Successful and unsuccessful campaign examples.
- At least two different time periods showing a change in audience interests.

The dataset must be realistic and internally consistent.

Clearly label synthetic data as demonstration data.

Do not present synthetic findings as actual business results.

---

# 14. ERROR HANDLING AND RELIABILITY

Implement:

- API exception handling.
- File validation.
- Invalid data handling.
- LLM timeout handling.
- Rate-limit handling.
- Hindsight connection error handling.
- Database transaction handling.
- Agent execution logging.
- Retry mechanisms where appropriate.
- Clear frontend error messages.

If an AI provider or Hindsight service is unavailable, communicate the failure clearly.

Do not silently replace actual Hindsight operations with fake local memory.

Do not return fabricated analysis when an agent fails.

Every agent execution should have an identifiable run status.

---

# 15. SECURITY REQUIREMENTS

- Hash passwords securely.
- Use authentication and authorization.
- Isolate data by user and brand.
- Validate uploaded files.
- Restrict file size and file type.
- Protect API keys using environment variables.
- Never expose API keys to the frontend.
- Prevent cross-brand data leakage.
- Avoid storing unnecessary personally identifiable information from audience comments.
- Ensure uploaded documents are treated as data, not executable instructions.
- Validate agent outputs before using them in other operations.

---

# 16. PROJECT STRUCTURE

Create a clean, modular folder structure.

```text
audienceiq/
│
├── frontend/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── layouts/
│       ├── dashboard/
│       ├── audience/
│       ├── content/
│       ├── strategy/
│       ├── memory/
│       ├── experiments/
│       ├── services/
│       └── styles/
│
├── backend/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── auth.py
│   │   ├── brands.py
│   │   ├── data.py
│   │   ├── audience.py
│   │   ├── content.py
│   │   ├── agents.py
│   │   ├── memory.py
│   │   └── experiments.py
│   │
│   ├── agents/
│   │   ├── orchestrator.py
│   │   ├── audience_agent.py
│   │   ├── content_agent.py
│   │   ├── strategy_agent.py
│   │   └── evaluator_agent.py
│   │
│   ├── hindsight/
│   │   ├── client.py
│   │   ├── retain.py
│   │   ├── recall.py
│   │   └── reflect.py
│   │
│   ├── rag/
│   │   ├── document_loader.py
│   │   ├── chunking.py
│   │   ├── embeddings.py
│   │   └── retriever.py
│   │
│   ├── analysis/
│   │   ├── metrics.py
│   │   ├── sentiment.py
│   │   ├── topics.py
│   │   └── performance.py
│   │
│   ├── ingestion/
│   │   ├── csv_processor.py
│   │   ├── excel_processor.py
│   │   ├── pdf_processor.py
│   │   └── validator.py
│   │
│   ├── database/
│   │   ├── models.py
│   │   ├── connection.py
│   │   └── migrations/
│   │
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── tests/
│
├── datasets/
│   └── demo/
│
├── documentation/
│
├── .env.example
├── .gitignore
├── README.md
└── docker-compose.yml
```

You may adjust the structure if necessary, but maintain separation between API routes, business logic, agents, analysis, memory and database operations.

---

# 17. DEVELOPMENT PRIORITIES

Build in the following order.

## Phase 1 — Backend Foundation

- Set up Python environment.
- Set up FastAPI.
- Set up PostgreSQL.
- Create database models.
- Implement authentication.
- Implement brand management.
- Configure environment variables.

## Phase 2 — Data Processing

- Implement CSV and Excel uploads.
- Implement PDF and text document processing.
- Build validation.
- Build data cleaning.
- Store processed records.
- Calculate numerical metrics.
- Test ingestion using demo data.

## Phase 3 — AI Analysis

- Implement Audience Intelligence Agent.
- Implement Content Intelligence Agent.
- Implement LLM integration.
- Implement structured outputs.
- Implement evidence grounding.

## Phase 4 — Hindsight and RAG

- Configure actual Hindsight connection.
- Implement retain, recall and reflect.
- Implement brand-specific memory banks.
- Implement document embeddings.
- Implement pgvector retrieval.
- Connect memory and RAG to agents.

## Phase 5 — Agent Orchestration

- Implement the central orchestrator.
- Connect all four agents.
- Implement Strategy Agent.
- Implement Evaluation and Learning Agent.
- Test the full learning cycle.

## Phase 6 — Frontend

- Create the dashboard layout.
- Connect all backend APIs.
- Build required screens.
- Display actual backend data.
- Add loading, empty and error states.
- Add charts where useful.

## Phase 7 — Testing and Demonstration

- Test the full upload-to-analysis workflow.
- Test brand memory isolation.
- Test Hindsight retain and recall.
- Test reflection.
- Test recommendation generation.
- Test outcome evaluation.
- Test that new experiences influence future recommendations.
- Fix bugs and document setup.

---

# 18. MVP ACCEPTANCE CRITERIA

The project is not complete just because the UI looks good.

The following must work:

| Requirement | Expected result |
|---|---|
| User authentication | Users can register and log in |
| Brand management | Users can create separate brand workspaces |
| File upload | CSV, Excel and supported documents can be uploaded |
| Data processing | Files are validated, cleaned and stored |
| Metrics | Engagement calculations are correct |
| Audience agent | Analyses real uploaded comments |
| Content agent | Analyses actual post performance |
| Hindsight retain | Important findings are genuinely stored |
| Hindsight recall | Relevant past experiences can be retrieved |
| Hindsight reflect | Higher-level insights can be generated |
| RAG | Uploaded brand documents can be retrieved |
| Strategy agent | Produces recommendations using current data and relevant memory |
| Evaluation agent | Evaluates actual outcomes |
| Learning loop | New outcomes are retained and used in future decisions |
| Memory screen | Displays actual Hindsight-backed information |
| Frontend | All screens are connected to backend APIs |

## Critical demonstration test

Use the same brand and objective for two strategy requests.

**First request:**

Ask the system to recommend a content strategy before it has accumulated campaign experiences.

**Then:**

1. Upload historical campaign data.
2. Analyse audience behaviour.
3. Generate recommendations.
4. Record which recommendations were implemented.
5. Upload new campaign results.
6. Run the Evaluation Agent.
7. Retain the findings in Hindsight.

**Second request:**

Ask the same strategic question again.

The system should retrieve relevant experiences and produce a recommendation that reflects what it has learned.

The difference must be explainable through actual retrieved memories and evidence.

This is the central proof that EnQue genuinely learns through experience.

---

# 19. OUT OF SCOPE FOR MVP

Do not waste development time on:

- Automatic Instagram publishing.
- Direct Instagram scraping.
- Full social media account integrations.
- Automated scheduling.
- Advanced multi-tenant enterprise billing.
- Complex permission hierarchies.
- Mobile applications.
- Unnecessary animations.
- Elaborate frontend visualizations.

These can be considered for future versions.

---

# 20. FINAL INSTRUCTIONS FOR ANTIGRAVITY

Build EnQue as a fully functional, modular, backend-driven AI application.

Follow these rules throughout development:

1. **Backend first.** Prioritize working data pipelines, database operations, agents, Hindsight and RAG over frontend polish.

2. **Real integrations only.** Use actual Groq API calls and the actual Hindsight SDK. Never create fake integrations or mock successful responses.

3. **No hardcoded intelligence.** Insights, recommendations, metrics and memories must be generated from actual stored or uploaded data.

4. **Separate responsibilities.** Keep agents, orchestration, data analysis, RAG, Hindsight and API routes modular.

5. **Hindsight is essential.** The application must demonstrate persistent memory and learning across multiple interactions and sessions.

6. **Evidence-based outputs.** Recommendations must be traceable to current data, retrieved documents or relevant memories.

7. **Simple frontend.** Build only the screens required to access and understand the system. Prioritize clarity and usability.

8. **Complete implementation.** Do not stop at a prototype, static dashboard, wireframe or collection of disconnected screens.

9. **Test continuously.** Test each backend module before integrating it with the next module.

10. **Document everything.** Include setup instructions, environment variables, database setup, Hindsight configuration, API documentation and demo instructions.

11. **No fake completion.** If an external API key, database or service is missing, clearly identify the dependency and provide setup instructions instead of pretending it works.

12. **Preserve working code.** Do not overwrite functioning modules unnecessarily while implementing new features.

### Expected final deliverable

A working EnQue application with:

- Functional frontend.
- Functional FastAPI backend.
- PostgreSQL database.
- Data ingestion and processing.
- Four specialized AI agents.
- Central agent orchestration.
- Real Hindsight persistent memory.
- RAG document retrieval.
- Evidence-based strategy generation.
- Campaign outcome evaluation.
- Continuous learning loop.
- Demo dataset.
- Setup documentation.
- Test coverage.

**The ultimate objective is to demonstrate a real AI system that accumulates business experience, remembers previous outcomes, understands changing audience behaviour and uses that knowledge to generate increasingly context-aware marketing strategies.**