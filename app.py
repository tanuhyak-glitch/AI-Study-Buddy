import streamlit as st
import json
import os
from datetime import datetime
from groq import Groq

# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

HISTORY_FILE = "study_history.json"


# =========================================================
# STYLING
# =========================================================

st.markdown("""
<style>
    .stApp {
        background-color: #f5f7fb;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    .hero {
        padding: 28px;
        border-radius: 18px;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        margin-bottom: 20px;
    }

    .hero h1 {
        color: white;
        font-size: 36px;
    }

    .hero p {
        color: #e0e7ff;
        font-size: 17px;
    }

    .stat-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 10px;
    }

    .stat-title {
        color: #6b7280;
        font-size: 14px;
    }

    .stat-value {
        color: #111827;
        font-size: 28px;
        font-weight: bold;
    }

    .feature-card {
        background: white;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        min-height: 150px;
    }

    div.stButton > button {
        border-radius: 10px;
        min-height: 42px;
        font-weight: 600;
    }

    div[data-testid="stExpander"] {
        background-color: white;
        border-radius: 10px;
    }

    h1, h2, h3 {
        color: #111827;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# GROQ AI
# =========================================================

def get_client():
    api_key = st.secrets.get("GROQ_API_KEY")

    if not api_key:
        st.error("Groq API key not found. Add it to .streamlit/secrets.toml")
        st.stop()

    return Groq(api_key=api_key)


def ask_ai(prompt, system_prompt="You are a helpful educational AI assistant."):
    client = get_client()

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


# =========================================================
# STUDY HISTORY
# =========================================================

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_history(entry):
    history = load_history()
    history.append(entry)

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False)


def create_history_entry(entry_type, topic, content):
    return {
        "type": entry_type,
        "topic": topic,
        "content": content,
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M")
    }


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:
    st.markdown("## 🎓 AI Study Buddy")
    st.caption("Your personal AI learning assistant")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📖 Topic Explainer",
            "📝 Notes Summarizer",
            "🧠 Interactive Quiz",
            "📚 Study History"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### Your Study Toolkit")
    st.caption("Learn • Summarize • Practice • Revise")

    st.divider()
    st.caption("Built with Python, Streamlit & Groq AI")


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    history = load_history()

    explanations = [
        item for item in history
        if item.get("type") == "Topic Explanation"
    ]

    summaries = [
        item for item in history
        if item.get("type") == "Notes Summary"
    ]

    quizzes = [
        item for item in history
        if item.get("type") == "Quiz Result"
    ]

    total_quizzes = len(quizzes)

    average_score = (
        sum(item.get("percentage", 0) for item in quizzes) / total_quizzes
        if total_quizzes > 0
        else 0
    )

    st.markdown("""
    <div class="hero">
        <h1>Welcome to AI Study Buddy 🎓</h1>
        <p>Your personal AI-powered space to learn smarter,
        summarize notes, practice quizzes and track your progress.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📊 Your Learning Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-title">Topics Explained</div>
            <div class="stat-value">{len(explanations)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-title">Notes Summarized</div>
            <div class="stat-value">{len(summaries)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-title">Quizzes Completed</div>
            <div class="stat-value">{total_quizzes}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-title">Average Quiz Score</div>
            <div class="stat-value">{average_score:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("✨ What can you do?")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📖 Topic Explainer</h3>
            <p>Understand difficult concepts using simple
            explanations, examples and programming illustrations.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h3>🧠 Interactive Quiz</h3>
            <p>Test your understanding with AI-generated
            questions and instant feedback.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📝 Notes Summarizer</h3>
            <p>Convert lengthy notes into concise,
            organized revision material.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h3>📚 Study History</h3>
            <p>Review your previous explanations,
            summaries and quiz results.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("🕒 Recent Activity")

    if history:
        for item in reversed(history[-5:]):
            st.markdown(
                f"**{item.get('type', 'Activity')}** — "
                f"{item.get('topic', 'Untitled')} "
                f"({item.get('timestamp', '')})"
            )
    else:
        st.info("Your activity will appear here after you start studying.")

    st.caption("Select a feature from the sidebar to get started.")


# =========================================================
# TOPIC EXPLAINER
# =========================================================

elif page == "📖 Topic Explainer":

    st.title("📖 Topic Explainer")
    st.caption("Understand complex topics in simple language.")

    topic = st.text_input(
        "What topic do you want to learn?",
        placeholder="Example: Recursion, DBMS normalization, Neural Networks..."
    )

    level = st.selectbox(
        "Explanation level",
        ["Beginner", "Intermediate", "Exam preparation"]
    )

    if st.button("✨ Explain Topic", type="primary"):

        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Generating your explanation..."):

                prompt = f"""
Explain the topic: {topic}

Explanation level: {level}

Organize the response using these sections:

1. Simple Definition
2. How It Works
3. Real-Life Analogy
4. Example
5. Programming Example (if applicable)
6. Important Points to Remember
7. Common Mistakes (if applicable)

Use clear language, structured headings and examples.
"""

                try:
                    explanation = ask_ai(prompt)

                    st.session_state.last_explanation = explanation
                    st.session_state.last_explanation_topic = topic

                except Exception as e:
                    st.error(f"AI request failed: {e}")

    if "last_explanation" in st.session_state:
        st.divider()

        st.subheader(
            f"📘 Learning: {st.session_state.last_explanation_topic}"
        )

        st.markdown(st.session_state.last_explanation)

        if st.button("💾 Save Explanation to History"):
            save_history(
                create_history_entry(
                    "Topic Explanation",
                    st.session_state.last_explanation_topic,
                    st.session_state.last_explanation
                )
            )
            st.success("Saved to Study History!")


# =========================================================
# NOTES SUMMARIZER
# =========================================================

elif page == "📝 Notes Summarizer":

    st.title("📝 Notes Summarizer")
    st.caption("Turn lengthy notes into easy revision material.")

    notes = st.text_area(
        "Paste your notes here",
        height=250,
        placeholder="Paste your class notes, textbook content or study material..."
    )

    summary_style = st.selectbox(
        "Summary style",
        [
            "Exam revision notes",
            "Short summary",
            "Detailed summary",
            "Bullet points"
        ]
    )

    if st.button("✨ Summarize Notes", type="primary"):

        if not notes.strip():
            st.warning("Please paste your notes first.")
        else:
            with st.spinner("Summarizing your notes..."):

                prompt = f"""
Summarize the following study notes.

Style: {summary_style}

Requirements:
- Preserve important concepts.
- Use headings.
- Explain key definitions.
- Include important points.
- Make it easy to revise.
- Do not invent information that is not supported by the notes.

NOTES:
{notes}
"""

                try:
                    summary = ask_ai(prompt)

                    st.session_state.last_summary = summary

                except Exception as e:
                    st.error(f"AI request failed: {e}")

    if "last_summary" in st.session_state:
        st.divider()
        st.subheader("📑 Your Summary")

        st.markdown(st.session_state.last_summary)

        if st.button("💾 Save Summary to History"):
            save_history(
                create_history_entry(
                    "Notes Summary",
                    "Study Notes",
                    st.session_state.last_summary
                )
            )
            st.success("Summary saved to Study History!")


# =========================================================
# INTERACTIVE QUIZ
# =========================================================

elif page == "🧠 Interactive Quiz":

    st.title("🧠 Interactive Quiz")
    st.caption("Practice what you have learned.")

    quiz_topic = st.text_input(
        "Quiz topic",
        placeholder="Example: Python, Operating Systems, Computer Networks..."
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    number_of_questions = st.selectbox(
        "Number of questions",
        [5, 10]
    )

    if st.button("🚀 Generate Quiz", type="primary"):

        if not quiz_topic.strip():
            st.warning("Please enter a quiz topic.")
        else:
            with st.spinner("Creating your quiz..."):

                prompt = f"""
Create {number_of_questions} multiple-choice questions
about {quiz_topic}.

Difficulty: {difficulty}

Return valid JSON in exactly this format:

{{
  "questions": [
    {{
      "question": "Question text",
      "options": [
        "A) Option one",
        "B) Option two",
        "C) Option three",
        "D) Option four"
      ],
      "answer": "A) Option one",
      "explanation": "Explain why the answer is correct."
    }}
  ]
}}

Requirements:
- Exactly {number_of_questions} questions.
- Four options per question.
- Only one correct answer.
- The answer must match one option exactly.
- Include an explanation for each answer.
"""

                try:
                    client = get_client()

                    response = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[
                            {
                                "role": "system",
                                "content": "You generate educational quizzes. Return valid JSON only."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.5,
                        response_format={"type": "json_object"}
                    )

                    quiz_data = json.loads(
                        response.choices[0].message.content
                    )

                    questions = quiz_data["questions"]

                    if not questions:
                        st.error("No questions were generated. Try again.")
                    else:
                        # Clear old radio selections
                        for i in range(10):
                            st.session_state.pop(f"option_{i}", None)

                        st.session_state.quiz_questions = questions
                        st.session_state.quiz_topic = quiz_topic
                        st.session_state.quiz_index = 0
                        st.session_state.quiz_submitted = {}
                        st.session_state.quiz_history_saved = False

                except Exception as e:
                    st.error(f"Quiz generation failed: {e}")

    # Display active quiz
    if "quiz_questions" in st.session_state:

        questions = st.session_state.quiz_questions
        index = st.session_state.quiz_index

        if index < len(questions):

            question = questions[index]

            st.divider()

            st.progress((index + 1) / len(questions))

            st.caption(
                f"Question {index + 1} of {len(questions)}"
            )

            st.subheader(question["question"])

            selected_option = st.radio(
                "Choose your answer:",
                question["options"],
                key=f"option_{index}",
                index=None
            )

            if index not in st.session_state.quiz_submitted:

                if st.button("Submit Answer", type="primary"):

                    if selected_option is None:
                        st.warning("Please select an answer.")
                    else:
                        is_correct = (
                            selected_option == question["answer"]
                        )

                        st.session_state.quiz_submitted[index] = is_correct

                        st.rerun()

            else:

                is_correct = st.session_state.quiz_submitted[index]

                if is_correct:
                    st.success("🎉 Correct answer!")
                else:
                    st.error("❌ Incorrect answer.")

                    st.write(
                        "**Correct answer:**",
                        question["answer"]
                    )

                st.info(
                    f"**Explanation:** {question['explanation']}"
                )

                if index < len(questions) - 1:

                    if st.button("➡️ Next Question", type="primary"):

                        st.session_state.quiz_index += 1
                        st.rerun()

                else:

                    if st.button("🏁 Finish Quiz", type="primary"):

                        st.session_state.quiz_index += 1
                        st.rerun()

        else:

            score = sum(
                st.session_state.quiz_submitted.values()
            )

            total = len(questions)

            percentage = (score / total) * 100

            st.divider()
            st.balloons()

            st.subheader("🏆 Quiz Completed!")

            col1, col2, col3 = st.columns(3)

            col1.metric("Score", f"{score}/{total}")
            col2.metric("Percentage", f"{percentage:.0f}%")

            if percentage >= 80:
                result = "Excellent work!"
            elif percentage >= 60:
                result = "Good job! Keep practicing."
            else:
                result = "Keep learning and try again!"

            col3.metric("Result", result)

            if not st.session_state.quiz_history_saved:

                quiz_result_content = (
                    f"Score: {score}/{total}\n"
                    f"Percentage: {percentage:.0f}%\n"
                    f"Result: {result}"
                )

                entry = create_history_entry(
                    "Quiz Result",
                    st.session_state.quiz_topic,
                    quiz_result_content
                )

                entry["score"] = score
                entry["total"] = total
                entry["percentage"] = percentage

                save_history(entry)

                st.session_state.quiz_history_saved = True

                st.success("Quiz result saved to Study History!")

            if st.button("🔄 Try Another Quiz"):

                quiz_keys = [
                    "quiz_questions",
                    "quiz_topic",
                    "quiz_index",
                    "quiz_submitted",
                    "quiz_history_saved"
                ]

                for key in quiz_keys:
                    st.session_state.pop(key, None)

                for i in range(10):
                    st.session_state.pop(f"option_{i}", None)

                st.rerun()


# =========================================================
# STUDY HISTORY
# =========================================================

elif page == "📚 Study History":

    st.title("📚 Study History")
    st.caption("Review your previous learning activities.")

    history = load_history()

    if history:

        filter_type = st.selectbox(
            "Filter by activity",
            [
                "All Activities",
                "Topic Explanation",
                "Notes Summary",
                "Quiz Result"
            ]
        )

        if filter_type == "All Activities":
            filtered_history = history
        else:
            filtered_history = [
                item for item in history
                if item.get("type") == filter_type
            ]

        st.write(f"**{len(filtered_history)} activities found**")

        for item in reversed(filtered_history):

            title = (
                f"{item.get('type', 'Activity')} | "
                f"{item.get('topic', 'Untitled')} | "
                f"{item.get('timestamp', '')}"
            )

            with st.expander(title):

                if item.get("type") == "Quiz Result":
                    st.write(item.get("content", ""))

                    if "percentage" in item:
                        st.metric(
                            "Quiz Percentage",
                            f"{item['percentage']:.0f}%"
                        )
                else:
                    st.markdown(item.get("content", ""))

        st.divider()

        st.subheader("⚙️ Manage History")

        confirm_clear = st.checkbox(
            "I understand that clearing history will permanently delete saved activities."
        )

        if st.button("🗑️ Clear All History"):

            if confirm_clear:
                with open(HISTORY_FILE, "w", encoding="utf-8") as file:
                    json.dump([], file)

                st.success("Study history cleared.")
                st.rerun()

            else:
                st.warning("Please confirm before clearing history.")

    else:
        st.info("No study history yet. Start learning to see your activities here!")