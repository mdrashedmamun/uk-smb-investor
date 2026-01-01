from uk_smb_engine.agents.translator_engine import MasterInvestorOrchestrator

def test_investor_brain():
    print("🧠 Booting up Investor Brain...")
    brain = MasterInvestorOrchestrator()
    
    # Scenario: "Sarah the Consultant" - Cash Headache
    print("\n--- TEST CASE: Sarah (Cash Crisis) ---")
    headache = "Running out of money"
    
    # Answers simulating a cash crunch
    sarah_answers = {
        # Cash Agent Answers
        "cash_balance": 2000,
        "monthly_burn": 4000,   # 0.5 months runway (BAD)
        "days_receivable": 45,  # Waiting 45 days (BAD)
        
        # Growth Agent Answers
        "marketing_spend": 500,
        "new_customers": 2,     # CAC = 250
        "aov": 2000             # Good LTV potential
    }
    
    result = brain.run_diagnosis(headache, sarah_answers)
    
    print("\n📊 SCORECARD:")
    for k, v in result.scorecard.items():
        print(f"  {k}: {v}")
        
    print("\n💡 INSIGHTS:")
    for i in result.insights:
        print(f"  {i}")
        
    print("\n🚀 ACTION PLAN:")
    for step in result.action_plan:
        print(f"  {step}")

if __name__ == "__main__":
    test_investor_brain()
