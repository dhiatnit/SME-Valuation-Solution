"""
Item #6 — Expert Recommendation Matrix.

Pure lookup: capital + score band → one prescription.
12 prescriptions total (4 capitals × 3 bands).
"""

RECOMMENDATIONS = {
    'human': {
        'weak':   "Build a #2; appoint deputy CEO to reduce key-man risk.",
        'ok':     "Document SOPs for the top 3 roles and cross-train backups.",
        'strong': "Maintain L&D budget at ≥ 2% of payroll; build succession plans.",
    },
    'tech': {
        'weak':   "Migrate from paper/spreadsheets to a proper ERP within 12 months.",
        'ok':     "Add 5 workflow automations and centralise data in a shared platform.",
        'strong': "Monetise your data assets; invest in AI/ML capabilities.",
    },
    'relational': {
        'weak':   "Sign 2 formal partnerships this quarter; build referral channels.",
        'ok':     "Launch a referral programme and grow brand/digital assets.",
        'strong': "Build a channel-sales or affiliate programme to scale GTM.",
    },
    'financial': {
        'weak':   "Refinance debt and cut client concentration below 50%.",
        'ok':     "Lift recurring revenue past 50% of total to boost predictability.",
        'strong': "Consider strategic acquisitions to compound your strong position.",
    },
}


def score_band(score: float) -> str:
    """1-10 score → 'weak' | 'ok' | 'strong'."""
    if score < 4:
        return 'weak'
    if score <= 7:
        return 'ok'
    return 'strong'


def get_recommendation(capital: str, score: float) -> dict:
    band = score_band(score)
    return {
        'capital': capital,
        'score': score,
        'band': band,
        'text': RECOMMENDATIONS[capital][band],
    }


def get_all_recommendations(capital_scores: dict) -> list:
    """Returns a list of 4 recommendations, one per capital."""
    return [get_recommendation(cap, capital_scores[cap])
            for cap in ('human', 'tech', 'relational', 'financial')]
