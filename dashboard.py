import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- CONFIGURATION & THEME ---
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Mini AI SaaS Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- MODERN UI STYLING (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .st_card {
        background-color: #1f222e;
        border: 1px solid #30334a;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, border-color 0.2s ease;
        margin-bottom: 1rem;
    }
    
    .st_card:hover {
        transform: translateY(-2px);
        border-color: #4CAF50;
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }

    [data-testid="stSidebar"] {
        background-color: #11131c;
        border-right: 1px solid #30334a;
    }

    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def fetch_models():
    try:
        res = requests.get(f"{BACKEND_URL}/jobs/models/all")
        return res.json() if res.status_code == 200 else []
    except:
        return []

def fetch_logs(job_id):
    try:
        res = requests.get(f"{BACKEND_URL}/jobs/{job_id}/logs")
        return pd.DataFrame(res.json()) if res.status_code == 200 else pd.DataFrame()
    except:
        return pd.DataFrame()

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.markdown("---")
    
    selected = st.radio(
        "CORE MODULES",
        ["Home Dashboard", "User Accounts", "Data Management", "AI Training Lab", "AI Analytics", "Model Leaderboard"],
        index=0
    )
    
    st.markdown("---")
    st.subheader("User Session")
    user_role = st.selectbox("Current Session Role", ["Admin", "Data Scientist", "Viewer"])

    if user_role == "Admin":
        st.success("🔓 Full Access Granted")
    elif user_role == "Data Scientist":
        st.info("🧪 Research Access")
    else:
        st.warning("👁️ Read-Only Mode")
    
    st.markdown("---")
    st.caption("v1.2 • RBAC & MongoDB Enabled")

# --- PAGE: HOME DASHBOARD ---
if selected == "Home Dashboard":
    st.header("Welcome to the Mini AI SaaS Platform! 🚀")
    
    if user_role == "Admin":
        st.markdown("### ⚠️ Admin Controls")
        with st.container():
            st.markdown('<div class="st_card" style="border-color: #ff4b4b;">', unsafe_allow_html=True)
            col_admin, _ = st.columns([1, 2])
            with col_admin:
                if st.button("🗑️ Wipe Database (DANGER)"):
                    st.error("Database Wipe Triggered. (Action simulation only)")
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("##### System Overview & Usage Analytics")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown('<div class="st_card"><h3>3</h3><p>Active Users</p></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="st_card"><h3>12</h3><p>Datasets Stored</p></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="st_card"><h3>84</h3><p>Training Jobs</p></div>', unsafe_allow_html=True)
    with col4: st.markdown('<div class="st_card"><h3>98.2%</h3><p>Peak Accuracy</p></div>', unsafe_allow_html=True)

# --- PAGE: USER ACCOUNTS ---
elif selected == "User Accounts":
    st.header("👤 User Management")
    if user_role in ["Admin", "Data Scientist"]:
        col_a, col_b = st.columns([1, 1.5])
        with col_a:
            st.subheader("Add New Account")
            with st.form("user_reg", clear_on_submit=True):
                name = st.text_input("Name")
                email = st.text_input("Email")
                pwd = st.text_input("Password", type="password")
                if st.form_submit_button("Register User"):
                    requests.post(f"{BACKEND_URL}/auth/register", json={"name":name,"email":email,"password":pwd})
                    st.success("User added to MySQL.")
        with col_b:
            st.subheader("Directory")
            st.info("Active users are synced with your MySQL instance.")
    else:
        st.warning("You do not have permission to manage users.")

# --- PAGE: DATA MANAGEMENT ---
elif selected == "Data Management":
    st.header("📂 Data Repository")
    if user_role != "Viewer":
        tabs = st.tabs(["📤 Upload Dataset", "📚 My Library"])
        with tabs[0]:
            st.markdown('<div class="st_card">', unsafe_allow_html=True)
            u_id = st.number_input("User ID", min_value=1)
            up_file = st.file_uploader("Drop CSV here", type="csv")
            if st.button("Push to Cloud"):
                if up_file:
                    files = {"file": (up_file.name, up_file.getvalue())}
                    requests.post(f"{BACKEND_URL}/datasets/upload/{u_id}", files=files)
                    st.success("File stored and metadata logged.")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("Access Denied: Viewers cannot upload datasets.")

# --- PAGE: AI TRAINING LAB ---
elif selected == "AI Training Lab":
    st.header("🧠 AI Training Simulation")
    col_left, col_right = st.columns([1, 2])
    with col_left:
        st.markdown('<div class="st_card">', unsafe_allow_html=True)
        j_id = st.number_input("Target Job ID", min_value=1)
        if user_role in ["Admin", "Data Scientist"]:
            if st.button("🔥 Start Simulation"):
                with st.spinner("Training..."):
                    requests.post(f"{BACKEND_URL}/jobs/simulate/{j_id}")
                st.balloons()
        else:
            st.button("🔥 Start Simulation (Disabled)", disabled=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_right:
        st.info("Run simulations here. Use the 'AI Analytics' tab for detailed telemetry graphs.")

# --- PAGE: AI ANALYTICS (The Integrated Module) ---
elif selected == "AI Analytics":
    st.header("📈 AI Training Analytics")
    models = fetch_models()
    
    if models:
        model_names = [f"{m['version']} (Job {m['job_id']})" for m in models]
        selected_model = st.selectbox("🔍 Select a Registered Model to Inspect", model_names)
        job_id = int(selected_model.split("Job ")[1].replace(")", ""))

        st.markdown("---")
        df = fetch_logs(job_id)

        if not df.empty:
            m1, m2, m3 = st.columns(3)
            with m1: st.metric("🎯 Final Accuracy", f"{df['accuracy'].iloc[-1]*100:.2f}%")
            with m2: st.metric("📉 Final Loss", f"{df['loss'].iloc[-1]:.4f}")
            with m3: st.metric("🔢 Total Epochs", len(df))

            st.markdown('<div class="st_card">', unsafe_allow_html=True)
            fig = px.line(df, x="epoch", y=["accuracy", "loss"], 
                         title=f"Telemetry: Accuracy vs Loss (Job #{job_id})",
                         labels={"value": "Score", "variable": "Metric"},
                         template="plotly_dark", color_discrete_sequence=["#4CAF50", "#FF4B4B"])
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning(f"No telemetry logs found for Job #{job_id} in MongoDB.")
    else:
        st.info("No models registered in MySQL yet. Please register a model via the API.")

# --- PAGE: MODEL LEADERBOARD ---
elif selected == "Model Leaderboard":
    st.header("🏆 Performance Leaderboard")
    if st.button("Refresh Rankings"):
        res = requests.get(f"{BACKEND_URL}/jobs/models/all")
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            st.dataframe(df.sort_values("accuracy", ascending=False), use_container_width=True)