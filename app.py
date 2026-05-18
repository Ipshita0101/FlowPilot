import streamlit as st
from modules.task_manager import (
    add_task,
    get_tasks,
    delete_task,
    complete_task
)
from modules.dashboard import get_dashboard_data

st.set_page_config(page_title="FlowPilot", layout="wide")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root tokens ── */
:root {
    --bg:        #0d0f14;
    --surface:   #13161e;
    --surface2:  #1b1f2b;
    --border:    rgba(255,255,255,0.07);
    --accent:    #5b6af7;
    --accent2:   #8b5cf6;
    --high:      #ff4d6d;
    --med:       #fbbf24;
    --low:       #34d399;
    --text:      #e8eaf0;
    --muted:     #7b82a0;
    --radius:    12px;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Animated background grid ── */
.stApp {
    background-color: var(--bg) !important;
    background-image:
        linear-gradient(rgba(91,106,247,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(91,106,247,0.04) 1px, transparent 1px);
    background-size: 40px 40px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * {
    color: var(--text) !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
}

/* Sidebar logo mark */
[data-testid="stSidebar"]::before {
    content: "⬡";
    display: block;
    font-size: 2rem;
    color: var(--accent);
    padding: 1.5rem 1.5rem 0.25rem;
    font-family: 'Syne', sans-serif;
}

/* ── Title ── */
h1 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 2.6rem !important;
    letter-spacing: -0.03em !important;
    background: linear-gradient(135deg, #fff 30%, var(--accent)) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    margin-bottom: 0 !important;
}

h2, h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    color: var(--text) !important;
}

/* Subtitle */
[data-testid="stMarkdownContainer"] p {
    color: var(--muted);
    font-size: 0.95rem;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1.25rem 1.5rem !important;
    transition: border-color 0.2s, transform 0.2s;
    position: relative;
    overflow: hidden;
}
[data-testid="stMetric"]:hover {
    border-color: var(--accent) !important;
    transform: translateY(-2px);
}
[data-testid="stMetric"]::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(91,106,247,0.06) 0%, transparent 60%);
    pointer-events: none;
}
[data-testid="stMetricLabel"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    color: var(--text) !important;
}

/* ── Progress bar ── */
[data-testid="stProgressBar"] > div {
    background: var(--surface2) !important;
    border-radius: 99px !important;
    height: 6px !important;
    overflow: hidden;
}
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
    border-radius: 99px !important;
    transition: width 0.8s cubic-bezier(.4,0,.2,1) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(91,106,247,0.18) !important;
}
.stSelectbox > div > div,
.stDateInput > div > div > input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
}
.stSelectbox > div > div:hover,
.stDateInput > div > div > input:hover {
    border-color: var(--accent) !important;
}

/* ── Labels ── */
label, .stTextInput label, .stTextArea label,
.stSelectbox label, .stDateInput label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.04em !important;
    border-radius: 8px !important;
    border: 1px solid var(--border) !important;
    background: var(--surface2) !important;
    color: var(--text) !important;
    padding: 0.45rem 1.1rem !important;
    transition: all 0.18s ease !important;
}
.stButton > button:hover {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
    color: #fff !important;
    box-shadow: 0 4px 20px rgba(91,106,247,0.35) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Alert / status boxes ── */
[data-testid="stAlert"] {
    border-radius: var(--radius) !important;
    border-left-width: 3px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
}

/* error → High priority */
[data-testid="stAlert"][data-baseweb="notification"][kind="error"] {
    background: rgba(255,77,109,0.08) !important;
    border-color: var(--high) !important;
    color: #ffb3c1 !important;
}
/* warning → Medium priority */
[data-testid="stAlert"][data-baseweb="notification"][kind="warning"] {
    background: rgba(251,191,36,0.08) !important;
    border-color: var(--med) !important;
    color: #fde68a !important;
}
/* success → Low priority / Completed */
[data-testid="stAlert"][data-baseweb="notification"][kind="success"] {
    background: rgba(52,211,153,0.08) !important;
    border-color: var(--low) !important;
    color: #6ee7b7 !important;
}
/* info → Pending */
[data-testid="stAlert"][data-baseweb="notification"][kind="info"] {
    background: rgba(91,106,247,0.08) !important;
    border-color: var(--accent) !important;
    color: #a5b4fc !important;
}

/* ── Task container cards ── */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 1.25rem 1.5rem !important;
    margin-bottom: 0.75rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"]:hover {
    border-color: rgba(91,106,247,0.4) !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3) !important;
}

/* ── Divider ── */
hr {
    border-color: var(--border) !important;
    margin: 0.5rem 0 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--surface2); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

/* ══════════════════════════════════════════
   TASK CARDS
══════════════════════════════════════════ */

.fp-task-card {
    background: linear-gradient(135deg, #16192400 0%, #1b1f2b 100%);
    background-color: #13161e;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.25rem 1.5rem 1rem;
    margin-bottom: 0.25rem;
    transition: box-shadow 0.25s ease, transform 0.2s ease, border-color 0.2s ease;
    position: relative;
    overflow: hidden;
}

.fp-task-card::before {
    content: "";
    position: absolute;
    top: 0; right: 0;
    width: 180px; height: 180px;
    background: radial-gradient(circle at top right, rgba(91,106,247,0.07), transparent 70%);
    pointer-events: none;
}

.fp-task-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 0 0 1px rgba(91,106,247,0.2);
}

/* Header row */
.fp-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.5rem;
}

.fp-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #e8eaf0;
    letter-spacing: -0.01em;
}

.fp-card-id {
    font-family: 'DM Sans', monospace;
    font-size: 0.75rem;
    color: #7b82a0;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 6px;
    padding: 2px 8px;
    letter-spacing: 0.05em;
}

