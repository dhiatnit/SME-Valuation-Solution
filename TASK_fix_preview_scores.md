# Fix: Live Score Preview — variabili mancanti in Step3Questionnaire.jsx

## Problema

Il pannello "Live Score Preview" non riflette tutte le domande del questionario.
Alcune variabili sono presenti come domande nel form ma non vengono watchwate
né incluse nel calcolo del preview.

| Capitale     | Mancante dal preview         | Peso reale |
|--------------|------------------------------|------------|
| Human        | `skillInvestment`            | 5%         |
| Technological| `dataStorage`                | 10%        |
| Technological| `proprietaryDataset`         | 5%         |
| Relational   | `partnershipStructure`       | 15%        |
| Relational   | `brandAssets`                | 10%        |

Il backend calcola tutto correttamente — il problema è solo nel preview visuale.

**File da modificare:** `frontend/src/components/steps/Step3Questionnaire.jsx`

---

## Fix 1 — Aggiungere le variabili mancanti al blocco `watch`

Trovare il blocco watch corrente (righe ~13-24) e aggiungere le 5 variabili mancanti:

```javascript
// Human Capital
const keyManRisk         = parseFloat(watch("keyManRisk"))         || 3;
const spanOfControl      = parseFloat(watch("spanOfControl"))      || 3;
const skillInvestment    = parseFloat(watch("skillInvestment"))    || 3;  // ← AGGIUNGERE
const talentRetention    = parseFloat(watch("talentRetention"))    || 3;
const sopStandardization = parseFloat(watch("sopStandardization")) || 3;
// Technological Capital
const opDigital          = parseFloat(watch("operationalDigitalization")) || 3;
const dataStorage        = parseFloat(watch("dataStorage"))               || 3;  // ← AGGIUNGERE
const wfAutomation       = parseFloat(watch("workflowAutomation"))        || 3;
const proprietaryDataset = parseFloat(watch("proprietaryDataset"))        || 3;  // ← AGGIUNGERE
const crmAdoption        = parseFloat(watch("crmAdoption"))               || 3;
// Relational Capital
const networkQuality      = parseFloat(watch("networkQuality"))       || 3;
const partnershipStructure= parseFloat(watch("partnershipStructure")) || 3;  // ← AGGIUNGERE
const ecosystemRef        = parseFloat(watch("ecosystemReferrals"))   || 3;
const brandAssets         = parseFloat(watch("brandAssets"))          || 3;  // ← AGGIUNGERE
const repeatCust          = parseFloat(watch("repeatCustomers"))      || 3;
```

---

## Fix 2 — Aggiornare i calcoli del preview

Sostituire i 3 blocchi di calcolo (righe ~32-59) con le versioni complete:

### Human Capital
```javascript
const normFounderDep    = (5 - keyManRisk) / 4;
const normSpan          = (spanOfControl - 1) / 4;
const normSkill         = (skillInvestment - 1) / 4;     // ← AGGIUNGERE
const normRetention     = (talentRetention - 1) / 4;
const normSop           = (sopStandardization - 1) / 4;
const humScore = (
  normFounderDep * 0.35 +
  normSpan       * 0.25 +
  normRetention  * 0.20 +
  normSop        * 0.15 +
  normSkill      * 0.05  // ← AGGIUNGERE
);
```

### Technological Capital
```javascript
const normOpDigital       = (opDigital - 1) / 4;
const normDataStorage     = (dataStorage - 1) / 4;         // ← AGGIUNGERE
const normAutomation      = (wfAutomation - 1) / 4;
const normProprietaryData = (proprietaryDataset - 1) / 4;  // ← AGGIUNGERE
const normCrm             = (crmAdoption - 1) / 4;
const techScore = (
  normOpDigital       * 0.25 +
  normAutomation      * 0.25 +
  normCrm             * 0.15 +
  normDataStorage     * 0.10 +  // ← AGGIUNGERE
  normProprietaryData * 0.05    // ← AGGIUNGERE
) / 0.80;  // parziale: esclude solo tech_investment (0.20) che viene dal backend
```

### Relational Capital
```javascript
const normNetwork      = (networkQuality - 1) / 4;
const normPartnership  = (partnershipStructure - 1) / 4;  // ← AGGIUNGERE
const normEco          = (ecosystemRef - 1) / 4;
const normBrand        = (brandAssets - 1) / 4;            // ← AGGIUNGERE
const normRepeat       = (repeatCust - 1) / 4;
const relScore = (
  normNetwork     * 0.30 +
  normEco         * 0.25 +
  normRepeat      * 0.20 +
  normPartnership * 0.15 +  // ← AGGIUNGERE
  normBrand       * 0.10    // ← AGGIUNGERE
);  // somma completa: nessuna divisione necessaria
```

---

## Verifica

Dopo il fix, cambiando ogni domanda del questionario il preview deve aggiornarsi:

| Domanda              | Capitale influenzato |
|----------------------|----------------------|
| Key-Man Risk         | Human ↑↓             |
| Span of Control      | Human ↑↓             |
| Skill Investment     | Human ↑↓             |
| Talent Retention     | Human ↑↓             |
| SOPs                 | Human ↑↓             |
| Op. Digitalization   | Technological ↑↓     |
| Data Storage         | Technological ↑↓     |
| Workflow Automation  | Technological ↑↓     |
| Proprietary Dataset  | Technological ↑↓     |
| CRM Adoption         | Technological ↑↓     |
| Network Quality      | Relational ↑↓        |
| Partnership Structure| Relational ↑↓        |
| Ecosystem Referrals  | Relational ↑↓        |
| Brand Assets         | Relational ↑↓        |
| Repeat Customers     | Relational ↑↓        |
