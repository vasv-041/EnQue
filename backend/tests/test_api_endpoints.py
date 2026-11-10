"""End-to-end HTTP API Integration Test Suite for EnQue.
Tests all endpoints using FastAPI TestClient to simulate live HTTP interactions:
- Auth: Register & Login (JWT token generation)
- Brand: Creation with auto Hindsight isolated bank assignment
- Ingestion: Uploading posts.csv & comments.csv via multipart form
- Content: Analytics & Top-performing calculation
- Audience: Sentiment, topics & questions breakdown
- Memory: Hindsight bank overview & recall
- Strategy & Chat: Central Orchestrator workflow
- Experiments: Creation & Evaluation learning loop
"""

import os
import sys

# Ensure backend package can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_full_system_e2e():
    print("\n" + "=" * 50)
    print("[*] 1. Testing Health Endpoint")
    print("=" * 50)
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"
    print("[OK] Health check passed:", res.json())

    print("\n" + "=" * 50)
    print("[*] 2. Testing Authentication (Register & Login)")
    print("=" * 50)
    user_email = "tester_e2e@enque.ai"
    reg_res = client.post("/api/auth/register", json={
        "name": "Integration Tester",
        "email": user_email,
        "password": "Password123!"
    })
    # If already registered in dev DB, login directly
    if reg_res.status_code == 400 and "already registered" in reg_res.text:
        print("[INFO] User already registered. Proceeding to login.")
    else:
        assert reg_res.status_code in (200, 201)
        print("[OK] Registration succeeded")

    login_res = client.post("/api/auth/login", json={
        "email": user_email,
        "password": "Password123!"
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    assert token is not None
    headers = {"Authorization": f"Bearer {token}"}
    print("[OK] Login succeeded, JWT acquired")

    print("\n" + "=" * 50)
    print("[*] 3. Testing Brand Workspace & Isolated Memory Bank Creation")
    print("=" * 50)
    brand_res = client.post("/api/brands", json={
        "brand_name": "Lumina Skincare Labs",
        "industry": "Clinical Cosmeceuticals",
        "description": "Evidence-backed skincare for acne-prone skin",
        "target_audience": "Millennial skincare enthusiasts",
        "brand_voice": "Clinical, educational and reassuring",
        "objectives": "Increase authority and educational engagement"
    }, headers=headers)
    assert brand_res.status_code in (200, 201)
    brand = brand_res.json()
    brand_id = brand["id"]
    bank_id = brand["hindsight_bank_id"]
    print(f"[OK] Brand created: ID={brand_id}, Hindsight Bank ID='{bank_id}'")

    print("\n" + "=" * 50)
    print("[*] 4. Testing Multi-Format Data Ingestion (CSV Upload)")
    print("=" * 50)
    posts_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "datasets", "demo", "posts.csv"))
    comments_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "datasets", "demo", "comments.csv"))

    assert os.path.exists(posts_path), f"Missing demo posts file at {posts_path}"
    assert os.path.exists(comments_path), f"Missing demo comments file at {comments_path}"

    with open(posts_path, "rb") as f:
        up_posts = client.post(
            "/api/data/upload",
            data={"brand_id": brand_id, "dataset_type": "posts"},
            files={"file": ("posts.csv", f, "text/csv")},
            headers=headers
        )
    assert up_posts.status_code == 200
    print("[OK] Posts uploaded:", up_posts.json())

    with open(comments_path, "rb") as f:
        up_comments = client.post(
            "/api/data/upload",
            data={"brand_id": brand_id, "dataset_type": "comments"},
            files={"file": ("comments.csv", f, "text/csv")},
            headers=headers
        )
    assert up_comments.status_code == 200
    print("[OK] Comments uploaded:", up_comments.json())

    files_list = client.get(f"/api/data/files?brand_id={brand_id}", headers=headers)
    assert files_list.status_code == 200
    f_data = files_list.json()
    print(f"[OK] Data summary verified: {f_data['total_posts']} posts, {f_data['total_comments']} comments")
    assert f_data["total_posts"] > 0
    assert f_data["total_comments"] > 0

    print("\n" + "=" * 50)
    print("[*] 5. Testing Content Analytics & Performance Calculations")
    print("=" * 50)
    content_res = client.get(f"/api/content/analytics?brand_id={brand_id}", headers=headers)
    assert content_res.status_code == 200
    c_data = content_res.json()
    print(f"[OK] Content Analytics: Avg Eng Rate = {c_data['avg_engagement_rate']}%, Avg Save Rate = {c_data['avg_save_rate']}%")

    top_res = client.get(f"/api/content/top-performing?brand_id={brand_id}&limit=3", headers=headers)
    assert top_res.status_code == 200
    print(f"[OK] Top {len(top_res.json())} performing posts fetched successfully")

    print("\n" + "=" * 50)
    print("[*] 6. Testing Audience Intelligence Extraction")
    print("=" * 50)
    aud_res = client.get(f"/api/audience/insights?brand_id={brand_id}", headers=headers)
    assert aud_res.status_code == 200
    a_data = aud_res.json()
    print(f"[OK] Audience Insights: Sentiment = {a_data['overall_sentiment']}, Topics = {a_data['dominant_topics'][:4]}")

    print("\n" + "=" * 50)
    print("[*] 7. Testing Central Orchestrator & Strategy Generation")
    print("=" * 50)
    strat_res = client.post("/api/agents/strategy", json={
        "brand_id": brand_id,
        "query": "Develop an educational strategy for next quarter"
    }, headers=headers)
    assert strat_res.status_code == 200
    s_data = strat_res.json()
    recs = s_data.get("recommendations", [])
    print(f"[OK] Orchestrator generated {len(recs)} strategic recommendations")
    assert len(recs) > 0
    print(f"     Top Rec: {recs[0]['recommendation']}")
    print(f"     Evidence Grounding: {recs[0].get('historical_evidence', 'N/A')}")

    print("\n" + "=" * 50)
    print("[*] 8. Testing Orchestrator Chat Endpoint")
    print("=" * 50)
    chat_res = client.post("/api/agents/chat", json={
        "brand_id": brand_id,
        "message": "Which format gives us the highest save rate?"
    }, headers=headers)
    assert chat_res.status_code == 200
    chat_data = chat_res.json()
    print(f"[OK] Agent Chat responded: {chat_data.get('agent_response')[:100]}...")

    print("\n" + "=" * 50)
    print("[*] 9. Testing Evaluation Agent & Continuous Learning Retention")
    print("=" * 50)
    # Create an experiment based on recommendation
    exp_res = client.post("/api/experiments", json={
        "brand_id": brand_id,
        "recommendation_id": recs[0].get("id"),
        "hypothesis": recs[0].get("recommendation"),
        "measurement_method": "Save rate >= 8.5%"
    }, headers=headers)
    assert exp_res.status_code == 200
    exp_id = exp_res.json()["id"]

    eval_res = client.post(f"/api/experiments/{exp_id}/evaluate", json={
        "actual_results": {
            "save_rate": 9.4,
            "engagement_rate": 24.5,
            "reach_growth": 18.0
        }
    }, headers=headers)
    assert eval_res.status_code == 200
    ev_data = eval_res.json()
    print(f"[OK] Experiment evaluated: Evaluation = {ev_data.get('evaluation')}")
    print(f"     Learning Summary = {ev_data.get('learning_summary')}")
    print(f"     Hindsight Retained = {ev_data.get('hindsight_retained')}")

    # Verify Hindsight Memory Overview
    mem_res = client.get(f"/api/memory/overview?brand_id={brand_id}", headers=headers)
    assert mem_res.status_code == 200
    m_data = mem_res.json()
    print(f"[OK] Hindsight Bank Overview: {m_data['total_campaign_learnings']} learnings stored in {m_data['hindsight_bank_id']}")
    assert m_data["total_campaign_learnings"] > 0

    print("\n" + "=" * 50)
    print("[*] ALL API ENDPOINTS & FLOWS VERIFIED SUCCESSFULLY")
    print("=" * 50)

if __name__ == "__main__":
    test_full_system_e2e()

