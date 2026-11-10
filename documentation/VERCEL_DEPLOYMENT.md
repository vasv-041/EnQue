# Vercel Deployment Guide for EnQue

EnQue is configured for unified full-stack deployment on Vercel:
- **Frontend**: React + Vite built via `@vercel/static-build`
- **Backend API**: FastAPI serverless functions via `@vercel/python` routed to `/api/*`, `/health`, and `/docs`

---

## Method 1: Deploy via GitHub (Recommended)

1. **Push your code to a GitHub repository**:
   ```powershell
   git remote add origin https://github.com/<your-username>/enque.git
   git branch -M main
   git push -u origin main
   ```

2. **Import into Vercel**:
   - Go to [vercel.com/new](https://vercel.com/new).
   - Select your `enque` repository.
   - Vercel will automatically detect `vercel.json`.

3. **Configure Environment Variables in Vercel Dashboard**:
   Under **Project Settings > Environment Variables**, add:
   - `GROQ_API_KEY`: `your-groq-api-key-here`
   - `GROQ_BASE_URL`: `https://api.groq.com/openai/v1`
   - `PRIMARY_LLM_MODEL`: `openai/gpt-oss-120b`
   - `FALLBACK_LLM_MODEL`: `qwen/qwen3.8-27b`
   - `HINDSIGHT_API_KEY`: `hsk_80eba63bced1d44577f6a63c3de31ea2_bc6cee42081a5a9b`
   - `HINDSIGHT_BASE_URL`: `https://api.hindsight.ai/v1`
   - `JWT_SECRET_KEY`: (any random secure string)
   - `DATABASE_URL`: `sqlite:////tmp/enque.db` (or a hosted PostgreSQL connection string such as Neon, Supabase, or Vercel Postgres)

4. **Click Deploy**:
   - Vercel builds the React frontend and packages FastAPI as serverless Python functions.

---

## Method 2: Deploy via Vercel CLI

1. **Install Vercel CLI globally**:
   ```powershell
   npm install -g vercel
   ```

2. **Authenticate with Vercel**:
   ```powershell
   vercel login
   ```

3. **Deploy from project root**:
   ```powershell
   vercel
   ```
   Follow the prompts to link the project and deploy preview.

4. **Deploy to Production**:
   ```powershell
   vercel --prod
   ```

---

## Project Routing Architecture on Vercel

Configured in [`vercel.json`](file:///c:/Users/CNR/Desktop/v/Project_Ideas/HackWithBangalore4.0/vercel.json):
- `/api/*` ➔ Serverless FastAPI backend entry point [`api/index.py`](file:///c:/Users/CNR/Desktop/v/Project_Ideas/HackWithBangalore4.0/api/index.py)
- `/health` ➔ FastAPI health check
- `/docs` ➔ OpenAPI Swagger documentation
- `/*` ➔ Static React + Vite frontend SPA (`frontend/dist/`)

