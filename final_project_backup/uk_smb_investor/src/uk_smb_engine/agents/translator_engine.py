from typing import Dict, List, Optional
from pydantic import BaseModel

# --- Data Models ---
class DiagnosticResult(BaseModel):
    scorecard: Dict[str, str]  # e.g., {"CAC": "£25 (Good)", "Runway": "2 Months (Critical)"}
    insights: List[str]
    action_plan: List[str]

class Question(BaseModel):
    id: str
    text: str
    helper_text: Optional[str] = None
    type: str = "number" # number, boolean, select

# --- Input Validation ---
class InputValidator:
    @staticmethod
    def validate_and_convert(value: any, field: str) -> float:
        try:
            if isinstance(value, (int, float)):
                return float(value)
            # Remove currency symbols, commas, spaces
            cleaned = str(value).replace('£', '').replace(',', '').replace(' ', '').strip()
            if not cleaned:
                return 0.0
            return float(cleaned)
        except:
            return 0.0 # Default to 0 for safety in this MVP, or could raise error

# --- The Specialist Agents ---

class BaseAgent:
    def diagnose(self, answers: Dict[str, any], profile: Dict[str, any]) -> Dict:
        return {"metrics": {}, "insights": []}

class UnitEconomicsAgent(BaseAgent):
    def get_questions(self) -> List[Question]:
        return [
            Question(id="marketing_spend", text="Last month, what was your total spend on ads, flyers, and marketing?", helper_text="e.g. £500 on FB ads, £200 on flyers. Enter 0 if purely organic."),
            Question(id="new_customers", text="How many NEW customers did you get last month?", helper_text="Don't count repeat business. Just new faces."),
            Question(id="aov", text="When a customer buys, what is the typical bill amount?", helper_text="e.g. £4.50 for coffee, £50 for haircut, £1,000 for website."),
        ]

    def diagnose(self, answers: Dict[str, any], profile: Dict[str, any]) -> Dict:
        insights = []
        metrics = {}
        
        spend = InputValidator.validate_and_convert(answers.get("marketing_spend"), "Marketing Spend")
        new_cust = InputValidator.validate_and_convert(answers.get("new_customers"), "New Customers")
        aov = InputValidator.validate_and_convert(answers.get("aov"), "AOV")
        
        # 1. CAC Logic + Funnel Fallback
        if new_cust > 0:
            cac = spend / new_cust
            metrics["CAC"] = f"£{cac:.2f}"
            
            if cac == 0:
                insights.append("🦄 **Unicorn Signal:** You are growing purely on organic word-of-mouth. This is powerful.")
            elif cac < aov * 0.3:
                 metrics["CAC Risk"] = "Low"
            elif cac > aov:
                 insights.append("🚨 **Treadmill of Death:** You spend more to get a customer than they pay you correctly. Stop ads.")
        else:
             metrics["CAC"] = "N/A (No Growth)"
             insights.append("⚠️ **Stagnation:** You acquired zero new customers last month.")

        return {"metrics": metrics, "insights": insights}

class CashFlowAgent(BaseAgent):
    def get_questions(self) -> List[Question]:
        return [
             Question(id="cash_balance", text="What is the total cash in all business accounts right now?", helper_text="Include savings and current accounts."),
             Question(id="monthly_burn", text="What are your total monthly costs (Rent + Staff + Materials)?", helper_text="Rough estimate of everything leaving the bank."),
             Question(id="days_receivable", text="On average, how many days after the work is done do you get paid?", helper_text="0 for retail/shops. 30+ for many B2B items.")
        ]

    def diagnose(self, answers: Dict[str, any], profile: Dict[str, any]) -> Dict:
        insights = []
        metrics = {}
        
        cash = InputValidator.validate_and_convert(answers.get("cash_balance"), "Cash")
        burn = InputValidator.validate_and_convert(answers.get("monthly_burn"), "Burn")
        days_wait = InputValidator.validate_and_convert(answers.get("days_receivable"), "Days Receivable")
        biz_model = profile.get("business_model", "Unknown")

        # 1. Runway Logic
        runway_months = cash / burn if burn > 0 else 999
        metrics["Runway"] = f"{runway_months:.1f} Months"
        
        if runway_months < 1:
            insights.append("🛑 **INSOLVENCY RISK:** You have less than 1 month of cash. Freeze hiring/spending immediately.")
        elif runway_months < 3:
            insights.append("⚠️ **Danger Zone:** You have less than 3 months runway. Prioritize sales over everything.")
            
        # 2. Bank of Client Logic (Context Aware)
        if days_wait > 30:
            if biz_model == "B2C":
                insights.append(f"🛑 **B2C Cash Trap:** You are B2C but waiting {int(days_wait)} days for cash? Consumers should pay instantly. Fix your payment processor.")
            else:
                insights.append("🏦 **Bank of the Client:** You are financing your B2B customers. Switch to deposits or invoice factoring.")
        elif days_wait > 7 and biz_model == "B2C":
             insights.append("⚠️ **Slow B2C Collection:** B2C payments should be instant. Why the delay?")

        return {"metrics": metrics, "insights": insights}

# --- The Master Orchestrator ---

class MasterInvestorOrchestrator:
    def __init__(self):
        self.agents = {
            "Growth": UnitEconomicsAgent(),
            "Cash": CashFlowAgent(),
            # Add others later
        }
    
    def triage(self, headache: str, profile: Dict[str, any]) -> List[str]:
        """Returns the sequence of Agents to run based on headache."""
        # Future: Use profile['industry'] to tweak sequence (e.g. Retail always needs constraints check)
        if headache == "Running out of money":
            return ["Cash", "Growth"]
        elif headache == "Not enough new customers":
            return ["Growth", "Cash"]
        else:
            return ["Cash", "Growth"] # Default safety

    def run_diagnosis(self, headache: str, answers: Dict[str, any], profile: Dict[str, any]) -> DiagnosticResult:
        sequence = self.triage(headache, profile)
        
        all_metrics = {}
        all_insights = []
        
        for agent_name in sequence:
            agent = self.agents[agent_name]
            result = agent.diagnose(answers, profile)
            all_metrics.update(result["metrics"])
            all_insights.extend(result["insights"])
            
        # Generate Triage Action Plan
        action_plan = []
        if any("INSOLVENCY" in i for i in all_insights):
            action_plan.append("1. **IMMEDIATE:** Call top 5 debtors and demand payment.")
            action_plan.append("2. **CUT:** Stop all non-essential software/subscriptions today.")
        elif any("Treadmill" in i for i in all_insights):
            action_plan.append("1. **STOP ADS:** Your marketing is burning cash. Pause campaigns.")
            action_plan.append("2. **PRICING:** Increase prices by 15% to cover acquisition costs.")
        else:
            cust_name = profile.get("name", "there")
            action_plan.append(f"1. **OPTIMIZE:** High five, {cust_name}. Your fundamentals are sound. Look for leverage.")
            
        return DiagnosticResult(
            scorecard=all_metrics,
            insights=all_insights,
            action_plan=action_plan
        )