/* Description */
.fp-card-desc {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    color: #a0a8c0;
    line-height: 1.55;
    margin-bottom: 1rem;
    padding-left: 2px;
}

/* Badge row */
.fp-card-meta {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 0.85rem;
}

.fp-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.03em;
    padding: 4px 10px;
    border-radius: 99px;
    white-space: nowrap;
}

.fp-date {
    background: rgba(255,255,255,0.04) !important;
    color: #7b82a0 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    margin-left: auto;
}

/* ── Override action buttons inside cards ── */
.fp-task-card + div .stButton > button {
    font-size: 0.82rem !important;
    padding: 0.35rem 0.9rem !important;
}

/* Complete button accent */
div[data-testid="column"]:first-child .stButton > button:hover {
    background: rgba(52,211,153,0.15) !important;
    border-color: #34d399 !important;
    color: #34d399 !important;
    box-shadow: 0 4px 16px rgba(52,211,153,0.2) !important;
}

/* Delete button accent */
div[data-testid="column"]:nth-child(2) .stButton > button:hover {
    background: rgba(255,77,109,0.12) !important;
    border-color: #ff4d6d !important;
    color: #ff4d6d !important;
    box-shadow: 0 4px 16px rgba(255,77,109,0.2) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Navigation ──────────────────────────────────────────────────────────────
menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Dashboard",
        "Add Task",
        "Task Manager"
    ]
)

# ── Header ──────────────────────────────────────────────────────────────────
st.title("FlowPilot")
st.subheader("Workflow & Productivity Platform")

# ── Dashboard metrics ────────────────────────────────────────────────────────
total_tasks, completed_tasks, pending_tasks, productivity = get_dashboard_data()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Tasks",
    total_tasks
)

col2.metric(
    "Completed",
    completed_tasks
)

col3.metric(
    "Pending",
    pending_tasks
)

st.progress(productivity / 100)

st.write(
    f"Productivity Score: {productivity:.2f}%"
)

# ── Add Task ─────────────────────────────────────────────────────────────────
if menu == "Add Task":

    st.header("Add New Task")

    title = st.text_input("Task Title")

    description = st.text_area("Task Description")

    priority = st.selectbox(
        "Priority",
        ["High", "Medium", "Low"]
    )

    status = st.selectbox(
        "Status",
        ["Pending", "Completed"]
    )

    due_date = st.date_input("Due Date")

    if st.button("Add Task"):

        add_task(
            title,
            description,
            priority,
            status,
            due_date
        )

        st.success("Task Added Successfully")

# ── Task Manager ─────────────────────────────────────────────────────────────
if menu == "Task Manager":

    st.header("Task Dashboard")

    filter_option = st.selectbox(
        "Filter Tasks",
        [
            "All",
            "Pending",
            "Completed",
            "High Priority",
            "Medium Priority",
            "Low Priority"
        ]
    )

    tasks = get_tasks()

    filtered_tasks = []

    for task in tasks:

        if filter_option == "All":

            filtered_tasks.append(task)

        elif filter_option == "Pending" and task[4] == "Pending":

            filtered_tasks.append(task)

        elif filter_option == "Completed" and task[4] == "Completed":

            filtered_tasks.append(task)

        elif filter_option == "High Priority" and task[3] == "High":

            filtered_tasks.append(task)

        elif filter_option == "Medium Priority" and task[3] == "Medium":

            filtered_tasks.append(task)

        elif filter_option == "Low Priority" and task[3] == "Low":

            filtered_tasks.append(task)


    for task in filtered_tasks:

        # ── Priority accent config ──
        priority_cfg = {
            "High":   ("--high",   "#ff4d6d", "#3a0d1a", "🔴", "⚡"),
            "Medium": ("--med",    "#fbbf24", "#3a2a00", "🟡", "⚡"),
            "Low":    ("--low",    "#34d399", "#003a27", "🟢", "⚡"),
        }
        status_cfg = {
            "Completed": ("#34d399", "#003a27", "✅"),
            "Pending":   ("#5b6af7", "#0d1240", "🕐"),
        }

        p_var, p_col, p_bg, p_dot, p_icon = priority_cfg.get(task[3], ("--muted", "#7b82a0", "#1b1f2b", "⚪", "⚡"))
        s_col, s_bg, s_icon = status_cfg.get(task[4], ("#7b82a0", "#1b1f2b", "❓"))

        with st.container():

            # ── Card HTML ──
            st.markdown(f"""
<div class="fp-task-card" style="border-left: 3px solid {p_col};">

  <div class="fp-card-header">
    <div class="fp-card-title">📌 {task[1]}</div>
    <div class="fp-card-id">#{task[0]}</div>
  </div>

  <div class="fp-card-desc">{task[2]}</div>

  <div class="fp-card-meta">
    <span class="fp-badge" style="background:{p_bg}; color:{p_col}; border:1px solid {p_col}40;">
      {p_icon} {p_dot} {task[3]}
    </span>
    <span class="fp-badge" style="background:{s_bg}; color:{s_col}; border:1px solid {s_col}40;">
      {s_icon} {task[4]}
    </span>
    <span class="fp-badge fp-date">
      📅 {task[5]}
    </span>
  </div>

</div>
""", unsafe_allow_html=True)

            # ── Action buttons ──
            btn_cols = st.columns([1, 1, 6])

            if task[4] == "Pending":
                with btn_cols[0]:
                    if st.button("✅ Complete", key=f"complete_{task[0]}"):
                        complete_task(task[0])
                        st.success("Task marked as completed!")
                        st.rerun()

            with btn_cols[1]:
                if st.button("🗑 Delete", key=f"delete_{task[0]}"):
                    delete_task(task[0])
                    st.warning("Task deleted.")
                    st.rerun()

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)