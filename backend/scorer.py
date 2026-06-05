"""
VALUE INTELLIGENCE PLATFORM
Livello 2 — Scoring Model (4 Capitali)

Riceve le variabili normalizzate dal Livello 1 (scala 0–1)
e restituisce:
  - Score per ciascuno dei 4 capitali       [0–1]
  - SQF (Strategic Quality Factor)          [0.6–1.4]
  - Quality Score (leggibile /100)          [0–100]
  - Risk Index                              [LOW / MEDIUM / HIGH]
  - Scalability Index                       [LOW / MEDIUM / HIGH]
  - GF (Growth Factor)                      [float]
"""


# ─────────────────────────────────────────────
# TABELLE DI CONTESTO
# ─────────────────────────────────────────────

# TODO: consolidare in constants.py (duplicato in valuation.py)
# Multipli EBITDA per settore (fonte: Mediobanca SME Report, Damodaran)
SECTOR_MULTIPLES = {
    "Tecnologia/SaaS":       7.5,
    "Servizi B2B":           5.5,
    "Manifatturiero":        4.5,
    "Healthcare":            6.0,
    "Retail/GDO":            4.0,
    "Edilizia/Immobiliare":  4.2,
    "Altro":                 5.0,
}

# Fattori di aggiustamento GF per settore
# Riflette la qualità attesa della crescita in quel mercato
SECTOR_GF_FACTORS = {
    "Tecnologia/SaaS":       1.20,
    "Servizi B2B":           1.00,
    "Manifatturiero":        0.85,
    "Healthcare":            1.10,
    "Retail/GDO":            0.90,
    "Edilizia/Immobiliare":  0.88,
    "Altro":                 1.00,
}

# Benchmark di settore per i 4 capitali
# financial: calcolato da dati AIDA + stime settoriali (aprile 2026)
# technological, human, relational: stime qualitative invariate
SECTOR_BENCHMARKS = {
    "Tecnologia/SaaS":      {"financial": 0.59, "technological": 0.78, "human": 0.62, "relational": 0.68},
    "Servizi B2B":          {"financial": 0.53, "technological": 0.52, "human": 0.58, "relational": 0.65},
    "Manifatturiero":       {"financial": 0.45, "technological": 0.42, "human": 0.53, "relational": 0.48},
    "Healthcare":           {"financial": 0.59, "technological": 0.55, "human": 0.68, "relational": 0.62},
    "Retail/GDO":           {"financial": 0.55, "technological": 0.48, "human": 0.50, "relational": 0.58},
    "Edilizia/Immobiliare": {"financial": 0.36, "technological": 0.38, "human": 0.50, "relational": 0.52},
    "Altro":                {"financial": 0.50, "technological": 0.50, "human": 0.55, "relational": 0.56},
}


# ─────────────────────────────────────────────
# PASSO 1 — SCORE PER CAPITALE
# ─────────────────────────────────────────────

def score_financial_capital(n: dict) -> float:
    """
    Capitale Finanziario — peso nel SQF: varia per settore (default 35%)
    Misura la solidità e qualità economica dell'azienda.

    Variabili (5):
      - ebitda_margin      (25%) → redditività operativa
      - revenue_cagr       (20%) → traiettoria di crescita
      - recurring_revenue  (20%) → qualità e prevedibilità dei ricavi
      - client_concentration (15%) → rischio di concentrazione (inversa)
      - debt_ebitda        (20%) → livello di indebitamento (inversa)

    Fonte soglie Debt/EBITDA: AIDA Bureau van Dijk, aprile 2026
    """
    score = (
        n["ebitda_margin"]       * 0.25 +
        n["revenue_cagr"]        * 0.20 +
        n["recurring_revenue"]   * 0.20 +
        n["client_concentration"]* 0.15 +
        n["debt_ebitda"]         * 0.20
    )
    return round(score, 4)


def score_technological_capital(n: dict) -> float:
    """
    Capitale Tecnologico — peso nel SQF: varia per settore (default 25%)
    Misura la maturità digitale e la capacità di crescere
    senza aumentare proporzionalmente i costi.

    Variabili (6):
      - operational_digitalization (25%) → integrazione digitale nelle operazioni
      - workflow_automation         (25%) → automazione dei processi
      - tech_investment             (20%) → investimento tecnologico su fatturato (quantitativo)
      - crm_adoption                (15%) → gestione clienti in CRM
      - data_storage                (10%) → centralizzazione informazioni
      - proprietary_dataset          (5%) → asset dati proprietari
    """
    score = (
        n["operational_digitalization"] * 0.25 +
        n["workflow_automation"]        * 0.25 +
        n["tech_investment"]            * 0.20 +
        n["crm_adoption"]               * 0.15 +
        n["data_storage"]               * 0.10 +
        n["proprietary_dataset"]        * 0.05
    )
    return round(score, 4)


