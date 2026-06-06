import streamlit as st
from ai_engine import generate_notes
from pdf_generator import create_pdf

if "final_notes" not in st.session_state:
    st.session_state.final_notes = None

# PAGE CONFIG
st.set_page_config(page_title="MindForge AI", page_icon="⚡", layout="wide")


# SESSION STATE (CHAT MEMORY)
if "chat" not in st.session_state:
    st.session_state.chat = []

# PREMIUM UI STYLING
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0f172a, #020617);
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0b1220;
}

/* Chat bubbles */
.stChatMessage {
    border-radius: 12px;
    padding: 10px;
}

/* Title gradient */
.title {
    text-align: center;
    font-size: 44px;
    font-weight: 800;
    background: linear-gradient(90deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 20px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)


# HEADER
st.markdown('<div class="title">MindForge AI ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your AI-powered Study Tutor for smart learning, notes & revision</div>', unsafe_allow_html=True)


# SIDEBAR SETTINGS
st.sidebar.header("⚙️ Study Preferences")
st.sidebar.markdown("---")
st.sidebar.subheader("📚 Study Tools")

create_notes = st.sidebar.button(
    "📚 Create Final Study Notes"
)

level = st.sidebar.selectbox(
    "Learning Level",
    ["Beginner 🌱", "Student 📚", "Advanced 🎓", "Revision ⚡", "Professional 💼"]
)

style = st.sidebar.selectbox(
    "Notes Style",
    ["Detailed Notes 📖", "Summary 📝", "Revision ⚡", "Flashcards 🧠", "Interview Prep 🎯"]
)

mood = st.sidebar.selectbox(
    "Current Mood",
    ["Motivated 😊", "Neutral 😐", "Tired 😴", "Stressed 😰", "Need Motivation 🔥"]
)
clear_chat = st.sidebar.button("🗑 New Chat")
if clear_chat:
    st.session_state.chat = []
    st.session_state.final_notes = None
    st.rerun()

# CHAT DISPLAY
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# USER INPUT (CHAT STYLE)
user_input = st.chat_input("Ask your study question...")

# AI RESPONSE LOGIC
if user_input:

    # Save user message
    st.session_state.chat.append({
        "role": "user",
        "content": user_input
    })

    # Strong AI prompt (important upgrade)
    prompt = f"""
You are MindForge AI, an expert AI study tutor.

Your job:
- Teach concepts clearly
- Use examples
- Make learning easy
- Adjust explanation based on student level

Student Info:
Level: {level}
Style: {style}
Mood: {mood}

Question:
{user_input}
"""

    with st.spinner("Thinking..."):
        response = generate_notes(prompt)

    # Save AI response
    st.session_state.chat.append({
        "role": "assistant",
        "content": response
    })


if create_notes:

    conversation = ""

    for msg in st.session_state.chat:

        role = "Student" if msg["role"] == "user" else "Tutor"

        conversation += f"{role}: {msg['content']}\n\n"

    notes_prompt = f"""
Create professional study notes from the following conversation.

Include:

1. Topic Overview
2. Key Concepts
3. Detailed Explanation
4. Examples
5. Important Points
6. Quick Revision
7. Summary

Conversation:

{conversation}
"""

    with st.spinner("Creating study notes..."):

        final_notes = generate_notes(notes_prompt)

    st.session_state.final_notes = final_notes

if st.session_state.final_notes:

    st.markdown("---")
    st.subheader("📚 Final Study Notes")

    st.markdown(st.session_state.final_notes)
if st.session_state.final_notes:

    pdf_file = create_pdf(st.session_state.final_notes)

    with open(pdf_file, "rb") as file:

        st.download_button(
            label="📄 Download Study Notes PDF",
            data=file,
            file_name="MindForge_Study_Notes.pdf",
            mime="application/pdf"
        )