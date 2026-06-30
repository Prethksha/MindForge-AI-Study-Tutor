import streamlit as st
from ai_engine import generate_notes
from pdf_generator import create_pdf

if "final_notes" not in st.session_state:
    st.session_state.final_notes = None

# PAGE CONFIG
st.set_page_config(page_title="MindForge AI", page_icon="⚡", layout="wide")
st.error("🚨 THIS IS MINDFORGE AI TEST")
st.info("💡 Tip: If AI is busy, just resend your question.")

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

# WELCOME SCREEN
if len(st.session_state.chat) == 0:

    st.markdown(
    """
    <div style='
        background: rgba(255,255,255,0.05);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-top: 20px;
    '>

    <h1 style='
        color:#8ea2ff;
        font-size:48px;
        margin-bottom:10px;
    '>
    ⚡ Welcome to MindForge AI
    </h1>

    <h4 style='color:#94a3b8;'>
    Learn Faster • Revise Smarter • Understand Better
    </h4>

    <br>

    <p style='font-size:18px;'>
    📚 Study Notes &nbsp;&nbsp;
    🧠 Concept Explanations &nbsp;&nbsp;
    ⚡ Quick Revision &nbsp;&nbsp;
    🎯 Interview Prep
    </p>

    <br>

    <p style='color:#cbd5e1;'>
    Ask any question and start learning instantly.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("### Quick Start")
col1, col2 = st.columns(2)

with col1:
    if st.button("📚 Generate Notes"):
        st.session_state.quick_prompt = "Generate detailed notes on Python"

with col2:
    if st.button("🎯 Interview Preparation"):
        st.session_state.quick_prompt = "Help me prepare for technical interviews"

# USER INPUT (CHAT STYLE)
user_input = st.chat_input("Ask your question...")

if not user_input and "quick_prompt" in st.session_state:
    user_input = st.session_state.quick_prompt
    del st.session_state.quick_prompt
# AI RESPONSE LOGIC
if user_input:

    # Save user message
    st.session_state.chat.append({
        "role": "user",
        "content": user_input
    }
    )

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
    st.rerun()

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

    with st.spinner("🧠 MindForge is thinking..."):
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