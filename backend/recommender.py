"""
VALUE INTELLIGENCE PLATFORM
Recommendation Engine — Multilingua (IT / EN)
Autore: G. Tedeschi (Master in Data Science for Management - Cattolica)

Logica di selezione:
  1. Ogni azione ha condizioni di attivazione basate su soglie critiche
  2. L'impatto è DINAMICO — proporzionale al gap dal valore ottimale
  3. Le azioni combo (più variabili critiche) ricevono un bonus
  4. L'obiettivo dell'imprenditore modifica i pesi finali
  5. La lingua viene passata come parametro ("it" o "en")
  6. Si restituiscono le Top 3 per impatto finale
"""


# ─────────────────────────────────────────────
# VALORI OTTIMALI DI RIFERIMENTO
# ─────────────────────────────────────────────

OPTIMAL = {
    "client_concentration_pct":    30,
    "recurring_revenue_pct":       60,
    "ebitda_margin_pct":           20,
    "cagr_pct":                    10,
    "tech_investment_pct":          5,
    "key_man_risk":                 2,   # target: fondatore con ≤1 ruolo C-level
    "span_of_control":              5,   # target: >25% direct reports
    "skill_investment":             4,   # target: >1.5% su fatturato
    "talent_retention":             4,   # target: 90-95%
    "sop_standardization":          4,   # target: alto livello di standardizzazione
    "operational_digitalization":   4,   # target: app separate per ogni area
    "workflow_automation":          4,   # target: 6-10 workflow automatizzati
    "crm_adoption":                 4,   # target: 50-90% clienti in CRM
    "network_quality":              4,   # target: mostly through organic/referral
    "partnership_structure":        4,   # target: 2-3 partnership firmate
    "repeat_customers":             4,   # target: 31-60%
}

# Target ottimali sector-specific: basati su Q3 AIDA (EBITDA) e Q3 stime ricerca (CAGR)
# Rappresentano l'obiettivo realistico per una PMI eccellente nel suo settore
OPTIMAL_EBITDA_BY_SECTOR = {
    "Tecnologia/SaaS":      18.9,   # Q3 AIDA
    "Servizi B2B":          18.1,   # Q3 AIDA
    "Manifatturiero":       15.6,   # Q3 AIDA
    "Healthcare":           17.8,   # Q3 AIDA
    "Retail/GDO":            6.4,   # Q3 AIDA — soglia di eccellenza per il Retail
    "Edilizia/Immobiliare":  9.4,   # Q3 AIDA
    "Altro":                13.5,
}

OPTIMAL_CAGR_BY_SECTOR = {
    "Tecnologia/SaaS":      20.0,   # Q3 stime ricerca
    "Servizi B2B":           9.0,
    "Manifatturiero":       10.0,
    "Healthcare":           11.0,
    "Retail/GDO":            7.0,
    "Edilizia/Immobiliare": 10.0,
    "Altro":                10.0,
}

# Moltiplicatore impatto per obiettivo — supporta IT e EN
OBJECTIVE_MULTIPLIERS = {
    "Preparazione exit/vendita":  {"human": 1.5, "financial": 1.3, "technological": 1.0, "relational": 1.1},
    "Preparing for exit/sale":    {"human": 1.5, "financial": 1.3, "technological": 1.0, "relational": 1.1},
    "Ricerca investitori":        {"financial": 1.4, "technological": 1.3, "human": 1.1, "relational": 1.0},
    "Seeking investors":          {"financial": 1.4, "technological": 1.3, "human": 1.1, "relational": 1.0},
    "Crescita organica":          {"technological": 1.4, "relational": 1.3, "financial": 1.1, "human": 1.0},
    "Organic growth":             {"technological": 1.4, "relational": 1.3, "financial": 1.1, "human": 1.0},
    "Passaggio generazionale":    {"human": 1.6, "relational": 1.2, "financial": 1.0, "technological": 0.9},
    "Generational transition":    {"human": 1.6, "relational": 1.2, "financial": 1.0, "technological": 0.9},
    "Stabilità":                  {"financial": 1.2, "human": 1.2, "technological": 1.0, "relational": 1.1},
    "Stability":                  {"financial": 1.2, "human": 1.2, "technological": 1.0, "relational": 1.1},
}


