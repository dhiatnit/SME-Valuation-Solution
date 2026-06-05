"""
VALUE INTELLIGENCE PLATFORM
Livello 3 — Valuation Model & Recommendation Engine

Riceve l'output del Livello 2 (scores, SQF, GF) e i dati grezzi
e restituisce:
  - Valore stimato in € con range di confidenza
  - Value Gap (% di potenziale non espresso)
  - Top 3 azioni prioritarie con impatto stimato
  - Output completo pronto per il dashboard
"""


# ─────────────────────────────────────────────
# COSTANTI
# ─────────────────────────────────────────────

# TODO: consolidare in constants.py (duplicato in scorer.py)
# Multipli EBITDA per settore
# Fonte ispirazione: Damodaran (NYU), Mediobanca SME Report
SECTOR_MULTIPLES = {
    "Tecnologia/SaaS":       7.5,
    "Servizi B2B":           5.5,
    "Manifatturiero":        4.5,
    "Healthcare":            6.0,
    "Retail/GDO":            4.0,
    "Edilizia/Immobiliare":  4.2,
    "Altro":                 5.0,
}

# Margine di confidenza sul valore stimato
# Riflette la varianza tipica nelle valutazioni di PMI non quotate
CONFIDENCE_RANGE = 0.10  # ±10%


# ─────────────────────────────────────────────
# PASSO 1 — VALORE STIMATO
# ─────────────────────────────────────────────

def calculate_value(ebitda: float, sector: str, sqf: float, gf: float) -> dict:
    """
    Applica la formula centrale del modello:
    V = EBITDA × Sector Multiple × SQF × GF

    Restituisce il valore puntuale e il range di confidenza ±10%.

    Perché ±10%:
      Le PMI non quotate non hanno un prezzo di mercato osservabile.
      Il range riflette la varianza tipica nelle transazioni M&A
      di piccole imprese (fonte: KPMG SME Transaction Report).
    """
    multiple = SECTOR_MULTIPLES.get(sector, 5.0)
    value    = ebitda * multiple * sqf * gf

    return {
        "value":         round(value),
        "value_min":     round(value * (1 - CONFIDENCE_RANGE)),
        "value_max":     round(value * (1 + CONFIDENCE_RANGE)),
        "multiple_used": multiple,
    }


# ─────────────────────────────────────────────
# PASSO 2 — VALUE GAP
# ─────────────────────────────────────────────

def calculate_value_gap(ebitda: float, sector: str, sqf: float, gf: float) -> dict:
    """
    Calcola il Value Gap: distanza percentuale tra valore attuale
    e valore ottimizzato (potenziale massimo raggiungibile).

    Scenario ottimizzato:
      SQF_max = 1.4 (massimo del range definito dal modello)
      GF_opt  = GF × 1.3, con cap a 1.5 per evitare stime irrealistiche

    Il Value Gap è la metrica più importante del dashboard:
    non dice solo quanto vale l'azienda oggi, ma quanto potrebbe
    valere — ed è la leva narrativa per le raccomandazioni.
    """
    current   = calculate_value(ebitda, sector, sqf, gf)
    gf_opt    = min(gf * 1.3, 1.5)
    optimized = calculate_value(ebitda, sector, 1.4, gf_opt)

    gap_pct = ((optimized["value"] - current["value"]) / current["value"]) * 100

    return {
        "current_value":    current["value"],
        "optimized_value":  optimized["value"],
        "gap_pct":          round(gap_pct, 1),
        "gap_absolute":     round(optimized["value"] - current["value"]),
    }


# ─────────────────────────────────────────────
# PASSO 3 — RECOMMENDATION ENGINE
# ─────────────────────────────────────────────

