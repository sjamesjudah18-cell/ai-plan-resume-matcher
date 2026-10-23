import streamlit as st

from modules.resume_parser import extract_resume_text
from modules.job_parser import extract_job_requirements
from modules.matcher import calculate_overall_match
from modules.ai_analyzer import analyze_resume_with_ai
from modules.skill_gap import analyze_skill_gap
from modules.ats_analyzer import analyze_ats
from modules.roadmap_generator import generate_learning_roadmap
from modules.resume_rewriter import rewrite_resume_section
from modules.career_copilot import ask_career_copilot


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Plan Resume Matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

    :root {
        --bg:#071525;
        --surface:#102238;
        --surface-soft:#0d1d30;
        --ink:#edf3f8;
        --muted:#aab8c8;
        --muted-2:#8292a5;
        --line:#29415c;
        --navy:#0b1728;
        --navy-2:#10243a;
        --accent:#ff8a3d;
        --accent-soft:#2b211b;
        --success:#62d6a7;
    }

    html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
    .stApp { background:var(--bg) !important; color:var(--ink) !important; }
    .main .block-container { max-width:1480px; padding:0 2.2rem 3.5rem; }
    [data-testid="stHeader"] { background:transparent !important; }
    [data-testid="stToolbar"] { display:none; }
    [data-testid="stSidebar"] { display:none; }

    /* Strong global text contrast */
    .main p, .main span, .main label, .main li, .main small,
    .main div[data-testid="stMarkdownContainer"] { color:var(--ink); }
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 { color:var(--ink) !important; }

    .top-nav { height:76px; display:flex; align-items:center; justify-content:space-between; border-bottom:1px solid var(--line); margin-bottom:3.4rem; }
    .brand { display:flex; align-items:center; gap:.55rem; font-weight:700; font-size:.92rem; color:var(--ink) !important; }
    .brand-mark { color:var(--accent) !important; font-size:1.55rem; line-height:1; }
    .nav-links { display:flex; align-items:center; gap:2rem; color:var(--muted) !important; font-size:.75rem; }
    .nav-links span { white-space:nowrap; color:var(--muted) !important; }
    .nav-user { display:flex; align-items:center; gap:.55rem; font-size:.78rem; color:var(--ink) !important; }
    .avatar { width:27px; height:27px; border-radius:50%; background:var(--navy); color:white !important; display:grid; place-items:center; font-size:.65rem; font-weight:700; }
    .nav-cta { background:var(--navy); color:#fff !important; border-radius:999px; padding:.62rem 1.05rem; font-size:.72rem; font-weight:700; }

    /* Circular contour pattern — preserved */
    .contour { position:relative; overflow:hidden; }
    .contour::after {
        content:""; position:absolute; width:440px; height:440px; right:-120px; top:-130px;
        pointer-events:none; opacity:.55;
        background:repeating-radial-gradient(ellipse at 60% 40%, transparent 0 13px, rgba(255,107,53,.25) 14px 15px, transparent 16px 27px);
        transform:rotate(-18deg);
    }

    .hero-wrap { min-height:440px; display:flex; align-items:center; padding:1rem 0 2.7rem; position:relative; }
    .hero-copy { max-width:780px; position:relative; z-index:2; }
    .eyebrow { display:inline-flex; align-items:center; gap:.5rem; padding:.38rem .72rem; border:1px solid var(--line); border-radius:999px; background:var(--surface); font-size:.69rem; font-weight:700; color:var(--ink) !important; }
    .eyebrow-dot { width:7px; height:7px; border-radius:50%; background:var(--accent); }
    .hero-title { font-family:'Playfair Display',Georgia,serif; font-size:clamp(3.4rem,6vw,5.9rem); line-height:.93; letter-spacing:-.055em; margin:1.25rem 0; color:var(--ink) !important; font-weight:600; }
    .hero-title .accent { color:var(--accent) !important; font-style:italic; }
    .hero-subtitle { max-width:620px; color:var(--muted) !important; font-size:1rem; line-height:1.75; margin-bottom:1.5rem; }
    .hero-actions { display:flex; align-items:center; gap:1.15rem; }
    .hero-actions span:last-child { color:var(--muted) !important; }
    .hero-note { position:absolute; right:2%; bottom:7%; max-width:155px; font-family:'Playfair Display',Georgia,serif; font-style:italic; font-size:.86rem; transform:rotate(-7deg); color:var(--ink) !important; }
    .hero-note::after { content:'↘'; display:block; color:var(--accent); font-size:1.6rem; }

    /* Main section banners: dark enough for guaranteed contrast */
    .section-banner {
        position:relative; overflow:hidden; background:var(--navy); color:#fff;
        border-radius:18px; padding:1.7rem 2rem 1.6rem; margin:0 0 1.5rem;
        min-height:150px; display:flex; flex-direction:column; justify-content:center;
        box-shadow:0 12px 28px rgba(0,0,0,.25);
    }
    .section-banner::after {
        content:''; position:absolute; width:390px; height:390px; right:-75px; top:-165px;
        opacity:.6; pointer-events:none;
        background:repeating-radial-gradient(ellipse at 55% 55%, transparent 0 13px, rgba(255,107,53,.27) 14px 15px, transparent 16px 28px);
        transform:rotate(-18deg);
    }
    .section-banner > * { position:relative; z-index:1; }
    .section-banner .section-kicker { color:#ff9a76 !important; margin-bottom:.35rem; }
    .section-banner .section-title { color:#ffffff !important; }
    .section-banner .section-subtitle { color:#c3d0df !important; max-width:760px; margin-bottom:0; }

    .section-kicker { font-size:.66rem; font-weight:800; color:var(--accent) !important; letter-spacing:.12em; text-transform:uppercase; margin-bottom:.45rem; }
    .section-title { font-family:'Playfair Display',Georgia,serif; font-size:2.45rem; line-height:1.02; letter-spacing:-.035em; color:var(--ink) !important; margin:0; }
    .section-subtitle { color:var(--muted) !important; font-size:.9rem; line-height:1.65; margin:.55rem 0 1.4rem; }

    /* Tool headers */
    .tool-header {
        position:relative; overflow:hidden; background:var(--navy-2); color:#fff;
        border-radius:16px; padding:1.15rem 1.45rem; margin:0 0 1.25rem;
        box-shadow:0 8px 20px rgba(0,0,0,.25);
    }
    .tool-header::after {
        content:''; position:absolute; width:220px; height:220px; right:-65px; top:-110px;
        opacity:.55; pointer-events:none;
        background:repeating-radial-gradient(ellipse at center, transparent 0 11px, rgba(255,107,53,.24) 12px 13px, transparent 14px 24px);
    }
    .tool-header h3 { position:relative; z-index:1; margin:0; color:#fff !important; font-family:'Playfair Display',Georgia,serif; font-size:1.7rem; }
    .tool-header p { position:relative; z-index:1; margin:.35rem 0 0; color:#c3d0df !important; font-size:.82rem; }

    /* Completely remove the old stats strip */
    .stat-strip { display:none !important; }

    .glass-card, .feature-card { background:var(--surface) !important; border:1px solid var(--line); border-radius:15px; padding:1.25rem; }
    .glass-card { min-height:150px; }
    .glass-card h3 { color:var(--ink) !important; margin-bottom:.5rem; }
    .glass-card p { color:var(--muted) !important; line-height:1.6; }

    /* Inputs: force readable text in every Streamlit child */
    textarea, input { border-radius:12px !important; background:#0c1b2d !important; border:1px solid #38536f !important; color:var(--ink) !important; -webkit-text-fill-color:var(--ink) !important; }
    textarea:focus, input:focus { border-color:var(--accent) !important; box-shadow:0 0 0 1px var(--accent) !important; }
    textarea::placeholder, input::placeholder { color:#8fa1b5 !important; opacity:1 !important; }
    label { color:var(--ink) !important; font-size:.78rem !important; font-weight:700 !important; }

    /* File uploader: no dark/hidden text */
    div[data-testid="stFileUploader"] { border:1px dashed #38536f !important; border-radius:12px; background:#102238 !important; padding:.45rem; }
    div[data-testid="stFileUploader"] * { color:var(--ink) !important; }
    div[data-testid="stFileUploader"] section { background:#102238 !important; }
    div[data-testid="stFileUploader"] button { background:#18304a !important; color:var(--ink) !important; border:1px solid #38536f !important; }
    div[data-testid="stFileUploader"] small { color:var(--muted) !important; }

    /* Buttons */
    .stButton > button { border-radius:999px !important; min-height:2.65rem; padding:0 1.15rem !important; font-weight:700 !important; border:1px solid var(--navy) !important; background:var(--navy) !important; color:white !important; transition:.2s ease !important; }
    .stButton > button:hover { transform:translateY(-1px); background:#1d2939 !important; border-color:#1d2939 !important; }
    .stButton > button[kind="primary"] { background:#35536f !important; border-color:#4a6b89 !important; color:#f4f7fa !important; box-shadow:0 8px 22px rgba(0,0,0,.20) !important; }
     .stButton > button[kind="primary"]:hover { background:#456984 !important; border-color:#5b7d99 !important; box-shadow:0 10px 26px rgba(0,0,0,.26) !important; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap:.35rem; background:transparent; border-bottom:1px solid var(--line); }
    .stTabs [data-baseweb="tab"] { border-radius:999px; padding:.65rem 1rem; color:var(--muted) !important; font-weight:700; font-size:.76rem; }
    .stTabs [data-baseweb="tab"] p { color:inherit !important; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color:#fff !important; background:var(--navy); }
    .stTabs [data-baseweb="tab"][aria-selected="true"] p { color:#fff !important; }
    .stTabs [data-baseweb="tab-highlight"] { display:none; }
    .stTabs [data-baseweb="tab-panel"] { padding-top:1.8rem; }

    [data-testid="stMetric"] { background:var(--surface) !important; border:1px solid var(--line); border-radius:14px; padding:1rem; }
    [data-testid="stMetricLabel"] { color:var(--muted) !important; }
    [data-testid="stMetricValue"] { color:var(--ink) !important; }
    .metric-card { background:var(--surface) !important; border:1px solid var(--line); border-radius:14px; padding:1.1rem; text-align:left; }
    .metric-label { color:var(--muted) !important; font-size:.72rem; }
    .metric-value { color:var(--ink) !important; font-family:'Playfair Display',Georgia,serif; font-size:2rem; margin-top:.25rem; }

    .status-pill { display:inline-block; padding:.4rem .7rem; border-radius:999px; background:#0e2b25; border:1px solid #245e4b; color:var(--success) !important; font-size:.72rem; font-weight:700; }
    .career-tools-panel { background:#0d1d30; border:1px solid var(--line); border-radius:18px; padding:1.35rem; box-shadow:0 12px 30px rgba(0,0,0,.22); }
    .career-tools-title { font-family:'Playfair Display',Georgia,serif; font-size:2rem; line-height:1.02; color:#fff !important; margin-bottom:.55rem; }
    .career-tools-subtitle { color:var(--muted) !important; font-size:.78rem; line-height:1.55; margin-bottom:1.1rem; }
    .feature-card { min-height:108px; transition:.2s; margin-bottom:.65rem; }
    .feature-card:hover { transform:translateY(-2px); box-shadow:0 12px 28px rgba(0,0,0,.28); }
    .feature-card.dark { background:var(--navy) !important; border-color:#273244; color:#fff; }
    .feature-card h3 { font-size:.98rem; margin:.55rem 0 .35rem; color:var(--ink) !important; }
    .feature-card p { color:var(--muted) !important; font-size:.76rem; line-height:1.55; }
    .feature-card.dark h3 { color:#fff !important; }
    .feature-card.dark p { color:#c3d0df !important; }
    .icon-bubble { width:34px; height:34px; border-radius:50%; display:grid; place-items:center; background:var(--accent-soft); color:var(--accent) !important; font-weight:800; }

    /* Floating Career Copilot */
    div[data-testid="stPopover"] {
        position:fixed !important; right:28px !important; bottom:24px !important; z-index:9999 !important;
    }
    div[data-testid="stPopover"] > button {
        width:62px !important; height:62px !important; min-width:62px !important;
        border-radius:50% !important; padding:0 !important;
        background:#263f58 !important; color:#f4f7fa !important;
        border:1px solid #5d7892 !important;
        box-shadow:0 12px 30px rgba(0,0,0,.38) !important;
        font-size:1.55rem !important;
    }
    div[data-testid="stPopover"] > button:hover { background:#304d69 !important; transform:translateY(-2px); }
    div[data-testid="stPopoverBody"] {
        background:#0d1d30 !important; border:1px solid #38536f !important;
        border-radius:18px !important; width:460px !important; max-width:calc(100vw - 32px) !important;
    }
    .copilot-chat-title { font-family:'Playfair Display',Georgia,serif; font-size:1.35rem; color:#fff; margin-bottom:.2rem; }
    .copilot-chat-subtitle { color:#aab8c8; font-size:.75rem; margin-bottom:1rem; }
    .copilot-message-user { background:#18304a; border:1px solid #38536f; border-radius:14px 14px 4px 14px; padding:.75rem .85rem; margin:.45rem 0 .45rem 2rem; color:#edf3f8; font-size:.82rem; }
    .copilot-message-ai { background:#102238; border:1px solid #29415c; border-radius:14px 14px 14px 4px; padding:.75rem .85rem; margin:.45rem 2rem .45rem 0; color:#edf3f8; font-size:.86rem; line-height:1.6; }
    .copilot-status { color:#8fa1b5; font-size:.7rem; margin-top:.3rem; }

    .quote-panel { background:var(--navy); color:#fff; border-radius:18px; padding:2rem; margin:2rem 0; position:relative; overflow:hidden; }
    .quote-panel h2 { font-family:'Playfair Display',Georgia,serif; font-size:2rem; max-width:560px; margin:0; color:#fff !important; }
    .quote-panel p { color:#c3d0df !important; }
    details { border-radius:12px !important; border:1px solid var(--line) !important; background:#0d1d30 !important; }
    details summary { color:var(--ink) !important; }
    .stAlert { border-radius:12px !important; }
    hr { border-color:var(--line) !important; }
    .footer { text-align:center; color:#8fa1b5 !important; padding:2.5rem 0 1rem; font-size:.72rem; }

    /* Streamlit markdown/content fallback */
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] li { color:var(--ink) !important; }
    .main .stCaption, .main [data-testid="stCaptionContainer"] p { color:var(--muted) !important; }

    /* ========================================================
       DARK BLUE APPLICATION THEME
       ======================================================== */
    .stApp, .main, [data-testid="stAppViewContainer"] { background:var(--bg) !important; }
    .main .block-container { color:var(--ink) !important; }
    .stMarkdown, .stText, .stCaption, .stSelectbox, .stTextInput, .stTextArea, .stNumberInput, .stMultiSelect, .stRadio, .stCheckbox { color:var(--ink) !important; }
    div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"] { background:#0c1b2d !important; border-color:#38536f !important; }
    div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea, div[data-baseweb="select"] * { color:#edf3f8 !important; -webkit-text-fill-color:#edf3f8 !important; }
    div[data-baseweb="select"] { border-radius:12px !important; }
    div[role="listbox"], ul[role="listbox"] { background:#102238 !important; color:#edf3f8 !important; }
    div[role="option"] { color:#edf3f8 !important; background:#102238 !important; }
    div[role="option"]:hover { background:#18304a !important; }
    [data-testid="stExpander"] { background:#0d1d30 !important; border:1px solid #29415c !important; border-radius:14px !important; }
    [data-testid="stExpander"] summary, [data-testid="stExpander"] summary p { color:#edf3f8 !important; }
    .stAlert { background:#12273d !important; border:1px solid #29415c !important; color:#edf3f8 !important; }
    .stAlert p, .stAlert span { color:#edf3f8 !important; }
    [data-testid="stSpinner"] { color:#edf3f8 !important; }
    .stProgress > div > div > div > div { background:var(--accent) !important; }
    .stProgress > div > div { background:#243b54 !important; }
    [data-testid="stFileUploaderDropzoneInstructions"] * { color:#c3d0df !important; }
    [data-testid="stFileUploaderDropzone"] { background:#0c1b2d !important; }
    .stCheckbox label, .stRadio label { color:#edf3f8 !important; }
    .stCheckbox span, .stRadio span { color:#edf3f8 !important; }
    .stTabs [data-baseweb="tab-list"] { background:#0d1d30 !important; border:1px solid #29415c; border-radius:999px; padding:.3rem; }
    .stTabs [data-baseweb="tab"] { color:#aab8c8 !important; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { background:#35536f !important; color:#ffffff !important; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] p { color:#ffffff !important; }
    .footer { color:#8292a5 !important; }
    hr { border-color:#29415c !important; }

    @media(max-width:900px){
        .main .block-container{padding:0 1rem 2.5rem}
        .nav-links{display:none}
        .hero-title{font-size:3.2rem}
    }
    </style>
    """,
    unsafe_allow_html=True
)


# SESSION STATE
# ============================================================

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "resume_file_name" not in st.session_state:
    st.session_state.resume_file_name = ""

if "job_analysis" not in st.session_state:
    st.session_state.job_analysis = None

if "match_result" not in st.session_state:
    st.session_state.match_result = None

if "ai_analysis" not in st.session_state:
    st.session_state.ai_analysis = None

if "skill_gap" not in st.session_state:
    st.session_state.skill_gap = None

if "ats_result" not in st.session_state:
    st.session_state.ats_result = None

if "roadmap" not in st.session_state:
    st.session_state.roadmap = None

if "rewrite_result" not in st.session_state:
    st.session_state.rewrite_result = None

if "copilot_result" not in st.session_state:
    st.session_state.copilot_result = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">
                📄 Plan Resume Matcher
            </div>
            <div class="sidebar-brand-subtitle">
                AI-powered career intelligence
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🧭 Features")

    sidebar_features = [
        "📄 Resume Parsing",
        "🎯 Resume Matching",
        "📈 ATS Simulation",
        "🤖 AI Copilot AI Analysis",
        "🧠 Skill Gap",
        "📚 Learning Roadmap",
        "✍️ Resume Rewriter",
        "🎤 Career Copilot",
    ]

    for feature in sidebar_features:

        st.markdown(
            f'<div class="sidebar-item">{feature}</div>',
            unsafe_allow_html=True
        )

    st.divider()

    st.markdown("### 📌 Current Session")

    if st.session_state.resume_file_name:

        st.success(
            f"✓ {st.session_state.resume_file_name}"
        )

    else:

        st.info(
            "No resume uploaded yet."
        )

    if st.session_state.job_analysis:

        st.success(
            "✓ Job description analyzed"
        )

    else:

        st.info(
            "Job description not analyzed"
        )

    st.divider()

    st.caption(
        "Built with Streamlit • Groq • ElevenLabs"
    )


st.markdown(
    """
    <div class="top-nav">
        <div class="brand"><span class="brand-mark">✦</span> Plan Resume Matcher</div>
        <div class="nav-links"><span>Features</span><span>How It Works</span><span>About</span><span class="nav-cta">Get Started →</span></div>
        <div class="nav-user"><span class="avatar">J</span><span>James⌄</span></div>
    </div>
    """, unsafe_allow_html=True
)

# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero-wrap contour">
        <div class="hero-copy">
            <div class="eyebrow"><span class="eyebrow-dot"></span> AI POWERED CAREER ASSISTANT</div>
            <div class="hero-title">Your Resume<br>Has <span class="accent">Potential.</span></div>
            <div class="hero-subtitle">Go beyond the basics. Get AI-powered insights, match with your ideal jobs, and build a career you’ll love.</div>
            <div class="hero-actions"><span class="nav-cta">Start Analysis →</span><span style="font-size:.78rem;color:#4d5552;">◉ &nbsp; See How It Works</span></div>
        </div>
        <div class="hero-note">Better matches.<br>Bigger opportunities.</div>
    </div>
    """, unsafe_allow_html=True
)


# ============================================================
# INPUT AREA
# ============================================================

st.markdown(
    '''
    <div class="section-banner">
        <div class="section-kicker">01 / RESUME INTELLIGENCE</div>
        <div class="section-title">Upload. Analyze.<br>Get Matched.</div>
        <div class="section-subtitle">Upload your resume and job description to get a complete AI-powered analysis with actionable insights.</div>
    </div>
    ''',
    unsafe_allow_html=True
)

input_col1, input_col2 = st.columns(
    [1, 1],
    gap="large"
)


# ============================================================
# RESUME INPUT
# ============================================================

with input_col1:

    st.markdown(
        """
        <div class="glass-card">
            <h3>📄 Your Resume</h3>
            <p>
                Upload your latest resume as a PDF.
                The system will extract the content automatically.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"],
        key="resume_upload"
    )

    if uploaded_file is not None:

        if (
            st.session_state.resume_file_name
            != uploaded_file.name
        ):

            try:

                resume_text = extract_resume_text(
                    uploaded_file
                )

                st.session_state.resume_text = (
                    resume_text
                )

                st.session_state.resume_file_name = (
                    uploaded_file.name
                )

                st.session_state.match_result = None
                st.session_state.ai_analysis = None
                st.session_state.skill_gap = None
                st.session_state.ats_result = None
                st.session_state.roadmap = None
                st.session_state.rewrite_result = None
                st.session_state.copilot_result = None

                st.success(
                    "Resume processed successfully!"
                )

            except Exception as e:

                st.error(
                    f"Resume processing error: {e}"
                )

    if st.session_state.resume_text:

        st.markdown(
            '<span class="status-pill">✓ Resume Ready</span>',
            unsafe_allow_html=True
        )

        with st.expander(
            "👀 Preview Extracted Resume"
        ):

            st.text(
                st.session_state.resume_text
            )


# ============================================================
# JOB INPUT
# ============================================================

with input_col2:

    st.markdown(
        """
        <div class="glass-card">
            <h3>💼 Target Job</h3>
            <p>
                Paste the complete job description.
                AI will use it as the target for your analysis.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    job_description = st.text_area(
        "Paste Job Description",
        height=235,
        placeholder=(
            "Example:\n\n"
            "Junior Full Stack AI Developer\n\n"
            "Requirements:\n"
            "- Python\n"
            "- React\n"
            "- FastAPI\n"
            "- SQL\n"
            "- Git\n"
            "- Machine Learning"
        ),
        key="job_description_input"
    )


# ============================================================
# ANALYZE JOB
# ============================================================

st.write("")

if st.button(
    "🔎 Analyze Target Job",
    use_container_width=True,
    type="primary"
):

    if not job_description.strip():

        st.warning(
            "Please enter a job description first."
        )

    else:

        with st.spinner(
            "Analyzing target job..."
        ):

            job_analysis = extract_job_requirements(
                job_description
            )

            st.session_state.job_analysis = (
                job_analysis
            )

            st.session_state.match_result = None
            st.session_state.ai_analysis = None
            st.session_state.skill_gap = None
            st.session_state.ats_result = None
            st.session_state.roadmap = None
            st.session_state.rewrite_result = None
            st.session_state.copilot_result = None

        st.success(
            "Target job analyzed successfully!"
        )


# ============================================================
# JOB REQUIREMENT SUMMARY
# ============================================================

if st.session_state.job_analysis:

    job_analysis = (
        st.session_state.job_analysis
    )

    required_skills = job_analysis.get(
        "skills",
        []
    )

    experience_years = job_analysis.get(
        "experience_years"
    )

    summary_col1, summary_col2 = st.columns(
        [3, 1]
    )

    with summary_col1:

        st.markdown(
            "### 📋 Detected Job Requirements"
        )

        if required_skills:

            st.write(
                " • ".join(
                    skill.title()
                    for skill in required_skills
                )
            )

        else:

            st.info(
                "No technical skills were detected."
            )

    with summary_col2:

        if experience_years is not None:

            st.metric(
                "Experience",
                f"{experience_years}+ yrs"
            )

        else:

            st.metric(
                "Experience",
                "Not specified"
            )


# ============================================================
# MAIN ANALYSIS BUTTON
# ============================================================

st.divider()

st.markdown(
    '''
    <div class="section-banner">
        <div class="section-kicker">02 / MATCH INTELLIGENCE</div>
        <div class="section-title">Your Resume Analysis</div>
        <div class="section-subtitle">See how closely your resume aligns with the target role and where you can improve.</div>
    </div>
    ''',
    unsafe_allow_html=True
)

if st.button(
    "🚀 Match My Resume",
    use_container_width=True,
    type="primary"
):

    if not st.session_state.resume_text:

        st.warning(
            "Please upload your resume first."
        )

    elif not job_description.strip():

        st.warning(
            "Please enter a job description first."
        )

    else:

        with st.spinner(
            "Calculating your resume-job match..."
        ):

            try:

                job_analysis = extract_job_requirements(
                    job_description
                )

                required_skills = job_analysis.get(
                    "skills",
                    []
                )

                result = calculate_overall_match(
                    st.session_state.resume_text,
                    job_description,
                    required_skills
                )

                st.session_state.match_result = (
                    result
                )

                st.success(
                    "Resume matching completed!"
                )

            except Exception as e:

                st.error(
                    f"Matching error: {e}"
                )


# ============================================================
# MATCH DASHBOARD
# ============================================================

if st.session_state.match_result:

    result = (
        st.session_state.match_result
    )

    st.markdown(
        "### 📊 Your Match Overview"
    )

    metric1, metric2, metric3 = st.columns(
        3
    )

    with metric1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    🎯 Overall Match
                </div>
                <div class="metric-value">
                    {result["overall_score"]}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with metric2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    🛠️ Skill Match
                </div>
                <div class="metric-value">
                    {result["skill_score"]}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with metric3:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    🧠 Semantic Similarity
                </div>
                <div class="metric-value">
                    {result["semantic_score"]}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    st.progress(
        result["overall_score"] / 100
    )

    match_col1, match_col2 = st.columns(
        2
    )

    with match_col1:

        st.markdown(
            "### ✅ Matched Skills"
        )

        matched_skills = result.get(
            "matched_skills",
            []
        )

        if matched_skills:

            for skill in matched_skills:

                st.success(
                    skill.title()
                )

        else:

            st.info(
                "No matched skills detected."
            )

    with match_col2:

        st.markdown(
            "### ❌ Missing Skills"
        )

        missing_skills = result.get(
            "missing_skills",
            []
        )

        if missing_skills:

            for skill in missing_skills:

                st.error(
                    skill.title()
                )

        else:

            st.success(
                "No missing skills detected!"
            )


career_tools_col, tools_content_col = st.columns([0.30, 0.70], gap="large")

with career_tools_col:

    st.markdown(
        """<div class="career-tools-panel">
<div class="section-kicker">03 / CAREER TOOLS</div>
<div class="career-tools-title">Everything You Need<br>for Your Career</div>
<div class="career-tools-subtitle">Six focused tools to improve your resume, skills, preparation, and job readiness.</div>

<div class="feature-card"><div class="icon-bubble">▣</div><h3>ATS Simulator</h3><p>Check how your resume performs with ATS-style checks.</p></div>
<div class="feature-card"><div class="icon-bubble">◉</div><h3>Skill Gap Analysis</h3><p>Find missing skills and understand what to learn next.</p></div>
<div class="feature-card"><div class="icon-bubble">✦</div><h3>Learning Roadmap</h3><p>Get a personalized learning plan based on your target job.</p></div>
<div class="feature-card"><div class="icon-bubble">▤</div><h3>Resume Rewriter</h3><p>Optimize your resume for better results without inventing facts.</p></div>
<div class="feature-card"><div class="icon-bubble">◈</div><h3>Career Copilot</h3><p>Get AI support for interview prep, career advice and more.</p></div>
<div class="feature-card"><div class="icon-bubble">↗</div><h3>Job Intelligence</h3><p>Understand your profile against the opportunities you target.</p></div>
</div>""",
        unsafe_allow_html=True
    )

with tools_content_col:

# FEATURE TABS
# ============================================================

    st.divider()

    tabs = st.tabs(
        [
            "📈 ATS",
            "🤖 AI Analysis",
            "🧠 Skill Gap",
            "📚 Roadmap",
            "✍️ Rewriter"
        ]
    )


    # ============================================================
    # TAB 1 — ATS
    # ============================================================

    with tabs[0]:

        st.markdown(
            """
            <div class="tool-header">
                <h3>📈 ATS Resume Simulator</h3>
                <p>Simulate common ATS-style checks against your target job.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.info(
            "This is a heuristic simulation. Different ATS platforms "
            "use different parsing and ranking methods."
        )

        if st.button(
            "📊 Run ATS Analysis",
            use_container_width=True,
            key="run_ats"
        ):

            if not st.session_state.resume_text:

                st.warning(
                    "Please upload your resume first."
                )

            elif not job_description.strip():

                st.warning(
                    "Please enter a job description first."
                )

            else:

                with st.spinner(
                    "Running ATS simulation..."
                ):

                    try:

                        ats_result = analyze_ats(
                            st.session_state.resume_text,
                            job_description
                        )

                        st.session_state.ats_result = (
                            ats_result
                        )

                        st.success(
                            "ATS analysis completed!"
                        )

                    except Exception as e:

                        st.error(
                            f"ATS analysis error: {e}"
                        )

        if st.session_state.ats_result:

            ats = (
                st.session_state.ats_result
            )

            ats_score = ats.get(
                "ats_score",
                0
            )

            st.markdown(
                "### 🎯 ATS Score"
            )

            ats_col1, ats_col2 = st.columns(
                [1, 2]
            )

            with ats_col1:

                st.metric(
                    "Simulated ATS Score",
                    f"{ats_score}/100"
                )

            with ats_col2:

                st.progress(
                    ats_score / 100
                )

            st.markdown(
                "### 📊 Score Breakdown"
            )

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "Keyword Coverage",
                    f"{ats['keyword_score']}%"
                )

            with c2:

                st.metric(
                    "Resume Structure",
                    f"{ats['structure_score']}%"
                )

            with c3:

                st.metric(
                    "Job Alignment",
                    f"{ats['job_alignment_score']}%"
                )

            st.markdown(
                "### 🔑 Keyword Analysis"
            )

            st.write(
                f"**Job keywords detected:** "
                f"{ats.get('total_keywords', 0)}"
            )

            matched_keywords = ats.get(
                "matched_keywords",
                []
            )

            missing_keywords = ats.get(
                "missing_keywords",
                []
            )

            keyword_col1, keyword_col2 = st.columns(2)

            with keyword_col1:

                st.write(
                    "#### ✅ Matched"
                )

                if matched_keywords:

                    for keyword in matched_keywords:

                        st.success(
                            keyword.title()
                        )

                else:

                    st.info(
                        "No matched keywords."
                    )

            with keyword_col2:

                st.write(
                    "#### ❌ Missing"
                )

                if missing_keywords:

                    for keyword in missing_keywords:

                        st.error(
                            keyword.title()
                        )

                else:

                    st.success(
                        "No missing keywords."
                    )

            st.markdown(
                "### 📄 Resume Structure"
            )

            st.write(
                f"**Extracted word count:** "
                f"{ats.get('word_count', 0)}"
            )

            detected_sections = ats.get(
                "detected_sections",
                []
            )

            if detected_sections:

                st.write(
                    "#### ✅ Detected Sections"
                )

                for section in detected_sections:

                    st.success(
                        section
                    )

            structure_checks = ats.get(
                "structure_checks",
                []
            )

            if structure_checks:

                st.write(
                    "#### 👍 ATS-Friendly Checks"
                )

                for check in structure_checks:

                    st.success(
                        check
                    )

            structure_warnings = ats.get(
                "structure_warnings",
                []
            )

            if structure_warnings:

                st.write(
                    "#### ⚠️ ATS Warnings"
                )

                for warning in structure_warnings:

                    st.warning(
                        warning
                    )

            st.markdown(
                "### 💡 Improvement Suggestions"
            )

            suggestions = ats.get(
                "suggestions",
                []
            )

            if suggestions:

                for suggestion in suggestions:

                    st.info(
                        suggestion
                    )

            else:

                st.success(
                    "No major ATS improvements detected."
                )


    # ============================================================
    # TAB 2 — AI ANALYSIS
    # ============================================================

    with tabs[1]:

        st.markdown(
            """
            <div class="tool-header">
                <h3>🤖 AI Resume Analysis</h3>
                <p>Get a recruiter-style analysis of your resume against the target role.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "✨ Analyze My Resume with AI",
            use_container_width=True,
            key="run_ai_analysis"
        ):

            if not st.session_state.resume_text:

                st.warning(
                    "Please upload your resume first."
                )

            elif not job_description.strip():

                st.warning(
                    "Please enter a job description first."
                )

            else:

                with st.spinner(
                    "Groq is analyzing your resume..."
                ):

                    try:

                        ai_result = analyze_resume_with_ai(
                            st.session_state.resume_text,
                            job_description
                        )

                        if ai_result.get(
                            "success"
                        ):

                            st.session_state.ai_analysis = (
                                ai_result.get(
                                    "analysis",
                                    {}
                                )
                            )

                            st.success(
                                "AI analysis completed!"
                            )

                        else:

                            st.session_state.ai_analysis = None

                            st.error(
                                ai_result.get(
                                    "error",
                                    "AI analysis failed."
                                )
                            )

                    except Exception as e:

                        st.session_state.ai_analysis = None

                        st.error(
                            f"AI Analysis Error: {e}"
                        )

        if st.session_state.ai_analysis:

            analysis = (
                st.session_state.ai_analysis
            )

            candidate_profile = analysis.get(
                "candidate_profile",
                {}
            )

            st.markdown(
                "### 👤 Candidate Profile"
            )

            p1, p2 = st.columns(2)

            with p1:

                st.write(
                    f"**Name:** "
                    f"{candidate_profile.get('name', 'Not specified')}"
                )

                st.write(
                    f"**Education:** "
                    f"{candidate_profile.get('education', 'Not specified')}"
                )

            with p2:

                st.write(
                    f"**Experience:** "
                    f"{candidate_profile.get('experience', 'Not specified')}"
                )

                st.write(
                    f"**Projects:** "
                    f"{candidate_profile.get('projects', 'Not specified')}"
                )

            st.markdown(
                "### 🎯 Job Fit"
            )

            job_fit = analysis.get(
                "job_fit",
                {}
            )

            st.write(
                f"**Fit Level:** "
                f"{job_fit.get('fit_level', 'Not specified')}"
            )

            if job_fit.get("summary"):

                st.write(
                    job_fit["summary"]
                )

            ai_sections = [
                (
                    "🛠️ Skills Identified",
                    "skills",
                    "write"
                ),
                (
                    "💪 Strengths",
                    "strengths",
                    "success"
                ),
                (
                    "⚠️ Weaknesses",
                    "weaknesses",
                    "warning"
                ),
                (
                    "📄 Resume Issues",
                    "resume_issues",
                    "error"
                ),
                (
                    "💡 Improvement Suggestions",
                    "improvement_suggestions",
                    "info"
                ),
                (
                    "📚 Recommended Learning",
                    "recommended_learning",
                    "write"
                ),
                (
                    "🎤 Interview Focus",
                    "interview_focus",
                    "write"
                )
            ]

            for title, key, display_type in ai_sections:

                st.markdown(
                    f"### {title}"
                )

                items = analysis.get(
                    key,
                    []
                )

                if items:

                    for item in items:

                        if display_type == "success":

                            st.success(
                                f"✓ {item}"
                            )

                        elif display_type == "warning":

                            st.warning(
                                f"• {item}"
                            )

                        elif display_type == "error":

                            st.error(
                                f"• {item}"
                            )

                        elif display_type == "info":

                            st.info(
                                f"• {item}"
                            )

                        else:

                            st.write(
                                f"• {item}"
                            )

                else:

                    st.info(
                        "No information returned."
                    )


    # ============================================================
    # TAB 3 — SKILL GAP
    # ============================================================

    with tabs[2]:

        st.markdown(
            """
            <div class="tool-header">
                <h3>🧠 Skill Gap Analysis</h3>
                <p>Find the technical skills required by the job that are missing from your resume.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "🔍 Analyze My Skill Gap",
            use_container_width=True,
            key="run_skill_gap"
        ):

            if not st.session_state.resume_text:

                st.warning(
                    "Please upload your resume first."
                )

            elif not job_description.strip():

                st.warning(
                    "Please enter a job description first."
                )

            else:

                with st.spinner(
                    "Analyzing your skill gap..."
                ):

                    try:

                        skill_gap = analyze_skill_gap(
                            st.session_state.resume_text,
                            job_description
                        )

                        st.session_state.skill_gap = (
                            skill_gap
                        )

                        st.success(
                            "Skill gap analysis completed!"
                        )

                    except Exception as e:

                        st.error(
                            f"Skill gap analysis error: {e}"
                        )

        if st.session_state.skill_gap:

            skill_gap = (
                st.session_state.skill_gap
            )

            coverage = skill_gap.get(
                "coverage_score",
                0
            )

            required = skill_gap.get(
                "required_skills",
                []
            )

            st.markdown(
                "### 📊 Skill Coverage"
            )

            sg1, sg2 = st.columns(2)

            with sg1:

                st.metric(
                    "Required Skill Coverage",
                    f"{coverage}%"
                )

            with sg2:

                st.metric(
                    "Required Skills",
                    len(required)
                )

            st.progress(
                coverage / 100
            )

            skill_col1, skill_col2 = st.columns(2)

            with skill_col1:

                st.markdown(
                    "### ✅ Skills You Have"
                )

                matched_skills = skill_gap.get(
                    "matched_skills",
                    []
                )

                if matched_skills:

                    for item in matched_skills:

                        st.success(
                            f"**{item['skill'].title()}** "
                            f"• {item['category']}"
                        )

                else:

                    st.info(
                        "No matching technical skills detected."
                    )

            with skill_col2:

                st.markdown(
                    "### ❌ Skills to Learn"
                )

                missing_skills = skill_gap.get(
                    "missing_skills",
                    []
                )

                if missing_skills:

                    for item in missing_skills:

                        skill_name = item["skill"]
                        category = item["category"]
                        priority = item["priority"]

                        if priority == "High":

                            st.error(
                                f"🔴 **{skill_name.title()}** "
                                f"• {category} • **High Priority**"
                            )

                        elif priority == "Medium":

                            st.warning(
                                f"🟡 **{skill_name.title()}** "
                                f"• {category} • **Medium Priority**"
                            )

                        else:

                            st.info(
                                f"🔵 **{skill_name.title()}** "
                                f"• {category} • **Low Priority**"
                            )

                else:

                    st.success(
                        "🎉 No major missing technical skills detected!"
                    )

            st.markdown(
                "### 📚 Learning Areas"
            )

            category_summary = skill_gap.get(
                "category_summary",
                {}
            )

            if category_summary:

                for category, skills in category_summary.items():

                    with st.expander(
                        f"📌 {category}"
                    ):

                        st.write(
                            ", ".join(
                                skill.title()
                                for skill in skills
                            )
                        )


    # ============================================================
    # TAB 4 — ROADMAP
    # ============================================================

    with tabs[3]:

        st.markdown(
            """
            <div class="tool-header">
                <h3>📚 AI Personalized Learning Roadmap</h3>
                <p>Turn your skill gaps into a practical step-by-step learning plan.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "🚀 Generate My Learning Roadmap",
            use_container_width=True,
            key="generate_roadmap"
        ):

            if not st.session_state.resume_text:

                st.warning(
                    "Please upload your resume first."
                )

            elif not job_description.strip():

                st.warning(
                    "Please enter a job description first."
                )

            else:

                if not st.session_state.skill_gap:

                    with st.spinner(
                        "Analyzing your skill gaps first..."
                    ):

                        try:

                            skill_gap = analyze_skill_gap(
                                st.session_state.resume_text,
                                job_description
                            )

                            st.session_state.skill_gap = (
                                skill_gap
                            )

                        except Exception as e:

                            st.error(
                                f"Skill gap analysis error: {e}"
                            )

                            st.stop()

                skill_gap = (
                    st.session_state.skill_gap
                )

                missing_skills = skill_gap.get(
                    "missing_skills",
                    []
                )

                with st.spinner(
                    "Groq is building your personalized roadmap..."
                ):

                    try:

                        roadmap_result = generate_learning_roadmap(
                            st.session_state.resume_text,
                            job_description,
                            missing_skills
                        )

                        if roadmap_result.get(
                            "success"
                        ):

                            st.session_state.roadmap = (
                                roadmap_result.get(
                                    "roadmap",
                                    {}
                                )
                            )

                            st.success(
                                "🎉 Personalized roadmap generated!"
                            )

                        else:

                            st.error(
                                roadmap_result.get(
                                    "error",
                                    "Roadmap generation failed."
                                )
                            )

                    except Exception as e:

                        st.error(
                            f"Roadmap generation error: {e}"
                        )

        if st.session_state.roadmap:

            roadmap = (
                st.session_state.roadmap
            )

            target_role = roadmap.get(
                "target_role",
                "Target Role"
            )

            roadmap_summary = roadmap.get(
                "roadmap_summary",
                ""
            )

            estimated_duration = roadmap.get(
                "estimated_duration",
                "Not specified"
            )

            st.markdown(
                f"### 🎯 {target_role}"
            )

            if roadmap_summary:

                st.write(
                    roadmap_summary
                )

            st.metric(
                "Estimated Duration",
                estimated_duration
            )

            st.markdown(
                "### 🗓️ Week-by-Week Roadmap"
            )

            weeks = roadmap.get(
                "weeks",
                []
            )

            if weeks:

                for week in weeks:

                    week_number = week.get(
                        "week",
                        ""
                    )

                    title = week.get(
                        "title",
                        "Learning Week"
                    )

                    focus = week.get(
                        "focus",
                        ""
                    )

                    with st.expander(
                        f"📅 Week {week_number}: {title}",
                        expanded=(week_number == 1)
                    ):

                        if focus:

                            st.write(
                                f"**Focus:** {focus}"
                            )

                        estimated_hours = week.get(
                            "estimated_hours",
                            0
                        )

                        if estimated_hours:

                            st.write(
                                f"⏱️ **Estimated Time:** "
                                f"{estimated_hours} hours"
                            )

                        skills = week.get(
                            "skills",
                            []
                        )

                        if skills:

                            st.write(
                                "#### 🛠️ Skills"
                            )

                            for skill in skills:

                                st.write(
                                    f"• {skill}"
                                )

                        topics = week.get(
                            "topics",
                            []
                        )

                        if topics:

                            st.write(
                                "#### 📚 Topics"
                            )

                            for topic in topics:

                                st.write(
                                    f"• {topic}"
                                )

                        tasks = week.get(
                            "tasks",
                            []
                        )

                        if tasks:

                            st.write(
                                "#### ✅ Tasks"
                            )

                            for index, task in enumerate(tasks):

                                st.checkbox(
                                    task,
                                    key=(
                                        f"roadmap_week_"
                                        f"{week_number}_"
                                        f"task_{index}"
                                    )
                                )

                        project = week.get(
                            "project",
                            ""
                        )

                        if project:

                            st.write(
                                "#### 🚀 Project"
                            )

                            st.info(
                                project
                            )

            st.markdown(
                "### 🚀 Recommended Projects"
            )

            projects = roadmap.get(
                "projects",
                []
            )

            if projects:

                for project in projects:

                    project_name = project.get(
                        "name",
                        "Project"
                    )

                    with st.expander(
                        f"🛠️ {project_name}"
                    ):

                        st.write(
                            f"**Description:** "
                            f"{project.get('description', '')}"
                        )

                        technologies = project.get(
                            "technologies",
                            []
                        )

                        if technologies:

                            st.write(
                                "**Technologies:** "
                                + ", ".join(
                                    technologies
                                )
                            )

                        st.write(
                            f"**Difficulty:** "
                            f"{project.get('difficulty', '')}"
                        )

                        st.write(
                            f"**Why this project:** "
                            f"{project.get('reason', '')}"
                        )

            st.markdown(
                "### 🏆 Milestones"
            )

            milestones = roadmap.get(
                "milestones",
                []
            )

            if milestones:

                for milestone in milestones:

                    st.write(
                        f"#### 🎯 "
                        f"{milestone.get('milestone', '')}"
                    )

                    st.write(
                        milestone.get(
                            "success_criteria",
                            ""
                        )
                    )

            st.markdown(
                "### 💼 Job Readiness Checklist"
            )

            checklist = roadmap.get(
                "job_readiness_checklist",
                []
            )

            if checklist:

                for index, item in enumerate(checklist):

                    st.checkbox(
                        item,
                        key=f"job_readiness_{index}"
                    )

            else:

                st.info(
                    "No job-readiness checklist was generated."
                )


    # ============================================================
    # TAB 5 — RESUME REWRITER
    # ============================================================

    with tabs[4]:

        st.markdown(
            """
            <div class="tool-header">
                <h3>✍️ AI Resume Rewriter</h3>
                <p>Improve a specific resume section while preserving your real information.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.info(
            "The AI is instructed not to invent skills, experience, "
            "achievements, metrics, projects, or certifications."
        )

        section_type = st.selectbox(
            "Choose the resume section:",
            [
                "Professional Summary",
                "Experience",
                "Projects",
                "Skills",
                "Education",
                "Achievements",
                "Custom Section"
            ],
            key="rewrite_section_type"
        )

        resume_section = st.text_area(
            "Paste the resume section:",
            height=220,
            placeholder=(
                "Paste one section from your resume here.\n\n"
                "Example:\n"
                "Built a chatbot using Python and an AI API.\n"
                "Developed a React frontend and FastAPI backend."
            ),
            key="rewrite_input"
        )

        if st.button(
            "✨ Rewrite This Section",
            use_container_width=True,
            key="rewrite_button"
        ):

            if not st.session_state.resume_text:

                st.warning(
                    "Please upload your resume first."
                )

            elif not job_description.strip():

                st.warning(
                    "Please enter a job description first."
                )

            elif not resume_section.strip():

                st.warning(
                    "Please paste a resume section first."
                )

            else:

                with st.spinner(
                    "Groq is rewriting your resume section..."
                ):

                    try:

                        rewrite_result = rewrite_resume_section(
                            resume_section,
                            job_description,
                            section_type
                        )

                        if rewrite_result.get(
                            "success"
                        ):

                            st.session_state.rewrite_result = (
                                rewrite_result.get(
                                    "result",
                                    {}
                                )
                            )

                            st.success(
                                "✨ Resume section rewritten successfully!"
                            )

                        else:

                            st.session_state.rewrite_result = None

                            st.error(
                                rewrite_result.get(
                                    "error",
                                    "Resume rewriting failed."
                                )
                            )

                    except Exception as e:

                        st.session_state.rewrite_result = None

                        st.error(
                            f"Resume rewriting error: {e}"
                        )

        if st.session_state.rewrite_result:

            rewrite = (
                st.session_state.rewrite_result
            )

            st.markdown(
                "### ✨ Improved Version"
            )

            rewritten_text = rewrite.get(
                "rewritten_text",
                ""
            )

            if rewritten_text:

                st.text_area(
                    "📋 Copy-ready resume section:",
                    value=rewritten_text,
                    height=230,
                    key="rewritten_output"
                )

            st.markdown(
                "### 📌 Improvements Made"
            )

            improvements = rewrite.get(
                "improvements",
                []
            )

            if improvements:

                for improvement in improvements:

                    st.info(
                        f"• {improvement}"
                    )

            st.markdown(
                "### 🔑 ATS Keywords Used"
            )

            ats_keywords = rewrite.get(
                "ats_keywords_used",
                []
            )

            if ats_keywords:

                st.write(
                    ", ".join(
                        str(keyword).title()
                        for keyword in ats_keywords
                    )
                )

            else:

                st.info(
                    "No ATS keywords were identified."
                )

            st.markdown(
                "### ⚠️ Missing Information"
            )

            missing_information = rewrite.get(
                "missing_information",
                []
            )

            if missing_information:

                for item in missing_information:

                    st.warning(
                        f"• {item}"
                    )

            else:

                st.success(
                    "No additional information was requested."
                )

            st.markdown(
                "### 🛡️ Fact Check Notes"
            )

            fact_check_notes = rewrite.get(
                "fact_check_notes",
                []
            )

            if fact_check_notes:

                for note in fact_check_notes:

                    st.success(
                        f"✓ {note}"
                    )

            else:

                st.info(
                    "No fact-check notes were returned."
                )




# ============================================================
# FLOATING CAREER COPILOT
# ============================================================

if "copilot_messages" not in st.session_state:
    st.session_state.copilot_messages = []

with st.popover("🤖 AI Copilot", help="Open Career Copilot"):
    st.markdown('<div class="copilot-chat-title">AI Career Copilot</div>', unsafe_allow_html=True)
    st.markdown('<div class="copilot-chat-subtitle">Ask about your resume, target job, skills, roadmap, interviews, or career preparation.</div>', unsafe_allow_html=True)

    if not st.session_state.resume_text or not job_description.strip():
        st.info("Upload your resume and enter a target job description first.")

    for message in st.session_state.copilot_messages:
        if message.get("role") == "user":
            st.markdown(
                f'<div class="copilot-message-user">{message.get("content", "")}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="copilot-message-ai">🤖 {message.get("content", "")}</div>',
                unsafe_allow_html=True
            )

    copilot_question = st.text_input(
        "",
        placeholder="Ask Career Copilot...",
        key="floating_copilot_question",
        label_visibility="collapsed"
    )

    if st.button("Send  ➜", use_container_width=True, key="floating_copilot_send"):
        if not st.session_state.resume_text:
            st.warning("Please upload your resume first.")
        elif not job_description.strip():
            st.warning("Please enter a job description first.")
        elif not copilot_question.strip():
            st.warning("Please enter a question first.")
        else:
            with st.spinner("Career Copilot is thinking..."):
                try:
                    copilot_result = ask_career_copilot(
                        question=copilot_question,
                        resume_text=st.session_state.resume_text,
                        job_description=job_description,
                        match_result=st.session_state.match_result,
                        skill_gap=st.session_state.skill_gap,
                        roadmap=st.session_state.roadmap,
                        generate_audio=True
                    )

                    if copilot_result.get("success"):
                        answer = copilot_result.get("answer", "")
                        st.session_state.copilot_messages.append({"role": "user", "content": copilot_question})
                        st.session_state.copilot_messages.append({"role": "assistant", "content": answer})
                        st.session_state.copilot_result = copilot_result
                        st.rerun()
                    else:
                        st.error(copilot_result.get("error", "Career Copilot failed."))
                except Exception as e:
                    st.error(f"Career Copilot error: {e}")

    # Hidden ElevenLabs playback: no visible audio player.
    copilot_audio = st.session_state.get("copilot_result", {}).get("audio") if st.session_state.get("copilot_result") else None
    if copilot_audio:
        import base64
        try:
            if isinstance(copilot_audio, bytes):
                audio_b64 = base64.b64encode(copilot_audio).decode("utf-8")
                st.markdown(
                    f'<audio autoplay style="display:none"><source src="data:audio/mpeg;base64,{audio_b64}" type="audio/mpeg"></audio>',
                    unsafe_allow_html=True
                )
            elif isinstance(copilot_audio, str) and copilot_audio.startswith("data:audio"):
                st.markdown(
                    f'<audio autoplay style="display:none"><source src="{copilot_audio}"></audio>',
                    unsafe_allow_html=True
                )
        except Exception:
            pass

st.markdown(
    """
    <div class="quote-panel contour">
        <div style="position:relative;z-index:2;">
            <div class="section-kicker" style="color:#ff7b4b;">04 / AI INSIGHTS</div>
            <h2>Build Your Career<br>with Confidence.</h2>
            <p>Personalized recommendations, actionable insights, and the right tools to achieve your goals.</p>
        </div>
    </div>
    """, unsafe_allow_html=True
)

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        <strong>Plan Resume Matcher</strong>
        <br>
        AI-powered resume analysis • ATS simulation •
        Career intelligence
        <br><br>
        Built with Streamlit • Groq • ElevenLabs
    </div>
    """,
    unsafe_allow_html=True
)