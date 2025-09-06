# Iron Lady – MVP Apps (Streamlit)

Two tiny, clear MVPs built with Python + Streamlit:

- FAQ Chatbot for Iron Lady (hardcoded responses + optional Gemini fallback)
- Simple To‑Do CRUD manager (create, view, mark done, delete) with a small AI suggestion bonus

This is intentionally minimal, beginner-friendly, and easy to review.

## 1) Requirements

- Python 3.9+
- Optional: Google Gemini API key (for AI enhancements)

Install dependencies:

```bash
pip install -r requirements.txt
```

## 2) Setup .env for Gemini

1. Copy `.env.example` to `.env`.
2. Paste your Gemini key:

```
GEMINI_API_KEY=your_key_here
```

On Windows PowerShell, to set only for the current session (alternative):

```powershell
$env:GEMINI_API_KEY="your_key_here"
```

## 3) Run the app

```bash
streamlit run app.py
```

Streamlit will open in your browser (usually http://localhost:8501).

## 4) Features

### FAQ Chatbot
- Hardcoded answers for common questions about Iron Lady programs
- Optional AI fallback with Gemini (toggle in sidebar)
- Clear chat button

### To‑Do Manager (CRUD)
- Add tasks (Create)
- View tasks list (Read)
- Mark as done or edit (Update)
- Delete tasks (Delete)
- Bonus: Suggest a task locally (no AI) or via Gemini
- Bonus: Summarize completed tasks button (local)

## 5) Project Files

- `app.py` – single Streamlit app with two pages (FAQ Chatbot and To‑Do Manager)
- `requirements.txt` – minimal dependencies (Streamlit, google-generativeai, python-dotenv)
- `.env.example` – template for your environment variables
- `README.md` – this file

## 6) Notes

- These are MVP-level prototypes, not production software.
- Clean, concise code; no external databases; uses `st.session_state` to persist during a session.
- If AI calls fail or a key is missing, the app gracefully falls back to local logic.
