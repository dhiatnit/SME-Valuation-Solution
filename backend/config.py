"""
Configuration constants for the Value Intelligence Platform backend.

All values here were team-approved in methodology_proposal.html.
Change with care — these drive every valuation the platform produces.
"""

# ──────────────────────────────────────────────────────────────────────
# Item #2 — Base sector EBITDA multiples (Italian SME-adjusted)
# ──────────────────────────────────────────────────────────────────────
SECTOR_MULTIPLES = {
    'secTech':   7.5,   # Technology / SaaS
    'secHealth': 7.0,   # Healthcare
    'secB2B':    6.0,   # B2B Services
    'secOther':  5.0,   # Generic baseline
    'secMfg':    4.5,   # Manufacturing
    'secRetail': 4.5,   # Retail / FMCG
    'secReal':   4.0,   # Construction / Real Estate
}

# ──────────────────────────────────────────────────────────────────────
# Item #3 — Sector weights for SQF calculation (rows sum to 1.0)
# Order: human, tech, relational, financial
# ──────────────────────────────────────────────────────────────────────
SECTOR_WEIGHTS = {
    'secTech':   {'human': 0.20, 'tech': 0.40, 'relational': 0.15, 'financial': 0.25},
    'secB2B':    {'human': 0.30, 'tech': 0.15, 'relational': 0.30, 'financial': 0.25},
    'secMfg':    {'human': 0.20, 'tech': 0.20, 'relational': 0.15, 'financial': 0.45},
    'secHealth': {'human': 0.35, 'tech': 0.20, 'relational': 0.15, 'financial': 0.30},
    'secRetail': {'human': 0.15, 'tech': 0.20, 'relational': 0.35, 'financial': 0.30},
    'secReal':   {'human': 0.20, 'tech': 0.10, 'relational': 0.25, 'financial': 0.45},
    'secOther':  {'human': 0.25, 'tech': 0.20, 'relational': 0.20, 'financial': 0.35},
}

# ──────────────────────────────────────────────────────────────────────
# Item #1 — Valuation formula constants
# Final Value = EBITDA × Multiple × (VAL_BASE + VAL_RANGE × SQF_norm)
# SQF=0 → 0.7× multiplier   SQF=0.5 → 1.0×   SQF=1.0 → 1.3×
# ──────────────────────────────────────────────────────────────────────
VAL_BASE  = 0.7
VAL_RANGE = 0.6

# ──────────────────────────────────────────────────────────────────────
# Item #4 — Value Gap "best practice" target
# Used to compute the optimised valuation a company could reach.
# 8.5/10 = top-quintile target (statistically realistic vs. unreachable 10)
# ──────────────────────────────────────────────────────────────────────
SQF_BEST_PRACTICE = 8.5

# ──────────────────────────────────────────────────────────────────────
# Item #5 — Asset premiums (€k, added flat to Final Value)
# The frontend `assets` field is a checkbox list → flat premium per kind.
# ──────────────────────────────────────────────────────────────────────
ASSET_PREMIUMS_K = {
    'patents':       80,    # +€80k flat if user declares patents
    'trademarks':    25,    # +€25k flat
    'software':     150,    # +€150k for proprietary software
    'contracts':    100,    # +€100k for multi-year contracts (default)
}

# ──────────────────────────────────────────────────────────────────────
# Frontend ↔ DB field name mappings
# ──────────────────────────────────────────────────────────────────────
HC_FIELD_MAP = {
    'keyManRisk':         'q1_key_man_risk',
    'spanOfControl':      'q2_span_of_control',
    'skillInvestment':    'q3_skill_investment',
    'talentRetention':    'q4_talent_retention',
    'sopStandardization': 'q5_sops_autonomy',
}

TC_FIELD_MAP = {
    'operationalDigitalization': 'q1_op_digitalization',
    'dataStorage':               'q2_data_storage',
    'workflowAutomation':        'q3_automation',
    'proprietaryDataset':        'q4_proprietary_data',
    'crmAdoption':               'q5_crm_adoption',
}

RC_FIELD_MAP = {
    'networkQuality':       'q1_network_quality',
    'partnershipStructure': 'q2_partnerships',
    'brandAssets':          'q3_brand_assets',
    'ecosystemReferrals':   'q4_ecosystem',
    'repeatCustomers':      'q5_repeat_customers',
}
