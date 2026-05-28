"""
🧠 Dyslexia Learning Platform - Prototype v1
=============================================
Phase 1: Onboarding + Phase 2: AI Assessment + Phase 3: Learning Modules
Built with Streamlit | LLM-powered assessment & adaptive learning
"""
####
import time
import streamlit as st
from llm_provider import get_llm
from prompts import ASSESSMENT_SYSTEM_PROMPT, build_assessment_prompt
from questions import get_questions_for_age
from video_bank import get_level_modules, get_module, get_total_modules
from phase3_prompts import (
    PRACTICE_SYSTEM_PROMPT, EXAM_SYSTEM_PROMPT, EVAL_SYSTEM_PROMPT,
    build_practice_prompt, build_exam_prompt, build_eval_prompt,
)
from singapore_map import (
    get_robot_intro, get_landmark, get_map_html, get_robot_html,
    get_floating_robot_html, get_robot_congrats_html, SINGAPORE_LANDMARKS,
)


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
        if st.button("📚 Start Learning Path →", use_container_width=True, type="primary"):
            # Initialize Phase 3 progress
            level = result.get("overall_level", 1)
            st.session_state.learning_level = level
            st.session_state.current_module_index = 0
            st.session_state.module_step = "video"  # video -> practice -> exam -> results
            st.session_state.practice_number = 1
            st.session_state.practice_activity = None
            st.session_state.exam_data = None
            st.session_state.exam_answers = {}
            st.session_state.exam_result = None
            st.session_state.module_progress = {}
            go_to_phase("learning")
            st.rerun()


# =============================================================================
# PHASE 3: LEARNING MODULES
# =============================================================================
def render_learning():
    child = st.session_state.child_data
    level = st.session_state.learning_level
    module_index = st.session_state.current_module_index
    step = st.session_state.module_step
    total_modules = get_total_modules(level)
    module = get_module(level, module_index)
    level_data = get_level_modules(level)

    # Sidebar progress
    with st.sidebar:
        st.markdown("### 📚 Learning Progress")
        st.markdown(f"**{level_data['name']}**")
        st.markdown("---")
        for i in range(total_modules):
            m = get_module(level, i)
            status = st.session_state.module_progress.get(i, "locked")
            if i == module_index:
                icon = "▶️"
            elif status == "passed":
                icon = "✅"
            elif status == "failed":
                icon = "🔁"
            elif i == 0 or st.session_state.module_progress.get(i - 1) == "passed":
                icon = "🔓"
            else:
                icon = "🔒"
            st.markdown(f"{icon} Module {i+1}: {m['name']}")

    # Floating robot assistant (bottom-right) - context-aware messages
    robot_messages = {
        "video": "📺 Watch the video carefully! I'm here if you need me!",
        "practice": "✏️ You're doing great! Try your best!",
        "exam": "📝 Exam time! You've got this! 💪",
        "exam_taking": "🤞 Take your time, read each question carefully!",
        "exam_results": "📊 Let's see how you did!",
    }
    robot_msg = robot_messages.get(step, "I'm here to help! 🌟")
    st.markdown(get_floating_robot_html(robot_msg), unsafe_allow_html=True)

    # 🗺️ Singapore Map (always visible, shows progress)
    # If exam passed, show map with next module as destination
    map_module_index = module_index
    if step == "exam_results" and st.session_state.exam_result and st.session_state.exam_result.get("passed"):
        # Show the robot has moved to the next stop
        map_module_index = min(module_index + 1, total_modules - 1)
        # Also ensure current module is marked passed in progress for the map
        st.session_state.module_progress[module_index] = "passed"

    landmark = get_landmark(level, map_module_index)
    with st.expander(f"🗺️ Journey Map — Currently at {landmark['emoji']} {landmark['name']}", expanded=True):
        st.components.v1.html(
            get_map_html(level, map_module_index, st.session_state.module_progress),
            height=320,
        )

    # Route to correct step within the module
    if step == "video":
        render_module_video(child, level, module, module_index, total_modules)
    elif step == "practice":
        render_module_practice(child, level, module, module_index)
    elif step == "exam":
        render_module_exam(child, level, module, module_index)
    elif step == "exam_taking":
        render_exam_taking(child, level, module, module_index)
    elif step == "exam_results":
        render_exam_results(child, level, module, module_index, total_modules)


