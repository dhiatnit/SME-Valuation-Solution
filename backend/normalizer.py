"""
VALUE INTELLIGENCE PLATFORM
Livello 1 — Normalizzazione delle Variabili

Ogni variabile viene portata su scala 0.0 – 1.0
Le variabili inverse (es. founder dependency, client concentration)
vengono penalizzate: più alto il valore grezzo, più basso il normalizzato.
"""


# ─────────────────────────────────────────────
# SOGLIE SETTORIALI — CALIBRATE SU DATI REALI
# ─────────────────────────────────────────────

# Fonte: AIDA Bureau van Dijk, Università Cattolica del Sacro Cuore, aprile 2026
# Campione: PMI italiane fatturato 2–50M€, per codice ATECO
EBITDA_THRESHOLDS = {
    "Tecnologia/SaaS":      {"q1": 4.32, "median": 9.95,  "q3": 18.86},
    "Servizi B2B":          {"q1": 1.99, "median": 7.69,  "q3": 18.09},
    "Manifatturiero":       {"q1": 5.27, "median": 9.54,  "q3": 15.57},
    "Healthcare":           {"q1": 5.24, "median": 10.61, "q3": 17.83},
    "Retail/GDO":           {"q1": 1.11, "median": 3.21,  "q3":  6.40},
    "Edilizia/Immobiliare": {"q1": 1.60, "median": 4.35,  "q3":  9.35},
    "Altro":                {"q1": 3.00, "median": 7.00,  "q3": 13.50},
}

# Fonte: stime aggregate ISTAT/Mediobanca/ANCE, mercato italiano PMI, periodo di riferimento 2021–2023
CAGR_THRESHOLDS = {
    "Tecnologia/SaaS":      {"q1": 3.0,  "median": 9.0,  "q3": 20.0},
    "Servizi B2B":          {"q1": 1.0,  "median": 4.0,  "q3":  9.0},
    "Manifatturiero":       {"q1": 1.0,  "median": 4.0,  "q3": 10.0},
    "Healthcare":           {"q1": 2.0,  "median": 5.0,  "q3": 11.0},
    "Retail/GDO":           {"q1":-1.0,  "median": 3.0,  "q3":  7.0},
    "Edilizia/Immobiliare": {"q1": 1.0,  "median": 4.0,  "q3": 10.0},
    "Altro":                {"q1": 1.5,  "median": 5.0,  "q3": 10.0},
}

# Fonte: AIDA Bureau van Dijk, Università Cattolica del Sacro Cuore, aprile 2026
# Campione: PMI italiane fatturato 2–50M€, per codice ATECO
# INVERSO: più alto il ratio, più alto il rischio finanziario
DEBT_EBITDA_THRESHOLDS = {
    "Tecnologia/SaaS":      {"q1": 0.00, "median": 0.01, "q3": 0.89},
    "Servizi B2B":          {"q1": 0.00, "median": 0.00, "q3": 0.84},
    "Manifatturiero":       {"q1": 0.03, "median": 0.90, "q3": 3.07},
    "Healthcare":           {"q1": 0.00, "median": 0.34, "q3": 1.73},
    "Retail/GDO":           {"q1": 0.00, "median": 0.30, "q3": 2.29},
    "Edilizia/Immobiliare": {"q1": 0.00, "median": 0.37, "q3": 2.35},
    "Altro":                {"q1": 0.01, "median": 0.32, "q3": 1.86},
}


# ─────────────────────────────────────────────
# VARIABILI QUANTITATIVE DA BILANCIO
# ─────────────────────────────────────────────

def normalize_ebitda_margin(margin_pct: float, sector: str = "Altro") -> float:
    """
    EBITDA Margin normalizzato su scala 0.0–1.0.
    Calibrato su dati reali AIDA Bureau van Dijk, aprile 2026.
    Campione: PMI italiane fatturato 2–50M€, per codice ATECO.

    Logica: Q1 → 0.2 | Mediana → 0.5 | Q3 → 0.7
    Interpolazione lineare tra i breakpoint.
    """
    t = EBITDA_THRESHOLDS.get(sector, EBITDA_THRESHOLDS["Altro"])
    if margin_pct < 0:
        return 0.0
    elif margin_pct < t["q1"]:
        return round(0.2 * (margin_pct / t["q1"]), 4) if t["q1"] > 0 else 0.1
    elif margin_pct < t["median"]:
        return round(0.2 + 0.3 * (margin_pct - t["q1"]) / (t["median"] - t["q1"]), 4)
    elif margin_pct < t["q3"]:
        return round(0.5 + 0.2 * (margin_pct - t["median"]) / (t["q3"] - t["median"]), 4)
    elif margin_pct < t["q3"] * 1.6:
        return round(0.7 + 0.2 * (margin_pct - t["q3"]) / (t["q3"] * 0.6), 4)
    else:
        return 1.0


