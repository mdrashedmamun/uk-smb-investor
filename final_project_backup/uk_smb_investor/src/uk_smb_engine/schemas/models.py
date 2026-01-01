from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional

class BusinessType(str, Enum):
    RETAIL = "retail"
    SERVICE = "service"
    TRADE = "trade"

class Transaction(BaseModel):
    date: str
    description: str
    amount: float
    type: str = Field(default="Expense", description="Credit/Debit/Transfer")
    category: str = Field(default="Uncategorized", description="Raw bank category")

class LabeledTransaction(Transaction):
    tag: str = Field(description="Action-Oriented Tag e.g., [COGS: Essential]")
    confidence: float = Field(ge=0.0, le=1.0)
    rule_applied: str = Field(default="LLM_Generation", description="Rule ID or Logic used")

class Diagnosis(BaseModel):
    severity: str = Field(description="Critical, Warning, or Info")
    title: str
    reason: str
    action: str

class AgentState(BaseModel):
    business_type: Optional[BusinessType] = None
    transactions: List[Transaction] = []
    labeled_transactions: List[LabeledTransaction] = []
    diagnoses: List[Diagnosis] = []
