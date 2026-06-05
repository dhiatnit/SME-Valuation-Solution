"""
Supabase database access layer.

Resolves frontend sector/lifecycle keys → DB integer IDs,
inserts company + 4 capital responses, and calls the 4 Delta RPC functions.

Requires env vars:
  SUPABASE_URL
  SUPABASE_SERVICE_ROLE_KEY   (service role — bypasses RLS for inserts)
"""
import os
from functools import lru_cache
from supabase import create_client, Client

from config import HC_FIELD_MAP, TC_FIELD_MAP, RC_FIELD_MAP


# ──────────────────────────────────────────────────────────────────────
# Client
# ──────────────────────────────────────────────────────────────────────
def get_supabase() -> Client:
    """Lazy-creates a Supabase client from env vars."""
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
    if not url or not key:
        raise RuntimeError(
            "Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY. "
            "Copy .env.example to .env and fill in your Supabase project credentials."
        )
    return create_client(url, key)


# ──────────────────────────────────────────────────────────────────────
# Lookup table resolution (frontend key → DB id)
# Cached because sectors/lifecycles never change at runtime.
# ──────────────────────────────────────────────────────────────────────
@lru_cache(maxsize=16)
def _resolve_lookup(table: str, key: str) -> int:
    sb = get_supabase()
    res = sb.table(table).select('id').eq('key', key).single().execute()
    if not res.data:
        raise ValueError(f"Unknown {table} key '{key}'")
    return res.data['id']


def resolve_sector_id(sector_key: str) -> int:
    return _resolve_lookup('sectors', sector_key)


def resolve_lifecycle_id(lifecycle_key: str) -> int:
    return _resolve_lookup('lifecycles', lifecycle_key)


# ──────────────────────────────────────────────────────────────────────
# Inserts — return new row UUID
# ──────────────────────────────────────────────────────────────────────
def insert_company(sb: Client, payload: dict, sector_id: int, lifecycle_id: int) -> str:
    row = {
        'company_name': payload['companyName'],
        'sector_id':    sector_id,
        'lifecycle_id': lifecycle_id,
        'objective':    payload.get('objective'),
        'horizon':      payload.get('horizon'),
        'assets':       payload.get('assets', []),
    }
    res = sb.table('companies').insert(row).execute()
    return res.data[0]['id']


def _insert_qualitative(sb: Client, table: str, field_map: dict,
                        company_id: str, sector_id: int, lifecycle_id: int,
                        payload: dict) -> str:
    """Shared helper for HC, TC, RC inserts."""
    row = {
        'company_id':   company_id,
        'sector_id':    sector_id,
        'lifecycle_id': lifecycle_id,
    }
    for fe_key, db_col in field_map.items():
        row[db_col] = payload[fe_key]
    res = sb.table(table).insert(row).execute()
    return res.data[0]['id']


def insert_hc(sb, company_id, sector_id, lifecycle_id, payload) -> str:
    return _insert_qualitative(sb, 'human_capital_responses', HC_FIELD_MAP,
                               company_id, sector_id, lifecycle_id, payload)


def insert_tc(sb, company_id, sector_id, lifecycle_id, payload) -> str:
    return _insert_qualitative(sb, 'tech_capital_responses', TC_FIELD_MAP,
                               company_id, sector_id, lifecycle_id, payload)


def insert_rc(sb, company_id, sector_id, lifecycle_id, payload) -> str:
    return _insert_qualitative(sb, 'relational_capital_responses', RC_FIELD_MAP,
                               company_id, sector_id, lifecycle_id, payload)


def insert_fc(sb, company_id, sector_id, lifecycle_id, payload) -> str:
    row = {
        'company_id':               company_id,
        'sector_id':                sector_id,
        'lifecycle_id':             lifecycle_id,
        'revenue_y1':               payload['revenueY1'],
        'revenue_y2':               payload['revenueY2'],
        'revenue_y3':               payload['revenueY3'],
        'ebitda':                   payload['ebitda'],
        'net_financial_position':   payload['netFinancialPosition'],
        'tech_investment_pct':      payload['techInvestment'],
        'recurring_revenue_pct':    payload['recurringRevenue'],
        'client_concentration_pct': payload['clientConcentration'],
    }
    res = sb.table('financial_capital_inputs').insert(row).execute()
    return res.data[0]['id']


# ──────────────────────────────────────────────────────────────────────
# Delta RPC calls — same call signature for all 4 capitals
# ──────────────────────────────────────────────────────────────────────
def call_delta(sb: Client, capital: str, response_id: str) -> list:
    """
    Calls one of the 4 score_*_capital_delta() SQL functions.
    capital: 'human' | 'tech' | 'relational' | 'financial'
    Returns list of {question, raw_score|raw_value, cluster_mean, delta_score, ...}.
    """
    fn = f'score_{capital}_capital_delta'
    res = sb.rpc(fn, {'p_response_id': response_id}).execute()
    return res.data or []
