
# MultiLayer GPT Manager API - Deployment Guide

## 📦 Contents
- insight_memory_api.py  --> API Code (Flask)
- Insights_Sample.json  --> Memory Storage (JSON)
- requirements.txt      --> Dependencies for deployment

---

## 🚀 Deployment on Render (Free):
1. Go to [https://render.com/](https://render.com/) and sign up/login.
2. Create a new Web Service.
3. Connect to your GitHub repository or upload this code manually.
4. Set the Start Command to: `python insight_memory_api.py`
5. Select Free Plan.
6. Your API will be publicly accessible at: `https://<your-subdomain>.onrender.com`

---

## 🚀 Deployment on Replit (Free):
1. Go to [https://replit.com/](https://replit.com/) and sign up/login.
2. Create a new Repl -> Select "Python".
3. Upload all these files.
4. Click "Run".
5. Get your public URL from the "Webview" section.

---

## ✅ API Endpoints:
- `GET /insights`  --> Retrieve all insights.
- `POST /insights`  --> Add new insight.
- `PUT /insights/<insight_id>`  --> Update an existing insight.
- `DELETE /insights/<insight_id>`  --> Delete an insight by ID.

---

## 📋 JSON Example for POST:
```json
{
    "id": "insight-1001",
    "date": "2025-05-11",
    "type": "Bot",
    "summary": "Sample insight from deployed API.",
    "relevance_to": "General",
    "confidence": "High",
    "significance": "5",
    "readiness": "New",
    "iteration_count": "1",
    "origin": "UserInput",
    "linked_bots": "TaskManager",
    "tags": "Productivity",
    "notes": "Generated via API"
}
```