def generate_recommendations(scores: dict, raw_inputs: dict, objective: str = None) -> list:
    """
    Genera le Top 3 azioni prioritarie confrontando gli score
    attuali con soglie critiche per ogni variabile.

    Logica:
      1. Valuta ogni condizione critica
      2. Assegna un impatto stimato sul valore (%)
      3. Ordina per impatto decrescente
      4. Restituisce le prime 3

    L'impatto % è una stima basata sulla variazione attesa del SQF
    applicata alla formula di valutazione. Non è una promessa —
    è un ordine di grandezza per prioritizzare le azioni.

    Il parametro 'objective' personalizza le raccomandazioni:
      - 'exit'        → priorità a trasferibilità e dipendenza
      - 'investitori' → priorità a crescita e ricorrenza
      - 'crescita'    → priorità a scalabilità e digitale
      - None          → raccomandazioni standard per impatto
    """
    actions = []

    # ── CAPITALE FINANZIARIO ──────────────────

    if raw_inputs.get("client_concentration_pct", 0) > 50:
        actions.append({
            "rank":    1,
            "title":   "Riduci la concentrazione clienti",
            "desc":    "Porta i top-3 clienti sotto il 40% del fatturato. "
                       "Diversifica il portafoglio con almeno 5 nuovi clienti mid-size.",
            "impact":  12,
            "capital": "financial",
            "horizon": "18–24 mesi",
            "sqf_delta": "+0.12 SQF",
        })

    if raw_inputs.get("recurring_revenue_pct", 0) < 30:
        actions.append({
            "rank":    2,
            "title":   "Introduci ricavi ricorrenti",
            "desc":    "Lancia un modello subscription o contratti pluriennali. "
                       "Target: portare la quota ricorrente sopra il 40%.",
            "impact":  9,
            "capital": "financial",
            "horizon": "12–18 mesi",
            "sqf_delta": "+0.09 SQF",
        })

    # ── CAPITALE UMANO ────────────────────────

    if raw_inputs.get("founder_dependency", 0) >= 4:
        actions.append({
            "rank":    3,
            "title":   "Rafforza il middle management",
            "desc":    "Riduci la dipendenza operativa dal fondatore. "
                       "Delega almeno 3 funzioni chiave a manager autonomi entro 24 mesi.",
            "impact":  7,
            "capital": "human",
            "horizon": "24–36 mesi",
            "sqf_delta": "+0.07 SQF",
        })

    if raw_inputs.get("management_structure", 0) <= 2:
        actions.append({
            "rank":    4,
            "title":   "Struttura il team manageriale",
            "desc":    "Definisci ruoli, responsabilità e KPI per ogni funzione. "
                       "Introduci un organigramma operativo condiviso.",
            "impact":  6,
            "capital": "human",
            "horizon": "12–18 mesi",
            "sqf_delta": "+0.06 SQF",
        })

    # ── CAPITALE TECNOLOGICO ──────────────────

    if raw_inputs.get("digital_maturity", 0) <= 2:
        actions.append({
            "rank":    5,
            "title":   "Accelera la maturità digitale",
            "desc":    "Digitalizza i processi core (operations, CRM, finance). "
                       "Target: eliminare i processi su carta entro 18 mesi.",
            "impact":  8,
            "capital": "technological",
            "horizon": "18–24 mesi",
            "sqf_delta": "+0.08 SQF",
        })

    if raw_inputs.get("tech_investment_pct", 0) < 2:
        actions.append({
            "rank":    6,
            "title":   "Aumenta l'investimento tecnologico",
            "desc":    "Porta il tech investment almeno al 3–4% del fatturato. "
                       "Focalizza su automazione e sistemi abilitanti.",
            "impact":  5,
            "capital": "technological",
            "horizon": "12–24 mesi",
            "sqf_delta": "+0.05 SQF",
        })

    if raw_inputs.get("business_model_scalability", 0) <= 2:
        actions.append({
            "rank":    7,
            "title":   "Migliora la scalabilità del modello",
            "desc":    "Riduci i costi variabili per unità di crescita. "
                       "Identifica i processi che non scalano e automatizzali.",
            "impact":  6,
            "capital": "technological",
            "horizon": "24–36 mesi",
            "sqf_delta": "+0.06 SQF",
        })

    # ── CAPITALE RELAZIONALE ──────────────────

    if raw_inputs.get("network_partnership_strength", 0) <= 2:
        actions.append({
            "rank":    8,
            "title":   "Sviluppa partnership strategiche",
            "desc":    "Costruisci un ecosistema di almeno 3 partner certificati. "
                       "Punta a co-marketing, referral o integrazioni di prodotto.",
            "impact":  5,
            "capital": "relational",
            "horizon": "18–24 mesi",
            "sqf_delta": "+0.05 SQF",
        })

    # ── PERSONALIZZAZIONE PER OBIETTIVO ───────

    if objective == "Preparazione exit/vendita":
        # In ottica exit la trasferibilità vale di più
        for a in actions:
            if a["capital"] == "human":
                a["impact"] += 3

    elif objective == "Ricerca investitori":
        # Gli investitori premiano crescita e ricorrenza
        for a in actions:
            if a["capital"] in ["financial", "technological"]:
                a["impact"] += 2

    # Ordina per impatto e restituisce top 3
    actions_sorted = sorted(actions, key=lambda x: x["impact"], reverse=True)
    return actions_sorted[:3]


