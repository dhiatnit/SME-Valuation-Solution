"""
Valuation engine — items #1, #2, #4, #5.

Computes the headline valuation, the optimised "best practice" valuation,
the value gap, and adds asset premiums.
"""
from config import (
    SECTOR_MULTIPLES, VAL_BASE, VAL_RANGE,
    SQF_BEST_PRACTICE, ASSET_PREMIUMS_K,
)


def _adjustment_factor(sqf: float) -> float:
    """
    Item #1 — How SQF translates into a multiplier on EBITDA × sector multiple.
      sqf=1  → 0.7×   sqf=5.5 → 1.0×   sqf=10 → 1.3×
    """
    sqf_norm = (sqf - 1) / 9
    return VAL_BASE + VAL_RANGE * sqf_norm


def asset_premiums(assets: list) -> float:
    """
    Item #5 — Sum of flat premiums for declared assets (€k).
    `assets` is a list of frontend checkbox keys, e.g. ['patents','software'].
    Unknown keys are silently ignored.
    """
    return sum(ASSET_PREMIUMS_K.get(a, 0) for a in (assets or []))


def compute_valuation(ebitda_k: float, sector_key: str, sqf: float, assets: list) -> dict:
    """
    Item #1 — The headline valuation.
      Final Value = EBITDA × Sector_Multiple × adjustment(sqf) + Asset Premiums

    All monetary values in € thousands.
    """
    multiple = SECTOR_MULTIPLES[sector_key]
    base_value     = ebitda_k * multiple
    adjustment     = _adjustment_factor(sqf)
    adjusted_value = base_value * adjustment
    premium        = asset_premiums(assets)
    final_value    = adjusted_value + premium

    return {
        'base_value_k':     round(base_value, 2),
        'sector_multiple':  multiple,
        'adjustment':       round(adjustment, 4),
        'adjusted_value_k': round(adjusted_value, 2),
        'asset_premium_k':  premium,
        'final_value_k':    round(final_value, 2),
    }


def compute_value_gap(ebitda_k: float, sector_key: str,
                      current_sqf: float, assets: list) -> dict:
    """
    Item #4 — Optimised value (if company hits best-practice SQF) and the gap.
    """
    current = compute_valuation(ebitda_k, sector_key, current_sqf, assets)
    optim   = compute_valuation(ebitda_k, sector_key, SQF_BEST_PRACTICE, assets)

    gap = optim['final_value_k'] - current['final_value_k']
    gap_pct = round((gap / current['final_value_k']) * 100, 2) if current['final_value_k'] else 0

    return {
        'current_value_k':   current['final_value_k'],
        'optimised_value_k': optim['final_value_k'],
        'value_gap_k':       round(gap, 2),
        'value_gap_pct':     gap_pct,
        'best_practice_sqf': SQF_BEST_PRACTICE,
    }
