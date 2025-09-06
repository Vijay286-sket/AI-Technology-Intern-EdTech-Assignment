FAQS = {
    "What is Iron Lady?": "Iron Lady is a leadership development platform focused on empowering women with practical leadership skills, confidence, and career acceleration.",
    "What programs do you offer?": "We offer leadership bootcamps, executive coaching, confidence-building workshops, and cohort-based programs tailored for different career stages.",
    "Who can join?": "Professionals, aspiring leaders, and women returning to the workforce—anyone looking to build leadership capabilities is welcome.",
    "How long are the programs?": "Programs range from short 2-hour workshops to 8–12 week cohort-based courses.",
    "Do you provide certificates?": "Yes, participants receive a certificate of completion for eligible programs.",
    "Is there a community?": "Yes, we provide an active peer community, mentorship, and alumni network for continued growth.",
}

SIMILARITY_KEYS = [k.lower() for k in FAQS.keys()]


def simple_match(query: str) -> str:
    q = (query or "").strip().lower()
    if not q:
        return "Please ask a question about Iron Lady's leadership programs."

    if q in FAQS:  # exact
        return FAQS[q]

    for key in SIMILARITY_KEYS:  # fuzzy contains
        if key in q or q in key:
            return FAQS[[k for k in FAQS.keys() if k.lower() == key][0]]

    hints = [
        ("program", "We offer leadership bootcamps, executive coaching, and workshops."),
        ("certificate", "Yes, certificates are provided for eligible programs."),
        ("duration", "Programs range from 2 hours to 8–12 weeks."),
        ("community", "Yes, we provide an active community, mentorship, and alumni network."),
        ("join", "Professionals and aspiring leaders can join; see our cohorts and workshops."),
    ]
    for word, ans in hints:
        if word in q:
            return ans

    return "I don't have that in my FAQs. Toggle 'Use AI if available' to try an AI answer or ask another question."
