// Frontend → Backend bridge.
// Sends the user's questionnaire to POST /api/valutazione and returns the
// full evaluation result (capital scores, SQF, valuation, value gap, recommendations).
//
// Payload contract: camelCase + raw frontend keys (secTech / lcStartup / objExit / hor35).
// The backend resolves sector/lifecycle keys to DB integer IDs server-side — no translation
// is needed on the client. This keeps the contract symmetric and language-independent.

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function submitValuation(formData) {
  const payload = {
    // ── Step 1 — Profile ──
    companyName: formData.companyName,
    sector:      formData.sector,        // 'secTech' | 'secB2B' | 'secMfg' | ...
    lifecycle:   formData.lifecycle,     // 'lcStartup' | 'lcGrowth' | ...
    objective:   formData.objective,     // 'objExit' | 'objInvestors' | ...
    horizon:     formData.horizon,       // 'hor12' | 'hor35' | 'hor5'
    assets:      formData.assets || [],

    // ── Step 2 — Financials (€k) ──
    revenueY1:             parseFloat(formData.revenueY1),
    revenueY2:             parseFloat(formData.revenueY2),
    revenueY3:             parseFloat(formData.revenueY3),
    ebitda:                parseFloat(formData.ebitda),
    netFinancialPosition:  parseFloat(formData.netFinancialPosition),
    techInvestment:        parseFloat(formData.techInvestment),

    // ── Step 3 — Financial sliders ──
    recurringRevenue:    parseFloat(formData.recurringRevenue),
    clientConcentration: parseFloat(formData.clientConcentration),

    // ── Step 3 — Human Capital (1-5) ──
    keyManRisk:         parseInt(formData.keyManRisk, 10),
    spanOfControl:      parseInt(formData.spanOfControl, 10),
    skillInvestment:    parseInt(formData.skillInvestment, 10),
    talentRetention:    parseInt(formData.talentRetention, 10),
    sopStandardization: parseInt(formData.sopStandardization, 10),

    // ── Step 3 — Technological Capital (1-5) ──
    operationalDigitalization: parseInt(formData.operationalDigitalization, 10),
    dataStorage:               parseInt(formData.dataStorage, 10),
    workflowAutomation:        parseInt(formData.workflowAutomation, 10),
    proprietaryDataset:        parseInt(formData.proprietaryDataset, 10),
    crmAdoption:               parseInt(formData.crmAdoption, 10),

    // ── Step 3 — Relational Capital (1-5) ──
    networkQuality:       parseInt(formData.networkQuality, 10),
    partnershipStructure: parseInt(formData.partnershipStructure, 10),
    brandAssets:          parseInt(formData.brandAssets, 10),
    ecosystemReferrals:   parseInt(formData.ecosystemReferrals, 10),
    repeatCustomers:      parseInt(formData.repeatCustomers, 10),
  };

  const response = await fetch(`${API_URL}/api/valutazione`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorBody = await response.text();
    console.error('Valuation API error:', response.status, errorBody);
    throw new Error(`Errore API (${response.status}) — ${errorBody}`);
  }

  return await response.json();
}
