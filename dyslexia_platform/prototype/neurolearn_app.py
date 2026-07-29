"""
NeuroLearn KIDS — Screen 1 (Login) + Screen 2 (Account Type Selection)
Run with: streamlit run neurolearn_app.py
"""

import streamlit as st

st.set_page_config(
    page_title="NeuroLearn KIDS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state ──────────────────────────────────────────────────────────────
if "screen" not in st.session_state:
    st.session_state.screen = "login"
if "user_role" not in st.session_state:
    st.session_state.user_role = None

# ── Query-param navigation (role card clicks pass ?role=... / ?go=...) ─────────
_params = st.query_params
if "role" in _params:
    st.session_state.user_role = _params["role"]
    st.session_state.screen = "role_confirmed"
    st.query_params.clear()
    st.rerun()
if "go" in _params:
    st.session_state.screen = _params["go"]
    st.query_params.clear()
    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════════════
def inject_css():
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700;800&display=swap');

* { box-sizing: border-box; }

html, body, .stApp {
    font-family: 'Lexend', 'Segoe UI', sans-serif !important;
    background: linear-gradient(140deg, #e0f7f4 0%, #ede9fe 55%, #fce8f3 100%) !important;
    min-height: 100vh;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 1.5rem 0 !important; max-width: 100% !important; }
[data-testid="stHorizontalBlock"] { gap: 0 !important; }

/* ── Right card panel ───────────────────────────────────────────────────── */
.right-card {
    background: #ffffff;
    border-radius: 24px;
    padding: 44px 52px 32px;
    box-shadow: 0 12px 48px rgba(0,0,0,0.09);
    min-height: 82vh;
    position: relative;
}

/* ── Brand panel ────────────────────────────────────────────────────────── */
.brand-panel {
    padding: 40px 24px 32px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.brand-logo { font-size: 4.5rem; line-height: 1; margin-bottom: 6px; }
.brand-name {
    font-size: 2.4rem;
    font-weight: 800;
    color: #0d9488;
    line-height: 1;
}
.brand-kids {
    font-size: 0.88rem;
    font-weight: 700;
    color: #7c3aed;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin-bottom: 20px;
}
.brand-divider {
    width: 44px; height: 4px;
    background: linear-gradient(90deg, #0d9488, #7c3aed);
    border-radius: 2px;
    margin: 0 auto 20px;
}
.brand-tagline {
    font-size: 1.42rem; font-weight: 700;
    color: #1e293b; line-height: 1.45;
    text-align: left; margin-bottom: 10px;
}
.brand-desc {
    font-size: 0.88rem; color: #64748b;
    line-height: 1.7; text-align: left;
    margin-bottom: 28px;
}
.brand-illus { font-size: 5rem; opacity: 0.82; margin-top: 20px; }
.brand-kids-illus { font-size: 1.8rem; opacity: 0.7; margin-top: 8px; }

/* ── Form headings ──────────────────────────────────────────────────────── */
.form-title {
    font-size: 2rem; font-weight: 800;
    color: #1e293b; margin-bottom: 4px; margin-top: 0;
}
.form-subtitle {
    font-size: 0.93rem; color: #64748b;
    margin-bottom: 28px; margin-top: 0;
}

/* ── Inputs ─────────────────────────────────────────────────────────────── */
.stTextInput > label {
    font-weight: 600 !important;
    color: #374151 !important;
    font-family: 'Lexend', sans-serif !important;
    font-size: 0.87rem !important;
}
.stTextInput > div > div > input {
    border-radius: 12px !important;
    border: 1.5px solid #e5e7eb !important;
    padding: 12px 16px !important;
    font-family: 'Lexend', sans-serif !important;
    font-size: 0.94rem !important;
    color: #1e293b !important;
}
.stTextInput > div > div > input:focus {
    border-color: #0d9488 !important;
    box-shadow: 0 0 0 3px rgba(13,148,136,0.12) !important;
}

/* ── Checkbox ────────────────────────────────────────────────────────────── */
.stCheckbox > label {
    font-size: 0.87rem !important;
    color: #64748b !important;
    font-family: 'Lexend', sans-serif !important;
}

/* ── Primary button (Login) ──────────────────────────────────────────────── */
button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    font-family: 'Lexend', sans-serif !important;
    height: 52px !important;
    letter-spacing: 0.01em !important;
    transition: all 0.2s !important;
}
button[data-testid="baseButton-primary"]:hover {
    box-shadow: 0 6px 20px rgba(13,148,136,0.38) !important;
    transform: translateY(-1px) !important;
}

/* ── Secondary buttons (social / back) ───────────────────────────────────── */
button[data-testid="baseButton-secondary"] {
    background: white !important;
    color: #374151 !important;
    border: 1.5px solid #e5e7eb !important;
    border-radius: 12px !important;
    font-family: 'Lexend', sans-serif !important;
    font-weight: 500 !important;
    height: 48px !important;
    transition: all 0.18s !important;
}
button[data-testid="baseButton-secondary"]:hover {
    border-color: #9ca3af !important;
    background: #f9fafb !important;
}

/* ── Or divider ──────────────────────────────────────────────────────────── */
.or-divider {
    display: flex; align-items: center; gap: 12px;
    margin: 14px 0; color: #9ca3af; font-size: 0.87rem;
}
.or-divider::before, .or-divider::after {
    content: ''; flex: 1; height: 1px; background: #e5e7eb;
}

/* ── Feature bar ─────────────────────────────────────────────────────────── */
.feature-bar {
    display: flex; gap: 0;
    background: #f8fafc;
    border-top: 1px solid #f1f5f9;
    padding: 18px 24px;
    border-radius: 0 0 24px 24px;
    margin: 24px -52px -32px;
}
.feat-item {
    display: flex; align-items: flex-start;
    gap: 12px; flex: 1;
    padding: 0 12px;
    border-right: 1px solid #e5e7eb;
}
.feat-item:last-child { border-right: none; }
.feat-icon {
    width: 38px; height: 38px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.15rem; flex-shrink: 0;
}
.feat-text h5 { margin: 0 0 2px; font-size: 0.83rem; color: #1e293b; font-weight: 700; }
.feat-text p  { margin: 0; font-size: 0.76rem; color: #64748b; line-height: 1.4; }

/* ── Footer ─────────────────────────────────────────────────────────────── */
.page-footer {
    text-align: center; padding: 14px 8px;
    font-size: 0.79rem; color: #94a3b8;
    margin-top: 10px;
}
.page-footer a { color: #94a3b8; text-decoration: none; margin: 0 6px; }
.page-footer a:hover { color: #0d9488; }

/* ── Step indicator ──────────────────────────────────────────────────────── */
.steps {
    display: flex; align-items: flex-start;
    gap: 0; margin-bottom: 30px;
}
.step-item { display: flex; flex-direction: column; align-items: center; gap: 5px; }
.s-done  { width:34px;height:34px;border-radius:50%;background:#0d9488;color:white;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px; }
.s-active{ width:34px;height:34px;border-radius:50%;background:#0d9488;color:white;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;box-shadow:0 0 0 5px rgba(13,148,136,0.18); }
.s-idle  { width:34px;height:34px;border-radius:50%;background:#e5e7eb;color:#9ca3af;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px; }
.s-label-done  { font-size:0.74rem;font-weight:600;color:#0d9488;text-align:center;max-width:80px; }
.s-label-active{ font-size:0.74rem;font-weight:600;color:#0d9488;text-align:center;max-width:80px; }
.s-label-idle  { font-size:0.74rem;font-weight:500;color:#9ca3af;text-align:center;max-width:80px; }
.s-line-done { width:72px;height:3px;background:#0d9488;margin-bottom:16px; }
.s-line-idle { width:72px;height:3px;background:#e5e7eb;margin-bottom:16px; }

/* ── Role cards (HTML links with query-param navigation) ─────────────────── */
.role-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin: 20px 0;
}
.role-card {
    text-decoration: none !important;
    border-radius: 16px;
    padding: 22px 18px 18px;
    text-align: center;
    display: block;
    border: 2px solid transparent;
    transition: transform 0.18s, box-shadow 0.18s, border-color 0.18s;
    cursor: pointer;
}
.role-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 28px rgba(0,0,0,0.12);
}
.role-card .rc-emoji { font-size: 2.5rem; margin-bottom: 8px; display: block; }
.role-card h4 { margin: 0 0 6px; font-size: 1rem; font-weight: 700; }
.role-card p  { margin: 0 0 14px; font-size: 0.8rem; line-height: 1.45; color: #64748b; }
.role-card .rc-arrow {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 1rem; font-weight: 700;
    color: white;
}

.rc-parent  { background:#f0fdfa; border-color:#a7f3d0; }
.rc-parent h4 { color:#0f766e; }
.rc-parent .rc-arrow  { background:#0d9488; }
.rc-parent:hover { border-color:#0d9488; }

.rc-teacher { background:#f5f3ff; border-color:#ddd6fe; }
.rc-teacher h4 { color:#6d28d9; }
.rc-teacher .rc-arrow { background:#7c3aed; }
.rc-teacher:hover { border-color:#7c3aed; }

.rc-student { background:#fffbeb; border-color:#fde68a; }
.rc-student h4 { color:#92400e; }
.rc-student .rc-arrow { background:#f59e0b; }
.rc-student:hover { border-color:#f59e0b; }

.rc-therapist { background:#fff1f2; border-color:#fecdd3; }
.rc-therapist h4 { color:#be123c; }
.rc-therapist .rc-arrow { background:#e11d48; }
.rc-therapist:hover { border-color:#e11d48; }

/* ── Security badge ──────────────────────────────────────────────────────── */
.security-badge {
    background: #f0fdfa;
    border: 1px solid #a7f3d0;
    border-radius: 12px;
    padding: 14px 18px;
    display: flex; align-items: center; gap: 14px;
    margin-top: 6px;
}
.security-badge .sb-text h5 { margin:0 0 3px;font-size:0.87rem;font-weight:700;color:#0f766e; }
.security-badge .sb-text p  { margin:0;font-size:0.79rem;color:#64748b;line-height:1.4; }
.sb-lock { font-size:1.6rem;margin-left:auto; }

/* ── Role confirmed banner ───────────────────────────────────────────────── */
.confirmed-banner {
    text-align: center;
    padding: 60px 40px;
}
.confirmed-banner .cb-icon { font-size: 4rem; margin-bottom: 16px; }
.confirmed-banner h2 { color: #0d9488; font-size: 1.8rem; font-weight: 800; margin-bottom: 8px; }
.confirmed-banner p  { color: #64748b; font-size: 0.95rem; }
</style>
        """,
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# SHARED COMPONENTS
# ══════════════════════════════════════════════════════════════════════════════

def render_brand_panel():
    st.markdown(
        """
<div class="brand-panel">
    <div class="brand-logo">🧠</div>
    <div class="brand-name">NeuroLearn</div>
    <div class="brand-kids">KIDS</div>
    <div class="brand-divider"></div>
    <div class="brand-tagline">AI-Powered Learning for Every Unique Mind</div>
    <div class="brand-desc">
        Personalized support to help children with dyslexia learn to read,
        build confidence and thrive.
    </div>
    <div class="brand-illus">📚✨</div>
    <div class="brand-kids-illus">👧🏽 🧒🏻 💻</div>
</div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_bar():
    st.markdown(
        """
<div class="feature-bar">
    <div class="feat-item">
        <div class="feat-icon" style="background:#f5f3ff;">🧠</div>
        <div class="feat-text">
            <h5>AI-Powered Assessment</h5>
            <p>Identify strengths and learning needs.</p>
        </div>
    </div>
    <div class="feat-item">
        <div class="feat-icon" style="background:#f0fdfa;">📖</div>
        <div class="feat-text">
            <h5>Adaptive Learning</h5>
            <p>Personalized lessons that grow with your child.</p>
        </div>
    </div>
    <div class="feat-item">
        <div class="feat-icon" style="background:#fff1f2;">📊</div>
        <div class="feat-text">
            <h5>Track Progress</h5>
            <p>Real-time insights for parents and educators.</p>
        </div>
    </div>
    <div class="feat-item">
        <div class="feat-icon" style="background:#fffbeb;">🛡️</div>
        <div class="feat-text">
            <h5>Trusted by Families</h5>
            <p>Designed with experts. Loved by families.</p>
        </div>
    </div>
</div>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    st.markdown(
        """
<div class="page-footer">
    © 2025 NeuroLearn Kids. All rights reserved. &nbsp;
    <a href="#">Privacy Policy</a> |
    <a href="#">Terms of Use</a> |
    <a href="#">Help Center</a>
</div>
        """,
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 1 — LOGIN
# ══════════════════════════════════════════════════════════════════════════════

def render_screen_login():
    st.markdown('<div class="right-card">', unsafe_allow_html=True)

    st.markdown(
        """
<h2 class="form-title">Welcome Back! 👋</h2>
<p class="form-subtitle">Sign in to continue your learning journey</p>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form", clear_on_submit=False):
        email    = st.text_input("Email Address", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        col_rem, col_forgot = st.columns([1, 1])
        with col_rem:
            st.checkbox("Remember me")
        with col_forgot:
            st.markdown(
                '<div style="text-align:right;padding-top:5px;">'
                '<a href="#" style="color:#0d9488;font-size:0.86rem;font-weight:600;'
                'text-decoration:none;">Forgot password?</a></div>',
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "Log In", use_container_width=True, type="primary"
        )

    if submitted:
        # Prototype: any non-empty input proceeds
        if email.strip() and password.strip():
            st.session_state.screen = "account_type"
            st.rerun()
        else:
            st.error("Please enter your email and password.")

    # ── Social login (visual only for prototype) ──────────────────────────
    st.markdown('<div class="or-divider">or continue with</div>', unsafe_allow_html=True)

    col_g, col_a = st.columns(2)
    with col_g:
        if st.button("🔵  Continue with Google", use_container_width=True):
            st.session_state.screen = "account_type"
            st.rerun()
    with col_a:
        if st.button("🍎  Continue with Apple", use_container_width=True):
            st.session_state.screen = "account_type"
            st.rerun()

    st.markdown(
        """
<div style="text-align:center;margin-top:20px;font-size:0.9rem;color:#64748b;">
    New to NeuroLearn Kids?
    <a href="?go=account_type"
       style="color:#0d9488;font-weight:700;text-decoration:none;margin-left:4px;">
       Create an Account
    </a>
</div>
        """,
        unsafe_allow_html=True,
    )

    render_feature_bar()
    st.markdown("</div>", unsafe_allow_html=True)
    render_footer()


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 2 — ACCOUNT TYPE SELECTION
# ══════════════════════════════════════════════════════════════════════════════

def render_screen_account_type():
    st.markdown('<div class="right-card">', unsafe_allow_html=True)

    # ── Step indicator ─────────────────────────────────────────────────────
    st.markdown(
        """
<div class="steps">
    <div class="step-item">
        <div class="s-done">✓</div>
        <div class="s-label-done">Sign In</div>
    </div>
    <div class="s-line-done"></div>
    <div class="step-item">
        <div class="s-active">2</div>
        <div class="s-label-active">Choose Account Type</div>
    </div>
    <div class="s-line-idle"></div>
    <div class="step-item">
        <div class="s-idle">3</div>
        <div class="s-label-idle">Profile Setup</div>
    </div>
</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<h2 class="form-title">Who are you?</h2>
<p class="form-subtitle">
    Select the option that best describes you to personalise your NeuroLearn Kids experience.
</p>
        """,
        unsafe_allow_html=True,
    )

    # ── Role cards (HTML links — query param captures selection) ──────────
    st.markdown(
        """
<div class="role-grid">

  <a href="?role=parent" class="role-card rc-parent">
    <span class="rc-emoji">👨‍👩‍👧</span>
    <h4>Parent / Guardian</h4>
    <p>Support my child's learning journey and track their progress.</p>
    <span class="rc-arrow">→</span>
  </a>

  <a href="?role=teacher" class="role-card rc-teacher">
    <span class="rc-emoji">👩‍🏫</span>
    <h4>Teacher</h4>
    <p>Manage my classroom and support students' learning.</p>
    <span class="rc-arrow">→</span>
  </a>

  <a href="?role=student" class="role-card rc-student">
    <span class="rc-emoji">🧒</span>
    <h4>Student</h4>
    <p>I want to learn, practise and improve my reading skills.</p>
    <span class="rc-arrow">→</span>
  </a>

  <a href="?role=therapist" class="role-card rc-therapist">
    <span class="rc-emoji">👩‍⚕️</span>
    <h4>Specialist / Therapist</h4>
    <p>Assess and support learners with personalised interventions.</p>
    <span class="rc-arrow">→</span>
  </a>

</div>
        """,
        unsafe_allow_html=True,
    )

    # ── Security badge ─────────────────────────────────────────────────────
    st.markdown(
        """
<div class="security-badge">
    <span style="font-size:1.8rem;">🛡️</span>
    <div class="sb-text">
        <h5>Your data is safe with us</h5>
        <p>We use enterprise-grade security to protect your information
           and ensure complete privacy.</p>
    </div>
    <span class="sb-lock">🔒</span>
</div>
<div style="text-align:center;margin-top:14px;font-size:0.84rem;color:#64748b;">
    Not sure which to choose?
    <a href="#" style="color:#0d9488;font-weight:600;text-decoration:none;margin-left:4px;">
        Learn more about each option
    </a>
</div>
        """,
        unsafe_allow_html=True,
    )

    render_feature_bar()
    st.markdown("</div>", unsafe_allow_html=True)

    # Back button below the card
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("← Back to Login", key="back_btn"):
        st.session_state.screen = "login"
        st.rerun()

    render_footer()


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN: ROLE CONFIRMED (placeholder — shows chosen role before onboarding)
# ══════════════════════════════════════════════════════════════════════════════

_ROLE_META = {
    "parent":    {"icon": "👨‍👩‍👧", "label": "Parent / Guardian",     "next": "Set up child profile →"},
    "teacher":   {"icon": "👩‍🏫",  "label": "Teacher",                "next": "Set up your classroom →"},
    "student":   {"icon": "🧒",   "label": "Student",                 "next": "Start your journey →"},
    "therapist": {"icon": "👩‍⚕️", "label": "Specialist / Therapist",  "next": "Set up your workspace →"},
}


def render_screen_role_confirmed():
    meta = _ROLE_META.get(st.session_state.user_role or "parent", _ROLE_META["parent"])
    st.markdown('<div class="right-card">', unsafe_allow_html=True)
    st.markdown(
        f"""
<div class="confirmed-banner">
    <div class="cb-icon">{meta['icon']}</div>
    <h2>Great choice, {meta['label']}!</h2>
    <p>Your account type has been selected.<br>
       Next step: complete your profile to get started.</p>
</div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(meta["next"], use_container_width=True, type="primary"):
            st.info("Next onboarding screen — coming in the next build.")
        if st.button("← Change role", use_container_width=True, key="change_role"):
            st.session_state.screen = "account_type"
            st.session_state.user_role = None
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    render_footer()


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    inject_css()

    left_col, right_col = st.columns([1, 2.2])

    with left_col:
        render_brand_panel()

    with right_col:
        screen = st.session_state.screen
        if screen == "login":
            render_screen_login()
        elif screen == "account_type":
            render_screen_account_type()
        elif screen == "role_confirmed":
            render_screen_role_confirmed()
        else:
            render_screen_login()


if __name__ == "__main__":
    main()