# ─────────────────────────────────────────────
# TESTI AZIONI — IT / EN
# ─────────────────────────────────────────────

ACTIONS_TEXT = {

    "riduci_concentrazione": {
        "it": {
            "title":  "Riduci la concentrazione clienti",
            "desc":   "I top-3 clienti rappresentano il {conc}% del fatturato — ogni cliente perso è un rischio sistemico.",
            "detail": "Diversifica con almeno 5 nuovi clienti mid-size. Valuta contratti pluriennali per ridurre il churn.",
            "kpi":    "Concentrazione: {conc}% → <40%",
        },
        "en": {
            "title":  "Reduce client concentration",
            "desc":   "Your top-3 clients account for {conc}% of revenue — losing any one of them is a systemic risk.",
            "detail": "Diversify with at least 5 new mid-size clients. Consider multi-year contracts to reduce churn.",
            "kpi":    "Concentration: {conc}% → <40%",
        },
    },

    "introduci_ricorrenti": {
        "it": {
            "title":  "Introduci ricavi ricorrenti",
            "desc":   "Solo il {rec}% del fatturato è ricorrente. Target: portarlo sopra il 50% con subscription o contratti.",
            "detail": "Lancia un modello subscription, retainer mensile o contratti pluriennali con rinnovo automatico.",
            "kpi":    "Ricavi ricorrenti: {rec}% → >50%",
        },
        "en": {
            "title":  "Introduce recurring revenue",
            "desc":   "Only {rec}% of your revenue is recurring. Target: bring it above 50% through subscriptions or contracts.",
            "detail": "Launch a subscription model, monthly retainer, or multi-year contracts with automatic renewal.",
            "kpi":    "Recurring revenue: {rec}% → >50%",
        },
    },

    "ottimizza_costi": {
        "it": {
            "title":  "Ottimizza la struttura dei costi",
            "desc":   "EBITDA margin al {margin}% — sotto la soglia di attrattività per investitori (15%+).",
            "detail": "Rivedi i costi fissi, negozia fornitori strategici, identifica linee di prodotto a bassa marginalità.",
            "kpi":    "EBITDA margin: {margin}% → >15%",
        },
        "en": {
            "title":  "Optimise cost structure",
            "desc":   "EBITDA margin at {margin}% — below the investor attractiveness threshold (15%+).",
            "detail": "Review fixed costs, renegotiate strategic suppliers, identify low-margin product or service lines.",
            "kpi":    "EBITDA margin: {margin}% → >15%",
        },
    },

    "accelera_crescita": {
        "it": {
            "title":  "Accelera la crescita del fatturato",
            "desc":   "CAGR al {cagr}% — sotto la media di settore. Una crescita bassa comprime il Growth Factor e il valore.",
            "detail": "Espandi in nuovi segmenti di mercato o geografie. Valuta upsell/cross-sell sulla base clienti esistente.",
            "kpi":    "CAGR: {cagr}% → >8%",
        },
        "en": {
            "title":  "Accelerate revenue growth",
            "desc":   "CAGR at {cagr}% — below sector average. Low growth compresses the Growth Factor and company value.",
            "detail": "Expand into new market segments or geographies. Consider upsell/cross-sell on your existing client base.",
            "kpi":    "CAGR: {cagr}% → >8%",
        },
    },

    "piano_resilienza": {
        "it": {
            "title":  "Piano di resilienza finanziaria",
            "desc":   "Doppio rischio critico: alta concentrazione clienti e quasi nessun ricavo ricorrente.",
            "detail": "Priorità assoluta: firma almeno 2 contratti pluriennali con clienti esistenti entro 6 mesi.",
            "kpi":    "Concentrazione <50% + Ricorrenti >25%",
        },
        "en": {
            "title":  "Financial resilience plan",
            "desc":   "Dual critical risk: high client concentration and almost no recurring revenue.",
            "detail": "Immediate priority: sign at least 2 multi-year contracts with existing clients within 6 months.",
            "kpi":    "Concentration <50% + Recurring >25%",
        },
    },

    "accelera_digitale": {
        "it": {
            "title":  "Accelera la maturità digitale",
            "desc":   "Maturità digitale a {dm}/5 — processi ancora manuali limitano efficienza e scalabilità.",
            "detail": "Digitalizza i processi core: CRM, operations, finance. Elimina i processi su carta entro 18 mesi.",
            "kpi":    "Digital maturity: {dm}/5 → 4/5",
        },
        "en": {
            "title":  "Accelerate digital maturity",
            "desc":   "Digital maturity at {dm}/5 — manual processes still limit efficiency and scalability.",
            "detail": "Digitalise core processes: CRM, operations, finance. Eliminate paper-based processes within 18 months.",
            "kpi":    "Digital maturity: {dm}/5 → 4/5",
        },
    },

    "aumenta_tech": {
        "it": {
            "title":  "Aumenta l'investimento in tecnologia",
            "desc":   "Tech investment al {tech}% del fatturato — insufficiente per sostenere la crescita digitale.",
            "detail": "Porta il tech investment al 4–5% del fatturato. Focalizza su automazione, CRM e sistemi abilitanti.",
            "kpi":    "Tech investment: {tech}% → >4%",
        },
        "en": {
            "title":  "Increase technology investment",
            "desc":   "Tech investment at {tech}% of revenue — insufficient to sustain digital growth.",
            "detail": "Bring tech investment to 4–5% of revenue. Focus on automation, CRM and enabling systems.",
            "kpi":    "Tech investment: {tech}% → >4%",
        },
    },

    "migliora_scalabilita": {
        "it": {
            "title":  "Migliora la scalabilità del modello",
            "desc":   "Scalabilità a {scal}/5 — la crescita aumenta i costi in modo quasi proporzionale.",
            "detail": "Identifica i colli di bottiglia operativi. Automatizza le attività ripetitive.",
            "kpi":    "Scalability: {scal}/5 → 4/5",
        },
        "en": {
            "title":  "Improve business model scalability",
            "desc":   "Scalability at {scal}/5 — growth increases costs almost proportionally.",
            "detail": "Identify operational bottlenecks. Automate repetitive tasks.",
            "kpi":    "Scalability: {scal}/5 → 4/5",
        },
    },

    "dati_proprietari": {
        "it": {
            "title":  "Costruisci un patrimonio di dati proprietari",
            "desc":   "Bassa maturità digitale e scarso investimento tech: l'azienda non accumula dati strategici.",
            "detail": "Implementa sistemi di raccolta dati su clienti e processi. I dati proprietari aumentano il valore in modo non lineare.",
            "kpi":    "Digital maturity ≥3 + Data strategy attiva",
        },
        "en": {
            "title":  "Build a proprietary data asset",
            "desc":   "Low digital maturity and limited tech investment: the company is not accumulating strategic data.",
            "detail": "Implement data collection systems on clients and processes. Proprietary data increases value non-linearly.",
            "kpi":    "Digital maturity ≥3 + Active data strategy",
        },
    },

    "rafforza_management": {
        "it": {
            "title":  "Rafforza il middle management",
            "desc":   "Dipendenza dal fondatore a {fd}/5 — l'azienda è vulnerabile senza di lui.",
            "detail": "Delega almeno 3 funzioni chiave a manager autonomi. Documenta i processi decisionali.",
            "kpi":    "Founder dependency: {fd}/5 → ≤2/5",
        },
        "en": {
            "title":  "Strengthen middle management",
            "desc":   "Founder dependency at {fd}/5 — the company is vulnerable without the founder.",
            "detail": "Delegate at least 3 key functions to autonomous managers. Document decision-making processes.",
            "kpi":    "Founder dependency: {fd}/5 → ≤2/5",
        },
    },

    "struttura_processi": {
        "it": {
            "title":  "Struttura processi e responsabilità",
            "desc":   "Struttura manageriale a {ms}/5 — ruoli e responsabilità non chiaramente definiti.",
            "detail": "Definisci organigramma, ruoli e KPI per ogni funzione. Introduci processi documentati per le decisioni operative.",
            "kpi":    "Management structure: {ms}/5 → 4/5",
        },
        "en": {
            "title":  "Structure processes and responsibilities",
            "desc":   "Management structure at {ms}/5 — roles and responsibilities are not clearly defined.",
            "detail": "Define org chart, roles and KPIs for each function. Introduce documented processes for operational decisions.",
            "kpi":    "Management structure: {ms}/5 → 4/5",
        },
    },

    "qualita_portfolio": {
        "it": {
            "title":  "Migliora la qualità del portfolio clienti",
            "desc":   "Portfolio clienti a {cpq}/5 — bassa fidelizzazione e/o clienti poco strategici.",
            "detail": "Classifica i clienti per marginalità e potenziale. Investi nella retention dei top-20%.",
            "kpi":    "Client portfolio quality: {cpq}/5 → 4/5",
        },
        "en": {
            "title":  "Improve client portfolio quality",
            "desc":   "Client portfolio at {cpq}/5 — low retention and/or low-value clients.",
            "detail": "Rank clients by margin and growth potential. Invest in retaining the top 20%.",
            "kpi":    "Client portfolio quality: {cpq}/5 → 4/5",
        },
    },

    "piano_successione": {
        "it": {
            "title":  "Sviluppa un piano di successione",
            "desc":   "Alta dipendenza dal fondatore e management debole: combinazione critica che blocca exit o investimento.",
            "detail": "Identifica e forma un successore interno. Costruisci un piano di transizione 24–36 mesi.",
            "kpi":    "Founder dependency ≤2 + Management ≥4",
        },
        "en": {
            "title":  "Develop a succession plan",
            "desc":   "High founder dependency and weak management: a critical combination that blocks any exit or investment.",
            "detail": "Identify and develop an internal successor. Build a 24–36 month transition plan.",
            "kpi":    "Founder dependency ≤2 + Management ≥4",
        },
    },

    "partnership_strategiche": {
        "it": {
            "title":  "Sviluppa partnership strategiche",
            "desc":   "Forza della rete a {ns}/5 — l'azienda opera in modo isolato dal suo ecosistema.",
            "detail": "Identifica 3 partner complementari nel tuo settore. Avvia accordi di co-marketing o referral.",
            "kpi":    "Network strength: {ns}/5 → 4/5",
        },
        "en": {
            "title":  "Develop strategic partnerships",
            "desc":   "Network strength at {ns}/5 — the company operates in isolation from its ecosystem.",
            "detail": "Identify 3 complementary partners in your sector. Initiate co-marketing or referral agreements.",
            "kpi":    "Network strength: {ns}/5 → 4/5",
        },
    },

    "brand_authority": {
        "it": {
            "title":  "Costruisci una brand authority nel settore",
            "desc":   "Rete debole e alta concentrazione clienti: l'azienda non è percepita come punto di riferimento.",
            "detail": "Investi in content marketing B2B, case study pubblici e presenza a eventi di settore.",
            "kpi":    "Network strength ≥3 + Nuovi lead inbound",
        },
        "en": {
            "title":  "Build sector brand authority",
            "desc":   "Weak network and high client concentration: the company is not perceived as a reference point.",
            "detail": "Invest in B2B content marketing, public case studies and industry event presence.",
            "kpi":    "Network strength ≥3 + New inbound leads",
        },
    },

    "ecosistema_digitale": {
        "it": {
            "title":  "Entra in un ecosistema digitale di settore",
            "desc":   "Bassa maturità digitale e rete debole: rischio di esclusione dai flussi digitali del settore.",
            "detail": "Integrati con marketplace, piattaforme o hub digitali del tuo settore.",
            "kpi":    "Almeno 2 integrazioni digitali attive",
        },
        "en": {
            "title":  "Join a sector digital ecosystem",
            "desc":   "Low digital maturity and weak network: risk of being excluded from the sector's digital flows.",
            "detail": "Integrate with marketplaces, platforms or digital hubs in your sector.",
            "kpi":    "At least 2 active digital integrations",
        },
    },
}