def normalize_revenue_cagr(cagr_pct: float, sector: str = "Altro") -> float:
    """
    Revenue CAGR normalizzato su scala 0.0–1.0.
    Calibrato su stime aggregate ISTAT/Mediobanca/ANCE per PMI italiane, 2021–2023.
    Il CAGR viene calcolato dal Livello 1 come (Rev_Y3/Rev_Y1)^(1/2) - 1.

    Logica: Q1 → 0.2 | Mediana → 0.5 | Q3 → 0.7
    Retail può avere Q1 negativo: declino gestito con penalizzazione continua.
    """
    t = CAGR_THRESHOLDS.get(sector, CAGR_THRESHOLDS["Altro"])
    if cagr_pct < -5:
        return 0.0
    elif cagr_pct < t["q1"]:
        return round(0.2 * (cagr_pct + 5) / (t["q1"] + 5), 4) if (t["q1"] + 5) > 0 else 0.1
    elif cagr_pct < t["median"]:
        return round(0.2 + 0.3 * (cagr_pct - t["q1"]) / (t["median"] - t["q1"]), 4)
    elif cagr_pct < t["q3"]:
        return round(0.5 + 0.2 * (cagr_pct - t["median"]) / (t["q3"] - t["median"]), 4)
    elif cagr_pct < t["q3"] * 1.5:
        return round(0.7 + 0.15 * (cagr_pct - t["q3"]) / (t["q3"] * 0.5), 4)
    else:
        return 1.0


def normalize_recurring_revenue(recurring_pct: float) -> float:
    """
    Percentuale di ricavi ricorrenti su totale (0–100)
    Dato dichiarato dall'imprenditore (non estraibile da bilancio)
    """
    if recurring_pct < 10:
        return 0.1
    elif recurring_pct < 25:
        return 0.3
    elif recurring_pct < 50:
        return 0.6
    elif recurring_pct < 75:
        return 0.8
    else:
        return 1.0


def normalize_client_concentration(top3_pct: float) -> float:
    """
    Concentrazione top-3 clienti su fatturato totale (0–100)
    INVERSA: più concentrato = più rischioso = score più basso
    Dato dichiarato dall'imprenditore
    """
    if top3_pct > 70:
        return 0.1
    elif top3_pct > 50:
        return 0.3
    elif top3_pct > 35:
        return 0.5
    elif top3_pct > 20:
        return 0.8
    else:
        return 1.0


def normalize_tech_investment(tech_rev_ratio_pct: float) -> float:
    """
    Tech investment / Revenue in percentuale (es. 3.5 per 3.5%)
    Dato ibrido: dichiarato dall'imprenditore + validato da bilancio
    """
    if tech_rev_ratio_pct < 1:
        return 0.1
    elif tech_rev_ratio_pct < 2:
        return 0.3
    elif tech_rev_ratio_pct < 4:
        return 0.5
    elif tech_rev_ratio_pct < 6:
        return 0.7
    elif tech_rev_ratio_pct < 10:
        return 0.9
    else:
        return 1.0


