"""Empower You — Career Guidance Platform for Students.
Streamlit UI layer. All logic is called through api.py."""

import streamlit as st
import pandas as pd
import api

# ─── Page Config ───
st.set_page_config(page_title="Empower You", page_icon="🚀", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
.stApp { font-family: 'Poppins', sans-serif; }
.main-banner {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem; border-radius: 16px; color: white; text-align: center; margin-bottom: 2rem;
}
.main-banner h1 { font-size: 2.5rem; margin: 0; }
.main-banner p { font-size: 1.1rem; opacity: 0.9; }
.career-card {
    background: #f8f9ff; border: 2px solid #e0e4f5; border-radius: 12px;
    padding: 1.5rem; margin: 1rem 0;
}
.phase-badge {
    display: inline-block; padding: 4px 12px; border-radius: 20px;
    font-size: 0.8rem; font-weight: 600; margin-bottom: 1rem;
}
.phase-1 { background: #e3f2fd; color: #1565c0; }
.phase-2 { background: #e8f5e9; color: #2e7d32; }
.phase-3 { background: #fff3e0; color: #e65100; }
.phase-4 { background: #ede7f6; color: #4527a0; }
.phase-5 { background: #fce4ec; color: #c62828; }
</style>
""", unsafe_allow_html=True)


# ─── Session State Init ───
def init_state():
    defaults = {
        "phase": 1,
        "user_info": {},
        "answers": {},
        "uploads": {},
        "result": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()


# ─── Banner ───
st.markdown("""
<div class="main-banner">
    <h1>🚀 Empower You</h1>
    <p>Discover your perfect career path — powered by AI</p>
</div>
""", unsafe_allow_html=True)


# ─── Progress Bar ───
phase = st.session_state.phase
TOTAL_PHASES = 5
phase_names = {1: "About You", 2: "Discover Yourself", 3: "Showcase", 4: "Career Paths", 5: "Analytics Report"}
st.progress(phase / TOTAL_PHASES, text=f"Phase {phase}/{TOTAL_PHASES} — {phase_names[phase]}")


# ═══════════════════════════════════════════
# PHASE 1: User Info
# ═══════════════════════════════════════════
if phase == 1:
    st.markdown('<span class="phase-badge phase-1">Phase 1 — About You</span>', unsafe_allow_html=True)
    st.subheader("Let's get to know you! 👋")

    options = api.get_form_options()

    name = st.text_input("What's your name?", placeholder="Enter your name")
    standard = st.selectbox("Which standard are you in?", ["-- Select --"] + options["standards"])
    hobbies = st.multiselect(
        "Pick your hobbies / interests (choose as many as you like)",
        options["hobbies"],
    )

    if st.button("Let's Go! →", type="primary", use_container_width=True):
        std = standard if standard != "-- Select --" else ""
        is_valid, error = api.validate_user_info(name, std, hobbies)
        if not is_valid:
            st.error(error)
        else:
            st.session_state.user_info = {"name": name, "standard": std, "hobbies": hobbies}
            st.session_state.phase = 2
            st.rerun()


# ═══════════════════════════════════════════
# PHASE 2: Hybrid Questions
# ═══════════════════════════════════════════
elif phase == 2:
    st.markdown('<span class="phase-badge phase-2">Phase 2 — Discover Yourself</span>', unsafe_allow_html=True)

    user = st.session_state.user_info
    st.subheader(f"Hey {user['name']}! Let's explore who you are 🔍")
    st.caption("No right or wrong answers. Just pick what feels most YOU.")

    questions = api.get_questions()

    with st.form("questions_form"):
        answers = {}

        for i, q in enumerate(questions):
            st.markdown(f"### {q['title']}")
            st.markdown(f"**{q['question']}**")

            input_type = q.get("input_type", "mcq")

            if input_type == "mcq":
                option_labels = [f"{opt['key']}. {opt['text']}" for opt in q["options"]]
                choice = st.radio(
                    f"q_{q['id']}",
                    option_labels,
                    index=None,
                    label_visibility="collapsed",
                    key=f"radio_{q['id']}",
                )
                if choice:
                    answers[q["id"]] = choice.split(".")[0].strip()

            elif input_type == "slider":
                col1, col2, col3 = st.columns([2, 3, 2])
                with col1:
                    st.caption(q["left_label"])
                with col3:
                    st.caption(q["right_label"])
                val = st.slider(
                    f"q_{q['id']}",
                    min_value=1, max_value=5, value=3,
                    label_visibility="collapsed",
                    key=f"slider_{q['id']}",
                )
                answers[q["id"]] = str(val)

            elif input_type == "text":
                text = st.text_area(
                    f"q_{q['id']}",
                    placeholder=q.get("placeholder", "Type here..."),
                    label_visibility="collapsed",
                    key=f"text_{q['id']}",
                    height=100,
                )
                if text:
                    answers[q["id"]] = text

            elif input_type == "ranking":
                st.caption("Drag to reorder, or use the numbers to rank (1 = most important)")
                items = q["items"]
                # Use selectboxes for ranking since streamlit has no native drag
                ranked = []
                used = []
                for rank in range(1, len(items) + 1):
                    available = [it["text"] for it in items if it["key"] not in used]
                    choice = st.selectbox(
                        f"#{rank}",
                        ["-- Pick --"] + available,
                        key=f"rank_{q['id']}_{rank}",
                    )
                    if choice != "-- Pick --":
                        # Find the key for this text
                        for it in items:
                            if it["text"] == choice:
                                ranked.append(it["key"])
                                used.append(it["key"])
                                break
                if len(ranked) == len(items):
                    answers[q["id"]] = ranked

            if i < len(questions) - 1:
                st.divider()

        submitted = st.form_submit_button("Next → Showcase Round", type="primary", use_container_width=True)

        if submitted:
            # Count required answers (sliders always have a value)
            mcq_qs = [q for q in questions if q.get("input_type") == "mcq"]
            mcq_answered = sum(1 for q in mcq_qs if q["id"] in answers)
            if mcq_answered < len(mcq_qs):
                st.error("Please answer all multiple-choice questions.")
            else:
                st.session_state.answers = answers
                st.session_state.phase = 3
                st.rerun()


# ═══════════════════════════════════════════
# PHASE 3: Audio-Visual Showcase
# ═══════════════════════════════════════════
elif phase == 3:
    st.markdown('<span class="phase-badge phase-3">Phase 3 — Showcase Your Talent</span>', unsafe_allow_html=True)

    user = st.session_state.user_info
    showcase_tasks = api.get_showcase_for_hobbies(user["hobbies"])

    if not showcase_tasks:
        st.info("No showcase tasks for your hobbies. Moving to results!")
        st.session_state.phase = 4
        st.rerun()
    else:
        st.subheader(f"🎬 {user['name']}, time to show off!")
        st.caption("This is optional but helps us understand you better. Upload what you can!")

        uploads = {}
        for i, task in enumerate(showcase_tasks):
            st.markdown(f"### {task['title']}")
            st.markdown(f"*{task['instruction']}*")

            upload_type = task["upload_type"]
            if upload_type == "video":
                file = st.file_uploader(
                    f"Upload video",
                    type=["mp4", "mov", "avi", "webm"],
                    key=f"upload_{i}",
                )
            elif upload_type == "audio":
                file = st.file_uploader(
                    f"Upload audio",
                    type=["mp3", "wav", "m4a", "ogg"],
                    key=f"upload_{i}",
                )
            elif upload_type == "image":
                file = st.file_uploader(
                    f"Upload image",
                    type=["jpg", "jpeg", "png", "webp"],
                    key=f"upload_{i}",
                )
            else:
                file = None

            if file:
                uploads[task["title"]] = {"file": file, "signals": task["signals"]}
                st.success(f"✅ Uploaded: {file.name}")

            if i < len(showcase_tasks) - 1:
                st.divider()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Skip → See Results", use_container_width=True):
                st.session_state.phase = 4
                st.rerun()
        with col2:
            if st.button("Submit & See Results →", type="primary", use_container_width=True):
                # Add showcase signals to answers
                st.session_state.uploads = {k: v["signals"] for k, v in uploads.items()}
                st.session_state.phase = 4
                st.rerun()


# ═══════════════════════════════════════════
# PHASE 4: Career Prediction + Audio-Visual
# ═══════════════════════════════════════════
elif phase == 4:
    st.markdown('<span class="phase-badge phase-4">Phase 4 — Your Career Paths</span>', unsafe_allow_html=True)

    user = st.session_state.user_info

    if st.session_state.result is None:
        with st.spinner(f"🤖 Analyzing your profile, {user['name']}... This takes a moment."):
            result = api.evaluate_career(user, st.session_state.answers)
            st.session_state.result = result

    result = st.session_state.result

    st.subheader(f"🎯 {user['name']}, here are your top career paths!")

    for career_name in result["careers"]:
        media = result["media"].get(career_name, {})
        icon = media.get("icon", "🌟")
        tagline = media.get("tagline", "")
        day_in_life = media.get("day_in_life", "")
        video_url = media.get("video", "")

        st.markdown(f"""<div class="career-card">
            <h3>{icon} {career_name}</h3>
            <p><em>{tagline}</em></p>
        </div>""", unsafe_allow_html=True)

        if day_in_life:
            with st.expander(f"📖 A Day in the Life of a {career_name}"):
                st.write(day_in_life)

        if video_url:
            with st.expander(f"🎬 Watch: Life as a {career_name}"):
                st.video(video_url)

    with st.expander("📋 Full AI Analysis"):
        st.markdown(result["prediction"])

    if st.button("See Analytics Report →", type="primary", use_container_width=True):
        st.session_state.phase = 5
        st.rerun()


# ═══════════════════════════════════════════
# PHASE 5: Analytics & Final Report
# ═══════════════════════════════════════════
elif phase == 5:
    st.markdown('<span class="phase-badge phase-5">Phase 5 — Your Analytics Report</span>', unsafe_allow_html=True)

    user = st.session_state.user_info
    result = st.session_state.result
    signals = result["signals"]

    st.subheader(f"📊 {user['name']}'s Personality & Career Analytics")

    # ─── Radar/Bar Chart: Dimension Scores ───
    st.markdown("### 🧠 Your Profile Dimensions")

    # Build chart data from signals
    chart_data = {}
    for dim, values in signals.items():
        label = dim.replace("_", " ").title()
        top_val = max(values, key=values.get)
        chart_data[label] = values[top_val]

    if chart_data:
        df_bar = pd.DataFrame({
            "Dimension": list(chart_data.keys()),
            "Strength": list(chart_data.values()),
        })
        st.bar_chart(df_bar.set_index("Dimension"), color="#667eea")

    # ─── Pie Chart: Domain Attraction ───
    st.markdown("### 🎯 Domain Attraction Breakdown")

    if "domain_attraction" in signals:
        domain_data = signals["domain_attraction"]
        df_domain = pd.DataFrame({
            "Domain": [d.title() for d in domain_data.keys()],
            "Score": list(domain_data.values()),
        })
        st.bar_chart(df_domain.set_index("Domain"), color="#764ba2")
    else:
        st.info("Not enough data for domain chart.")

    # ─── Core Driver Chart ───
    st.markdown("### 💡 What Drives You")

    if "core_driver" in signals:
        driver_data = signals["core_driver"]
        df_driver = pd.DataFrame({
            "Driver": [d.title() for d in driver_data.keys()],
            "Score": list(driver_data.values()),
        })
        st.bar_chart(df_driver.set_index("Driver"), color="#e65100")

    # ─── Thinking Style ───
    if "thinking_style" in signals:
        st.markdown("### 🧩 Thinking Style")
        style_data = signals["thinking_style"]
        df_style = pd.DataFrame({
            "Style": [s.title() for s in style_data.keys()],
            "Score": list(style_data.values()),
        })
        st.bar_chart(df_style.set_index("Style"), color="#2e7d32")

    st.divider()

    # ─── Profile Summary ───
    st.markdown("### 📋 Profile Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📛 Name:**")
        st.write(user["name"])
        st.markdown("**🎓 Standard:**")
        st.write(user["standard"])
    with col2:
        st.markdown("**🎯 Hobbies:**")
        for h in user["hobbies"]:
            st.write(f"• {h}")

    st.divider()

    # ─── Top signals summary ───
    st.markdown("### 🏆 Key Insights")
    for dim, values in signals.items():
        label = dim.replace("_", " ").title()
        top_val = max(values, key=values.get)
        st.write(f"**{label}:** {top_val.title()}")

    st.divider()

    # ─── Career Recommendations ───
    st.markdown("### 🚀 Recommended Career Paths")
    st.markdown(result["prediction"])

    st.divider()

    st.success(f"🌟 {user['name']}, remember — there's no single right path. Explore, experiment, and stay curious!")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Start Over", use_container_width=True):
            for key in ["phase", "user_info", "answers", "uploads", "result"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    with col2:
        if st.button("📥 Download Report (Coming Soon)", use_container_width=True, disabled=True):
            pass
