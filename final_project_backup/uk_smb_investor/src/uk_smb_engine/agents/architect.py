from typing import List
from ..schemas.models import Diagnosis

class SimplicityArchitect:
    def generate_report(self, diagnoses: List[Diagnosis]) -> str:
        report = ["# 🌞 Monday Morning Checklist\n"]
        
        if not diagnoses:
            return "No critical issues found. Keep pushin'!"

        for i, diag in enumerate(diagnoses, 1):
            icon = "🛑" if diag.severity == "Critical" else "⚠️" if diag.severity == "Warning" else "✅"
            
            item = f"{i}. {icon} {diag.title}\n"
            item += f"   **Why:** {diag.reason}\n"
            item += f"   **Action:** {diag.action}\n"
            report.append(item)
            
        return "\n".join(report)