def normalize_debt_ebitda(net_financial_position: float, ebitda: float, sector: str = "Altro") -> float:
    """
    Debt/EBITDA normalizzato su scala 0.0–1.0.
    Calibrato su dati reali AIDA Bureau van Dijk, aprile 2026.
    INVERSO: ratio più alto = più indebitamento = score più basso.

    Se NFP è negativa (azienda ha più liquidità che debiti) → score 1.0.
    Se EBITDA è zero o negativo → score 0.1 (segnale di rischio estremo).

    Logica:
      ratio ≤ 0         → 1.0  (posizione netta di cassa)
      ratio ≤ Q1        → 0.9  (ottimo, pochissimo debito)
      Q1 < ratio ≤ median → interpolazione lineare 0.7–0.9
      median < ratio ≤ Q3 → interpolazione lineare 0.3–0.7
      Q3 < ratio ≤ Q3*2  → interpolazione lineare 0.1–0.3
      ratio > Q3*2       → 0.05 (leverage estremo)
    """
    if ebitda <= 0:
        return 0.1

    ratio = net_financial_position / ebitda

    if ratio <= 0:
        return 1.0

    t = DEBT_EBITDA_THRESHOLDS.get(sector, DEBT_EBITDA_THRESHOLDS["Altro"])

    # Gestione edge case: settori con Q1 = 0 e median = 0 (Servizi B2B, Tecnologia)
    # In questi casi saltiamo l'interpolazione Q1→median e andiamo direttamente a median→Q3
    if ratio <= t["q1"] and t["q1"] > 0:
        return round(0.9 - 0.2 * (ratio / t["q1"]) * 0, 4)  # flat a 0.9

    if t["median"] > 0 and ratio <= t["median"]:
        # Interpolazione lineare 0.9 → 0.7 tra Q1 e median
        if t["median"] - t["q1"] > 0:
            return round(0.9 - 0.2 * (ratio - t["q1"]) / (t["median"] - t["q1"]), 4)
        else:
            return 0.7

    if ratio <= t["q3"]:
        # Interpolazione lineare 0.7 → 0.3 tra median e Q3
        denom = t["q3"] - t["median"] if t["q3"] - t["median"] > 0 else 1
        return round(0.7 - 0.4 * (ratio - t["median"]) / denom, 4)

    if ratio <= t["q3"] * 2:
        # Interpolazione lineare 0.3 → 0.1 tra Q3 e Q3*2
        return round(0.3 - 0.2 * (ratio - t["q3"]) / t["q3"], 4)

    return 0.05


# ─────────────────────────────────────────────
# VARIABILI QUALITATIVE (scala 1–5)
# ─────────────────────────────────────────────

def normalize_qualitative(value: int) -> float:
    """
    Normalizzazione lineare standard per variabili qualitative 1–5
    Usata per: management_structure, digital_maturity,
               client_portfolio_quality, business_model_scalability,
               network_partnership_strength
    """
    if value < 1 or value > 5:
        raise ValueError(f"Valore qualitativo deve essere tra 1 e 5, ricevuto: {value}")
    return (value - 1) / 4


def normalize_inverse(value: int) -> float:
    """
    Normalizzazione lineare inversa per variabili qualitative 1–5
    5 = valore massimo negativo → score 0.0
    1 = valore minimo negativo  → score 1.0
    Usata per: key_man_risk
    """
    if value < 1 or value > 5:
        raise ValueError(f"Valore qualitativo deve essere tra 1 e 5, ricevuto: {value}")
    return (5 - value) / 4

# ── HUMAN CAPITAL ─────────────────────────────
# key_man_risk usa normalize_inverse() direttamente.
# span_of_control, skill_investment, talent_retention, sop_standardization
# usano tutti normalize_qualitative() direttamente.

# ── TECHNOLOGICAL CAPITAL ─────────────────────

# operational_digitalization, data_storage, workflow_automation,
# proprietary_dataset, crm_adoption
# usano tutti normalize_qualitative() direttamente.

# ── RELATIONAL CAPITAL ───────────────────────

# network_quality, partnership_structure, brand_assets,
# ecosystem_referrals, repeat_customers
# usano tutti normalize_qualitative() direttamente.


# ─────────────────────────────────────────────
# CALCOLO CAGR DA RICAVI GREZZI
# ─────────────────────────────────────────────

def calculate_cagr(revenue_y1: float, revenue_y3: float) -> float:
    """
    Calcola il CAGR a 2 anni dai ricavi anno 1 e anno 3
    Formula: (Rev_Y3 / Rev_Y1)^(1/2) - 1
    Restituisce la percentuale (es. 8.5 per 8.5%)
    """
    if revenue_y1 <= 0:
        raise ValueError("Revenue anno 1 deve essere positivo")
    cagr = ((revenue_y3 / revenue_y1) ** 0.5) - 1
    return round(cagr * 100, 2)


# ─────────────────────────────────────────────
# FUNZIONE PRINCIPALE — normalizza tutti gli input
# ─────────────────────────────────────────────

