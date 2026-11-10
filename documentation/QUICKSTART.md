# EnQue Quickstart & Demonstration Guide

This guide provides instructions to run, demo, and verify **EnQue** across all 5 continuous learning stages.

---

## ⚡ Quick Start

### 1. Start the Backend API
In your primary terminal:
```powershell
# Set root pythonpath
$env:PYTHONPATH="."

# Launch FastAPI development server
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive API documentation will be available at: **[http://localhost:8000/docs](http://localhost:8000/docs)**.

### 2. Start the Frontend Dashboard
In a secondary terminal:
```powershell
cd frontend
npm run dev
```
Open **[http://localhost:5173](http://localhost:5173)** in your browser.

---

## 🎭 Demonstrating the Platform Walkthrough

### Step 1: Sign in & Workspace Setup
1. On the authentication screen, the demo credentials (`demo@enque.ai` / `demo1234`) are pre-populated. Click **Sign In** (or click Register if using a clean database).
2. The **Brand Setup** screen comes pre-filled with **GlowUp Skincare** details. Click **Create Brand Workspace**.
3. The system assigns an isolated Hindsight memory bank: `bank_<id>_glowup_skincare`.

### Step 2: Seed the Demo Dataset
1. The **Data Loader** appears with the GlowUp Skincare dataset (25 posts across Reels, Carousels, and Single Images, plus 30 customer comments).
2. Click **Load Demo Data**. The application uploads the files to `/api/data/upload` and redirects directly to the Executive Dashboard.

### Step 3: Explore Intelligence & Analytics
1. **Overview Screen**: Inspect aggregate metrics (Avg Engagement Rate: ~22.1%, Avg Save Rate: ~9.0%), format-level comparisons, and overall positive audience sentiment.
2. **Audience Insights Screen**: Review discussion topics (`#barrier`, `#niacinamide`, `#purging`), customer inquiries, and flagged product pain points.
3. **Content Analytics Screen**: Compare Reel vs Carousel vs Single Image performance.

### Step 4: The 5-Stage Continuous Learning Demonstration
1. Go to the **AI Strategy** tab.
2. Click **Generate Strategy**: The orchestrator triggers Audience & Content agents and returns recommendations.
   - Note the **Initial Confidence** (`Medium`) and baseline hypothesis framing.
3. Go to the **Experiments** tab:
   - Observe the created hypothesis.
   - When real campaign performance data comes in (e.g. Save Rate = 9.4%), the **Evaluation Agent** compares actual vs. expected results, generates an experiential summary, and commits it into **Hindsight persistent memory**.
4. Go to the **AI Memory** tab:
   - View the retained learning committed to the isolated bank.
5. Return to **AI Strategy** and click **Generate Strategy** again:
   - The Strategy Agent queries Hindsight memory, retrieves the past successful outcome, and generates an updated strategy.
   - Note the updated **Confidence Level** (`High (Backed by verified experiential outcome)`) and explicit citation of the previous experiment outcome.

---

## 🧪 Automated Verification
To verify the complete 8-step lifecycle programmatically:
```powershell
$env:PYTHONPATH="."
python backend/tests/test_sync_learning_cycle.py
```
All 8 verification checkpoints will execute and report `[OK]`.

