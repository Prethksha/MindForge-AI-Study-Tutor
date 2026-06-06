import streamlit as st
from ai_engine import generate_notes
from pdf_generator import create_pdf

# Page Config
st.set_page_config(
    page_title="AI Study Companion",
    page_icon="📚",
    layout="wide"
)

# Title
st.title("📚 AI Study Companion")
st.write("Generate smart notes based on your learning level and study goals.")

# Sidebar
st.sidebar.header("⚙️ Study Preferences")

level = st.sidebar.selectbox(
    "Select Learning Level",
    [
        "🌱 Beginner",
        "📚 Student",
        "🎓 Advanced Learner",
        "⚡ Last-Minute Revision",
        "💼 Professional"
    ]
)

style = st.sidebar.selectbox(
    "Select Notes Style",
    [
        "📖 Detailed Notes",
        "📝 Summary",
        "⚡ Revision Notes",
        "🧠 Flashcards",
        "🎯 Interview Prep"
    ]
)

mood = st.sidebar.selectbox(
    "Current Mood",
    [
        "😊 Motivated",
        "😐 Neutral",
        "😴 Tired",
        "😰 Stressed",
        "🔥 Need Motivation"
    ]
)

# Main Section
topic = st.text_input(
    "📌 Enter Topic",
    placeholder="Example: Machine Learning, Photosynthesis, JavaScript Closures...",
    key="main_topic_input"
)

generate = st.button("🚀 Generate Notes")

if generate:
    if not topic:
        st.warning("Please enter a topic.")
    else:
        prompt = f"""
        Topic: {topic}
        Learning Level: {level}
        Notes Style: {style}
        Mood: {mood}
        """

        with st.spinner("Generating notes..."):
            result = generate_notes(prompt)

        st.success("Notes Generated Successfully!")

        st.markdown("## 📖 Generated Notes")
        st.write(result)

        pdf_file = create_pdf(result)

        with open(pdf_file, "rb") as file:
         st.download_button(
              label="📄 Download Notes as PDF",
              data=file,
              file_name="study_notes.pdf",
              mime="application/pdf"
    )