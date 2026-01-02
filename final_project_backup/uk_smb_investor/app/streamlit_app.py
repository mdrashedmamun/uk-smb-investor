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
    }
    
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
    st.session_state["step"] = "triage"
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
# --- STEP 1: INTAKE (The 7 Diagnostic Questions) ---
if st.session_state["step"] == "triage":
    st.markdown("## 🏥 The Business Physical")
    st.write("We need 7 numbers to diagnose your business stage. Be honest - I'm a machine, I don't judge.")
    
    with st.form("intake_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            revenue = st.text_input("1. Annual Revenue ($)", help="e.g. 1000000")
            margin = st.slider("2. Net Profit Margin (%)", -20, 50, 10, help="What do you keep after everything?")
            cac = st.text_input("3. Cost to Acquire Customer ($)", help="How much marketing spend to get 1 sale?")
            ltv = st.text_input("4. Customer Lifetime Value ($)", help="How much does one customer pay you in total over years?")
        with col2:
            offer_price = st.text_input("5. Price of Core Offer ($)", help="What is the price of your main product/service?")
            upsell_rate = st.slider("6. Upsell / Retainer Conversion (%)", 0, 100, 15, help="What % of customers buy your next thing?")
            bottleneck = st.selectbox(
                "7. What feels broken?",
                ["Running out of cash (Survival)", "Sales are flat (Stagnation)", "Chaotic / No Systems (Operations)", "Marketing is expensive (Funnel)", "I need to scale (Growth)"]
            )
        
        submitted = st.form_submit_button("Run Diagnosis 🚀")
        
        if submitted:
            try:
                def start_clean(val):
                    if not val: return 0.0
                    return float(val.replace(',', '').replace('$', '').replace('£', '').strip())
                answers = {
                    "revenue": start_clean(revenue),
                    "profit_margin": margin / 100.0,
                    "cac": start_clean(cac),
                    "ltv": start_clean(ltv),
                    "offer_price": start_clean(offer_price),
                    "upsell_rate": upsell_rate / 100.0,
                    "bottleneck": bottleneck.split(" (")[0],
                    "net_profit": start_clean(revenue) * (margin / 100.0)
                }
                
                # Special logic
                if "Growth" in bottleneck:
                    answers["user_intent"] = "open_new_location"
                elif "Funnel" in bottleneck:
                    answers["lead_source"] = "cold_traffic"
                
                st.session_state["answers"] = answers
                st.session_state["headache"] = answers["bottleneck"]
                st.session_state["step"] = "results"
                st.rerun()
            except ValueError:
                st.error("Please enter valid numbers.")
# --- STEP 3: RESULTS ---
elif st.session_state["step"] == "results":
    if st.button("← Back to Questions"):
        st.session_state["step"] = "triage"
        st.rerun()
    brain = st.session_state["brain"]
    result = brain.run_diagnosis(
        st.session_state["headache"], 
        st.session_state["answers"],
        st.session_state.get("profile", {})
    )
    
    st.markdown("## 📊 Your Investor Scorecard")
    
    cols = st.columns(len(result.scorecard))
    for i, (metric, value) in enumerate(result.scorecard.items()):
        cols[i].metric(metric, value)
        
    st.markdown("---")
    
    st.markdown("## 🔍 Strategic Insights")
    for insight in result.insights:
        if "🦄" in insight:
             st.success(insight)
        elif "🛑" in insight:
             st.error(insight)
        else:
             st.warning(insight)
        st.write("")
    st.markdown("## 🚀 Your 90-Day Action Plan")
    for step in result.action_plan:
        st.write(step)
    
    st.markdown("---")
    st.markdown("### 💌 Want to save your report?")
    
    with st.expander("Email me my report (Optional)"):
        st.write("We'll send you this analysis plus a weekly growth tip.")
        name = st.text_input("Name")
        email = st.text_input("Email")
        industry = st.selectbox("Industry", ["Retail", "Service", "Trade", "Tech", "Other"])
        
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