def render_module_video(child, level, module, module_index, total_modules):
    """Step 1: Watch the learning video."""
    st.markdown(f"""
    <div class="main-header">
        <h1>📚 Module {module_index + 1}: {module['name']}</h1>
        <p>Level {level} — Step 1: Watch & Learn</p>
    </div>
    """, unsafe_allow_html=True)

    # Module info card
    st.markdown(f"""
    <div class="assessment-card">
        <h3>🎯 What you'll learn</h3>
        <p>{module['description']}</p>
        <p><strong>Skills:</strong> {', '.join(module['skills'])}</p>
    </div>
    """, unsafe_allow_html=True)

    # Video embed
    st.markdown("### 🎬 Watch this video:")
    st.markdown(f"**{module['video_title']}**")
    st.video(module["video_url"])

    st.markdown("---")
    st.info("👆 Watch the video above, then click **Continue to Practice** when you're ready!")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✏️ Continue to Practice →", use_container_width=True, type="primary"):
            st.session_state.module_step = "practice"
            st.session_state.practice_number = 1
            st.session_state.practice_activity = None
            st.rerun()


def render_module_practice(child, level, module, module_index):
    """Step 2: Practice activities (3 per module)."""
    practice_num = st.session_state.practice_number

    st.markdown(f"""
    <div class="main-header">
        <h1>✏️ Practice: {module['name']}</h1>
        <p>Activity {practice_num} of 3 — Learning by doing!</p>
    </div>
    <div class="progress-bar">
        <div class="progress-fill" style="width: {int((practice_num - 1) / 3 * 100)}%"></div>
    </div>
    """, unsafe_allow_html=True)

    # Generate activity if not already generated
    if st.session_state.practice_activity is None:
        with st.spinner("🤖 Generating a fun activity for you..."):
            try:
                llm = get_llm()
                prompt = build_practice_prompt(
                    child["child_name"], child["child_age"],
                    level, module, practice_num
                )
                activity = llm.chat_json(PRACTICE_SYSTEM_PROMPT, prompt)
                st.session_state.practice_activity = activity
                st.rerun()
            except Exception as e:
                st.error(f"Error generating activity: {e}")
                if st.button("🔄 Retry"):
                    st.rerun()
                return

    activity = st.session_state.practice_activity
    content = activity.get("content", {})

    # Display activity
    st.markdown(f"### {activity.get('title', 'Practice Activity')}")
    st.markdown(activity.get("instruction", ""))
    st.markdown(f"**{content.get('question', '')}**")

    # Input based on type
    answer = None
    if activity.get("type") == "multiple_choice" and content.get("options"):
        answer = st.radio("Choose:", content["options"], key=f"practice_{practice_num}")
    else:
        answer = st.text_input("Your answer:", key=f"practice_{practice_num}", placeholder="Type here...")

    # Hint
    with st.expander("💡 Need a hint?"):
        st.info(content.get("hint", "Think carefully!"))

    # Check answer
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Check Answer", use_container_width=True, type="primary"):
            correct = content.get("correct_answer", "")
            if answer and answer.lower().strip() in correct.lower():
                st.balloons()
                st.success(f"🎉 Correct! {activity.get('encouragement', 'Great job!')}")
                st.info(f"📖 {content.get('explanation', '')}")
            else:
                st.warning(f"Not quite! The answer is: **{correct}**")
                st.info(f"📖 {content.get('explanation', '')}")

    with col2:
        if st.button("Next →", use_container_width=True):
            if practice_num >= 3:
                # Move to exam
                st.session_state.module_step = "exam"
                st.session_state.practice_activity = None
            else:
                st.session_state.practice_number = practice_num + 1
                st.session_state.practice_activity = None
            st.rerun()


