// We always send the standard Italian strings to the backend so its mathematical
// logic (like finding the correct EBITDA multiple) remains stable and untouched.
const getSectorMap = () => ({
  "secB2B":    "Servizi B2B",
  "secTech":   "Tecnologia/SaaS",
  "secManuf":  "Manifatturiero",
  "secHealth": "Healthcare",
  "secRetail": "Retail/GDO",
  "secReal":   "Edilizia/Immobiliare",
  "secOther":  "Altro",
});

const getObjectiveMap = () => ({
  "objInvestors": "Ricerca investitori",
  "objExit":      "Preparazione exit/vendita",
  "objGrowth":    "Crescita organica",
  "objGen":       "Passaggio generazionale",
  "objStability": "Stabilità",
});

export async function submitValuation(formData) {
  const API_URL = 'http://localhost:8000';
  const lang = formData.language || 'it';
  // Use the standard map regardless of language
  const sectorMap = getSectorMap();
  const objectiveMap = getObjectiveMap();

  try {
    const response = await fetch(`${API_URL}/api/valutazione`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        // Step 1
        company_name: formData.companyName,
        sector:       sectorMap[formData.sector]       || formData.sector,
        lifecycle:    formData.lifecycle,
        objective:    objectiveMap[formData.objective] || formData.objective,
        horizon:      formData.horizon,
        assets:       formData.assets,
        language:     lang,
        
        // Step 2
        revenue_y1:          parseFloat(formData.revenueY1),
        revenue_y2:          parseFloat(formData.revenueY2),
        revenue_y3:          parseFloat(formData.revenueY3),
        ebitda:                  parseFloat(formData.ebitda),
        net_financial_position:  parseFloat(formData.netFinancialPosition),
        tech_investment_pct:     parseFloat(formData.techInvestment),

        // Step 3
        recurring_revenue_pct:         parseFloat(formData.recurringRevenue),
        client_concentration_pct:      parseFloat(formData.clientConcentration),
        // Human Capital
        key_man_risk:                  parseInt(formData.keyManRisk),
        span_of_control:               parseInt(formData.spanOfControl),
        skill_investment:              parseInt(formData.skillInvestment),
        talent_retention:              parseInt(formData.talentRetention),
        sop_standardization:           parseInt(formData.sopStandardization),
        // Technological Capital
        operational_digitalization:    parseInt(formData.operationalDigitalization),
        data_storage:                  parseInt(formData.dataStorage),
        workflow_automation:           parseInt(formData.workflowAutomation),
        proprietary_dataset:           parseInt(formData.proprietaryDataset),
        crm_adoption:                  parseInt(formData.crmAdoption),
        // Relational Capital
        network_quality:               parseInt(formData.networkQuality),
        partnership_structure:         parseInt(formData.partnershipStructure),
        brand_assets:                  parseInt(formData.brandAssets),
        ecosystem_referrals:           parseInt(formData.ecosystemReferrals),
        repeat_customers:              parseInt(formData.repeatCustomers),
      })
    });

    if (!response.ok) {
      throw new Error('Errore API durante la fetching dei dati.');
    }
    return await response.json();

  } catch (err) {
    console.error("Valuation Error:", err);
    throw err;
  }
}