"""
Valuation engine — implements prof's formula (Final Exam Project, PDF page 6):

    V = EBITDA × Sector_Multiple × SQF × GF

  + Asset Premiums  (our extension — adds declared intangibles on top)

SQF (Strategic Quality Factor): aggregated 4-capital score, range [0.6, 1.4]
GF  (Growth Factor):           CAGR + growth quality, range [0.7, 1.3]
"""
from config import (
    SECTOR_MULTIPLES,
    SQF_PROF_MIN, SQF_PROF_MAX,
    GF_MIN, GF_MAX,
    VALUE_RANGE_PCT,
    SQF_BEST_PRACTICE,
    ASSET_PREMIUMS_K,
)


# ──────────────────────────────────────────────────────────────────────
# Scale converters
# ──────────────────────────────────────────────────────────────────────
def sqf_internal_to_prof(sqf_1_10: float) -> float:
    """Map our internal 1-10 SQF to the prof's [0.6, 1.4] multiplicative factor."""
    sqf_norm = (sqf_1_10 - 1) / 9          # → [0, 1]
    return round(SQF_PROF_MIN + (SQF_PROF_MAX - SQF_PROF_MIN) * sqf_norm, 4)


def compute_gf(cagr_delta: float, recurring_delta: float) -> float:
    """
    Growth Factor — prof's definition:
      "Expected CAGR + quality of growth (organic vs. episodic),
       normalised by sector and company size."

    We use:
      - CAGR Delta (1-10, peer-relative growth)         → "expected growth"
      - Recurring Revenue Delta (1-10, peer-relative)   → "quality of growth"
    The average of these two (in 1-10 space) linearly remaps to [0.7, 1.3].
    """
    avg_1_10 = (cagr_delta + recurring_delta) / 2
    norm     = (avg_1_10 - 1) / 9                       # → [0, 1]
    return round(GF_MIN + (GF_MAX - GF_MIN) * norm, 4)


# ──────────────────────────────────────────────────────────────────────
# Asset premiums (Item #5 — our extension to the prof's formula)
# ──────────────────────────────────────────────────────────────────────
def asset_premiums(assets: list) -> float:
    """Sum of flat premiums for declared assets (€k). Keys match frontend Step1."""
    return sum(ASSET_PREMIUMS_K.get(a, 0) for a in (assets or []))


# ──────────────────────────────────────────────────────────────────────
# Main valuation
# ──────────────────────────────────────────────────────────────────────
def compute_valuation(
    ebitda_k: float,
    sector_key: str,
    sqf_internal: float,    # 1-10
    gf: float,              # 0.7-1.3
    assets: list,
) -> dict:
    """
    Prof's formula:   V = EBITDA × Sector_Multiple × SQF × GF
    Our extension:    + Asset Premiums (flat add for declared intangibles)

    All monetary values in € thousands.
    """
    multiple   = SECTOR_MULTIPLES[sector_key]
    sqf_prof   = sqf_internal_to_prof(sqf_internal)
    base_value = ebitda_k * multiple
    core_value = base_value * sqf_prof * gf
    premium    = asset_premiums(assets)
    final      = core_value + premium

    return {
        'base_value_k':     round(base_value, 2),     # EBITDA × Multiple alone
        'sector_multiple':  multiple,
        'sqf_prof':         sqf_prof,                 # in [0.6, 1.4]
        'gf':               gf,                       # in [0.7, 1.3]
        'core_value_k':     round(core_value, 2),     # = EBITDA × Mult × SQF × GF
        'asset_premium_k':  premium,                  # our extension
        'final_value_k':    round(final, 2),
    }


def compute_value_gap(
    ebitda_k: float,
    sector_key: str,
    sqf_internal: float,    # current 1-10 SQF
    gf: float,
    assets: list,
) -> dict:
    """
    Value Gap (prof's term): the distance to bridge between current value and
    optimised potential value (if SQF reached the best-practice target).

    We model the optimised case as:
      - SQF lifted to the best-practice target (8.5/10)
      - GF unchanged (growth trajectory takes longer to shift)
      - Asset premiums unchanged
    """
    current   = compute_valuation(ebitda_k, sector_key, sqf_internal, gf, assets)
    optimised = compute_valuation(ebitda_k, sector_key, SQF_BEST_PRACTICE, gf, assets)

    gap_k   = optimised['final_value_k'] - current['final_value_k']
    gap_pct = round((gap_k / current['final_value_k']) * 100, 2) if current['final_value_k'] else 0

    return {
        'current_value_k':   current['final_value_k'],
        'optimised_value_k': optimised['final_value_k'],
        'value_gap_k':       round(gap_k, 2),
        'value_gap_pct':     gap_pct,
        'best_practice_sqf': SQF_BEST_PRACTICE,
    }
