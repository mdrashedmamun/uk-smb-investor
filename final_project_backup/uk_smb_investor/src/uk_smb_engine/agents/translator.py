from typing import List
from ..schemas.models import LabeledTransaction, Diagnosis, BusinessType

class UKContextTranslator:
    def __init__(self, business_type: BusinessType):
        self.business_type = business_type

    def analyze(self, transactions: List[LabeledTransaction]) -> List[Diagnosis]:
        opportunities = []
        
        # 1. Calculate Metrics
        revenue = sum(t.amount for t in transactions if "[Revenue" in t.tag)
        # Simplified: Estimate Cash Buffer (In real app, this comes from Balance History)
        # For MVP/Sim, we assume a flag or heuristics. 
        # Here we'll infer 'Low Cash' if we see a 'Low Cash' warning from Diagnostician? 
        # No, Agents run sequentially. Translator runs BEFORE Diagnostician in original plan?
        # Actually Config said: Labeler -> Translator -> Diagnostician.
        
        # Let's use simple heuristic rules for the MVP based on transaction patterns
        # or simplified assumptions.
        
        # 2. Scheme Logic: VAT Cash Accounting (For Trade)
        if self.business_type == BusinessType.TRADE:
            # Logic: If Revenue high but cash tight?
            # For this MVP test, we'll check if Revenue > £85k (VAT Reg) 
            # and logic typically applies.
            if revenue * 12 > 85000: # Projecting monthly revenue
                 opportunities.append(Diagnosis(
                    severity="Opportunity",
                    title="VAT Cash Accounting Scheme",
                    reason="Trade businesses often wait for payment. Don't pay HMRC until you get paid.",
                    action="Switch to Cash Accounting to boost cash flow."
                ))

        # 3. Scheme Logic: Flat Rate Scheme (For Service)
        if self.business_type == BusinessType.SERVICE:
            # Logic: Low expenses?
            expenses = sum(abs(t.amount) for t in transactions if t.amount < 0 and "Revenue" not in t.tag)
            # If Expense/Revenue ratio is low (high margin)
            if revenue > 0 and (expenses / revenue) < 0.2:
                 opportunities.append(Diagnosis(
                    severity="Opportunity",
                    title="VAT Flat Rate Scheme",
                    reason=f"Your expenses are low ({int(expenses/revenue*100)}% of turnover).",
                    action="Check if Flat Rate saves you money (keep ~14% of VAT)."
                ))

        return opportunities
