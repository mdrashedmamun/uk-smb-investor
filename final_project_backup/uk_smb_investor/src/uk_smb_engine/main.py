from uk_smb_engine.schemas.models import BusinessType, Transaction, AgentState
from uk_smb_engine.agents.labeler import SmartLabeler
from uk_smb_engine.agents.diagnostician import BottleneckDiagnostician
from uk_smb_engine.agents.architect import SimplicityArchitect
from uk_smb_engine.agents.translator import UKContextTranslator

def main():
    print("Initializing UK SMB Engine...")
    
    # 1. Setup Dummy Data (Consultant Case)
    demo_transactions = [
        Transaction(date="2025-03-01", description="Client Retainer", amount=6000.0, type="Income"),
        Transaction(date="2025-03-02", description="Starbucks", amount=-4.50, type="Expense"),
        Transaction(date="2025-03-05", description="Apple Store", amount=-2000.0, type="Expense"),
        Transaction(date="2025-03-06", description="Xero Subscription", amount=-30.0, type="Expense")
    ]
    
    state = AgentState(
        business_type=BusinessType.SERVICE,
        transactions=demo_transactions
    )
    
    print(f"Loaded {len(state.transactions)} transactions for {state.business_type} business.")
    
    # 2. Run Smart Labeler
    print("\n--- Phase 1: Smart Labeling ---")
    labeler = SmartLabeler(state.business_type)
    state.labeled_transactions = labeler.process(state.transactions)
    for tx in state.labeled_transactions:
        print(f" > {tx.description:<20} -> {tx.tag}")

    # 3. Run Context Translator (The Expert)
    print("\n--- Phase 2: UK Context & Optimization ---")
    translator = UKContextTranslator(state.business_type)
    opportunities = translator.analyze(state.labeled_transactions)
    state.diagnoses.extend(opportunities) # Compile into diagnoses list
    for op in opportunities:
        print(f" > [Opportunity] {op.title}")

    # 4. Run Diagnostician (The Strategist)
    print("\n--- Phase 3: Diagnosis ---")
    diagnostician = BottleneckDiagnostician(state.business_type)
    risks = diagnostician.diagnose(state.labeled_transactions)
    state.diagnoses.extend(risks)
    for d in risks:
        print(f" > [{d.severity}] {d.title}")

    # 5. Run Architect
    print("\n--- Phase 4: Final Report ---")
    architect = SimplicityArchitect()
    report = architect.generate_report(state.diagnoses)
    print(report)

if __name__ == "__main__":
    main()
