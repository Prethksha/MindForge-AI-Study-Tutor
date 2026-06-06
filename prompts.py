def get_prompt(topic, level, style, mood):
    return f"""
You are an AI Study Companion.

TOPIC: {topic}
LEVEL: {level}
STYLE: {style}
MOOD: {mood}

Generate:
1. Simple explanation
2. Structured notes
3. Summary
4. 5 MCQ quiz
5. Motivation message

Keep output clean and readable.
"""