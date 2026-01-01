from typing import List
from ..schemas.models import Transaction, LabeledTransaction, BusinessType

class SmartLabeler:
    def __init__(self, business_type: BusinessType):
        self.business_type = business_type

    def process(self, transactions: List[Transaction]) -> List[LabeledTransaction]:
        """
        Applies Business-Specific Rules to tag transactions.
        """
        labeled_data = []
        for tx in transactions:
            tag = "Uncategorized"
            confidence = 0.5
            rule = "Default"

            # Normalize for matching
            desc = tx.description.lower()
            
            # --- LEVEL 0: Global Safety Checks ---
            if any(x in desc for x in ["transfer to personal", "personal", "gym", "betting"]):
                tag = "[Compliance_Risk: High]"
                confidence = 0.99
                rule = "Global_Rule: Integrity Check"
                labeled_data.append(LabeledTransaction(**tx.dict(), tag=tag, confidence=confidence, rule_applied=rule))
                continue
            
            # --- LEVEL 1: Business-Context Logic ---
            
            # CASE: SERVICE Business (Consultant)
            if self.business_type == BusinessType.SERVICE:
                if any(x in desc for x in ["starbucks", "pret", "costa", "lunch", "dinner"]):
                    tag = "[Compliance_Risk: High]"
                    confidence = 0.95
                    rule = "Service_Rule: Food is Personal"
                elif any(x in desc for x in ["apple", "macbook", "laptop"]):
                    # Check context: Usually growth, but requires Diagnostician to validate Cash
                    tag = "[Growth_Invest: Accelerate]" 
                    confidence = 0.8
                    rule = "Service_Rule: Equipment"
                elif any(x in desc for x in ["xero", "adobe", "subscription", "saas"]):
                    tag = "[Admin_Bloat: Review]"
                    confidence = 0.9
                    rule = "Service_Rule: Software"
                elif "retainer" in desc or "fee" in desc:
                    tag = "[Revenue: Recurring]"
                    confidence = 0.95
                    rule = "Service_Rule: Revenue"

            # CASE: TRADE Business (Plumber)
            elif self.business_type == BusinessType.TRADE:
                if any(x in desc for x in ["screwfix", "wickes", "plumb", "timber"]):
                    tag = "[COGS: Essential]"
                    confidence = 0.95
                    rule = "Trade_Rule: Materials"
                elif "fuel" in desc or "petrol" in desc or "shell" in desc:
                    tag = "[COGS: Essential]"
                    confidence = 0.9
                    rule = "Trade_Rule: Fuel"
                elif "lease" in desc:
                    tag = "[Admin_Bloat: Review]"
                    confidence = 0.85
                    rule = "Trade_Rule: Finance"

            # CASE: RETAIL Business (Bakery)
            elif self.business_type == BusinessType.RETAIL:
                if any(x in desc for x in ["flour", "sugar", "wholesale"]):
                    tag = "[COGS: Essential]"
                    confidence = 0.95
                    rule = "Retail_Rule: Inventory"

            # --- LEVEL 2: Fallback ---
            if tag == "Uncategorized":
                if tx.amount > 0:
                     tag = "[Revenue: Project]"
                else:
                     tag = "[Admin_Bloat: Review]"
                rule = "Fallback_Generic"
                confidence = 0.5

            labeled_data.append(LabeledTransaction(
                **tx.dict(),
                tag=tag,
                confidence=confidence,
                rule_applied=rule
            ))
            
        return labeled_data
