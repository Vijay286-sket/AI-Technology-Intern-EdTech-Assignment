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

---

## 7) Deploy to Streamlit Community Cloud (Free)

You can deploy this repo in a few clicks.

1. Go to: https://share.streamlit.io
2. Connect your GitHub and select this repo:
   - Repository: `Vijay286-sket/AI-Technology-Intern-EdTech-Assignment`
   - Branch: `main`
   - Main file path: `app.py`
3. In the app settings, open “Secrets” and add:

```
GEMINI_API_KEY=your_key_here
```

4. Save and deploy. The app will build and give you a public URL.

Optional: add this link here once live (replace the placeholder):

- Live App: https://share.streamlit.io/your-deployment-url

### Tips
- If build fails due to dependency versions, ensure the platform uses Python 3.9+ and the included `requirements.txt`.
- Secrets are not stored in the repo—only in Streamlit Cloud.
