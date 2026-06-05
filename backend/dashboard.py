"""
Dashboard response adapter.

Step4Dashboard.jsx was written against an older backend contract. This module
transforms our clean internal results into the exact shape the dashboard reads,
so the React code doesn't need to change.

Field mapping (backend → frontend):
    capital_scores (1-10)        →  scores.{financial,technological,human,relational} (0-100)
    sqf (1-10)                   →  quality_score (0-100)
    valuation.final_value_k      →  estimated_value (€, not €k)
    value_gap                    →  value_gap_pct, gap_absolute
    recommendations              →  top3_actions[{title,desc,impact,horizon,sqf_delta,capital}]
"""
from config import SECTOR_MULTIPLES, OBJECTIVE_PRIORITY, DEFAULT_PRIORITY, VALUE_RANGE_PCT


# Frontend uses 'technological' (not 'tech') in dashboard score keys
_CAPITAL_KEY_MAP = {
    'human':      'human',
    'tech':       'technological',
    'relational': 'relational',
    'financial':  'financial',
}

# Cluster mean = 5.5 by Delta design. Convert to 0-100 scale for benchmark display.
_PEER_BENCHMARK_0_100 = 55.0

# Action-card horizon hints by score band
_HORIZON_BY_BAND = {
    'weak':   '3 months',
    'ok':     '6 months',
    'strong': '12 months',
}


def _scale_to_100(score_1_10: float) -> int:
    """Convert a 1-10 Delta score to a 0-100 dashboard number (rounded)."""
    return round((score_1_10 / 10.0) * 100)


def build_dashboard_response(
    capital_scores: dict,    # {'human':6.4, 'tech':7.1, 'relational':5.8, 'financial':6.9}
    sqf: float,              # 1-10
    sector_key: str,
    valuation: dict,         # output of compute_valuation()
    value_gap: dict,         # output of compute_value_gap()
    recommendations: list,   # output of get_all_recommendations()
    objective: str = None,   # Idea A — frontend Step1 objective ('objExit', etc.)
) -> dict:
    """Returns the full Step4Dashboard-ready payload."""

    # ── 1. Scores section (0-100) ──
    scores_100 = {
        _CAPITAL_KEY_MAP[cap]: _scale_to_100(score)
        for cap, score in capital_scores.items()
    }

    benchmarks = {k: int(_PEER_BENCHMARK_0_100) for k in scores_100}
    gaps_vs_benchmark = {k: scores_100[k] - int(_PEER_BENCHMARK_0_100) for k in scores_100}

    # ── 2. Valuation in € (frontend divides by 1M for display) ──
    estimated_value_eur = valuation['final_value_k'] * 1000
    # ±10% range per prof's dashboard example (PDF page 9)
    value_min = round(estimated_value_eur * (1 - VALUE_RANGE_PCT))
    value_max = round(estimated_value_eur * (1 + VALUE_RANGE_PCT))

    # ── 3. Quality score (0-100) and risk band from SQF ──
    quality_score = _scale_to_100(sqf)
    if   sqf >= 7.0: risk_label = 'LOW'
    elif sqf >= 4.5: risk_label = 'MEDIUM'
    else:            risk_label = 'HIGH'

    # ── 4. Top 3 actions: Idea A — pick the 3 MOST RELEVANT capitals for the
    #     user's stated objective. Within each objective's priority order, we
    #     skip the lowest-priority capital (rank 4) so the dashboard always
    #     surfaces what matters for the user's goal. ──
    priority = OBJECTIVE_PRIORITY.get(objective, DEFAULT_PRIORITY)
    # Sort recommendations by (priority asc, then score asc) — top 3 = highest priority
    sorted_recs = sorted(
        recommendations,
        key=lambda r: (priority.get(r['capital'], 99), r['score'])
    )
    top3 = []
    for rec in sorted_recs[:3]:
        # Impact estimate: improving a weak capital to 8.5 gives a meaningful uplift.
        # Rough rule: each +1 SQF point ≈ +6.67% on final value (the 0.6 VAL_RANGE / 9).
        sqf_uplift = max(0, 8.5 - rec['score'])  # 1-10 scale
        impact_pct = round(sqf_uplift * (0.6 / 9) * 100, 1)
        top3.append({
            'capital':   _CAPITAL_KEY_MAP[rec['capital']],
            'title':     _action_title(rec['capital'], rec['band']),
            'desc':      rec['text'],
            'impact':    impact_pct,
            'horizon':   _HORIZON_BY_BAND[rec['band']],
            'sqf_delta': f'+{round(sqf_uplift, 1)} SQF',
        })

    return {
        # Legacy/dashboard fields
        'estimated_value':    estimated_value_eur,
        'value_min':          value_min,
        'value_max':          value_max,
        'multiple_used':      SECTOR_MULTIPLES[sector_key],
        'value_gap_pct':      value_gap['value_gap_pct'],
        'gap_absolute':       value_gap['value_gap_k'] * 1000,
        'scores':             scores_100,
        'benchmarks':         benchmarks,
        'gaps_vs_benchmark':  gaps_vs_benchmark,
        'quality_score':      quality_score,
        'risk_index':         {'label': risk_label},
        'top3_actions':       top3,
    }


# Short action titles per (capital, band) — keeps the recommendation text as `desc`
_ACTION_TITLES = {
    ('human',      'weak'):   'Reduce key-person dependency',
    ('human',      'ok'):     'Formalise core processes',
    ('human',      'strong'): 'Invest in continuous learning',
    ('tech',       'weak'):   'Digitise core operations',
    ('tech',       'ok'):     'Automate & centralise',
    ('tech',       'strong'): 'Monetise data assets',
    ('relational', 'weak'):   'Build strategic partnerships',
    ('relational', 'ok'):     'Grow referral & brand',
    ('relational', 'strong'): 'Scale GTM channels',
    ('financial',  'weak'):   'Strengthen the balance sheet',
    ('financial',  'ok'):     'Boost recurring revenue',
    ('financial',  'strong'): 'Pursue M&A opportunities',
}


def _action_title(capital: str, band: str) -> str:
    return _ACTION_TITLES.get((capital, band), capital.capitalize())
