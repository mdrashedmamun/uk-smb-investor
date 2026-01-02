from typing import Dict, List, Optional
from pydantic import BaseModel
# --- Data Models ---
class DiagnosticResult(BaseModel):
    scorecard: Dict[str, str]
    insights: List[str]
    action_plan: List[str]
# --- The V3.5 Logic Engine (Ported from session_flow.yaml) ---
class MasterInvestorOrchestrator:
    def run_diagnosis(self, headache: str, answers: Dict[str, any], profile: Dict[str, any]) -> DiagnosticResult:
        
        # 1. Unpack Inputs
        revenue = answers.get("revenue", 0.0)
        margin = answers.get("profit_margin", 0.0)
        cac = answers.get("cac", 0.0)
        ltv = answers.get("ltv", 0.0)
        price = answers.get("offer_price", 0.0)
        upsell = answers.get("upsell_rate", 0.0)
        bottleneck = answers.get("bottleneck", "")
        lead_source = answers.get("lead_source", "") 
        user_intent = answers.get("user_intent", "") 
        
        metrics = {
            "Revenue": f"£{revenue:,.0f}",
            "Margin": f"{margin*100:.1f}%",
            "LTV:CAC": f"{ltv/cac:.1f}" if cac > 0 else "∞",
            "Offer": f"£{price:,.0f}"
        }
        
        insights = []
        actions = []
        active_states = []
        
        # --- PHASE 1: DETECT ACTIVE STATES ---
        
        # 1. Insolvency (Survival)
        if margin < 0.0 or "Survival" in bottleneck:
            active_states.append("insolvency_crisis")
            insights.append("🛑 **INSOLVENCY RISK:** You are burning cash or running on fumes.")
            actions.append("1. **FREEZE:** Stop all hiring and non-essential spend today.")
            actions.append("2. **DEMAND:** Call top 5 debtors and collect cash immediately.")
        # 2. Treadmill Trap (Unit Economics)
        if (cac > price * 0.5) or ("Funnel" in bottleneck and ltv/cac < 3.0):
            active_states.append("treadmill_trap")
            insights.append("⚠️ **The Treadmill Trap:** You are renting customers, not acquiring them.")
            actions.append("1. **RAISE PRICES:** Increase core price by 15% immediately.")
            actions.append("2. **AUDIT:** Stop ads with ROAS < 2.0.")
        # 3. Misaligned Offer (Video 5)
        if (lead_source == "cold_traffic" and cac > 200 and price > 2000) or (cac > 1000):
             active_states.append("misaligned_offer_funnel")
             insights.append("🛑 **Offer Trap:** You are trying to marry strangers on the first date.")
             actions.append("1. **SPLIT OFFER:** Create a lower-ticket 'Bridge' offer (£500-£2k).")
             actions.append("2. **NURTURE:** Stop direct selling. Build a video funnel first.")
        # 4. Undermonetized Excellence (Optimization)
        if margin > 0.15 and upsell < 0.10 and "Growth" not in bottleneck:
            active_states.append("undermonetized_excellence")
            insights.append("🦄 **Hidden Gold Mine:** Your core business is great, but you leave money on the table.")
            actions.append("1. **The 4 Skits:** Script 4 upsell scenarios for your team.")
            actions.append("2. **Nudge:** Add a 'Speed' or 'VIP' option to every quote.")
        # 5. Pricing Paralysis
        if margin < 0.10 and margin >= 0.0 and "Stagnation" in bottleneck:
            active_states.append("pricing_paralysis")
            insights.append("⚠️ **Inflation Victim:** Your costs rose, but your prices didn't.")
            actions.append("1. **The 6% Rule:** Raise prices 6% tomorrow. Use the 'Inflation Letter' script.")
        # 6. Underspending Paradox (Growth)
        if (ltv/cac > 4.0) and "Growth" in bottleneck:
            active_states.append("underspending_paradox")
            insights.append("🚀 **Green Light:** You have a money printing machine.")
            actions.append("1. **SCALE:** Double ad spend on your best channel.")
            actions.append("2. **FINANCE:** Secure a credit line to float the ad spend.")
        # --- PHASE 2: PRIORITIZATION (Meta-Rules) ---
        
        final_plan = []
        
        # Rule 1: Survival blocks EVERYTHING
        if "insolvency_crisis" in active_states:
            final_plan = [a for a in actions if "FREEZE" in a or "DEMAND" in a]
            insights = [i for i in insights if "INSOLVENCY" in i]
            
        # Rule 2: Offer Fix blocks Growth
        elif "misaligned_offer_funnel" in active_states:
            final_plan = [a for a in actions if "SPLIT" in a or "NURTURE" in a]
            insights = [i for i in insights if "Trap" in i]
            if "underspending_paradox" in active_states:
                insights.append("🚫 **Growth Blocked:** High CAC detected. Fix offer before scaling ads.")
        # Rule 3: Correction blocks Growth
        elif "treadmill_trap" in active_states or "pricing_paralysis" in active_states:
             final_plan = [a for a in actions if "RAISE" in a or "6%" in a]
             if "underspending_paradox" in active_states:
                  insights.append("🚫 **Growth Blocked:** Fix margins before pouring fuel on the fire.")
        # Rule 4: Optimization (Nail it then Scale it)
        elif "undermonetized_excellence" in active_states:
             if user_intent == "open_new_location":
                 insights.append("🛑 **Wait to Expand:** Nail your Upsell metrics first.")
                 final_plan = [a for a in actions if "Skits" in a]
             else:
                 final_plan = actions
        # Rule 5: Pure Growth
        elif "underspending_paradox" in active_states:
             final_plan = actions
        
        # Fallback
        if not final_plan:
            final_plan.append("1. **Review P&L:** Your numbers look average. Look for 10% cost cuts.")
            final_plan.append("2. **Reactivate:** Email past customers with a generic offer.")
        return DiagnosticResult(
            scorecard=metrics,
            insights=insights,
            action_plan=final_plan
        )
