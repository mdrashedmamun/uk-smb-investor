import streamlit as st
import sys
import os
import json
from datetime import datetime

# Add src to python path so we can import the engine from anywhere
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from uk_smb_engine.agents.translator_engine import MasterInvestorOrchestrator

def save_optional_data(email, name, industry, diagnosis_data):
    """Save opt-in data for future personalization"""
    if not email:  # Only save if user opted in
        return
    
    data_entry = {
        "timestamp": datetime.now().isoformat(),
        "email": email,
        "name": name,
        "industry": industry,
        "headache": st.session_state.get("headache"),
        "scorecard": diagnosis_data.scorecard,
        # "insights": diagnosis_data.insights # Optional: save insights too if needed
    }
    
    # For MVP: Log to Console (Cloud Logs capture this) and Session State
    print(f"🎯 LEAD CAPTURED: {json.dumps(data_entry)}")
    
    if "user_insights" not in st.session_state:
        st.session_state.user_insights = []
    st.session_state.user_insights.append(data_entry)


# Set Page Config
st.set_page_config(page_title="SMB Investor Brain", page_icon="🧠", layout="centered")

# Initialize Session State
if "brain" not in st.session_state:
    st.session_state["brain"] = MasterInvestorOrchestrator()
if "step" not in st.session_state:
    st.session_state["step"] = "triage" # Start at Triage (Value First)
if "profile" not in st.session_state:
    st.session_state["profile"] = {}
if "answers" not in st.session_state:
    st.session_state["answers"] = {}
if "headache" not in st.session_state:
    st.session_state["headache"] = None

# --- Custom CSS ---
st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; }
    .big-font { font-size:24px !important; font-weight: bold; }
    .success-box { padding: 1rem; background-color: #d1fae5; border-radius: 5px; color: #064e3b; }
    .warning-box { padding: 1rem; background-color: #fef3c7; border-radius: 5px; color: #92400e; }
    .danger-box { padding: 1rem; background-color: #fee2e2; border-radius: 5px; color: #991b1b; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("🧠 The Digital Business Investor")
st.markdown("### Get an investor-grade diagnosis of your business in 2 minutes.")

# --- STEP 1: TRIAGE ---
if st.session_state["step"] == "triage":
    st.write("First, let's focus on what matters.")
    headache = st.radio(
        "What is your biggest headache right now?",
        ["Running out of money (Cash)", "Not enough new customers (Growth)", "Too much chaos / burnout (Operations)"]
    )
    
    if st.button("Start Diagnosis"):
        st.session_state["headache"] = headache.split(" (")[0] # Clean string
        st.session_state["step"] = "questions"
        st.rerun()

# --- STEP 2: QUESTIONS ---
elif st.session_state["step"] == "questions":
    brain = st.session_state["brain"]
    headache = st.session_state["headache"]
    # Profile is empty for now (Anonymous MVP)
    profile = st.session_state.get("profile", {})
    
    # Get sequence of agents based on headache & profile
    agent_sequence = brain.triage(headache, profile)
    
    # Flatten all questions from all agents in sequence
    all_questions = []
    for agent_name in agent_sequence:
        agent = brain.agents[agent_name]
        all_questions.extend(agent.get_questions())
    
    # Progress Logic
    total_q = len(all_questions)
    
    st.progress(0.1)
    st.caption(f"Ready to analyze {total_q} strategic points.")
    
    with st.form("diagnosis_form"):
        st.write(f"**Focus Area: {headache}**")
        
        for q in all_questions:
            val = st.text_input(q.text, help=q.helper_text, key=q.id)
        
        if st.form_submit_button("Generate Report"):
            # UI Validation
            errors = []
            for q in all_questions:
                val = st.session_state.get(q.id, "")
                
                # Check if it looks roughly like a number
                clean = val.replace('£', '').replace(',', '').replace('.', '').replace(' ', '').strip()
                if val and not clean.isdigit():
                    errors.append(f"Invalid number for: {q.text}")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                # Collect answers from state
                for q in all_questions:
                    st.session_state["answers"][q.id] = st.session_state[q.id]
                st.session_state["step"] = "results"
                st.rerun()

# --- STEP 3: RESULTS ---
elif st.session_state["step"] == "results":
    brain = st.session_state["brain"]
    result = brain.run_diagnosis(
        st.session_state["headache"], 
        st.session_state["answers"],
        st.session_state.get("profile", {})
    )
    
    st.markdown("## 📊 Your Investor Scorecard")
    
    # Display Scorecard
    cols = st.columns(len(result.scorecard))
    for i, (metric, value) in enumerate(result.scorecard.items()):
        cols[i].metric(metric, value)
        
    st.markdown("---")
    
    st.markdown("## 🔍 Strategic Insights")
    for insight in result.insights:
        if "🦄" in insight:
             st.markdown(f'<div class="success-box">{insight}</div>', unsafe_allow_html=True)
        elif "🛑" in insight:
             st.markdown(f'<div class="danger-box">{insight}</div>', unsafe_allow_html=True)
        else:
             st.markdown(f'<div class="warning-box">{insight}</div>', unsafe_allow_html=True)
        st.write("") # Spacer

    st.markdown("## 🚀 Your 90-Day Action Plan")
    for step in result.action_plan:
        st.write(step)
    
    st.markdown("---")
    st.markdown("### 💌 Want to save your report?")
    
    with st.expander("Email me my report (Optional)"):
        st.write("We'll send you this analysis plus a weekly growth tip.")
        name = st.text_input("Name")
        email = st.text_input("Email")
        industry = st.selectbox(
            "Industry", 
            ["Retail", "Service", "Trade", "Tech", "Other"]
        )
        
        if st.button("Send Report"):
            if email:
                save_optional_data(email, name, industry, result)
                st.success(f"Report sent to {email}! (Data Saved)")
            else:
                st.error("Please enter an email.")

    if st.button("Start Over"):
        st.session_state["step"] = "triage"
        st.session_state["answers"] = {}
        st.rerun()
