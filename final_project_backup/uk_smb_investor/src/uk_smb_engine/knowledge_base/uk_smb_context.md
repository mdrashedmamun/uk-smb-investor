# UK SMB Context & Benchmark Data
*Source: "Backing Your Business: Evidence Annex" (UK Gov, 2024)*

## 1. Action-Oriented Taxonomy & Validation Rules
*Agents must ONLY use these tags. Apply the Validation Rules strictly based on BUSINESS TYPE.*

### Business Specific Rules
#### [Type: Service] (Consultants, Agencies)
*   **Starbucks/Lunch:** `[Compliance_Risk: High]` (Unless "Client Meeting" in description).
*   **Software Subs:** `[Admin_Bloat: Review]` (Unless essential to delivery).
*   **COGS:** NONE. All costs are overhead.

#### [Type: Retail] (Bakeries, Shops)
*   **Ingredients/Stock:** `[COGS: Essential]`.
*   **Staff Food:** `[Compliance_Risk: High]` (Unless "Staff Welfare").
*   **Equipment:** `[Growth_Invest: Accelerate]` (Based on margin).

#### [Type: Trade] (Plumbers, Builders)
*   **Materials (Pipes/Wood):** `[COGS: Essential]`.
*   **Tools/Vans:** `[Growth_Invest: Accelerate]` (Tools) or `[Admin_Bloat: Review]` (Leases).
*   **Fuel:** `[COGS: Essential]` (If work vehicle).

### General Categories (Fallback)
*   **`[Admin_Bloat: Review]`**: Recurring >£10/month.
*   **`[Compliance_Risk: High]`**: Personal spending patterns.
*   **`[Staff_Cost: Monitor]`**: Wages, NI.
*   **`[Revenue: Recurring]`** vs **`[Revenue: Project]`**.

---

## 2. UK Risk Thresholds (The "Danger Math")

### The VAT "Cliff Edge" (Tiered Logic)
*   **Context:** UK VAT Threshold is £90,000 (Updated 2024).
*   **Level 1 (£75k - £82k):** "Awareness Alert" - You are approaching the zone.
*   **Level 2 (£82k - £84.5k):** "Planning Alert" - Decide strategy NOW (Voluntary vs Flat Rate).
*   **Level 3 (£84.5k+):** "URGENT STOP" - Do not invoice until registered.

### The "Owner Trap" (Low Productivity)
*   **Logic:** `IF Admin_Task_Volume > 10 transactions/week AND Software_Spend < £50`
*   **Diagnosis:** "You are doing manual data entry instead of paying £30 for Xero."

### Cash Buffer Health
*   **Logic:** `IF Cash_Balance < 1.0 * Average_Monthly_Expense`
*   **Diagnosis:** "Dangerously Low Cash."

---

## 3. Key UK Terminology (For Translation)
*   **Sales Tax** -> **VAT** (Value Added Tax).
*   **Social Security** -> **National Insurance** (NI).
*   **LLC/Inc** -> **Ltd** (Private Limited Company) or **Sole Trader**.
*   **IRS** -> **HMRC** (Her Majesty's Revenue and Customs).

## 4. Relevant Grants & Schemes
*   **Help to Grow:** 90% government funded management training.
*   **Employment Allowance:** Reduction in employer NI bills (up to £5,000 off).
*   **R&D Tax Credits:** For innovation (often missed by small tech-enabled firms).

---

## 5. UK VAT Schemes (Business-Specific Optimization)
*Use `[Business Type]` and `Cash Buffer` to recommend the right scheme.*

### VAT Cash Accounting Scheme
*   **For:** Trade businesses (plumbers, builders, contractors) or ANY business with late-paying clients.
*   **When:** Turnover < £1.35 million AND cash flow is tight (Cash Buffer < 2 months).
*   **Benefit:** Pay VAT to HMRC only when YOU get paid by customers.
*   **Math:** If customers pay in 60 days, you keep VAT cash for 60 extra days.
*   **Action Rule:** `IF [Type: Trade] AND Cash_Buffer < 2 months -> RECOMMEND "Switch to Cash Accounting"`

### VAT Flat Rate Scheme
*   **For:** Simple service businesses with minimal expenses (Consultants).
*   **When:** Turnover < £150,000 AND business is VAT-registered.
*   **Benefit:** Pay fixed % of turnover (simpler, often cheaper).
    *   *Example:* IT Consultants pay ~14.5% flat rate vs 20% standard, keeping the difference as profit.
*   **Trade-off:** Cannot reclaim input VAT on most purchases (except capital goods >£2k).
*   **Action Rule:** `IF [Type: Service] AND Software_Spend < £100/month -> CONSIDER "Flat Rate Scheme"`