# ─────────────────────────────────────────────
# FUNZIONE PRINCIPALE — esegue tutto il Livello 3
# ─────────────────────────────────────────────

def run_valuation(scoring_output: dict, raw_inputs: dict, sector: str, objective: str = None) -> dict:
    """
    Funzione principale del Livello 3.
    Riceve l'output del Livello 2 e i dati grezzi originali.
    Restituisce l'output completo pronto per il dashboard.

    Input:
      scoring_output — dizionario output di run_scoring_model() dal L2
      raw_inputs     — dizionario degli input originali dell'imprenditore
      sector         — stringa settore
      objective      — obiettivo dell'imprenditore (opzionale)

    Output: dizionario completo con tutti i dati del dashboard
    """
    ebitda = raw_inputs["ebitda"]
    sqf    = scoring_output["sqf"]
    gf     = scoring_output["gf"]

    # Calcoli
    valuation     = calculate_value(ebitda, sector, sqf, gf)
    value_gap     = calculate_value_gap(ebitda, sector, sqf, gf)

    # _ebitda_margin_pct e _cagr_pct sono presenti solo nel flusso completo L1→L3.
    # Se run_valuation() viene chiamata standalone questi campi potrebbero mancare.
    from recommender import generate_recommendations
    actions = generate_recommendations(
        scores            = scoring_output["scores"],
        raw_inputs        = raw_inputs,
        ebitda_margin_pct = raw_inputs.get("_ebitda_margin_pct", 0),
        cagr_pct          = raw_inputs.get("_cagr_pct", 0),
        objective         = objective,
        lang              = "it",
        sector            = sector
    )

    return {
        # Valutazione
        "estimated_value":   valuation["value"],
        "value_min":         valuation["value_min"],
        "value_max":         valuation["value_max"],
        "multiple_used":     valuation["multiple_used"],

        # Value Gap
        "value_gap_pct":     value_gap["gap_pct"],
        "optimized_value":   value_gap["optimized_value"],
        "gap_absolute":      value_gap["gap_absolute"],

        # Score e indici (dal L2)
        "scores":            scoring_output["scores"],
        "sqf":               sqf,
        "gf":                gf,
        "quality_score":     scoring_output["quality_score"],
        "risk_index":        scoring_output["risk_index"],
        "scalability_index": scoring_output["scalability_index"],
        "benchmarks":        scoring_output["benchmarks"],
        "gaps_vs_benchmark": scoring_output["gaps_vs_benchmark"],

        # Raccomandazioni
        "top3_actions":      actions,
    }


# ─────────────────────────────────────────────
# FUNZIONE DI FORMATTAZIONE per output leggibile
# ─────────────────────────────────────────────

def format_currency(value: float) -> str:
    """Formatta un valore in € leggibile (es. 1.960.000 → € 1.96M)"""
    if value >= 1_000_000:
        return f"€ {value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"€ {value/1_000:.0f}K"
    return f"€ {value:.0f}"