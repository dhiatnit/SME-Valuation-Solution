Progetto: Value Intelligence Platform

Corso: Management for Digital Enterprise — Prof. G. Tedeschi

Università: Cattolica del Sacro Cuore, Milano
Deadline: 29 maggio 2026

DESCRIZIONE
Piattaforma web per la valutazione strategica delle PMI italiane.
Risponde alla domanda: "Quanto vale la mia azienda, cosa guida
quel valore e come posso farlo crescere?"

STRUTTURA DEL PROGETTO
La cartella contiene:

- backend/        → Python/FastAPI (logica del modello)
- frontend/       → React/Vite (interfaccia utente)
- Aida_Data/      → PDF con dati estratti da AIDA Bureau van Dijk

BACKEND — 5 file principali

1. normalizer.py  → Livello 1: normalizza tutti gli input su scala 0-1
2. scorer.py      → Livello 2: calcola score per i 4 capitali e SQF
3. valuation.py   → Livello 3: calcola valore in € e Value Gap
4. recommender.py → Top 3 azioni prioritarie con impatto dinamico
5. main.py        → FastAPI: espone POST /api/valutazione

FORMULA CENTRALE

V = EBITDA × Sector_Multiple × SQF × GF

Dove:

- SQF (Strategic Quality Factor): score aggregato 4 capitali, range 0.6–1.4
- GF (Growth Factor): CAGR + qualità crescita
- Value Gap: distanza tra valore attuale e potenziale ottimizzato

I 4 CAPITALI

- Finanziario (35%): EBITDA margin, CAGR, ricavi ricorrenti, concentrazione clienti
- Tecnologico (25%): maturità digitale, tech investment, scalabilità
- Umano (25%): founder dependency, management structure, client portfolio
- Relazionale (15%): network strength

FRONTEND

- React 18 + Vite + Tailwind CSS
- Framer Motion per animazioni
- Recharts per radar chart 4 capitali
- i18n custom (IT/EN) — NON usa i18next
- Flusso a 4 step: Profilo → Bilancio → Quiz → 

Dashboard

- Gira su localhost:5173
- Chiama backend su localhost:8000

AVVIO

cd frontend && npm run dev:all
(avvia frontend e backend insieme con concurrently)

STATO ATTUALE

- Backend completo e testato
- Frontend funzionante con chiamata API reale
- Multilingua IT/EN funzionante
- In corso: calibrazione modello con dati reali AIDA
  (raccolti dati per Tech/SaaS, mancano 5 settori)