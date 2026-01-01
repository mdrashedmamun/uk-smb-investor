from typing import List
from ..schemas.models import LabeledTransaction, Diagnosis, BusinessType

class BottleneckDiagnostician:
    def __init__(self, business_type: BusinessType):
        self.business_type = business_type

    def diagnose(self, transactions: List[LabeledTransaction]) -> List[Diagnosis]:
        diagnoses = []
        
        # 1. Aggregate Data
        revenue = sum(t.amount for t in transactions if "[Revenue" in t.tag)
        software_spend = sum(abs(t.amount) for t in transactions if "Software" in t.rule_applied or "Admin_Bloat" in t.tag)
        compliance_risks = [t for t in transactions if "Compliance_Risk" in t.tag]
        
        # 2. Rule: Compliance Check
        if compliance_risks:
            items = ", ".join([t.description for t in compliance_risks])
            diagnoses.append(Diagnosis(
                severity="Warning",
                title="Personal Spend Detected",
                reason=f"Found personal items in business account: {items}",
                action="Stop using business card for coffee/meals."
            ))

        # 3. Rule: VAT Cliff
        projected_revenue = revenue * 12 if len(transactions) > 0 else 0
        if projected_revenue >= 85000:
             diagnoses.append(Diagnosis(
                severity="Critical",
                title="VAT Threshold Breached",
                reason=f"Projected Revenue £{projected_revenue:,.0f} exceeds the £90k limit.",
                action="URGENT: Register for VAT immediately. You may be fined."
            ))
        elif 80000 < projected_revenue < 85000:
             diagnoses.append(Diagnosis(
                severity="Warning",
                title="VAT Cliff Edge Approaching",
                reason=f"Projected Revenue £{projected_revenue:,.0f} is close to £90k limit.",
                action="Plan VAT strategy now (Voluntary vs Flat Rate)."
            ))

        # 4. Rule: Service Specific - Equipment
        equipment = [t for t in transactions if "Growth_Invest" in t.tag]
        for eq in equipment:
             diagnoses.append(Diagnosis(
                severity="Info",
                title="Capital Investment Noted",
                reason=f"Purchase of {eq.description} (£{abs(eq.amount)}).",
                action="Ensure you keep the receipt for Capital Allowances."
            ))
            
        return diagnoses