# ─────────────────────────────────────────────
# FUNZIONI DI SUPPORTO
# ─────────────────────────────────────────────

def gap_score(current, optimal, inverse=False, scale=5) -> float:
    if inverse:
        gap = max(0, current - optimal) / (scale - optimal)
    else:
        gap = max(0, optimal - current) / optimal
    return round(min(gap, 1.0), 3)


def dynamic_impact(base_impact: float, gap: float, combo_bonus: float = 0) -> int:
    return round(base_impact * (0.5 + gap * 0.5) + combo_bonus)


def get_text(action_key: str, lang: str, **kwargs) -> dict:
    lang = lang if lang in ("it", "en") else "it"
    texts = ACTIONS_TEXT[action_key][lang]
    return {
        "title":  texts["title"],
        "desc":   texts["desc"].format(**kwargs),
        "detail": texts["detail"],
        "kpi":    texts["kpi"].format(**kwargs),
    }


def horizon(it_text: str, en_text: str, lang: str) -> str:
    return it_text if lang == "it" else en_text


# ─────────────────────────────────────────────
# LIBRERIA AZIONI
# ─────────────────────────────────────────────

def build_action_library(raw: dict, ebitda_margin_pct: float, cagr_pct: float,
                         lang: str = "it", sector: str = "Altro") -> list:

    actions = []
    conc  = raw.get("client_concentration_pct", 0)
    rec   = raw.get("recurring_revenue_pct", 0)
    tech  = raw.get("tech_investment_pct", 0)
    fd    = raw.get("key_man_risk", 3)
    ms    = raw.get("span_of_control", 3)
    dm    = raw.get("operational_digitalization", 3)
    cpq   = raw.get("repeat_customers", 3)
    scal  = raw.get("workflow_automation", 3)
    ns    = raw.get("network_quality", 3)

    opt_ebitda = OPTIMAL_EBITDA_BY_SECTOR.get(sector, OPTIMAL_EBITDA_BY_SECTOR["Altro"])
    opt_cagr   = OPTIMAL_CAGR_BY_SECTOR.get(sector, OPTIMAL_CAGR_BY_SECTOR["Altro"])

    # ── FINANZIARIO ───────────────────────────
    if conc > 40:
        g = gap_score(conc, OPTIMAL["client_concentration_pct"], inverse=True, scale=100)
        cb = 2 if rec < 25 else 0
        t = get_text("riduci_concentrazione", lang, conc=round(conc, 1))
        actions.append({**t, "impact": dynamic_impact(14, g, cb), "capital": "financial",
                        "horizon": horizon("18–24 mesi", "18–24 months", lang),
                        "sqf_delta": f"+{round(g * 0.15, 2)} SQF"})

    if rec < 50:
        g = gap_score(rec, OPTIMAL["recurring_revenue_pct"], scale=100)
        cb = 2 if conc > 50 else 0
        t = get_text("introduci_ricorrenti", lang, rec=round(rec, 1))
        actions.append({**t, "impact": dynamic_impact(12, g, cb), "capital": "financial",
                        "horizon": horizon("12–18 mesi", "12–18 months", lang),
                        "sqf_delta": f"+{round(g * 0.12, 2)} SQF"})

    ebitda_threshold = OPTIMAL_EBITDA_BY_SECTOR.get(sector, 13.5) * 0.75
    if ebitda_margin_pct < ebitda_threshold:
        g = gap_score(ebitda_margin_pct, opt_ebitda, scale=100)
        t = get_text("ottimizza_costi", lang, margin=round(ebitda_margin_pct, 1))
        t["kpi"] = f"EBITDA margin: {round(ebitda_margin_pct, 1)}% → >{round(opt_ebitda, 1)}%"
        actions.append({**t, "impact": dynamic_impact(10, g), "capital": "financial",
                        "horizon": horizon("12–24 mesi", "12–24 months", lang),
                        "sqf_delta": f"+{round(g * 0.10, 2)} SQF"})

    cagr_threshold = OPTIMAL_CAGR_BY_SECTOR.get(sector, 10.0) * 0.60
    if cagr_pct < cagr_threshold:
        g = gap_score(cagr_pct, opt_cagr, scale=100)
        t = get_text("accelera_crescita", lang, cagr=round(cagr_pct, 1))
        t["kpi"] = f"CAGR: {round(cagr_pct, 1)}% → >{round(opt_cagr, 1)}%"
        actions.append({**t, "impact": dynamic_impact(9, g), "capital": "financial",
                        "horizon": horizon("18–36 mesi", "18–36 months", lang),
                        "sqf_delta": f"+{round(g * 0.09, 2)} GF"})

    if conc > 60 and rec < 20:
        t = get_text("piano_resilienza", lang)
        actions.append({**t, "impact": dynamic_impact(15, 0.9, 3), "capital": "financial",
                        "horizon": horizon("6–12 mesi", "6–12 months", lang),
                        "sqf_delta": "+0.18 SQF"})

    # ── TECNOLOGICO ───────────────────────────
    if dm <= 3:
        g = gap_score(dm, OPTIMAL["operational_digitalization"], scale=5)
        cb = 2 if tech < 2 else 0
        t = get_text("accelera_digitale", lang, dm=dm)
        actions.append({**t, "impact": dynamic_impact(10, g, cb), "capital": "technological",
                        "horizon": horizon("18–24 mesi", "18–24 months", lang),
                        "sqf_delta": f"+{round(g * 0.10, 2)} SQF"})

    if tech < 4:
        g = gap_score(tech, OPTIMAL["tech_investment_pct"], scale=100)
        t = get_text("aumenta_tech", lang, tech=round(tech, 1))
        actions.append({**t, "impact": dynamic_impact(8, g), "capital": "technological",
                        "horizon": horizon("12–24 mesi", "12–24 months", lang),
                        "sqf_delta": f"+{round(g * 0.08, 2)} SQF"})

    if scal <= 3:
        g = gap_score(scal, OPTIMAL["workflow_automation"], scale=5)
        t = get_text("migliora_scalabilita", lang, scal=scal)
        actions.append({**t, "impact": dynamic_impact(8, g), "capital": "technological",
                        "horizon": horizon("24–36 mesi", "24–36 months", lang),
                        "sqf_delta": f"+{round(g * 0.08, 2)} SQF"})

    if dm <= 2 and tech < 3:
        t = get_text("dati_proprietari", lang)
        actions.append({**t, "impact": dynamic_impact(9, 0.7, 2), "capital": "technological",
                        "horizon": horizon("18–30 mesi", "18–30 months", lang),
                        "sqf_delta": "+0.10 SQF"})

    # ── UMANO ─────────────────────────────────
    if fd >= 3:
        g = gap_score(fd, OPTIMAL["key_man_risk"], inverse=True, scale=5)
        cb = 3 if ms <= 2 else 0
        t = get_text("rafforza_management", lang, fd=fd)
        actions.append({**t, "impact": dynamic_impact(12, g, cb), "capital": "human",
                        "horizon": horizon("24–36 mesi", "24–36 months", lang),
                        "sqf_delta": f"+{round(g * 0.12, 2)} SQF"})

    if ms <= 3:
        g = gap_score(ms, OPTIMAL["span_of_control"], scale=5)
        t = get_text("struttura_processi", lang, ms=ms)
        actions.append({**t, "impact": dynamic_impact(9, g), "capital": "human",
                        "horizon": horizon("12–18 mesi", "12–18 months", lang),
                        "sqf_delta": f"+{round(g * 0.09, 2)} SQF"})

    if cpq <= 3:
        g = gap_score(cpq, OPTIMAL["repeat_customers"], scale=5)
        t = get_text("qualita_portfolio", lang, cpq=cpq)
        actions.append({**t, "impact": dynamic_impact(7, g), "capital": "relational",
                        "horizon": horizon("12–24 mesi", "12–24 months", lang),
                        "sqf_delta": f"+{round(g * 0.07, 2)} SQF"})

    if fd >= 4 and ms <= 3:
        t = get_text("piano_successione", lang)
        actions.append({**t, "impact": dynamic_impact(13, 0.85, 2), "capital": "human",
                        "horizon": horizon("24–36 mesi", "24–36 months", lang),
                        "sqf_delta": "+0.15 SQF"})

    # ── RELAZIONALE ───────────────────────────
    if ns <= 3:
        g = gap_score(ns, OPTIMAL["network_quality"], scale=5)
        t = get_text("partnership_strategiche", lang, ns=ns)
        actions.append({**t, "impact": dynamic_impact(8, g), "capital": "relational",
                        "horizon": horizon("18–24 mesi", "18–24 months", lang),
                        "sqf_delta": f"+{round(g * 0.08, 2)} SQF"})

    if ns <= 2 and conc > 50:
        t = get_text("brand_authority", lang)
        actions.append({**t, "impact": dynamic_impact(7, 0.6, 1), "capital": "relational",
                        "horizon": horizon("12–24 mesi", "12–24 months", lang),
                        "sqf_delta": "+0.07 SQF"})

    if ns <= 2 and dm <= 3:
        t = get_text("ecosistema_digitale", lang)
        actions.append({**t, "impact": dynamic_impact(6, 0.5, 1), "capital": "relational",
                        "horizon": horizon("18–30 mesi", "18–30 months", lang),
                        "sqf_delta": "+0.06 SQF"})

    return actions


