# SME Valuation Solution

An interactive web platform for strategic valuation of Italian small and medium enterprises (SMEs). Answers the question: *"What is my business worth, what drives that value, and how can I grow it?"*

---

## Why thresholds instead of linear formulas

You might ask: why not simply `value / max_value`? For example, `16% / 40% = 0.4`.

The answer is that business value does **not** grow linearly with margins. The difference between a 5% and 10% EBITDA margin is enormous in terms of business health. The difference between 25% and 30% is far less significant. Thresholds capture this real non-linearity — which is why we follow the **Altman Z-Score model**, which uses exactly the same approach.

---

## Why some variables are inverse

**Client Concentration** and **Founder Dependency** are inverse measures because they measure *risk*, not quality. Higher values are worse for the business:

- Concentration 55% → normalized score 0.3 (high risk)
- Concentration 15% → normalized score 1.0 (low risk)

Without inverting, a company with 90% of revenue from a single client would receive a high score — the opposite of what the model should communicate.

---

## Where the weights come from

The honest answer: there are no "scientifically certified" weights for this specific model. No one has them. Even professional business valuation models use weights derived from a mix of literature, empirical experience, and defensible methodological choices.

**What matters is not having the "right" weights — it's being able to justify them with coherent logic.**

### Logic behind each weight

#### Financial Capital (internal weights: 30/25/25/20)

| Variable | Weight | Why |
|----------|--------|-----|
| EBITDA Margin | 30% | The most direct measure of operating profitability — the foundation of any valuation |
| Revenue CAGR | 25% | Growth trajectory directly impacts the multiple a buyer is willing to pay |
| Recurring Revenue | 25% | Recurring revenue = predictability = reduced risk for the buyer. Equals CAGR in importance |
| Client Concentration | 20% | It's a risk, not a strength — lower weight than the others but a critical signal |

**Why these four?** We follow Altman Z-Score logic: select a few high-signal variables instead of many redundant ones. As your professor said: *"The smartest model is not the one with the most variables, but the one that selects the most relevant ones."*

#### Technological Capital (internal weights: 40/35/25)

| Variable | Weight | Why |
|----------|--------|-----|
| Digital Maturity | 40% | The enabling condition — without digitalization there is no automation or scalability |
| Tech Investment | 35% | The concrete, measurable signal of the company's technological commitment |
| Scalability | 25% | Partly dependent on digital maturity — lower weight to avoid double-counting |

#### Human Capital (internal weights: 40/35/25)

| Variable | Weight | Why |
|----------|--------|-----|
| Founder Dependency | 40% | The single most penalizing factor in due diligence — a buyer wants a business that works without the founder |
| Management Structure | 35% | Managerial team = autonomous execution capacity |
| Client Portfolio Quality | 25% | Proxy for the quality of commercial relationships managed by the team |

**Logic behind the 40/35 split:** inspired by literature on *business transferability* — the central theme in pre-exit valuations.

#### Relational Capital (internal weights: 60/40)

| Variable | Weight | Why |
|----------|--------|-----|
| Network Strength | 60% | The only variable that directly measures the network — it must dominate |
| Client Concentration | 40% | Used as a proxy: depending on few clients also means weak relational networks |

---

## How to explain this in a presentation

The most effective answer to a jury:

> "The weights are not arbitrary — they follow three hierarchical principles. First: objective and verifiable variables outweigh declared ones. Second: factors that directly impact business transferability outweigh contextual factors. Third: we avoided double-counting by assigning lower weights to variables already indirectly captured by others."

---

## Step 3: Questionnaire Logic

The three categories now modify the Live Score Preview. Here's what changed:

- **Tech Focus (green)** — proxy for Technological Capital; responds to Digital Maturity (weight 40/65) and Model Scalability (weight 25/65), normalized to available weights (excluding tech_investment, which is not a form input)
- **Relational Focus (purple)** — proxy for Relational Capital; responds to Network Strength (60%) and Client Concentration (40%), mirroring the backend formula exactly

---

## Database

> The normalization thresholds are empirically calibrated on a sample of **4,184 Italian SMEs** (ATECO 62 sector) extracted from AIDA — Bureau van Dijk, April 2026. The median ROS (Return on Sales) for the sector is 5.79%, significantly lower than generic literature assumptions — this demonstrates why a model calibrated to the Italian context is necessary.

---

## Tech stack

- **Backend:** Python, FastAPI
- **Frontend:** React 18, Vite, Tailwind CSS, Framer Motion
- **Data:** AIDA / Bureau van Dijk (Italian SME benchmarks)
- **Database:** Supabase (PostgreSQL)

See `CLAUDE.md` for detailed architecture and setup.
