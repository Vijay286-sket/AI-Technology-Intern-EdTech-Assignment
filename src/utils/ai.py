from __future__ import annotations

from typing import Optional


def ai_answer(query: str, api_key: Optional[str]) -> str:
    """Answer using Gemini if key is provided; else return empty string.
    Keeps failures silent to maintain simple UX.
    """
    if not api_key:
        return ""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        prompt = (
            "You are a helpful assistant answering FAQs about a women's leadership program "
            "called Iron Lady. Be concise and factual. If unsure, say you are unsure.\n\n"
            f"User question: {query}"
        )
        model = genai.GenerativeModel("gemini-1.5-flash")
        resp = model.generate_content(prompt)
        return (resp.text or "").strip()
    except Exception:
        return ""


def ai_short_task(api_key: Optional[str]) -> str:
    """Generate one short, practical task using Gemini."""
    if not api_key:
        return ""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        prompt = (
            "Suggest one short, practical task to improve leadership or productivity. "
            "Return only the task phrase."
        )
        model = genai.GenerativeModel("gemini-1.5-flash")
        resp = model.generate_content(prompt)
        return (resp.text or "").strip()
    except Exception:
        return ""