def normalize_all_inputs(raw_inputs: dict, sector: str = "Altro") -> dict:
    """
    Riceve il dizionario grezzo degli input e restituisce
    tutti i valori normalizzati su scala 0–1.

    Input attesi (raw_inputs):
    {
        # Da bilancio
        "revenue_y1": float,              # Ricavi anno 1 in €
        "revenue_y2": float,              # Ricavi anno 2 in €
        "revenue_y3": float,              # Ricavi anno 3 in €
        "ebitda": float,                  # EBITDA in €
        "net_financial_position": float,  # Posizione finanziaria netta in €
        "tech_investment_pct": float,     # Tech invest / revenue %

        # Dichiarati dall'imprenditore
        "recurring_revenue_pct": float,    # % ricavi ricorrenti
        "client_concentration_pct": float, # % top-3 clienti

        # Human Capital (1–5)
        "key_man_risk": int,         # Q1 — ruoli C-level del fondatore (INVERSA)
        "span_of_control": int,      # Q2 — % direct reports / totale dipendenti
        "skill_investment": int,     # Q3 — % fatturato su formazione
        "talent_retention": int,     # Q4 — % dipendenti rimasti ultimi 12 mesi
        "sop_standardization": int,  # Q5 — grado di standardizzazione processi

        # Technological Capital (1–5)
        "operational_digitalization": int,  # Q1 — gestione operazioni quotidiane
        "data_storage": int,                # Q2 — dove sono stored le informazioni
        "workflow_automation": int,         # Q3 — numero workflow automatizzati
        "proprietary_dataset": int,         # Q4 — dimensione dataset proprietario
        "crm_adoption": int,                # Q5 — % clienti gestiti in CRM

        # Relational Capital (1–5)
        "network_quality": int,         # Q1 — come i clienti trovano l'azienda
        "partnership_structure": int,   # Q2 — numero partnership firmate
        "brand_assets": int,            # Q3 — numero asset digitali pubblici
        "ecosystem_referrals": int,     # Q4 — partner che mandano clienti attivamente
        "repeat_customers": int,        # Q5 — % clienti che riacquistano
    }
    """

    # Calcoli derivati da bilancio
    cagr = calculate_cagr(raw_inputs["revenue_y1"], raw_inputs["revenue_y3"])
    ebitda_margin = (raw_inputs["ebitda"] / raw_inputs["revenue_y3"]) * 100
    debt_ebitda_ratio = raw_inputs["net_financial_position"] / raw_inputs["ebitda"] \
                        if raw_inputs["ebitda"] > 0 else 0

    normalized = {
        # Quantitativi — sector-aware
        "ebitda_margin":           normalize_ebitda_margin(ebitda_margin, sector),
        "revenue_cagr":            normalize_revenue_cagr(cagr, sector),
        "recurring_revenue":       normalize_recurring_revenue(raw_inputs["recurring_revenue_pct"]),
        "client_concentration":    normalize_client_concentration(raw_inputs["client_concentration_pct"]),
        "debt_ebitda":             normalize_debt_ebitda(
                                       raw_inputs["net_financial_position"],
                                       raw_inputs["ebitda"],
                                       sector
                                   ),
        "tech_investment":         normalize_tech_investment(raw_inputs["tech_investment_pct"]),

        # Human Capital
        "key_man_risk":               normalize_inverse(raw_inputs["key_man_risk"]),
        "span_of_control":            normalize_qualitative(raw_inputs["span_of_control"]),
        "skill_investment":           normalize_qualitative(raw_inputs["skill_investment"]),
        "talent_retention":           normalize_qualitative(raw_inputs["talent_retention"]),
        "sop_standardization":        normalize_qualitative(raw_inputs["sop_standardization"]),

        # Technological Capital
        "operational_digitalization": normalize_qualitative(raw_inputs["operational_digitalization"]),
        "data_storage":               normalize_qualitative(raw_inputs["data_storage"]),
        "workflow_automation":        normalize_qualitative(raw_inputs["workflow_automation"]),
        "proprietary_dataset":        normalize_qualitative(raw_inputs["proprietary_dataset"]),
        "crm_adoption":               normalize_qualitative(raw_inputs["crm_adoption"]),

        # Relational Capital
        "network_quality":            normalize_qualitative(raw_inputs["network_quality"]),
        "partnership_structure":      normalize_qualitative(raw_inputs["partnership_structure"]),
        "brand_assets":               normalize_qualitative(raw_inputs["brand_assets"]),
        "ecosystem_referrals":        normalize_qualitative(raw_inputs["ecosystem_referrals"]),
        "repeat_customers":           normalize_qualitative(raw_inputs["repeat_customers"]),

        # Valori derivati (utili per Livello 2 e 3)
        "_cagr_pct":               cagr,
        "_ebitda_margin_pct":      round(ebitda_margin, 2),
        "_ebitda_raw":             raw_inputs["ebitda"],
        "_revenue_y3":             raw_inputs["revenue_y3"],
        "_debt_ebitda_ratio":      round(debt_ebitda_ratio, 2),
        "_net_financial_position": raw_inputs["net_financial_position"],
    }

    return normalized