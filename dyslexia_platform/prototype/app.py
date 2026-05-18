"""
🧠 Dyslexia Learning Platform - Prototype v1
=============================================
Phase 1: Onboarding + Phase 2: AI Assessment
Built with Streamlit | LLM-powered assessment
"""

import time
import streamlit as st
from llm_provider import get_llm
from prompts import ASSESSMENT_SYSTEM_PROMPT, build_assessment_prompt
from questions import get_questions_for_age


# =============================================================================
# PAGE CONFIG & STYLING
# =============================================================================
st.set_page_config(
    page_title="🧠 Dyslexia Learning Platform",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for dyslexia-friendly, appealing UI
st.markdown("""
<style>
    /* Import dyslexia-friendly font */
    @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&display=swap');

    /* Global styles */
    .stApp {
        font-family: 'Lexend', sans-serif;
    }

    /* Larger line spacing for readability */
    p, li, label, .stMarkdown {
        line-height: 1.8 !important;
        letter-spacing: 0.02em;
    }

    /* Warm, calming color scheme */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }

    .main-header h1 {
        font-size: 2.2rem;
        margin: 0;
        font-weight: 600;
    }

    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }

    /* Card styling */
    .assessment-card {
        background: white;
        border: 2px solid #e8ecf4;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }

    .assessment-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    }

    /* Progress indicator */
    .progress-bar {
        background: #f0f2f6;
        border-radius: 50px;
        height: 12px;
        margin: 1rem 0;
        overflow: hidden;
    }

    .progress-fill {
        background: linear-gradient(90deg, #667eea, #764ba2);
        height: 100%;
        border-radius: 50px;
        transition: width 0.5s ease;
    }

    /* Result cards */
    .result-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
    }

    .score-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.1rem;
    }

    /* Dimension scores */
    .dimension-row {
        display: flex;
        align-items: center;
        padding: 0.8rem 0;
        border-bottom: 1px solid #eee;
    }

    .dimension-label {
        flex: 1;
        font-weight: 500;
    }

    .dimension-bar {
        flex: 2;
        background: #f0f2f6;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
        margin: 0 1rem;
    }

    /* Question styling */
    .question-number {
        background: #667eea;
        color: white;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        margin-right: 0.8rem;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 12px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 500 !important;
        font-family: 'Lexend', sans-serif !important;
        transition: all 0.3s !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
    }

    /* Welcome animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }

    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================
if "phase" not in st.session_state:
    st.session_state.phase = "welcome"  # welcome -> onboarding -> assessment -> results
if "child_data" not in st.session_state:
    st.session_state.child_data = {}
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "responses" not in st.session_state:
    st.session_state.responses = []
if "question_start_time" not in st.session_state:
    st.session_state.question_start_time = None
if "assessment_result" not in st.session_state:
    st.session_state.assessment_result = None


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def reset_app():
    """Reset all session state."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def go_to_phase(phase: str):
    st.session_state.phase = phase


# =============================================================================
# WELCOME SCREEN
# =============================================================================
def render_welcome():
    st.markdown("""
    <div class="main-header fade-in">
        <h1>🧠 Dyslexia Learning Platform</h1>
        <p>AI-powered assessment to understand your child's unique learning profile</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🎯 Personalized")
        st.markdown("Assessment tailored to your child's age and responses")
    with col2:
        st.markdown("### 🤖 AI-Powered")
        st.markdown("Advanced AI analyzes patterns to identify learning needs")
    with col3:
        st.markdown("### 💜 Supportive")
        st.markdown("No judgement — just understanding and a clear path forward")

    st.markdown("---")
    st.markdown("#### How it works:")
    st.markdown("""
    1. **📝 Register** — Tell us about your child (2 min)
    2. **🧪 Assessment** — Your child answers 5-6 fun questions (5 min)
    3. **📊 Results** — AI analyzes responses and creates a learning profile
    4. **📚 Path** — Get a personalized learning path recommendation
    """)

    st.markdown("")
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        if st.button("🚀 Get Started", use_container_width=True, type="primary"):
            go_to_phase("onboarding")
            st.rerun()


# =============================================================================
# PHASE 1: ONBOARDING
# =============================================================================
def render_onboarding():
    st.markdown("""
    <div class="main-header">
        <h1>📝 Let's Get to Know Your Child</h1>
        <p>Phase 1 of 2 — This helps us tailor the assessment</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("onboarding_form"):
        st.markdown("#### 👤 Parent Information")
        parent_name = st.text_input("Your Name", placeholder="e.g., Sarah Johnson")
        parent_email = st.text_input("Email", placeholder="e.g., sarah@example.com")

        st.markdown("---")
        st.markdown("#### 👶 Child Information")

        col1, col2 = st.columns(2)
        with col1:
            child_name = st.text_input("Child's Name", placeholder="e.g., Alex")
        with col2:
            child_age = st.number_input("Child's Age", min_value=4, max_value=16, value=7)

        grade = st.selectbox("Current Grade/Class", [
            "Pre-K / Kindergarten",
            "Grade 1", "Grade 2", "Grade 3",
            "Grade 4", "Grade 5", "Grade 6",
            "Grade 7+",
        ])

        st.markdown("---")
        st.markdown("#### 📋 Quick Background (Optional)")
        concerns = st.text_area(
            "What concerns do you have about your child's reading/writing?",
            placeholder="e.g., Mixes up b and d, reads slowly, avoids reading aloud...",
            height=100,
        )

        previous_diagnosis = st.radio(
            "Has your child been previously assessed for dyslexia?",
            ["No", "Yes - diagnosed", "Yes - not diagnosed", "Unsure"],
            horizontal=True,
        )

        submitted = st.form_submit_button("Continue to Assessment →", type="primary", use_container_width=True)

        if submitted:
            if not parent_name or not child_name:
                st.error("Please fill in at least your name and your child's name.")
            else:
                st.session_state.child_data = {
                    "parent_name": parent_name,
                    "parent_email": parent_email,
                    "child_name": child_name,
                    "child_age": child_age,
                    "grade": grade,
                    "concerns": concerns,
                    "previous_diagnosis": previous_diagnosis,
                }
                go_to_phase("assessment")
                st.rerun()


# =============================================================================
# PHASE 2: ASSESSMENT
# =============================================================================
def render_assessment():
    child = st.session_state.child_data
    questions = get_questions_for_age(child["child_age"])
    total = len(questions)
    current = st.session_state.current_question

    # Header with progress
    progress_pct = int((current / total) * 100)
    st.markdown(f"""
    <div class="main-header">
        <h1>🧪 Assessment for {child['child_name']}</h1>
        <p>Question {current + 1} of {total} — Take your time!</p>
    </div>
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress_pct}%"></div>
    </div>
    """, unsafe_allow_html=True)

    # Start timer for this question
    if st.session_state.question_start_time is None:
        st.session_state.question_start_time = time.time()

    # Show current question
    if current < total:
        q = questions[current]

        st.markdown(f"""
        <div class="assessment-card">
            <span class="question-number">{current + 1}</span>
            <strong>{q['dimension'].replace('_', ' ').title()}</strong>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"### {q['question']}")

        # Render input based on question type
        answer = None
        if q["type"] == "multiple_choice":
            answer = st.radio(
                "Choose your answer:",
                q["options"],
                key=f"q_{current}",
                label_visibility="collapsed",
            )
        else:
            answer = st.text_input(
                "Type your answer:",
                key=f"q_{current}",
                placeholder="Type here...",
            )

        # Hint expander
        with st.expander("💡 Need a hint?"):
            st.info(q["hint"])

        # Submit answer
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Next →", use_container_width=True, type="primary"):
                elapsed = round(time.time() - st.session_state.question_start_time, 1)

                st.session_state.responses.append({
                    "question": q["question"],
                    "expected": q["expected"],
                    "answer": answer or "(no answer)",
                    "dimension": q["dimension"],
                    "time_seconds": elapsed,
                })

                st.session_state.current_question += 1
                st.session_state.question_start_time = None

                if st.session_state.current_question >= total:
                    go_to_phase("analyzing")
                st.rerun()
    else:
        go_to_phase("analyzing")
        st.rerun()


# =============================================================================
# ANALYZING SCREEN (AI CALL)
# =============================================================================
def render_analyzing():
    child = st.session_state.child_data

    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI is Analyzing Responses...</h1>
        <p>Our AI specialist is reviewing the assessment</p>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("🧠 Analyzing patterns, scoring dimensions, classifying severity..."):
        try:
            llm = get_llm()
            user_message = build_assessment_prompt(
                child["child_name"],
                child["child_age"],
                st.session_state.responses,
            )
            result = llm.chat_json(ASSESSMENT_SYSTEM_PROMPT, user_message)
            st.session_state.assessment_result = result
            go_to_phase("results")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error during assessment: {str(e)}")
            st.info("💡 Check your `.env` file and make sure LLM_PROVIDER and credentials are set correctly.")
            if st.button("🔄 Retry"):
                st.rerun()


# =============================================================================
# RESULTS SCREEN
# =============================================================================
def render_results():
    child = st.session_state.child_data
    result = st.session_state.assessment_result

    st.markdown(f"""
    <div class="main-header">
        <h1>📊 Assessment Results for {child['child_name']}</h1>
        <p>AI-powered dyslexia screening report</p>
    </div>
    """, unsafe_allow_html=True)

    # Overall level
    level = result.get("overall_level", "N/A")
    severity = result.get("severity", "unknown")
    confidence = result.get("confidence", 0)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Level", f"{level} / 5")
    with col2:
        st.metric("⚡ Severity", severity.title())
    with col3:
        st.metric("🎯 Confidence", f"{int(confidence * 100)}%")

    st.markdown("---")

    # Summary
    st.markdown("### 📝 Summary")
    st.markdown(f"""
    <div class="result-card">
        {result.get('summary', 'Assessment complete.')}
    </div>
    """, unsafe_allow_html=True)

    # Encouragement
    st.success(f"💜 {result.get('encouragement', 'Every child learns differently — and that is okay!')}")

    # Dimension breakdown
    st.markdown("### 🎯 Dimension Scores")
    dimensions = result.get("dimensions", {})

    dimension_labels = {
        "phonemic_awareness": "🔊 Phonemic Awareness",
        "letter_recognition": "🔤 Letter Recognition",
        "reading_spelling": "📖 Reading & Spelling",
        "comprehension": "🧠 Comprehension",
        "visual_processing": "👁️ Visual Processing",
    }

    for key, label in dimension_labels.items():
        dim = dimensions.get(key, {})
        score = dim.get("score", 0)
        notes = dim.get("notes", "")

        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"**{label}**")
        with col2:
            st.progress(score / 5)
            st.caption(notes)

    # Dyslexia type & recommendations
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏷️ Dyslexia Type")
        dtype = result.get("dyslexia_type", "unknown").replace("_", " ").title()
        st.markdown(f"**{dtype}**")

    with col2:
        st.markdown("### 🎯 Recommended Focus Areas")
        for area in result.get("recommended_focus", []):
            st.markdown(f"- ✅ {area}")

    # Raw responses review
    st.markdown("---")
    with st.expander("📋 View Detailed Responses"):
        for i, r in enumerate(st.session_state.responses, 1):
            correct = "✅" if r["answer"].lower().strip() in r["expected"].lower() else "❌"
            st.markdown(f"**Q{i}** [{r['dimension']}]: {r['question']}")
            st.markdown(f"  - Answer: `{r['answer']}` {correct} (Expected: `{r['expected']}`) — ⏱️ {r['time_seconds']}s")

    # Actions
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Start Over", use_container_width=True):
            reset_app()
            st.rerun()
    with col2:
        if st.button("📚 View Learning Path (Coming Soon)", use_container_width=True, disabled=True):
            pass


# =============================================================================
# MAIN ROUTER
# =============================================================================
def main():
    phase = st.session_state.phase

    # Sidebar info
    with st.sidebar:
        st.markdown("### 🧠 Dyslexia Platform")
        st.markdown("**Prototype v1**")
        st.markdown("---")
        st.markdown(f"📍 Phase: `{phase}`")
        if st.session_state.child_data:
            st.markdown(f"👶 Child: {st.session_state.child_data.get('child_name', '-')}")
            st.markdown(f"🎂 Age: {st.session_state.child_data.get('child_age', '-')}")
        st.markdown("---")
        if st.button("🏠 Reset", use_container_width=True):
            reset_app()
            st.rerun()

    # Route to correct phase
    if phase == "welcome":
        render_welcome()
    elif phase == "onboarding":
        render_onboarding()
    elif phase == "assessment":
        render_assessment()
    elif phase == "analyzing":
        render_analyzing()
    elif phase == "results":
        render_results()


if __name__ == "__main__":
    main()