def score_human_capital(n: dict) -> float:
    """
    Capitale Umano & Organizzativo — peso nel SQF: varia per settore (default 25%)
    Misura la trasferibilità e solidità organizzativa dell'azienda.

    Variabili (5):
      - key_man_risk          (35%) → dipendenza dal fondatore (inversa — già invertita in L1)
      - span_of_control       (25%) → struttura di delega e middle management
      - talent_retention      (20%) → stabilità della forza lavoro
      - sop_standardization   (15%) → maturità dei processi operativi
      - skill_investment       (5%) → investimento nello sviluppo delle competenze
    """
    score = (
        n["key_man_risk"]        * 0.35 +
        n["span_of_control"]     * 0.25 +
        n["talent_retention"]    * 0.20 +
        n["sop_standardization"] * 0.15 +
        n["skill_investment"]    * 0.05
    )
    return round(score, 4)


def score_relational_capital(n: dict) -> float:
    """
    Capitale Relazionale — peso nel SQF: varia per settore (default 15%)
    Misura la forza della rete e delle relazioni strategiche.

    Nota: client_concentration è RIMOSSA da questo capitale
    (già usata nel capitale finanziario). repeat_customers
    sostituisce la proxy di fidelizzazione.

    Variabili (5):
      - network_quality        (30%) → canali di acquisizione clienti indipendenti
      - ecosystem_referrals    (25%) → partner che generano clienti attivamente
      - repeat_customers       (20%) → fidelizzazione e lealtà del cliente
      - partnership_structure  (15%) → solidità della rete di partnership formali
      - brand_assets           (10%) → visibilità e presenza digitale
    """
    score = (
        n["network_quality"]       * 0.30 +
        n["ecosystem_referrals"]   * 0.25 +
        n["repeat_customers"]      * 0.20 +
        n["partnership_structure"] * 0.15 +
        n["brand_assets"]          * 0.10
    )
    return round(score, 4)


# ─────────────────────────────────────────────
# PASSO 2 — SQF (Strategic Quality Factor)
# ─────────────────────────────────────────────

def calculate_sqf(scores: dict) -> float:
    """
    Aggrega i 4 score nel SQF finale.
    Range output: [0.6 – 1.4]

    Pesi:
      Finanziario   35% — più pesante, oggettivo e verificabile
      Tecnologico   25% — abilitante per la crescita
      Umano         25% — critico per trasferibilità
      Relazionale   15% — rilevante ma più soggettivo

    Formula di riscalamento:
      sqf_raw è in [0, 1]
      SQF = 0.6 + (sqf_raw × 0.8) → mappa su [0.6, 1.4]

    Interpretazione:
      SQF < 0.8   → azienda con fragilità strutturali significative
      SQF 0.8–1.0 → azienda nella media
      SQF 1.0–1.2 → azienda solida, sopra la media
      SQF > 1.2   → azienda eccellente, alta attrattività
    """
    sqf_raw = (
        scores["financial"]    * 0.35 +
        scores["technological"]* 0.25 +
        scores["human"]        * 0.25 +
        scores["relational"]   * 0.15
    )
    sqf = 0.6 + (sqf_raw * 0.8)
    return round(sqf, 4)


# ─────────────────────────────────────────────
# PASSO 3 — GROWTH FACTOR (GF)
# ─────────────────────────────────────────────

def calculate_gf(n: dict, sector: str) -> float:
    """
    Growth Factor: misura la qualità e sostenibilità della crescita attesa.
    Combina CAGR (velocità) con Recurring Revenue (qualità).
    Viene aggiustato per settore e normalizzato per non distorcere
    eccessivamente la valutazione finale.

    Formula:
      gf_raw = (CAGR_norm × 60%) + (Recurring_norm × 40%)
      GF = gf_raw × fattore_settore

    Range tipico: [0.3 – 1.2]
    """
    gf_raw = (
        n["revenue_cagr"]      * 0.60 +
        n["recurring_revenue"] * 0.40
    )
    sector_factor = SECTOR_GF_FACTORS.get(sector, 1.0)
    gf = gf_raw * sector_factor
    return round(gf, 4)


