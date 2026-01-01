import unittest
from uk_smb_engine.schemas.models import BusinessType, Transaction, AgentState
from uk_smb_engine.agents.labeler import SmartLabeler
from uk_smb_engine.agents.translator import UKContextTranslator
from uk_smb_engine.agents.diagnostician import BottleneckDiagnostician

class TestThreeBusinessValidation(unittest.TestCase):
    
    def run_pipeline(self, state):
        # 1. Label
        state.labeled_transactions = SmartLabeler(state.business_type).process(state.transactions)
        # 2. Translate
        ops = UKContextTranslator(state.business_type).analyze(state.labeled_transactions)
        state.diagnoses.extend(ops)
        # 3. Diagnose
        risks = BottleneckDiagnostician(state.business_type).diagnose(state.labeled_transactions)
        state.diagnoses.extend(risks)
        return state

    def test_case_1_consultant_service(self):
        """Case 1: Sarah the Consultant. High Margin. No COGS."""
        transactions = [
            Transaction(date="2025-01", description="Client Project Fee", amount=6800.0, type="Income"), # ~82k/yr
            Transaction(date="2025-01", description="Starbucks", amount=-4.50, type="Expense"),
            Transaction(date="2025-01", description="Xero", amount=-30.0, type="Expense")
        ]
        state = AgentState(business_type=BusinessType.SERVICE, transactions=transactions)
        self.run_pipeline(state)
        
        # Check Tags
        tags = {t.description: t.tag for t in state.labeled_transactions}
        self.assertIn("Compliance_Risk", tags["Starbucks"]) # Coffee is Personal
        self.assertIn("Admin_Bloat", tags["Xero"])
        
        # Check Opportunity
        titles = [d.title for d in state.diagnoses]
        self.assertIn("VAT Flat Rate Scheme", titles) # High margin should trigger this

    def test_case_2_plumber_trade(self):
        """Case 2: Mike the Plumber. Materials vs Tools."""
        transactions = [
            Transaction(date="2025-01", description="Big Job Payment", amount=10000.0, type="Income"), # ~120k/yr
            Transaction(date="2025-01", description="Screwfix Direct", amount=-450.0, type="Expense"), # COGS
            Transaction(date="2025-01", description="Van Lease", amount=-350.0, type="Expense"), # Overhead
            Transaction(date="2025-01", description="Shell Petrol", amount=-80.0, type="Expense") # Fuel
        ]
        state = AgentState(business_type=BusinessType.TRADE, transactions=transactions)
        self.run_pipeline(state)
        
        # Check Tags
        tags = {t.description: t.tag for t in state.labeled_transactions}
        self.assertIn("COGS", tags["Screwfix Direct"])
        self.assertIn("COGS", tags["Shell Petrol"])
        self.assertIn("Admin_Bloat", tags["Van Lease"]) # Lease is overhead
        
        # Check Opportunity
        titles = [d.title for d in state.diagnoses]
        self.assertIn("VAT Cash Accounting Scheme", titles) # High Rev should trigger this

    def test_case_3_bakery_retail(self):
        """Case 3: Bella the Baker. Inventory."""
        transactions = [
            Transaction(date="2025-01", description="Daily Sales", amount=7500.0, type="Income"), # ~90k/yr
            Transaction(date="2025-01", description="Flour Wholesale", amount=-2000.0, type="Expense")
        ]
        state = AgentState(business_type=BusinessType.RETAIL, transactions=transactions)
        self.run_pipeline(state)

        # Check Tags
        tags = {t.description: t.tag for t in state.labeled_transactions}
        self.assertIn("COGS", tags["Flour Wholesale"])
        
if __name__ == '__main__':
    unittest.main()