def render_module_exam(child, level, module, module_index):
    """Step 3: Generate and show exam."""
    st.markdown(f"""
    <div class="main-header">
        <h1>📝 Module Exam: {module['name']}</h1>
        <p>5 questions — Score 3/5 to pass!</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="assessment-card">
        <h3>📋 Exam Rules</h3>
        <ul>
            <li>5 questions covering everything in this module</li>
            <li>No hints this time — show what you've learned!</li>
            <li>Score 3 out of 5 (60%) to pass and unlock the next module</li>
            <li>Take your time, read carefully</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.exam_data is None:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Start Exam", use_container_width=True, type="primary"):
                with st.spinner("🤖 Generating exam questions..."):
                    try:
                        llm = get_llm()
                        prompt = build_exam_prompt(child["child_name"], child["child_age"], level, module)
                        exam = llm.chat_json(EXAM_SYSTEM_PROMPT, prompt)
                        st.session_state.exam_data = exam
                        st.session_state.exam_answers = {}
                        st.session_state.module_step = "exam_taking"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error generating exam: {e}")
    else:
        st.session_state.module_step = "exam_taking"
        st.rerun()


def render_exam_taking(child, level, module, module_index):
    """Step 3b: Child takes the exam."""
    exam = st.session_state.exam_data
    questions = exam.get("questions", [])

    st.markdown(f"""
    <div class="main-header">
        <h1>📝 {exam.get('exam_title', 'Module Exam')}</h1>
        <p>Answer all 5 questions, then submit</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("exam_form"):
        for i, q in enumerate(questions):
            st.markdown(f"---")
            st.markdown(f"**Question {q['id']}:** {q['question']}")

            if q.get("type") == "multiple_choice" and q.get("options"):
                st.session_state.exam_answers[q["id"]] = st.radio(
                    f"Answer Q{q['id']}:",
                    q["options"],
                    key=f"exam_q_{q['id']}",
                    label_visibility="collapsed",
                )
            else:
                st.session_state.exam_answers[q["id"]] = st.text_input(
                    f"Answer Q{q['id']}:",
                    key=f"exam_q_{q['id']}",
                    placeholder="Type your answer...",
                    label_visibility="collapsed",
                )

        st.markdown("---")
        submitted = st.form_submit_button("📨 Submit Exam", type="primary", use_container_width=True)

        if submitted:
            # Build responses for evaluation
            responses_for_eval = []
            for q in questions:
                responses_for_eval.append({
                    "id": q["id"],
                    "question": q["question"],
                    "correct_answer": q["correct_answer"],
                    "child_answer": st.session_state.exam_answers.get(q["id"], "(no answer)"),
                })

            # Call LLM to evaluate
            with st.spinner("🤖 Evaluating your answers..."):
                try:
                    llm = get_llm()
                    eval_prompt = build_eval_prompt(
                        child["child_name"], child["child_age"],
                        level, module["name"], responses_for_eval
                    )
                    result = llm.chat_json(EVAL_SYSTEM_PROMPT, eval_prompt)
                    st.session_state.exam_result = result
                    st.session_state.module_step = "exam_results"
                    st.rerun()
                except Exception as e:
                    st.error(f"Error evaluating exam: {e}")


def render_exam_results(child, level, module, module_index, total_modules):
    """Step 4: Show exam results and progression."""
    result = st.session_state.exam_result
    passed = result.get("passed", False)
    score = result.get("total_correct", 0)
    percentage = result.get("score_percentage", 0)

    if passed:
        header_text = "🎉 Congratulations! You Passed!"
        st.balloons()
    else:
        header_text = "💪 Keep Going! You Can Do It!"

    st.markdown(f"""
    <div class="main-header">
        <h1>{header_text}</h1>
        <p>{module['name']} Exam — Score: {score}/5 ({percentage}%)</p>
    </div>
    """, unsafe_allow_html=True)

    # Score display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("✅ Correct", f"{score}/5")
    with col2:
        st.metric("📊 Score", f"{percentage}%")
    with col3:
        st.metric("🏆 Result", "PASSED ✅" if passed else "RETRY 🔁")

    # Feedback
    st.markdown("---")
    st.markdown(f"### 📝 Feedback")
    st.markdown(result.get("overall_feedback", ""))

    # Question-by-question results
    st.markdown("### 📋 Question Breakdown")
    for qr in result.get("question_results", []):
        icon = "✅" if qr.get("correct") else "❌"
        st.markdown(f"{icon} **Q{qr['id']}**: {qr.get('feedback', '')}")
        if not qr.get("correct"):
            st.caption(f"Your answer: {qr.get('child_answer')} | Correct: {qr.get('expected')}")

    # Strengths and weaknesses
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 💪 Strong Areas")
        for area in result.get("strong_areas", []):
            st.markdown(f"- ✅ {area}")
    with col2:
        st.markdown("### 🎯 Areas to Improve")
        for area in result.get("weak_areas", []):
            st.markdown(f"- 📌 {area}")

    # Actions
    st.markdown("---")
    if passed:
        st.session_state.module_progress[module_index] = "passed"

        # 🤖 Robot congrats + map showing progress
        landmark = get_landmark(level, module_index)
        next_landmark_name = None
        if module_index + 1 < total_modules:
            next_lm = get_landmark(level, module_index + 1)
            next_landmark_name = f"{next_lm['emoji']} {next_lm['name']}"

        st.markdown(get_robot_congrats_html(
            landmark["name"], landmark["emoji"], next_landmark_name
        ), unsafe_allow_html=True)

        if module_index + 1 < total_modules:
            if st.button(f"📚 Next Module: {get_module(level, module_index + 1)['name']} →",
                         use_container_width=True, type="primary"):
                st.session_state.current_module_index = module_index + 1
                st.session_state.module_step = "video"
                st.session_state.practice_activity = None
                st.session_state.exam_data = None
                st.session_state.exam_result = None
                st.session_state.exam_answers = {}
                st.rerun()
        else:
            st.success("🎓 **You've completed all modules in this level!** 🎉")
            st.info("Level promotion assessment coming in Phase 4...")
    else:
        st.session_state.module_progress[module_index] = "failed"
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔁 Retry Module (Watch Video Again)", use_container_width=True):
                st.session_state.module_step = "video"
                st.session_state.practice_activity = None
                st.session_state.exam_data = None
                st.session_state.exam_result = None
                st.session_state.exam_answers = {}
                st.rerun()
        with col2:
            if st.button("📝 Retry Exam Only", use_container_width=True, type="primary"):
                st.session_state.module_step = "exam"
                st.session_state.exam_data = None
                st.session_state.exam_result = None
                st.session_state.exam_answers = {}
                st.rerun()


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

        # Debug: Jump to Phase 3
        st.markdown("---")
        st.markdown("#### 🛠️ Debug")
        debug_level = st.selectbox("Test Level:", [1, 2, 3, 4, 5], key="debug_level")
        if st.button("⚡ Jump to Phase 3", use_container_width=True):
            st.session_state.child_data = {
                "parent_name": "Test Parent",
                "parent_email": "test@test.com",
                "child_name": "Alex",
                "child_age": 7,
                "grade": "Grade 2",
                "concerns": "",
                "previous_diagnosis": "No",
            }
            st.session_state.learning_level = debug_level
            st.session_state.current_module_index = 0
            st.session_state.module_step = "video"
            st.session_state.practice_number = 1
            st.session_state.practice_activity = None
            st.session_state.exam_data = None
            st.session_state.exam_answers = {}
            st.session_state.exam_result = None
            st.session_state.module_progress = {}
            go_to_phase("learning")
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
    elif phase == "learning":
        render_learning()


if __name__ == "__main__":
    main()
