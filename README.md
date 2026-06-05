Perché le soglie e non una formula lineare
Potresti chiederti: perché non semplicemente valore / valore_massimo? Ad esempio 16% / 40% = 0.4.
La risposta è che il valore aziendale non cresce linearmente con i margini. La differenza tra un EBITDA margin del 5% e del 10% è enorme in termini di salute aziendale. La differenza tra 25% e 30% è molto meno significativa. Le soglie catturano questa non-linearità reale, ed è per questo che si ispirano al modello Altman Z-Score che usa esattamente lo stesso approccio.







Perché alcune variabili sono inverse
Client Concentration e Founder Dependency sono inverse perché misurano un rischio, non una qualità. Più sono alte, peggio è per l'azienda:
Concentration 55% → normalizzato 0.3  (rischio alto)
Concentration 15% → normalizzato 1.0  (rischio basso)
Se non le invertissi, un'azienda con il 90% del fatturato su un solo cliente riceverebbe uno score alto — il contrario di quello che il modello deve comunicare.







Da dove vengono i pesi
La risposta onesta è: non esistono pesi "scientificamente certificati" per questo modello specifico. Nessuno li ha. Anche i modelli professionali di valutazione aziendale usano pesi che derivano da una combinazione di letteratura, esperienza empirica e scelte metodologiche difendibili.
Quello che conta non è avere i pesi "giusti" — è saperli giustificare con una logica coerente.

La logica dietro ogni peso
Capitale Finanziario — pesi interni (30/25/25/20)
VariabilePesoPerchéEBITDA Margin30%È il dato più diretto di redditività operativa — la base di qualsiasi valutazione aziendaleRevenue CAGR25%La traiettoria di crescita impatta direttamente il multiplo che un acquirente è disposto a pagareRecurring Revenue25%Ricavi ricorrenti = prevedibilità = riduzione del rischio per l'acquirente. Vale quanto il CAGRClient Concentration20%È un rischio, non una qualità — pesa meno degli altri tre ma è un segnale critico
Perché questi quattro e non altri
Seguono la logica del modello Altman Z-Score — selezioni poche variabili ad alta segnaletica invece di molte variabili ridondanti. Il professore lo ha detto esplicitamente: "il modello più intelligente non è quello con più variabili, è quello che seleziona le più rilevanti."

Capitale Tecnologico — pesi interni (40/35/25)
VariabilePesoPerchéDigital Maturity40%È la condizione abilitante — senza digitalizzazione non c'è né automazione né scalabilitàTech Investment35%È il segnale concreto e misurabile dell'impegno tecnologico dell'aziendaScalability25%Dipende in parte dalla maturità digitale — peso minore per evitare doppio conteggio

Capitale Umano — pesi interni (40/35/25)
VariabilePesoPerchéFounder Dependency40%È il fattore singolo più penalizzante in una due diligence — un acquirente vuole un'azienda che funziona senza il fondatoreManagement Structure35%Team manageriale = capacità di esecuzione autonomaClient Portfolio Quality25%Qui entra come proxy della qualità delle relazioni commerciali gestite dal team
La logica dei pesi 40/35 qui si ispira alla letteratura sulla trasferibilità aziendale — il tema centrale nelle valutazioni pre-exit.

Capitale Relazionale — pesi interni (60/40)
VariabilePesoPerchéNetwork Strength60%È l'unica variabile che misura direttamente la rete — deve dominareClient Concentration40%Usata come proxy: dipendere da pochi clienti significa anche avere una rete relazionale debole

Come lo spieghi in presentazione
La risposta più efficace alla giuria è questa:

"I pesi non sono arbitrari — seguono tre principi gerarchici. Primo: le variabili oggettive e verificabili pesano più di quelle dichiarate. Secondo: i fattori che impattano direttamente la trasferibilità dell'azienda pesano più di quelli contestuali. Terzo: abbiamo evitato il doppio conteggio assegnando peso minore alle variabili già catturate indirettamente da altre."



## Step 3 Questionaire - Logica
Le tre voci ora modificano il Live Score Preview. Ecco cosa è cambiato:

Tech Focus (verde) — proxy del Capitale Tecnologico, reagisce a Maturità Digitale (peso 40/65) e Scalabilità del Modello (peso 25/65), normalizzati sui pesi disponibili (senza tech_investment che non è un input del form)
Relational Focus (viola) — proxy del Capitale Relazionale, reagisce a Forza della Rete (60%) e alla concentrazione clienti (40%), specchiando esattamente la formula backend


## Banca Dati
"Le soglie di normalizzazione sono calibrate empiricamente su un campione di 4.184 PMI italiane ATECO 62 estratto da AIDA — Bureau van Dijk, aprile 2026. La mediana del ROS per il settore è 5.79%, significativamente inferiore alle assunzioni generiche della letteratura — questo dimostra perché un modello calibrato sul contesto italiano è necessario."