# ─────────────────────────────────────────────
# PASSO 4 — INDICI DERIVATI
# ─────────────────────────────────────────────

def calculate_quality_score(sqf: float) -> int:
    """
    Trasforma il SQF [0.6–1.4] in un punteggio leggibile [0–100].
    Usato nel dashboard come 'Quality Score'.

    Formula: ((SQF - 0.6) / 0.8) × 100
    """
    score = ((sqf - 0.6) / 0.8) * 100
    return round(score)


def calculate_risk_index(scores: dict) -> dict:
    """
    Risk Index: misura il rischio strutturale complessivo.
    Pesa principalmente il capitale finanziario e umano
    perché sono i driver principali di rischio per investitori.

    Formula:
      risk_raw = 1 - (Financial×50% + Human×30% + Relational×20%)
      Più basso il risk_raw, più bassa la qualità → più alto il rischio

    Soglie:
      risk_raw < 0.30 → HIGH   (azienda fragile)
      risk_raw < 0.60 → MEDIUM (rischi presenti ma gestibili)
      risk_raw ≥ 0.60 → LOW    (azienda solida)
    """
    risk_raw = (
        scores["financial"]   * 0.50 +
        scores["human"]       * 0.30 +
        scores["relational"]  * 0.20
    )
    if risk_raw < 0.30:
        return {"label": "HIGH",   "color": "#e17055", "value": round(risk_raw, 4)}
    elif risk_raw < 0.60:
        return {"label": "MEDIUM", "color": "#fdcb6e", "value": round(risk_raw, 4)}
    else:
        return {"label": "LOW",    "color": "#00b894", "value": round(risk_raw, 4)}


def calculate_scalability_index(scores: dict, n: dict) -> dict:
    """
    Scalability Index: misura il potenziale di crescita senza
    aumentare proporzionalmente i costi.
    Pesa tecnologico e scalability come driver principali.

    Soglie:
      < 0.40 → LOW
      < 0.70 → MEDIUM
      ≥ 0.70 → HIGH
    """
    scalability_raw = (
        scores["technological"]  * 0.50 +
        n["workflow_automation"] * 0.30 +
        scores["relational"]     * 0.20
    )
    if scalability_raw < 0.40:
        return {"label": "LOW",    "color": "#e17055", "value": round(scalability_raw, 4)}
    elif scalability_raw < 0.70:
        return {"label": "MEDIUM", "color": "#fdcb6e", "value": round(scalability_raw, 4)}
    else:
        return {"label": "HIGH",   "color": "#00b894", "value": round(scalability_raw, 4)}


# ─────────────────────────────────────────────
# FUNZIONE PRINCIPALE — esegue tutto il Livello 2
# ─────────────────────────────────────────────

def run_scoring_model(normalized: dict, sector: str) -> dict:
    """
    Riceve l'output del Livello 1 (normalized) e il settore.
    Restituisce tutti gli score e indici calcolati.

    Input:
      normalized — dizionario output di normalize_all_inputs() dal L1
      sector     — stringa settore (es. "Servizi B2B")

    Output:
      {
        scores: { financial, technological, human, relational },
        sqf,
        gf,
        quality_score,
        risk_index,
        scalability_index,
        benchmarks,
        gaps_vs_benchmark
      }
    """
    # Score per capitale
    scores = {
        "financial":     score_financial_capital(normalized),
        "technological": score_technological_capital(normalized),
        "human":         score_human_capital(normalized),
        "relational":    score_relational_capital(normalized),
    }

    # SQF e GF
    sqf = calculate_sqf(scores)
    gf  = calculate_gf(normalized, sector)

    # Indici derivati
    quality_score     = calculate_quality_score(sqf)
    risk_index        = calculate_risk_index(scores)
    scalability_index = calculate_scalability_index(scores, normalized)

    # Benchmark e gap vs settore
    benchmarks = SECTOR_BENCHMARKS.get(sector, SECTOR_BENCHMARKS["Altro"])
    gaps = {
        cap: round(scores[cap] - benchmarks[cap], 4)
        for cap in scores
    }

    return {
        "scores":            scores,
        "sqf":               sqf,
        "gf":                gf,
        "quality_score":     quality_score,
        "risk_index":        risk_index,
        "scalability_index": scalability_index,
        "benchmarks":        benchmarks,
        "gaps_vs_benchmark": gaps,
    }