# ─────────────────────────────────────────────
# FUNZIONE PRINCIPALE
# ─────────────────────────────────────────────

def generate_recommendations(
    scores: dict,
    raw_inputs: dict,
    ebitda_margin_pct: float,
    cagr_pct: float,
    objective: str = None,
    lang: str = "it",
    sector: str = "Altro"
) -> list:
    """
    Genera le Top 3 azioni prioritarie.

    Parametri:
      lang   — "it" per italiano, "en" per inglese (default: "it")
      sector — settore per soglie sector-aware (default: "Altro")
    """
    actions = build_action_library(raw_inputs, ebitda_margin_pct, cagr_pct, lang, sector)

    multipliers = OBJECTIVE_MULTIPLIERS.get(objective, {
        "financial": 1.0, "technological": 1.0, "human": 1.0, "relational": 1.0
    })
    for action in actions:
        action["impact"] = round(action["impact"] * multipliers.get(action["capital"], 1.0))

    return sorted(actions, key=lambda x: x["impact"], reverse=True)[:3]


# ─────────────────────────────────────────────
# TEST
# ─────────────────────────────────────────────

if __name__ == "__main__":

    raw_example = {
        "client_concentration_pct":    55,
        "recurring_revenue_pct":       35,
        "tech_investment_pct":         3.2,
        "key_man_risk":                4,
        "span_of_control":             3,
        "skill_investment":            2,
        "talent_retention":            3,
        "sop_standardization":         2,
        "operational_digitalization":  3,
        "data_storage":                3,
        "workflow_automation":         2,
        "proprietary_dataset":         2,
        "crm_adoption":                3,
        "network_quality":             2,
        "partnership_structure":       2,
        "brand_assets":                3,
        "ecosystem_referrals":         2,
        "repeat_customers":            3,
    }

    scores_example = {
        "financial": 0.595, "technological": 0.500,
        "human": 0.3375,    "relational": 0.270
    }

    for lang in ["it", "en"]:
        obj = "Ricerca investitori" if lang == "it" else "Seeking investors"
        print(f"\n{'='*58}")
        print(f"  LINGUA: {lang.upper()} | {obj}")
        print(f"{'='*58}")
        actions = generate_recommendations(
            scores_example, raw_example,
            ebitda_margin_pct=16.0, cagr_pct=11.8,
            objective=obj, lang=lang
        )
        for i, a in enumerate(actions, 1):
            print(f"\n  {i}. {a['title']}  →  +{a['impact']}% V")
            print(f"     {a['desc']}")
            print(f"     {a['kpi']}")
            print(f"     {a['horizon']}  |  {a['sqf_delta']}")
