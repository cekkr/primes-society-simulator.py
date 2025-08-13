Riccardo Cecchini

# **PRIME SOCIETY - MANUALE DI SIMULAZIONE**
## *Un Simulatore di Evoluzione Socio-Economica Basato sui Numeri Primi*

---

## **PARTE 1: FONDAMENTI E PERSONE**

### **1. CONCETTO BASE**
Prime Society simula una società dove il nutrimento deriva dai numeri. Il numero 1 è la risorsa base prodotta naturalmente dal pianeta. La scoperta dei numeri primi permette trasformazioni più efficienti. Le persone nascono, lavorano, si relazionano, votano, abitano e muoiono in un sistema economico completamente libero.

### **2. GENERAZIONE INIZIALE DEL MONDO**

#### **2.1 Parametri Globali**
```
POPOLAZIONE_INIZIALE = 1000 persone
PRODUZIONE_BASE_ANNUA = POPOLAZIONE_INIZIALE × 365 unità di "1"
REGIONI = 5
DISTRETTI_PER_REGIONE = 4  
CELLE_PER_DISTRETTO = 100 (griglia 10×10)
```

#### **2.2 Distribuzione Territoriale**
- Ogni cella può contenere illimitati edifici (verticalmente)
- Spazio edificabile per cella = 1000 unità cubiche
- Distribuzione iniziale: 70% celle vuote, 30% con edifici base

### **3. SISTEMA PERSONALITÀ**

#### **3.1 Generazione Individuo**
Ogni persona nasce con 10 assi di personalità, valore tra -100 e +100:

```
Per ogni nuovo individuo:
  Per ogni tratto:
    SE ha_genitori:
      valore = (madre.tratto + padre.tratto)/2 + random(-20, +20)
    ALTRIMENTI:
      valore = random(-100, +100)
```

**I 10 Assi:**

1. **Generosità [-100] ↔ Avidità [+100]**
2. **Inventiva [-100] ↔ Imitazione [+100]**
3. **Diplomazia [-100] ↔ Aggressività [+100]**
4. **Umiltà [-100] ↔ Ambizione [+100]**
5. **Sociale [-100] ↔ Pragmatico [+100]**
6. **Sincerità [-100] ↔ Inganno [+100]**
7. **Condivisione [-100] ↔ Sfruttamento [+100]**
8. **Riflessività [-100] ↔ Impulsività [+100]**
9. **Conservatore [-100] ↔ Progressista [+100]**
10. **Materialista [-100] ↔ Spirituale [+100]**

#### **3.2 Attributi Derivati**

**Intelligenza** (fisso dalla nascita):
```
intelligenza = 50 + (inventiva × 0.3) + (riflessività × 0.2) + random(-10, +10)
```

**Carisma** (dinamico):
```
carisma = 50 + (diplomazia × 0.3) + (felicità × 0.2) + (salute × 0.1) + aspetto_fisico
```

**Conoscenza** (accumulo):
```
conoscenza_base = (intelligenza/100) × anni_studio × qualità_scuola
conoscenza_primi = lista_primi_appresi[]
```

**Felicità** (ricalcolata ogni giorno):
```
felicità = temperamento_base + 
          (bisogni_soddisfatti × 20) +
          (relazioni_positive × 15) +
          (successo_lavorativo × 10) +
          (allineamento_culturale × 10) -
          (stress × 20) -
          (conflitti × 15)
```

**Salute** (decade con età):
```
salute = 100 - (età/aspettativa_vita × 50) + 
         (qualità_nutrizione × 0.2) +
         (accesso_cure × 0.3) -
         (stress_cronico × 0.2)
```

### **4. SISTEMA ENERGETICO GIORNALIERO**

#### **4.1 Budget Energetico**
```
energia_giornaliera = 100 + (salute × 0.2) - (età/100 × 20)
```

#### **4.2 Spesa Energetica**
- Movimento: 1 energia per cella
- Lavoro base: 40 energia
- Lavoro straordinario: fino a 60 (accumula stress)
- Socializzazione: 10 energia per interazione
- Studio: 20 energia per sessione
- Riposo attivo: recupera 10 energia

### **5. CICLO VITALE**

#### **5.1 Fasi della Vita**
```
0-16 anni: INFANZIA
  - Non lavora
  - Costa 10 risorse/giorno alla famiglia
  - Accumula conoscenza base
  
16-25 anni: FORMAZIONE
  - Può lavorare al 50% efficienza
  - Può studiare (velocità 2x)
  - Inizia relazioni romantiche
  
25-55 anni: PRODUTTIVITÀ PIENA
  - 100% efficienza lavorativa
  - Può avere figli
  - Accumula ricchezza
  
55-70 anni: ESPERIENZA
  - 80% efficienza fisica
  - 120% efficienza decisionale
  - Bonus network e mentoring
  
70+ anni: ANZIANITÀ
  - 40% efficienza
  - Richiede cure crescenti
  - Trasferisce conoscenza
```

#### **5.2 Morte**
```
aspettativa_vita_base = 75 + (progresso_medico × 0.1)
modificatori = (ricchezza_relativa × 10) + (felicità_media × 5) - (stress_cronico × 10)
morte_quando = età > aspettativa_vita + random(-5, +5) + modificatori
```

### **6. RELAZIONI E ACCOPPIAMENTO**

#### **6.1 Formazione Coppia**
```
attrazione = |100 - Σ|differenze_tratti|/10|
compatibilità_economica = min(ricchezza_A, ricchezza_B) / max(ricchezza_A, ricchezza_B)
probabilità_coppia = attrazione × 0.4 + 
                    compatibilità_economica × 0.3 +
                    prossimità_fisica × 0.2 +
                    allineamento_culturale × 0.1

SE probabilità > soglia_personale E entrambi_disponibili:
  forma_coppia()
```

#### **6.2 Decisione Figli**
```
desiderio_figli = (100 - materialismo) × 0.3 + 
                 (felicità_coppia) × 0.3 +
                 (stabilità_economica) × 0.4

costo_previsto_figlio = 10 × 365 × 18 [anni] × qualità_vita_desiderata

SE desiderio > 60 E risorse > costo_previsto × 1.5:
  genera_figlio()
```

#### **6.3 Eredità Genetica e Culturale**
```
Per ogni tratto del figlio:
  componente_genetica = (madre.tratto + padre.tratto) / 2
  variazione_casuale = random(-20, +20)
  influenza_ambiente = meme_dominante_quartiere × 0.1
  
  tratto_finale = componente_genetica + variazione_casuale + influenza_ambiente
  tratto_finale = clamp(tratto_finale, -100, 100)
```

### **7. BISOGNI E CONSUMO**

#### **7.1 Requisiti Giornalieri**
```
nutrizione_necessaria = 1 unità/giorno
spazio_abitativo_minimo = 10 + (n_famiglia × 5) unità cubiche
comfort_desiderato = 50 + (materialismo × 0.5) + (ricchezza × 0.001)
```

#### **7.2 Soddisfazione Bisogni**
```
SE nutrizione < necessaria:
  salute -= 5/giorno
  felicità -= 10/giorno
  SE salute <= 0: morte()

SE spazio < minimo:
  stress += 5/giorno
  probabilità_malattia += 1%

SE comfort < desiderato:
  felicità -= (desiderato - attuale) × 0.1
  motivazione_lavorativa -= 5%
```

### **8. MEMORIA E APPRENDIMENTO**

#### **8.1 Sistema di Memoria**
```
memoria_personale = {
  interazioni[]: lista_ultimi_1000_eventi,
  rancori[]: persone_che_hanno_tradito,
  gratitudine[]: persone_che_hanno_aiutato,
  conoscenze[]: network_sociale,
  esperienze_lavorative[]: storia_impieghi
}
```

#### **8.2 Apprendimento Numeri Primi**
```
difficoltà_primo(n) = posizione(n)² / intelligenza
tempo_apprendimento = difficoltà × 10 giorni
costo_apprendimento = difficoltà × 100 risorse

SE supera_test_apprendimento():
  aggiungi_a_conoscenza_primi(n)
  può_lavorare_con(n)
```

### **9. DECISIONI QUOTIDIANE**

#### **9.1 Albero Decisionale Giornaliero**
```
OGNI MATTINA:
  valuta_stato_attuale()
  
  SE felicità < 20 OR stress > 80:
    priorità = recupero_benessere
  ALTRIMENTI SE risorse < 100:
    priorità = lavoro_extra
  ALTRIMENTI SE ambizione > 50:
    priorità = avanzamento_carriera
  ALTRIMENTI:
    priorità = bilanciamento_vita
    
  pianifica_giornata(priorità)
```

#### **9.2 Valutazione Opportunità**
```
Per ogni opportunità disponibile:
  utilità_attesa = beneficio_economico × 0.4 +
                  crescita_personale × 0.2 +
                  impatto_relazioni × 0.2 +
                  allineamento_valori × 0.2
                  
  rischio_percepito = rischio_reale × (impulsività/100) +
                     esperienza_passata
                     
  SE utilità_attesa/rischio_percepito > soglia_personale:
    persegui_opportunità()
```

---

# **PRIME SOCIETY - MANUALE DI SIMULAZIONE**
## **PARTE 2: ECONOMIA E NUMERI PRIMI (VERSIONE INTEGRATA)**

---

### **10. SISTEMA DEI NUMERI PRIMI**

#### **10.1 Meccanica Fondamentale e Valore Nutritivo**
```
RISORSA_BASE = "1"
produzione_giornaliera_globale = POPOLAZIONE_INIZIALE × 1
distribuzione_territoriale = uniforme_su_celle_non_edificate

FUNZIONE_NUTRIZIONE_COMPLETA:
  
  Per numeri primi:
    nutrizione_base = posizione_nel_ranking_primi
    
    // Bonus per primi di primi (posizione che è primo)
    SE è_primo(posizione):
      nutrizione *= 1.5
      // P₂(3)→3, P₃(5)→4.5, P₅(11)→7.5, P₇(17)→10.5, P₁₁(31)→16.5
    
    // Penalità per primi gemelli (differenza = 2)
    SE |primo - primo_precedente| == 2 OR |primo - primo_successivo| == 2:
      nutrizione *= 0.9
      // Coppie: (3,5), (5,7), (11,13), (17,19), (29,31), (41,43)
  
  Per numeri composti:
    nutrizione_base = Σ(posizione_primi_fattori)
    
    // BONUS SINERGIE:
    SE fattori_sono_consecutivi:
      nutrizione *= 1.5  // 6=2×3, 15=3×5, 35=5×7, 77=7×11
    
    SE c'è_salto_di_primo:
      nutrizione *= 1.3  // 10=2×5, 14=2×7, 22=2×11, 33=3×11
    
    SE tre_o_più_fattori_primi_distinti:
      nutrizione *= 1.7  // 30=2×3×5, 42=2×3×7, 66=2×3×11
    
    SE è_potenza_di_primo:
      nutrizione = posizione × esponente × (1 + 0.1×esponente)
      // 4=2²→2.4, 8=2³→3.9, 27=3³→7.8, 125=5³→11.7
    
    SE è_quasi_primo (prodotto di 2 primi grandi > P₁₀):
      nutrizione *= 1.4  // 143=11×13, 221=13×17, 323=17×19
```

#### **10.2 Peso, Trasportabilità ed Efficienza**
```
CALCOLO_PESO:
  peso_base(primo) = posizione²
  
  Per composti:
    peso = Σ(posizione_fattore × occorrenze)²
    
  Esempi dettagliati:
    2: peso = 1² = 1
    3: peso = 2² = 4  
    5: peso = 3² = 9
    6 (2×3): peso = (1×1)² + (2×1)² = 1 + 4 = 5
    30 (2×3×5): peso = (1+2+3)² = 36 (ma sinergia riduce a 14)
    125 (5³): peso = (3×3)² = 81

EFFICIENZA = nutrizione / peso

TABELLA_EFFICIENZA_STRATEGICA:
Numero | Nutrizione | Peso | Efficienza | Strategia
-------|------------|------|------------|------------
2      | 1.0        | 1    | 1.00       | Early game base
3      | 3.0        | 4    | 0.75       | Premio alto valore
6      | 4.5        | 5    | 0.90       | Ottimo early-mid
11     | 7.5        | 25   | 0.30       | Prestigio > efficienza
30     | 10.2       | 14   | 0.73       | Best mid-game
77     | 13.5       | 41   | 0.33       | Late game nutriente
143    | 15.4       | 61   | 0.25       | Specializzazione lusso

costo_trasporto = peso × distanza × (1 + congestione_rotta × 0.5)
tempo_trasporto = √peso × distanza / efficienza_infrastrutture
```

#### **10.3 Scoperta Progressiva dei Primi**
```
MECCANICA_SCOPERTA:
  
  // Costi crescono cubicamente
  costo_ricerca(Pn) = n³ × 100 risorse
  tempo_minimo(Pn) = n² giorni
  intelligenza_minima(Pn) = 30 + n × 2
  
  // Bonus per pattern recognition
  SE primo ∈ sequenza_aritmetica_nota:
    costo *= 0.7  // Es: AP-3: {3,7,11}, AP-6: {5,11,17,23,29}
  
  SE primo è_Sophie_Germain (2p+1 è primo):
    costo *= 0.8  // Es: 2→5, 3→7, 5→11, 11→23
  
  SE primo è_Mersenne (2^p - 1):
    costo *= 0.6  // Es: 3, 7, 31, 127 (molto rari ma pattern chiaro)

TABELLA_PROGRESSIONE:
P₁(2):   100 risorse, 1 giorno, IQ 32+
P₃(5):   2,700 risorse, 9 giorni, IQ 36+
P₅(11):  12,500 risorse, 25 giorni, IQ 40+ (×0.75 bonus = 9,375)
P₇(17):  34,300 risorse, 49 giorni, IQ 44+ (×0.75 bonus = 25,725)
P₁₁(31): 133,100 risorse, 121 giorni, IQ 52+ (×0.75 bonus = 99,825)
P₂₅(97): 1,562,500 risorse, 625 giorni, IQ 80+
P₅₀(229): 12,500,000 risorse, 2,500 giorni, IQ 130+ (genio richiesto)

probabilità_scoperta_giornaliera = 
  (inventiva/100) × 
  (intelligenza/requisito_IQ) × 
  (√risorse_investite/costo_standard) ×
  (1 + sinergia_team × 0.5) ×
  (1 + strumenti_avanzati × 0.3)
```

#### **10.4 Trasformazione, Produzione e Tecnologie**
```
PROCESSI_PRODUTTIVI:

1) COMBINAZIONE_BASE:
   Input: [numero_a, numero_b]
   Output: a × b
   Perdita: 5% (entropia)
   Tempo: √(peso_output) ore
   
2) TECNOLOGIE_SBLOCCABILI:
   
   Livello_1 (5,000 conoscenza globale):
   - CATALISI: -20% tempo produzione
   - COMPRESSIONE: -15% peso trasporto
   
   Livello_2 (15,000 conoscenza):
   - FATTORIZZAZIONE_PARZIALE: Scompone composti (recupera 60%)
   - SINTESI_MULTIPLA: Combina 3+ numeri in un passo
   
   Livello_3 (40,000 conoscenza):
   - CRISTALLIZZAZIONE: +30% nutrizione, +50% peso (forma pura)
   - TUNNELING: Trasporto istantaneo (costa energia = peso²)
   
   Livello_4 (100,000 conoscenza):
   - FUSIONE_QUANTICA: Nessun limite peso in produzione
   - TRASMUTAZIONE: Converti primo in primo adiacente (-50% efficienza)

3) SPECIALIZZAZIONI_PRODUTTIVE:
   - Puristi: Solo primi non composti (alta qualità)
   - Sinergisti: Solo combinazioni con bonus (6, 15, 30...)
   - Volumetrici: Mass production di bassi (2, 3, 4, 6)
   - Esotici: Quasi-primi e numeri > 100
```

### **11. SISTEMA AZIENDALE AVANZATO**

#### **11.1 Tipologie e Strategie**
```
TIPI_AZIENDA_SPECIALIZZATI:
  
  ESTRATTIVE_BASE: 
    Raccolgono "1", bassi costi, volumi alti
    
  LABORATORI_PRIMI:
    Scoprono nuovi primi, alto rischio/reward
    Focus: P₁-P₁₀ (early) vs P₂₀+ (late game)
    
  FABBRICHE_SINERGIA:
    Producono solo composti con bonus (6, 15, 30, 42...)
    Margini 40-60%
    
  RAFFINERIE_POTENZE:
    Specializzate in 4, 8, 9, 16, 25, 27...
    Clientela: power users
    
  TRADING_HOUSES:
    Arbitraggio inter-regionale
    Profitto da asimmetrie informative
    
  BOUTIQUE_LUSSO:
    Solo numeri > 100 o quasi-primi
    Margini 200%+, volumi bassi

cultura_aziendale_emergente = {
  SE fondatori.inventiva > 70:
    tipo = "Innovatori Seriali"
    bonus_scoperte = +40%
    turnover_alto = true  // Geni difficili da gestire
    
  SE fondatori.avidità > 70:
    tipo = "Massimizzatori"
    margini = +30%
    reputazione = -20%
    
  SE fondatori.sociale > 70:
    tipo = "Benefit Corporation"  
    prezzi = -15%
    loyalty_dipendenti = +50%
    sussidi_governativi = +20%
}
```

#### **11.2 Gerarchie e Scalabilità**
```
STRUTTURA_DINAMICA:
  
  fatturato_mensile = entrate - costi
  complexity_score = n_prodotti × n_regioni × n_primi_conosciuti
  
  livelli_gerarchia = log₂(fatturato/1000) + log₂(complexity_score)
  
  // Span of control variabile
  subordinati_per_manager = 5 + (organizzazione_skill × 0.1) - (complexity × 0.05)
  
  // Costo coordinamento cresce non-linearmente
  overhead = n_dipendenti^1.2 × (livelli^2 / efficienza_comunicazione)
  
  CRISI_ORGANIZZATIVA:
    SE n_dipendenti > capacità_gestionale:
      produttività *= 0.7
      errori += 40%
      TRIGGER: ristrutturazione OR scissione
```

#### **11.3 Innovazione e Proprietà Intellettuale**
```
SISTEMA_BREVETTI:
  
  Quando_scopri_primo(n):
    brevetto = {
      monopolio_primo_puro: 365 giorni,
      royalty_su_composti: 10% per 730 giorni,
      blocco_reverse_engineering: 180 giorni
    }
    
  Quando_scopri_sinergia():
    segreto_industriale = 100 giorni
    vantaggio_first_mover = efficienza +20% permanente
    
  SPIONAGGIO_INDUSTRIALE:
    SE (dipendente.lealtà < 30) AND (competitor.offerta > 2x_stipendio):
      probabilità_leak = 60%
      
    costo_reverse_engineering = brevetto_valore × 0.4
    tempo_reverse = 90 giorni × complessità
    
  PATENT_TROLLING:
    SE azienda.tipo == "Non-Practicing Entity":
      compra_brevetti_fallimenti()
      causa_chiunque_produca()
      estorce_licensing_fees()
```

### **12. MERCATO DINAMICO E PRICE DISCOVERY**

#### **12.1 Order Book e Market Making**
```
MERCATO_CONTINUO:
  
  Per_ogni_prodotto:
    order_book = {
      bids: [(prezzo, quantità, compratore)...],  // Ordinati ↓
      asks: [(prezzo, quantità, venditore)...],   // Ordinati ↑
      spread: min(asks).prezzo - max(bids).prezzo
    }
    
  market_maker_automatico:
    SE spread > 5%:
      piazza_ordini_both_sides(spread/2)
      profitto = volume × spread × 0.4
      
  FLASH_CRASH:
    SE volume_vendite > 10x_media AND tempo < 60 secondi:
      HALT_TRADING(300 secondi)
      reset_a_prezzi_pre_crash × 0.9
```

#### **12.2 Strumenti Finanziari Derivati**
```
PRODOTTI_FINANZIARI:
  
  1) FUTURES_PRIMI:
     Contratto: "P₂₅(97) scoperto entro giorni X"
     Payoff: 100x se succede, 0 altrimenti
     Crea: incentivo R&D, bolla speculativa
     
  2) OPTIONS_NUTRIZIONE:
     Call: Diritto comprare numero Y a prezzo Z
     Put: Diritto vendere numero Y a prezzo Z
     Permette: hedging, speculazione
     
  3) COLLATERALIZED_NUMBER_OBLIGATIONS (CNO):
     Pool di numeri diversi → tranche per rischio
     Senior: Primi bassi stabili (AAA)
     Mezzanine: Composti medi (BBB)  
     Equity: Quasi-primi volatili (Junk)
     
  4) CREDIT_DEFAULT_SWAPS:
     Assicurazione su fallimento aziende
     Premio: 2% annuo × probabilità_default
     Trigger: cascata sistemica se troppo interconnessi
```

#### **12.3 Cicli Speculativi e Bolle**
```
DINAMICA_BOLLE:
  
  FASE_1_INNOVAZIONE:
    Scoperta nuovo primo importante → Entusiasmo razionale
    Prezzi +20%, Volumi +50%
    
  FASE_2_BOOM:
    Media_coverage → Retail_investors_entrano
    Prezzi +100%, "Nuovo paradigma"
    
  FASE_3_EUFORIA:  
    Leverage 10:1, "Primi to the moon!"
    Prezzi +500%, Società_zombie_IPO
    
  FASE_4_TRIGGER:
    Qualcuno_importante_vende OR cattive_notizie
    Prezzi -20% in un giorno
    
  FASE_5_PANICO:
    Margin_calls → Vendite_forzate → Spirale
    Prezzi -80% dal picco
    
  FASE_6_DEPRESSIONE:
    Sottovalutazione, Credito_congelato
    Opportunità per value_investors
```

### **13. SUPPLY CHAIN COMPLESSE**

#### **13.1 Network Effects e Dipendenze**
```
GRAFO_DIPENDENZE:
  
  Ogni_azienda_ha:
    fornitori_critici[]: Senza = stop produzione
    fornitori_ottimali[]: Senza = -30% efficienza  
    clienti_chiave[]: > 20% fatturato ciascuno
    
  CONTAGIO_FALLIMENTO:
    SE azienda_fallisce:
      Per ogni cliente:
        SE dipendenza > 50%:
          probabilità_fallimento_cliente = 40%
      Per ogni fornitore:
        SE cliente > 30% fatturato:
          probabilità_fallimento_fornitore = 60%
          
  RESILIENZA:
    diversificazione = 1 / concentrazione_Herfindahl
    buffer_inventory = giorni_sopravvivenza_senza_fornitori
    resilienza_score = diversificazione × buffer × capitale/debiti
```

#### **13.2 Just-In-Time vs Inventory**
```
STRATEGIE_INVENTORY:
  
  JUST_IN_TIME:
    inventory_target = domanda_giornaliera × 1.1
    costi_storage = minimi
    rischio_shortage = alto
    SE disruption: produzione_stop immediato
    
  BUFFER_STRATEGICO:
    inventory_target = domanda_mensile
    costi_storage = 5% valore/mese
    rischio_shortage = basso
    resilienza += 50%
    
  SPECULATIVO:
    SE prevede_aumento_prezzi:
      accumula_inventory = capitale_disponibile × 0.7
      SE giusto: profitto 30-200%
      SE sbagliato: costi_storage + obsolescenza
```

### **14. ECONOMIA INTER-REGIONALE**

#### **14.1 Vantaggi Comparati**
```
SPECIALIZZAZIONI_REGIONALI:
  
  Regione_A: "Silicon Prairie"
    Conoscenza_media +40%
    Costo_R&D -30%
    Focus: Primi P₂₀-P₅₀
    
  Regione_B: "Manufacture Hub"
    Efficienza_produzione +50%
    Costo_lavoro -40%
    Focus: Mass production 2,3,4,6
    
  Regione_C: "Trade Coast"
    Costi_trasporto -60%
    Network_globale +100%
    Focus: Arbitraggio e logistica
    
  Regione_D: "Luxury Valley"
    Qualità_percepita +80%
    Margini +150%
    Focus: Quasi-primi e numeri > 200
    
  Regione_E: "Frontier Lands"
    Risorse_base +200%
    Infrastrutture -70%
    Focus: Estrazione "1" e primi bassi
```

#### **14.2 Trade Wars e Tariffe**
```
POLITICHE_COMMERCIALI:
  
  TARIFFE_IMPORT:
    SE regione.protezionismo > 50:
      tariffa = 10-40% valore_import
      
    Effetti:
      prezzi_locali += tariffa × 0.7
      produzione_locale += 20%
      innovazione_locale -= 15%
      relazioni_diplomatiche -= 30
      
  EMBARGO:
    SE conflitto_ideologico > 80:
      blocco_totale_trade
      
    Conseguenze:
      mercato_nero emerge (prezzi 3x)
      produzione_sostituti_locali
      polarizzazione_globale
      
  DUMPING:
    SE azienda_sussidiata vende sotto_costo:
      distrugge_concorrenza_locale
      poi alza_prezzi (monopolio)
      trigger_antidumping_laws
```

### **15. METRICHE E INDICATORI ECONOMICI**

#### **15.1 Dashboard Economico Globale**
```
INDICATORI_MACRO:
  
  GDP = Σ(tutte_transazioni_valore)
  GDP_per_capita = GDP / popolazione
  
  GINI = disuguaglianza_ricchezza [0-1]
  
  INFLAZIONE:
    CPI_basket = [2×5, 3×10, 6×3, 15×1]  // Paniere standard
    inflazione = (CPI_oggi - CPI_anno_fa) / CPI_anno_fa
    
  UNEMPLOYMENT = senza_lavoro / forza_lavoro
  
  INNOVATION_INDEX = nuovi_primi_anno / popolazione × 1000
  
  HAPPINESS_INDEX = mediana(felicità_popolazione)
  
  VELOCITY_MONEY = GDP / money_supply
  
  DEBT/GDP = debito_totale / GDP
```

#### **15.2 Early Warning Signals**
```
ALERT_SISTEMA:
  
  SE inflazione > 20% mensile:
    WARNING: "Iperinflazione imminente"
    SUGGERIMENTO: "Politica monetaria restrittiva"
    
  SE GINI > 0.8:
    WARNING: "Disuguaglianza critica"
    SUGGERIMENTO: "Riforme redistributive"
    
  SE unemployment > 25%:
    WARNING: "Crisi occupazionale"
    SUGGERIMENTO: "Stimolo fiscale"
    
  SE debt/GDP > 150%:
    WARNING: "Insostenibilità debitoria"
    SUGGERIMENTO: "Austerity o default controllato"
    
  SE nessun_nuovo_primo per 500 giorni:
    WARNING: "Stagnazione innovativa"
    SUGGERIMENTO: "Incentivi R&D"
```

### **16. MECCANISMI ANTI-COLLASSO**

#### **16.1 Stabilizzatori Automatici**
```
INTERVENTI_EMERGENZA:
  
  // Previene estinzione
  SE popolazione < 100:
    spawn_migranti(50)
    bonus_fertilità = 200%
    
  // Previene carestia totale  
  SE nutrizione_media < 0.3:
    helicopter_drop("1" × popolazione × 7)
    sblocco_emergenza_tecnologie_produzione
    
  // Reset monetario
  SE inflazione > 10000% annuale:
    nuova_valuta()
    conversione = vecchia / 1000
    price_freeze(30 giorni)
    
  // Antitrust automatico
  SE market_concentration > 90%:
    break_up_monopolio()
    sussidi_startup_competitors
    
  // Bailout sistemico
  SE aziende_fallite > 30% in 30 giorni:
    iniezione_liquidità = GDP × 0.1
    garanzie_statali_prestiti
    moratoria_fallimenti(90 giorni)
```

#### **16.2 Meccanismi di Resilienza**
```
ADAPTIVE_SYSTEMS:
  
  // Apprendimento collettivo
  Dopo_ogni_crisi:
    memoria_istituzionale += lesson_learned
    regolamentazione_preventiva += safeguards
    MA: regulatory_capture possibile dopo 1000 giorni
    
  // Diversificazione forzata
  SE dipendenza_singolo_primo > 60%:
    incentivi_diversificazione
    ricerca_sostituti_accelerata
    
  // Ciclo naturale pulizia
  Ogni 3000-5000 giorni:
    "Disruzione tecnologica"
    Vecchi monopoli obsoleti
    Nuove opportunità emergono
    Redistribuzione parziale ricchezza
```

---

**FINE PARTE 2 INTEGRATA**

Ora il sistema economico è molto più ricco e realistico, con:
- Meccaniche di trading sofisticate
- Veri vantaggi strategici basati sui pattern dei primi
- Strumenti finanziari complessi che possono creare bolle
- Supply chain interconnesse con effetti domino
- Specializzazioni regionali e trade wars
- Sistemi di bilanciamento che prevengono il collasso totale

# **PRIME SOCIETY - MANUALE DI SIMULAZIONE**
## **PARTE 3: TERRITORIO, ABITAZIONI E POLITICA**

---

### **17. SISTEMA TERRITORIALE E GEOGRAFICO**

#### **17.1 Struttura Spaziale del Mondo**
```
ORGANIZZAZIONE_TERRITORIALE:
  
  MONDO = {
    5 REGIONI → 20 DISTRETTI → 2000 CELLE TOTALI
  }
  
  Ogni_REGIONE:
    4 distretti
    Caratteristiche_uniche (clima economico)
    Confini con 2-3 altre regioni
    
  Ogni_DISTRETTO:  
    100 celle (griglia 10×10)
    Centro_urbano: celle [4,4] a [6,6] (9 celle centrali)
    Periferia: anello esterno
    Confini: bordi della griglia
    
  Ogni_CELLA:
    Spazio_edificabile: 1000 unità cubiche
    Costruzione_verticale: illimitata
    Densità_max: determinata da domanda
    Coordinate: [x, y, z] dove z = altezza
```

#### **17.2 Caratteristiche Geografiche**
```
GENERAZIONE_MAPPA:
  
  Per_ogni_cella:
    // Valore base terreno
    fertilità_risorse = perlin_noise(x, y) × 100  // 0-100
    
    // Attrattività naturale  
    features = {
      fiume: SE adjacent_to_water → attrattività +30
      collina: SE elevation > 50 → vista +20, costruzione +10% costo
      pianura: SE elevation < 20 → costruzione -20% costo
      costa: SE border_region → trade +40%, rischio_eventi +20%
    }
    
    // Risorse "1" naturali
    produzione_base_1 = fertilità × (1 + bonus_features) / 100
    
  INFRASTRUTTURE_INIZIALI:
    strade_principali = pathfinding(centro → centro)
    strade_secondarie = grid_connections
    capacità_strada = 100 transiti/giorno base
```

### **18. MERCATO IMMOBILIARE DINAMICO**

#### **18.1 Spazio come Risorsa Continua**
```
SISTEMA_ABITATIVO:
  
  // NO prezzi fissi, tutto emergente
  
  Ogni_edificio = {
    spazio_totale: m³ costruiti
    spazio_utilizzabile: totale × 0.85
    piani: altezza / 3 metri
    unità_abitative: configurazione_dinamica
    qualità_costruzione: 1-100
    età: giorni_da_costruzione
    manutenzione: costo_giornaliero
  }
  
  BISOGNO_SPAZIO_FAMIGLIA:
    minimo_vitale = 10 × n_membri m³
    comfort_base = 25 × n_membri m³  
    desiderato = comfort_base × (1 + materialismo/100)
    lusso = 50 × n_membri × status_ambito m³
    
  CONFIGURAZIONE_DINAMICA:
    proprietario_decide_divisione():
      SE domanda_piccoli > domanda_grandi:
        suddividi_in_monolocali(15 m³ each)
      SE domanda_famiglie:
        crea_appartamenti(60-120 m³)
      SE domanda_lusso:
        mantieni_intero(500+ m³)
```

#### **18.2 Formazione Prezzi Immobiliari**
```
VALORE_LOCATION(x, y, z):
  
  // Fattori base posizione
  distanza_centro = √((x-5)² + (y-5)²)
  valore_centralità = 100 / (distanza_centro + 1)
  
  // Accessibilità economica
  posti_lavoro_vicini = Σ(aziende_nel_raggio(3) × posti × qualità)
  accessibilità_lavoro = log(posti_lavoro_vicini + 1) × 10
  
  // Educazione
  scuole_vicine = trova_scuole(raggio: 2)
  valore_educazione = best(scuole_vicine).qualità × 20
  
  // Composizione sociale
  ricchezza_media_vicini = avg(ricchezza[x±1, y±1])
  omogeneità_culturale = 1 - varianza(memi_vicini)
  prestigio_sociale = ricchezza_media_vicini^0.5 × omogeneità_culturale
  
  // Servizi e amenità
  servizi_score = conta_servizi(raggio: 2) × 5
  verde_pubblico = celle_parco(raggio: 3) × 10
  
  // Vista e ambiente  
  vista_score = SE z > 10: bonus_elevazione(z)
  rumore = -Σ(aziende_produttive(raggio: 1) × 10)
  inquinamento = -traffico_medio_zona × 5
  
  // Sicurezza percepita
  criminalità = eventi_negativi_90giorni / popolazione_zona
  sicurezza = 100 - criminalità × 10
  
  VALORE_FINALE_m³ = (
    valore_centralità × 0.15 +
    accessibilità_lavoro × 0.25 +
    valore_educazione × 0.15 +
    prestigio_sociale × 0.20 +
    servizi_score × 0.10 +
    ambiente × 0.10 +
    sicurezza × 0.05
  ) × qualità_edificio × (1 - età/10000)
```

#### **18.3 Dinamiche di Mercato**
```
MECCANISMO_ASTA:
  
  Quando_spazio_disponibile:
    proprietario.prezzo_richiesto = valore_stimato × (1 + avidità/200)
    
    interessati = persone.filter(
      bisogno_casa AND 
      budget >= prezzo × 0.8 AND
      distanza_lavoro < tolleranza
    )
    
    Per_ogni_interessato:
      offerta = min(
        budget_disponibile,
        valore_percepito × (1 + urgenza/100)
      )
      
    SE max(offerte) >= prezzo_richiesto × 0.95:
      vendi_a_miglior_offerente()
    ALTRIMENTI:
      ogni_7_giorni: prezzo *= 0.97
      
AFFITTO_VS_ACQUISTO:
  
  affitto_mensile = valore_proprietà × (0.003 + rischio_zona × 0.001)
  
  decisione_individuale:
    SE (affitto × 12 × 30) < prezzo_acquisto:
      preferenza = "affitto"
    SE stabilità_lavoro > 80% AND capitale > 20% prezzo:
      preferenza = "acquisto"
    SE speculazione_immobiliare AND ricchezza > necessità × 5:
      compra_per_investimento()
```

### **19. SVILUPPO URBANO E ZONIZZAZIONE**

#### **19.1 Zonizzazione Emergente**
```
FORMAZIONE_QUARTIERI:
  
  // Nessuna zonizzazione top-down, emerge dal mercato
  
  CLUSTERING_NATURALE:
    Quando_azienda_si_installa:
      attrae_lavoratori_vicino
      aumenta_valore_commerciale_zona
      respinge_residenziale_lusso
      
    Quando_famiglia_ricca_si_installa:
      attrae_simili (effetto_network)
      attrae_servizi_lusso
      prezzi_salgono
      poveri_espulsi
      
  TIPOLOGIE_EMERGENTI:
    
    CBD (Central Business District):
      - Alta densità uffici
      - Prezzi estremi (1000+/m³)
      - Pochi residenti
      - Traffico pendolari massimo
      
    Quartiere_Creativo:
      - Mix abitativo/lavorativo
      - Prezzi medi (200-400/m³)
      - Alta inventiva media
      - Locali culturali emergono
      
    Suburbia_Familiare:
      - Bassa densità
      - Prezzi medio-bassi (100-250/m³)
      - Scuole prioritarie
      - Omogeneità culturale alta
      
    Industrial_Park:
      - Fabbriche cluster
      - Prezzi bassi (50-150/m³)
      - Inquinamento alto
      - Abitazioni operaie adiacenti
      
    Slum:
      - Sovraffollamento estremo
      - Prezzi minimi (10-50/m³)
      - Servizi assenti
      - Criminalità alta
      - MA: solidarietà sociale alta
      
    Gated_Community:
      - Accesso controllato
      - Prezzi lusso (500-2000/m³)
      - Servizi privati
      - Segregazione volontaria
```

#### **19.2 Gentrification e Displacement**
```
PROCESSO_GENTRIFICATION:
  
  FASE_1_PIONIERI:
    artisti_e_creativi.trova_zona_cheap_but_cool()
    affitti_bassi + spazi_grandi = attrattivo
    cultura_underground.emerge()
    
  FASE_2_SCOPERTA:
    media.racconta_quartiere_trendy()
    giovani_professionisti.arrivano()
    primi_locali_hipster.aprono()
    prezzi +20% anno
    
  FASE_3_ACCELERAZIONE:
    investitori.comprano_per_ristrutturare()
    brand_chains.rimpiazzano_negozi_locali()
    prezzi +50% anno
    residenti_originali.inizio_espulsione()
    
  FASE_4_SATURAZIONE:
    solo_ricchi.possono_permettersi()
    carattere_originale.perso()
    prezzi.stabilizzano()
    
  RESISTENZA_GENTRIFICATION:
    SE comunità.coesione > 70:
      organizza_proteste()
      crea_community_land_trust()
      rallenta_processo × 0.5
```

### **20. MOBILITÀ E TRASPORTI**

#### **20.1 Sistema di Trasporto**
```
INFRASTRUTTURE_TRASPORTO:
  
  STRADE:
    capacità_base = 100 veicoli/ora
    congestione = traffico / capacità
    SE congestione > 1:
      velocità = velocità_base / congestione²
      stress_viaggiatori += 20
      
  TRASPORTO_PUBBLICO:
    bus: copertura 60%, costo 2/viaggio
    metro: copertura 30%, costo 5/viaggio, velocità 3x
    
  DECISIONE_MODALITÀ:
    SE distanza < 2 celle: camminare
    SE ricchezza > medio AND has_parking: auto
    SE vicino_metro: metro
    ALTRIMENTI: bus
    
PENDOLARISMO:
  
  tempo_viaggio = distanza / velocità_effettiva
  costo_viaggio = carburante + usura + (parking SE centro)
  stress_viaggio = tempo² × traffico × (100 - comfort_mezzo)
  
  energia_persa = 5 × tempo_viaggio
  tempo_libero = 100 - lavoro - viaggio×2 - necessità_base
  
  SE tempo_libero < 10:
    burnout_risk += 10/giorno
    cerca_casa_più_vicina.priority = MAX
```

#### **20.2 Impatto sulla Vita**
```
QUALITÀ_VITA_SPAZIALE:
  
  accessibilità_score = {
    lavoro: 100 - (minuti_commute × 2)
    servizi: servizi_raggiungibili_15min × 10
    sociale: amici_nel_raggio_30min × 5
    natura: parchi_raggiungibili_walking × 20
  }
  
  isolamento_sociale:
    SE distanza_media_amici > 5 celle:
      interazioni_sociali -= 50%
      felicità -= 15
      rischio_depressione += 30%
      
  segregazione_economica:
    SE deviazione_standard(ricchezza_quartiere) < 10%:
      echo_chamber += 30
      innovazione_locale -= 20%
      pregiudizi += 40%
```

### **21. SISTEMA POLITICO**

#### **21.1 Struttura Democratica**
```
GERARCHIA_POLITICA:
  
  Livello_1_BLOCCO (20-30 persone):
    Rappresentante: eletto direttamente
    Mandato: 180 giorni
    Poteri: gestione spazi comuni, micro-tasse
    
  Livello_2_QUARTIERE (200-300 persone):
    Consigliere: eletto dai rappresentanti
    Mandato: 365 giorni
    Poteri: servizi locali, regolamenti commerciali
    
  Livello_3_DISTRETTO (2000-3000 persone):
    Sindaco: eletto dai consiglieri
    Mandato: 730 giorni
    Poteri: tasse, educazione, infrastrutture
    
  Livello_4_REGIONE (8000-12000 persone):
    Governatore: eletto dai sindaci
    Mandato: 1095 giorni
    Poteri: politica economica, giustizia
    
MECCANISMO_ELETTORALE:
  
  candidatura_probabilità = (
    ambizione × 
    carisma × 
    (ricchezza/media_ricchezza)^0.3 ×
    (reputazione/100)
  ) / 10000
  
  SE probabilità > random():
    candida_con_piattaforma()
```

#### **21.2 Ideologie e Piattaforme**
```
SPETTRO_POLITICO (2 assi principali):
  
  Asse_Economico:
    SINISTRA [-100]: Alta tassazione, welfare, regolamentazione
    CENTRO [0]: Bilanciamento, pragmatismo
    DESTRA [+100]: Basse tasse, libero mercato, deregulation
    
  Asse_Sociale:
    PROGRESSISTA [-100]: Innovazione, inclusione, cambiamento
    MODERATO [0]: Stabilità, gradualismo
    CONSERVATORE [+100]: Tradizione, omogeneità, ordine
    
  GENERAZIONE_PIATTAFORMA:
    posizione_reale = {
      economica: pragmatico - sociale,
      sociale: progressista - conservatore
    }
    
    SE inganno > 50:
      posizione_dichiarata = posizione_che_massimizza_voti
    ALTRIMENTI:
      posizione_dichiarata = posizione_reale × (sincerità/100)
```

#### **21.3 Meccanismi di Voto**
```
DECISIONE_VOTO_INDIVIDUALE:
  
  Per_ogni_candidato:
    
    // Voto razionale
    allineamento = 100 - |mia_posizione - candidato_posizione|
    beneficio_atteso = stima_politiche_impatto_personale()
    razionale_score = allineamento × 0.5 + beneficio × 0.5
    
    // Voto emotivo  
    carisma_appeal = candidato.carisma × affinità_personale
    tribal_identity = stesso_meme_culturale ? 50 : 0
    emotivo_score = carisma_appeal + tribal_identity
    
    // Influenza sociale
    peer_pressure = % amici_che_supportano × conformismo
    propaganda_effect = esposizione_messaggi × (100 - riflessività)
    sociale_score = peer_pressure + propaganda_effect
    
    // Peso componenti basato su sapienza
    voto_finale_score = 
      razionale_score × (sapienza/100) +
      emotivo_score × (50/100) +
      sociale_score × ((100-sapienza)/100)
      
  vota_per(candidato_max_score)
  
  // Astensionismo
  SE max_score < 30 OR felicità < 20:
    non_votare()
```

### **22. POLITICHE E GOVERNANCE**

#### **22.1 Leve Politiche per Livello**
```
POTERI_BLOCCO:
  - Tassa_blocco: 0-5% transazioni locali
  - Manutenzione: pulizia, illuminazione
  - Mediazione: risoluzione dispute vicinato
  - Eventi: organizzazione sociale
  
POTERI_QUARTIERE:
  - Licenze_commerciali: chi può aprire negozi
  - Orari_apertura: regolamentazione
  - Tassa_proprietà: 0-10% valore immobili
  - Sicurezza: pattugliamento
  
POTERI_DISTRETTO:
  - Educazione: curriculum, budget scuole
  - Salario_minimo: floor stipendi
  - Ambiente: limiti inquinamento
  - Trasporti: investimenti infrastrutture
  - Tasse_reddito: 5-40% progressiva
  
POTERI_REGIONE:
  - Politica_monetaria: può stampare valuta locale
  - Giustizia: leggi e enforcement
  - Commercio: tariffe import/export
  - Welfare: sussidi e pensioni
  - Ricerca: finanziamenti pubblici R&D
  
IMPLEMENTAZIONE_POLITICHE:
  
  Quando_politica_approvata:
    costo_implementazione = complessità × resistenza_burocratica
    tempo_effetti = 30-365 giorni (base complessità)
    
    SE opposizione > 60%:
      proteste()
      efficacia × 0.5
      possibile_revoca()
```

#### **22.2 Corruzione e Lobbying**
```
SISTEMA_INFLUENZA:
  
  LOBBYING_LEGALE:
    aziende_possono_donare = max(fatturato × 0.01)
    
    influenza_acquistata = donazione / (costo_influenza × integrità_politico)
    
    SE influenza > soglia:
      politico.bias_decisioni += direzione_lobby × 30%
      
  CORRUZIONE_ILLEGALE:
    SE politico.inganno > 70 AND azienda.avidità > 70:
      
      tangente_richiesta = beneficio_azienda × 0.1
      
      SE azienda.paga():
        politico.ricchezza += tangente
        azienda.ottiene_favore()
        
        probabilità_scoperta = (100 - inganno_politico) × 
                              giornalisti_investigativi × 
                              whistleblower_probability
                              
      SE scoperto:
        politico.reputazione = 0
        politico.incarcerato(180 giorni)
        azienda.multa(tangente × 10)
        
  CLIENTELISMO:
    politico_può_assumere = n_posizioni_pubbliche
    
    SE nepotismo > merito:
      assumi_famiglia_e_amici()
      efficienza_pubblica -= 40%
      MA: loyalty_network += 100%
```

### **23. CULTURA E MEMI IDEOLOGICI**

#### **23.1 Nascita e Diffusione Memi**
```
GENERAZIONE_MEMI_CULTURALI:
  
  Ogni_100_giorni:
    SE random() < creatività_sociale:
      
      inventor = persona_random(inventiva > 70 OR carisma > 70)
      
      nuovo_meme = {
        nome: genera_nome_accattivante(),
        effetti: {
          modifica_tratto[random]: ±20%,
          modifica_comportamento: pattern_nuovo,
          modifica_priorità: shift_valori
        },
        attrattività: carisma_inventor × novità
      }
      
PROPAGAZIONE:
  
  Per_ogni_interazione_sociale:
    
    esposizione = portatore.evangelism × tempo_contatto
    
    resistenza = target.riflessività × 
                (100 - conformismo) × 
                satisfaction_status_quo
                
    SE esposizione > resistenza:
      target.adotta_meme()
      target.immunity[meme] = 365 giorni
      
  VIRAL_SPREAD:
    SE adozioni_7giorni > popolazione × 0.1:
      meme.status = "viral"
      spread_rate × 3
      media_coverage = true
```

#### **23.2 Esempi di Memi Culturali**
```
MEMI_ECONOMICI:
  
  "Grindset Primo":
    - Ambizione +40%
    - Stress +30%
    - Lavoro 14 ore/giorno normale
    - Burnout rate 3x
    
  "FIRE Movement" (Financial Independence Retire Early):
    - Frugalità +60%
    - Risparmio 70% reddito
    - Target: libertà a 40 anni
    - Felicità -20% ora, +50% dopo
    
  "Degrowth Collective":
    - Materialismo -80%
    - Produttività -40%
    - Felicità +30%
    - Sostenibilità +100%
    
MEMI_SOCIALI:
  
  "Nuclear Traditional":
    - Conservatorismo +50%
    - Famiglia priorità assoluta
    - Fertilità +40%
    - Innovazione -20%
    
  "Radical Atomization":
    - Individualismo +80%
    - Relazioni -60%
    - Mobilità +100%
    - Depressione +40%
    
  "Neo-Tribalism":
    - Lealtà gruppo +100%
    - Xenofobia +60%
    - Coesione interna +80%
    - Conflitti esterni +70%
```

#### **23.3 Effetti Politici dei Memi**
```
INTERAZIONE_MEMI_POLITICA:
  
  Quando_meme_dominante(> 50% popolazione):
    
    politici.devono_allinearsi OR perdere_elezioni
    
    leggi.drift_verso(valori_meme)
    
    istituzioni.catturate_da(ideologia)
    
  POLARIZZAZIONE:
    SE due_memi_opposti > 30% each:
      
      centro_politico.scompare()
      
      elezioni.diventano_esistenziali()
      
      violenza_politica.probabilità += 50%
      
      possibile.scissione_territorio()
      
  RIVOLUZIONI_CULTURALI:
    SE nuovo_meme.radicalità > 80 AND adozione > 60%:
      
      vecchio_sistema.collassa()
      
      nuove_istituzioni.create()
      
      purge.oppositori (esilio o peggio)
      
      storia.riscritta()
```

### **24. CICLI E CRISI POLITICHE**

#### **24.1 Cicli Politici Naturali**
```
FASI_CICLO_POLITICO:
  
  1_LUNA_DI_MIELE (giorni 0-180):
    Fiducia alta
    Riforme facili passano
    Media favorevoli
    Opposizione debole
    
  2_REALITY_CHECK (giorni 180-365):
    Promesse vs realtà
    Prima opposizione
    Scandali minori
    Base ancora solida
    
  3_CONSOLIDAMENTO (giorni 365-730):
    Fazioni cristallizzate
    Battaglie legislative
    Compromessi necessari
    Fatica riformista
    
  4_DECLINO (giorni 730-1095):
    Scandali maggiori
    Opposizione forte
    Base delusa
    Lame duck period
    
TRIGGER_CRISI:
  
  SE corruzione_scoperta AND economia_male:
    CRISI_LEGITTIMITÀ
    
  SE disuguaglianza > 85 AND disoccupazione > 30%:
    CRISI_SOCIALE
    
  SE deficit > 200% PIL:
    CRISI_FISCALE
    
  SE due_fazioni 50/50 AND odio > 80:
    CRISI_COSTITUZIONALE
```

#### **24.2 Risoluzioni delle Crisi**
```
PERCORSI_RISOLUZIONE:
  
  RIFORME_DALL_ALTO:
    SE leadership.intelligenza > 80 AND pragmatismo > 70:
      implementa_riforme_preventive()
      cede_potere_parziale()
      evita_collasso()
      
  RIVOLUZIONE_PACIFICA:
    SE opposizione.organizzata AND regime.debole:
      proteste_massa()
      regime.cade()
      nuove_elezioni()
      
  RIVOLUZIONE_VIOLENTA:
    SE oppressione > 80 AND disperazione > 90:
      insurrezione_armata()
      guerra_civile(durata: 180-730 giorni)
      vincitore.impone_nuovo_ordine()
      
  COLPO_DI_STATO:
    SE militari.scontenti OR elite.panico:
      takeover_improvviso()
      costituzione.sospesa()
      governo_emergenza()
      
  COLLASSO_TOTALE:
    SE nessuna_fazione > 30% supporto:
      anarchia()
      territori.frammentano()
      warlords_locali()
      dark_age(1000 giorni)
```

### **25. INTEGRAZIONE SISTEMI**

#### **25.1 Feedback Loops Territorio-Economia-Politica**
```
CICLI_RINFORZANTI:
  
  RICCHEZZA→POTERE→RICCHEZZA:
    ricchi.comprano_influenza →
    politiche.favorevoli →
    ricchi.più_ricchi →
    ciclo.ripete()
    
  SEGREGAZIONE→POLARIZZAZIONE→SEGREGAZIONE:
    quartieri.omogenei →
    echo_chambers →
    estremizzazione →
    più_segregazione →
    ciclo.accelera()
    
  INNOVAZIONE→CRESCITA→INVESTIMENTI→INNOVAZIONE:
    scoperte.nuovi_primi →
    economia.boom →
    R&D.funding++ →
    più_scoperte →
    ciclo.virtuoso()
    
CICLI_BILANCIANTI:
  
  MONOPOLIO→REAZIONE→COMPETIZIONE:
    concentrazione.eccessiva →
    regolamentazione OR innovazione_disruptiva →
    nuovi_entranti →
    frammentazione_mercato
    
  AUTORITARISMO→RESISTENZA→LIBERALIZZAZIONE:
    repressione++ →
    underground_resistance →
    costi_controllo > benefici →
    apertura_graduale OR rivoluzione
```

#### **25.2 Metriche di Sistema Integrate**
```
DASHBOARD_SOCIETÀ:
  
  // Economiche (da Parte 2)
  GDP, GINI, Inflazione, Disoccupazione
  
  // Territoriali
  Segregazione_Index = varianza(ricchezza_per_quartiere)
  Sprawl_Index = densità_centro / densità_periferia
  Housing_Affordability = affitto_medio / salario_medio
  Commute_Time_Medio = avg(tempo_viaggio_lavoro)
  
  // Politiche
  Democracy_Index = partecipazione × alternanza × libertà
  Corruption_Index = tangenti_totali / GDP
  Stability_Index = 100 - (proteste + violenza + crisi)
  
  // Culturali
  Diversity_Index = 1 - Σ(frazione_meme²)
  Innovation_Culture = nuovi_memi_anno / popolazione
  Social_Cohesion = interazioni_cross_gruppo / interazioni_totali
  
  // Benessere Integrato
  Quality_of_Life = (GDP_pro_capite^0.3) × 
                   (1 - GINI) × 
                   felicità_mediana × 
                   aspettativa_vita × 
                   libertà_percepita
```

---

**FINE PARTE 3**

Il sistema territoriale, abitativo e politico è ora completamente integrato con:
- Mercato immobiliare totalmente emergente basato su domanda/offerta
- Sviluppo urbano organico con quartieri che si auto-organizzano
- Sistema politico multi-livello con ideologie e corruzione
- Memi culturali che influenzano comportamenti e politica
- Cicli di crisi e rinnovamento
- Feedback loops che collegano tutti i sistemi

# **PRIME SOCIETY - MANUALE DI SIMULAZIONE**
## **PARTE 4: ESEMPI DI GAMEPLAY E PATTERNS EMERGENTI**

---

### **26. STORIE INDIVIDUALI TIPICHE**

#### **26.1 L'Ascesa dell'Innovatore**
```
STORIA: "Marco il Matematico"

Giorno 0-5000: INFANZIA
- Nasce con Inventiva: 85, Intelligenza: 92
- Famiglia povera (Distretto industriale)
- Padre operaio conosce solo primi fino a P₃(5)

Giorno 5000-9000: FORMAZIONE
- Scuola pubblica scarsa ma Marco eccelle
- Docente nota talento, mentoring gratuito
- Apprende fino a P₁₀(29) con borse studio
- Stress: 60 (pressione economica famiglia)

Giorno 9000-12000: BREAKTHROUGH
- Assunto in laboratorio R&D medio
- Stipendio: 50/giorno (manda 30 a famiglia)
- Scopre pattern nei primi gemelli
- Giorno 11543: SCOPRE P₂₃(83)!
- Brevetto vale 2,000,000 risorse

Giorno 12000-15000: IMPERO
- Fonda "PrimeTech Industries"
- Monopolio temporaneo su 83 e composti
- Fattura 50,000/mese
- SI TRASFERISCE in villa centro (500 m³)
- Famiglia lo segue, tensioni per cambio classe

Giorno 15000-18000: CADUTA
- Brevetto scade
- Competitors copiano con prezzi -70%
- Marco non sa gestire azienda (Diplomazia: 20)
- Trusted manager lo truffa (Inganno manager: 90)
- Fallimento, torna in periferia

Giorno 18000+: REDENZIONE?
- Depressione (Felicità: -40)
- Moglie lo lascia per stress finanziario
- MA: Mantiene conoscenza
- Diventa tutor primi per sopravvivere
- Suoi studenti fonderanno nuovo lab
- Legacy: "Metodo Marco" per pattern recognition

MORALE: Intelligenza ≠ Successo sostenibile
```

#### **26.2 La Dinastia Mercantile**
```
STORIA: "Famiglia Chen - Tre Generazioni"

GENERAZIONE 1: Chen Senior
- Tratti: Avidità: 70, Diplomazia: 80, Inganno: 60
- Strategia: Arbitraggio inter-regionale
- Compra P₅(11) a Regione_A per 100
- Vende a Regione_B per 180
- Accumula capitale: 500,000 in 20 anni
- Sposa figlia del Governatore (power match)

GENERAZIONE 2: Chen Junior
- Tratti ereditati: Avidità: 75, Ambizione: 85
- Educazione elite: Conosce fino a P₃₀
- Espande in manifattura composti
- Scopre sinergia 30=2×3×5 super efficiente
- Controlla 35% mercato nutrizione Regione_B
- Entra in politica: Eletto Sindaco
- USA posizione per favorire famiglia

GENERAZIONE 3: I Gemelli Chen
- Twin_A: Ribelle (Sociale: 90, rifiuta famiglia)
  - Fonda cooperativa anti-monopolio
  - Compete direttamente con famiglia
  - Divide base clienti con prezzi etici
  
- Twin_B: Erede (Avidità: 95, Inganno: 85)
  - Corrompe regolatori
  - Crea cartello segreto con "competitors"
  - Manipola prezzi primi
  - Scandal: Giornalista espone tutto
  - Famiglia perde 80% ricchezza
  - Twin_A compra assets famiglia a sconto

EPILOGO: Valori familiari vs Valori personali
```

#### **26.3 Il Rivoluzionario Accidentale**
```
STORIA: "Sara l'Idealista"

Background:
- Tratti: Sociale: 95, Carisma: 78, Intelligenza: 60
- Nasce in slum (parents lavoratori primi bassi)
- Vede disuguaglianza ogni giorno

Fase Attivista (giorni 6000-10000):
- Organizza proteste per salario minimo
- Arrestata 3 volte, radicalizza in prigione
- Crea meme "Primi per Tutti" (effetto: Condivisione +50%)
- Meme diventa virale tra poveri

Fase Politica (giorni 10000-13000):
- Candidata Consigliere con piattaforma radical
- Perde, ma ottiene 40% voti (shock per elite)
- Elite tenta corruzione: offre 100,000
- Sara rifiuta pubblicamente → Eroe popolare

Fase Rivoluzione (giorni 13000-14000):
- Crisi economica, disoccupazione 40%
- Sara guida occupazione fabbriche
- Governo ordina repressione
- Video violenza diventa virale
- Governo cade in 30 giorni

Fase Potere (giorni 14000-18000):
- Sara eletta Governatore emergenza
- Implementa "Primi Basic Income"
- Nazionalizza grandi labs
- Economia initial crash -30%
- MA: Disuguaglianza da 0.85 a 0.45
- Felicità mediana +40%

Corruzione del Potere (giorni 18000+):
- Pressioni continue cambiano Sara
- Pragmatismo sostituisce idealismo
- Inizia compromessi con elite
- Supporters si sentono traditi
- Nuovo movimento nasce contro di lei

IRONIA: Rivoluzionari diventano establishment
```

### **27. DINAMICHE AZIENDALI EMERGENTI**

#### **27.1 Guerra dei Primi tra MegaCorp**
```
SCENARIO: "La Corsa al P₅₀(229)"

SETUP:
- 3 MegaCorp controllano 70% mercato
- PrimeCorp: Focus ricerca pura
- SynerGen: Focus combinazioni
- TradeMax: Focus distribuzione

ANNO 1: INVESTIMENTI
PrimeCorp: 
- Budget R&D: 10,000,000
- Team: 50 scienziati top (IQ medio: 120)
- Strategia: Forza bruta su P₅₀

SynerGen:
- Budget: 5,000,000
- Strategia: Scoprire P₄₈ e P₄₉ prima
- Logic: Pattern recognition più facile

TradeMax:
- Budget: 2,000,000
- Strategia: Spionaggio industriale
- Infiltra spie in entrambe

ANNO 2: BREAKTHROUGH PARZIALI
- SynerGen scopre P₄₈(223)!
- Stock price +200%
- USA profitti per accelerare P₄₉
- PrimeCorp panic, raddoppia team
- TradeMax spy ruba dati parziali P₅₀

ANNO 3: LA SCOPERTA
- TradeMax usa dati rubati + luck
- SCOPRE P₅₀(229) per primo!
- Brevetto 365 giorni monopolio
- PrimeCorp e SynerGen citano in giudizio
- Battaglia legale costa milioni

CONSEGUENZE:
- TradeMax domina mercato lusso
- PrimeCorp CEO licenziato, ristruttura
- SynerGen pivot verso medio mercato
- Pubblico perde fiducia in R&D ethics
- Governo introduce "Patent Reform Act"

LEZIONI:
- R&D puro ≠ Vittoria garantita
- Spionaggio può battere innovazione
- First mover advantage cruciale
```

#### **27.2 Startup Disruptive**
```
CASE STUDY: "NumShare - L'Uber dei Primi"

PROBLEMA IDENTIFICATO:
- Molte persone hanno eccesso alcuni primi
- Altri hanno carenza quegli stessi primi
- Inefficienza mercato: 40% spreco

SOLUZIONE STARTUP:
Fondatori: 3 ventenni (Inventiva media: 75)
App: Matching peer-to-peer real time
- User_A: "Ho eccesso 17, cerco 13"
- User_B: "Ho eccesso 13, cerco 17"
- Match istantaneo, scambio diretto
- Fee: 5% del valore transazione

CRESCITA ESPONENZIALE:
Mese 1: 100 users, 50 transazioni
Mese 6: 10,000 users, 5,000 trans/giorno
Anno 1: 100,000 users, 25% tutto mercato

REAZIONE INCUMBENT:
- Trading houses perdono 30% revenue
- Tentano acquisizione: Offerta 50M
- Founders rifiutano
- Incumbents lobbying per ban
- "Regulation Safety Act" proposto

PIVOT STRATEGICO:
- NumShare diventa "decentrato"
- Nessun server centrale
- Peer-to-peer puro
- Impossibile da bannare
- Fee scende a 1% (automated)

EPILOGO:
- Trading houses crollano 70%
- NumShare founders = billionaires
- MA: Tassazione impossibile
- Governo perde 20% revenue
- Economia sommersa cresce
```

### **28. CRISI SISTEMICHE E CASCATE**

#### **28.1 Il Grande Crash dei Quasi-Primi**
```
CRONOLOGIA DELLA BOLLA:

GIORNO 0: INNOVAZIONE
- Scoperta: Quasi-primi (143, 221, 323) hanno proprietà nascosta
- Se combinati in sequenza → Super-nutrizione
- Papers scientifici confermano

GIORNI 1-100: ENTUSIASMO RAZIONALE
- Early adopters comprano quasi-primi
- Prezzi +50%
- Aziende pivot verso produzione
- Investimenti razionali

GIORNI 100-300: MANIA
- Media: "Quasi-Primi sono il futuro!"
- Tutti vogliono quasi-primi
- Prezzi +500%
- Leverage 10:1 comune
- Nonna investe pensione

GIORNI 300-400: PICCO FOLLE
- 323 vale più di tutto 2-30 combinato
- Aziende normali abbandonate
- Solo quasi-primi prodotti
- GDP nominale +200% (inflazione)

GIORNO 401: IL TRIGGER
- Scienziato prestigioso pubblica:
- "Errore calcolo - nessun super bonus"
- Articolo virale in 2 ore

GIORNI 402-410: PANICO
- Vendite massive
- Prezzi -90%
- Margin calls cascata
- Banche esposte crollano

GIORNI 410-500: DEPRESSIONE
- 50% aziende fallite
- Disoccupazione 45%
- Suicidi +300%
- Governo stampa moneta
- Iperinflazione

GIORNI 500-1000: RICOSTRUZIONE
- Nuovo sistema bancario
- Regole leverage max 3:1
- "Never Forget 401"
- MA: Memoria corta...

LEZIONI SISTEMICHE:
- Informazione asimmetrica → Bolle
- Leverage amplifica tutto
- Cascate inevitabili in sistemi connessi
- Regolazione sempre in ritardo
```

#### **28.2 La Grande Migrazione Climatica**
```
EVENTO: Regione_A diventa inabitabile

TRIGGER:
- Bug algoritmo produzione
- Regione_A: produzione "1" crolla 90%
- Carestia immediata
- Governo locale paralizzato

ONDATA 1 (giorni 1-30): ELITE FUGGE
- 1000 ricchi migrano immediate
- Portano capitale e conoscenza
- Comprano proprietà Regione_B e C
- Prezzi case +40% overnight

ONDATA 2 (giorni 30-100): CLASSE MEDIA
- 10,000 persone vendono tutto
- Viaggiano in carovane
- Regione_B chiude frontiere
- Campi profughi a confini

ONDATA 3 (giorni 100-365): DISPERATI
- 30,000 poveri restanti
- Niente da perdere
- Attraversano illegalmente
- Tensioni con locali

CONSEGUENZE REGIONE_B:
- Salari -30% (eccesso offerta lavoro)
- Affitti +100% (carenza abitazioni)
- Servizi collassano (sovraccarico)
- Criminalità +200%
- Partiti anti-immigrazione 60% voti

CONSEGUENZE REGIONE_C:
- Accoglie selettivamente (solo high-skill)
- Brain gain: +30% innovazione
- Tensioni culturali ma gestibili
- Economia boom da nuovi talenti

REGIONE_A DOPO 1 ANNO:
- População: 100 (da 50,000)
- Ghost cities
- Natura riprende spazio
- Alcuni pionieri tornano
- "Rebuild from zero" opportunity

SOLUZIONI EMERGENTI:
- Quota system inter-regionale
- Migrant bonds (paghi per entrare)
- Assimilazione forzata vs multicultura
- Muri vs ponti (literally)
```

### **29. PATTERNS CULTURALI E MEMETICI**

#### **29.1 Ciclo dei Memi Generazionali**
```
PATTERN: "La Spirale Generazionale"

GENERAZIONE 1: COSTRUTTORI
Contesto: Post-crisi, povertà
Meme dominante: "Lavoro Duro Paga"
- Ambizione: +60
- Risparmio: 70% reddito
- Felicità differita
- Costruiscono ricchezza base

GENERAZIONE 2: CONSOLIDATORI
Contesto: Crescita, opportunità
Meme: "Ottimizza e Scala"
- Educazione massima
- Corporate ladder
- Stabilità > rischio
- Picco ricchezza famiglia

GENERAZIONE 3: CREATIVI
Contesto: Ricchezza ereditata
Meme: "Segui la Passione"
- Arte e innovazione
- Rifiuto materialismo (parziale)
- Startup e rischio
- Alcuni successi, molti fallimenti

GENERAZIONE 4: PERDUTI
Contesto: Disuguaglianza, no opportunità
Meme: "Sistema è Rotto"
- Cinismo +80
- Rifiuto lavoro tradizionale
- Gig economy
- Vivono con genitori fino a 40

GENERAZIONE 5: RIVOLUZIONARI
Contesto: Crisi sistemica
Meme: "Burn It Down"
- Radicali politici
- Violenza normalizzata
- Reset completo
- Ciclo ricomincia...

DURATA CICLO: ~5000 giorni (13.7 anni × 5)
```

#### **29.2 Evoluzione dei Quartieri**
```
LIFECYCLE QUARTIERE TIPO:

FASE 1: TERRA DI NESSUNO
- Vuoto o industriale dismesso
- Criminalità alta
- Affitti: 10/m³
- Solo disperati

FASE 2: PIONIERI ARTISTI
- Spazi grandi economici
- Community underground
- Gallery e club illegali
- Affitti: 20-30/m³
- Polizia ignora

FASE 3: COOL DISCOVERY
- Blog: "Hidden gem!"
- Primi coffee shop hipster
- Studenti arrivano
- Affitti: 50-80/m³
- Tensione vecchi/nuovi

FASE 4: MAINSTREAM APPEAL
- Articoli mainstream media
- Ristoranti trendy
- Professionals comprano
- Affitti: 150-250/m³
- Artisti espulsi

FASE 5: CORPORATE TAKEOVER
- Starbucks in ogni angolo
- Luxury condos
- Boutique chains
- Affitti: 400-600/m³
- Zero autenticità

FASE 6: STAGNAZIONE
- Troppo caro per giovani
- Troppo noioso per ricchi
- Negozi chiudono
- Affitti: calano 20%
- Cerca nuova identità

FASE 7: DECLINO O REINVENZIONE
Path A: Diventa dormitorio
Path B: Nuovo gruppo etnico
Path C: Ritorno artisti (raro)

DURATA TOTALE: 3000-4000 giorni
```

### **30. STRATEGIE EMERGENTI DEI GIOCATORI**

#### **30.1 Meta-Strategie Economiche**
```
STRATEGIE VINCENTI OSSERVATE:

1. "PRIMO MONOPOLISTA"
- Rush tecnologico su un primo alto
- Monopolizza prima che altri arrivino
- Milk monopoly per 365 giorni
- Reinvesti in prossimo primo
- Ripeti fino a dominanza

2. "SINERGY MASTER"
- Ignora primi alti
- Focus su combinazioni efficienti
- 30, 42, 66, 70, 78
- Margini bassi, volumi altissimi
- Domina mercato mass market

3. "ARBITRAGE KING"
- Zero produzione
- Solo trading inter-regionale
- Sfrutta asimmetrie informative
- Network > tutto
- Rischio minimo, profitto stabile

4. "INTEGRATION VERTICAL"
- Controlla intera supply chain
- Dall'estrazione "1" a retail
- Elimina intermediari
- Margini totali 200%+
- Ma capital intensive

5. "DISRUPTOR SERIAL"
- Crea startup
- Distrugge incumbent
- Vende al picco
- Ripete in altro settore
- Portfolio approach
```

#### **30.2 Strategie Politico-Sociali**
```
POWER GAMES:

1. "PUPPET MASTER"
- Mai candidarsi direttamente
- Finanzia candidati multiple fazioni
- Vince sempre chiunque vinca
- Influenza da dietro
- Nessun rischio reputazione

2. "POPULIST WAVE"
- Identifica rabbia popolare
- Crea meme semplice potente
- Cavalca onda fino al potere
- Poi pivot pragmatico
- Base delusa ma ormai tardi

3. "DYNASTY BUILDER"
- Focus su famiglia e educazione
- Ogni generazione più potente
- Matrimoni strategici
- Network compounds
- Potere multi-generazionale

4. "CULTURE WARRIOR"
- Crea polarizzazione artificiale
- "Noi vs Loro" narrative
- Mobilita base emotiva
- Distrae da issues reali
- Mantiene potere nel caos

5. "TECHNOCRAT GREY"
- Competenza > Carisma
- Risolve problemi reali
- Noioso ma efficace
- Sopravvive tutti
- Potere slow but steady
```

### **31. EMERGENZE NARRATIVE UNICHE**

#### **31.1 Eventi Imprevisti Memorabili**
```
STORIE EMERGENTI DOCUMENTATE:

"IL PARADOSSO DEL SANTO AVIDO"
- Giorgio: Avidità 95, MA Intelligenza 10
- Troppo stupido per essere efficacemente avido
- Dona per errore fortune multiple
- Diventa santo per sbaglio
- Meme "Santo Giorgio" (+Generosità 30%)
- Muore povero ma amato

"LA RIVOLUZIONE DEI CLONI"
- Bug: 100 persone nascono identiche
- Stessi exact tratti
- Si riconoscono, si organizzano
- Fondano "Clone Corp"
- Perfetta coordinazione
- Dominano economia in 1000 giorni
- Società li teme e discrimina
- Clone Wars civili

"L'AMORE CHE DISTRUSSE UN'ECONOMIA"
- Figlia CEO_A ama figlio CEO_B
- Famiglie rivali (Romeo e Giulietta)
- Fuggono insieme con segreti industriali
- Fondano competitor C
- A e B si distruggono in guerra prezzi
- C domina mercato
- Sposano e uniscono tutto
- Monopolio totale via romance

"IL PRIMO CHE NON DOVEVA ESISTERE"
- Giovane scopre P₁₀₀ per errore
- (Saltando P₅₁ a P₉₉)
- Sistema va in crash logico
- Nessuno capisce come usarlo
- Valore undefined
- Economia ferma 100 giorni
- Filosofi dibattono significato
- Alla fine: Vale 0 (troppo avanzato)
```

### **32. ENDGAME SCENARIOS**

#### **32.1 Possibili Stati Finali**
```
SCENARIO 1: "UTOPIA TECNOLOGICA"
Condizioni:
- Tutti primi fino a P₁₀₀₀ scoperti
- Scarsità eliminata
- Automazione totale
- Basic income universale

Società:
- Lavoro = optional
- Focus su arte/filosofia
- Felicità media > 90
- MA: Mancanza purpose?

---

SCENARIO 2: "DYSTOPIA CORPORATIVA"
Condizioni:
- 1 azienda controlla 95%
- Governo = subsidiary
- Persone = employee-citizens
- Efficienza massima

Società:
- Zero freedom
- MA: Zero povertà
- Felicità: 50 (stabile)
- Innovazione: morta

---

SCENARIO 3: "FRAMMENTAZIONE TRIBALE"
Condizioni:
- 50+ micro-stati
- Ogni quartiere indipendente
- Guerra costante per risorse
- Technology regredisce

Società:
- Libertà massima
- Violenza massima
- Innovazione random
- Cicli costruzione/distruzione

---

SCENARIO 4: "EQUILIBRIO PERFETTO"
Condizioni:
- GINI = 0.3-0.4 stabile
- Democrazia funzionante
- Innovazione costante moderata
- Nessuna crisi major

Società:
- Noioso?
- Stabile per 10,000+ giorni
- "Fine della storia"
- MA: Pressioni esterne?

---

SCENARIO 5: "SINGOLARITÀ NUMERICA"
Condizioni:
- AI scopre pattern universale primi
- Tutti primi calcolabili istantaneamente
- Scarsità concetto obsoleto
- Economia post-numerica

Società:
- Deve reinventare tutto
- Nuovo sistema valore?
- Identità crisis totale
- Possibile transcendenza
```

### **33. METRICHE DI SUCCESSO DEL SIMULATORE**

#### **33.1 KPIs per Valutare la Simulazione**
```
CRITERI DI UNA "BUONA" SIMULAZIONE:

DIVERSITÀ NARRATIVA:
- Unique stories per run > 50
- Nessuna strategia dominante sempre
- Sorprese anche dopo 100 runs

REALISMO EMERGENTE:
- Patterns riconoscibili da storia reale
- MA: Non deterministici
- Plausibilità psicologica comportamenti

BILANCIAMENTO DINAMICO:
- Nessun equilibrio permanente
- MA: No collassi totali frequenti
- Recupero sempre possibile

PROFONDITÀ STRATEGICA:
- Multiple vie al successo
- Trade-offs meaningful
- Conseguenze long-term di scelte

EMOTIONAL ENGAGEMENT:
- Giocatori si affezionano a persone
- Rabbia per ingiustizie
- Gioia per successi
- Narrativa emergente compelling

INSIGHTS GENERATI:
- Comprensione sistemi economici
- Riflessione su valori
- "What if" scenarios
- Critica sociale emergente
```

### **34. SETUP E CONFIGURAZIONI INIZIALI**

#### **34.1 Parametri di World Generation**
```
PRESETS DISPONIBILI:

"STANDARD":
{
  popolazione: 1000,
  regioni: 5,
  primi_iniziali: [2,3,5],
  ricchezza_media: 1000,
  GINI_iniziale: 0.4,
  memi_iniziali: 3 random
}

"HARDCORE CAPITALISM":
{
  popolazione: 2000,
  GINI_iniziale: 0.7,
  tasse_base: 5%,
  welfare: disabled,
  antitrust: disabled
}

"SOCIAL DEMOCRACY":
{
  popolazione: 1000,
  GINI_iniziale: 0.2,
  tasse_base: 40%,
  welfare: strong,
  educazione: free
}

"POST-APOCALYPSE":
{
  popolazione: 100,
  primi_conosciuti: [2],
  infrastrutture: 10%,
  criminalità: 80%,
  survival_mode: true
}

"TECH SINGULARITY":
{
  popolazione: 1000,
  primi_iniziali: fino a P₅₀,
  R&D_boost: 500%,
  innovation_speed: 5x
}

"HISTORICAL":
{
  start_year: -1000,
  tech_progression: realistic,
  lifespan_iniziale: 40,
  no_democracy: 2000 giorni
}
```

#### **34.2 Condizioni di Vittoria Personalizzabili**
```
OBIETTIVI SELEZIONABILI:

ECONOMICI:
[ ] Raggiungi GDP 1,000,000
[ ] Scopri P₁₀₀
[ ] Crea monopolio duraturo
[ ] Elimina povertà (0 sotto sussistenza)

SOCIALI:
[ ] Felicità media > 80 per 1000 giorni
[ ] GINI < 0.3 per 500 giorni
[ ] Zero criminalità per 365 giorni
[ ] Aspettativa vita > 100

POLITICI:
[ ] Democrazia stabile 5000 giorni
[ ] Rivoluzione successful
[ ] Unifica tutte regioni
[ ] Crea utopia anarchica

PERSONALI:
[ ] Dinastia 10 generazioni
[ ] Storia d'amore epica
[ ] Vendetta ultimate
[ ] Legacy immortale

SANDBOX:
[ ] Nessun obiettivo
[ ] Solo osserva
[ ] Sperimenta
[ ] Crea storie
```

---

**FINE PARTE 4**

Questa parte finale mostra come tutti i sistemi interagiscono per creare:
- Storie personali complesse e toccanti
- Dinamiche aziendali realistiche
- Crisi sistemiche con effetti cascata
- Pattern culturali riconoscibili
- Strategie emergenti non ovvie
- Eventi unici memorabili
- Multiple ending possibili
- Setup configurabili per diversi stili

Il simulatore genera narrativa emergente infinita mantenendo coerenza sistemica e profondità strategica.


## **PARTE 5: ARCHITETTURA TECNICA E ALGORITMI CHIAVE**

---

### **35. ARCHITETTURA GENERALE DEL SISTEMA**

#### **35.1 Core Loop e Timing**
```
MAIN_SIMULATION_LOOP:

TICK_RATE = 1 giorno simulato / secondo reale (configurabile)

Per ogni TICK:
  1. FASE_INDIVIDUALE (40% CPU)
     - Aggiorna energia/bisogni
     - Decisioni personali
     - Movimento/interazioni
     
  2. FASE_LAVORO (25% CPU)
     - Matching lavoratori/posizioni
     - Produzione/scoperte
     - Calcolo salari/profitti
     
  3. FASE_MERCATO (20% CPU)
     - Order matching
     - Price discovery
     - Transazioni
     
  4. FASE_SOCIALE (10% CPU)
     - Propagazione memi
     - Formazione relazioni
     - Eventi random
     
  5. FASE_SISTEMA (5% CPU)
     - Metriche globali
     - Trigger eventi
     - Auto-bilanciamento

OTTIMIZZAZIONI:
- Spatial hashing per interazioni locali
- LOD (Level of Detail) per persone distanti
- Batch processing per mercati
- Cache aggressive per pathfinding
```

#### **35.2 Strutture Dati Fondamentali**
```
ENTITÀ_PRINCIPALI:

Persona = {
  id: UUID,
  tratti: Float[10] (-100 to 100),
  conoscenza_primi: Set<Int>, // quali primi conosce
  memoria: CircularBuffer<Evento>(1000),
  relazioni: Map<PersonaID, Float>,
  posizione: (x, y, z),
  energia: Float,
  bisogni: Queue<Necessità>
}

Azienda = {
  id: UUID,
  dipendenti: Tree<Persona>, // gerarchia
  conoscenza_collettiva: Set<Int>, // unione dipendenti
  cultura: Float[10], // media ponderata fondatori
  contratti: List<Contratto>,
  capitale: Double,
  inventory: Map<Numero, Quantità>
}

Edificio = {
  posizione: (x, y, z_base),
  altezza: Float,
  spazio_totale: Float,
  unità: List<SpazioAbitativo>,
  proprietario: EntityID,
  valore_mercato: Double, // ricalcolato daily
  abitanti: List<Persona>
}

Numero = {
  valore: Int,
  è_primo: Boolean,
  posizione_primo: Int?, // null se non primo
  fattorizzazione: Map<Primo, Esponente>,
  nutrizione: Float, // cached
  peso: Float, // cached
}
```

### **36. SISTEMA DEL MERCATO DEL LAVORO**

#### **36.1 Job Matching Algorithm**
```
ALGORITMO_MATCHING_LAVORO:

Ogni mattina:
  
  // LATO DOMANDA (Aziende)
  Per ogni azienda:
    calcola_necessità_competenze():
      prodotti_target = piano_produzione
      primi_necessari = unione(fattorizzazioni(prodotti))
      
      gap_conoscenza = primi_necessari - conoscenza_attuale
      
      posizioni_aperte = {
        critico: primi_mancanti ∩ primi_alto_valore,
        importante: primi_mancanti ∩ primi_medio,
        nice_to_have: primi_complementari
      }
      
    calcola_budget_assunzioni():
      max_budget = fatturato × 0.3 × (1 + espansione_planned)
      per_posizione = max_budget / n_posizioni
      aggiustamento = f(scarsità_competenza, urgenza)
  
  // LATO OFFERTA (Lavoratori)
  Per ogni persona.cerca_lavoro:
    calcola_employability():
      // Più primi alti conosci, più sei prezioso
      valore_conoscenza = Σ(posizione_primo² per primo in conoscenza)
      
      employability = valore_conoscenza × 
                     (intelligenza/100) × 
                     (1 + esperienza/10) ×
                     reputazione_professionale
      
    genera_aspettativa_salariale():
      base = media_mercato_per_competenze
      aggiustamenti = {
        ambizione: base × (1 + ambizione/200),
        necessità: SE disoccupato_lungo base × 0.7,
        alternativa: best_offer_attuale × 1.2
      }
      
  // MATCHING
  two_sided_matching():
    // Aziende rankano candidati
    Per azienda, per posizione:
      score_candidato = (
        match_competenze × 0.4 +
        costo_inverso × 0.3 +
        cultural_fit × 0.2 +
        potenziale_crescita × 0.1
      )
      
    // Candidati rankano aziende  
    Per candidato:
      score_azienda = (
        salario_offerto × 0.4 +
        prestigio × 0.2 +
        distanza_casa⁻¹ × 0.2 +
        growth_opportunity × 0.2
      )
      
    // Gale-Shapley stable matching
    stable_marriage_algorithm(aziende, candidati)
```

#### **36.2 Dinamiche Salariali e Sfruttamento**
```
NEGOZIAZIONE_SALARIO:

potere_contrattuale_lavoratore = (
  scarsità_competenze × 0.3 +
  alternative_disponibili × 0.3 +
  informazione_mercato × 0.2 +
  network_support × 0.2
) × (1 + carisma/100)

potere_contrattuale_azienda = (
  monopolio_locale × 0.4 +
  disoccupazione_zona × 0.3 +
  sostituibilità_ruolo × 0.3
) × (1 + manager.inganno/100)

salario_finale = salario_equo × (
  0.5 + 
  0.5 × (potere_lavoratore / (potere_lavoratore + potere_azienda))
)

SFRUTTAMENTO_DETECTION:
  
  sfruttamento_score = (
    (valore_prodotto - salario) / valore_prodotto
  ) × (
    ore_lavoro / ore_standard
  ) × (
    1 + stress_imposto/100
  )
  
  SE sfruttamento_score > soglia:
    lavoratore.accumula_risentimento()
    SE risentimento > 80:
      azioni = [
        sabotaggio_sottile,
        furto_piccolo,
        leak_informazioni,
        organizza_sindacato,
        quit_improvviso
      ]
      
FURTO_INTELLETTUALE:
  SE dipendente.lealtà < 30 AND opportunità_presente:
    probabilità_furto = (
      inganno_dipendente × 
      valore_segreto × 
      (1 - paura_conseguenze)
    ) / 10000
    
    SE furto_successo:
      dipendente.vende_a_competitor()
      OR dipendente.fonda_startup_competing()
```

### **37. SISTEMA DI APPRENDIMENTO E CONOSCENZA**

#### **37.1 Meccanica Studio Numeri Primi**
```
APPRENDIMENTO_PRIMI:

costo_studio(primo_n) = {
  base: posizione(primo_n)³ × 100,
  tempo: posizione(primo_n)² giorni,
  energia: 30/giorno durante studio,
  
  // Prerequisiti a cascata
  prerequisiti: tutti_primi[1 to n-1],
  
  // Modificatori
  modificatori: {
    intelligenza: costo × (100/intelligenza),
    insegnante: costo × 0.6 se tutor_esperto,
    gruppo_studio: costo × 0.8 se team > 3,
    materiali: costo × 0.7 se biblioteca_premium,
    pattern_noto: costo × 0.5 se in_sequenza_nota
  }
}

PROCESSO_APPRENDIMENTO:
  
  ogni_giorno_studio:
    progresso += (intelligenza × concentrazione × qualità_ambiente) / difficoltà
    
    // Chance breakthrough
    SE random() < inventiva/10000:
      progresso += 20%
      "Eureka moment!"
      
    // Chance dimenticanza sotto stress
    SE stress > 80:
      progresso *= 0.9
      
    SE progresso >= 100:
      aggiungi_a_conoscenza(primo)
      può_insegnare_fino_a(primo - 2)
      
KNOWLEDGE_DECAY:
  // Conoscenza non usata decade
  Per ogni primo_conosciuto:
    SE non_usato_per > 365 giorni:
      probabilità_dimenticanza = 1% / giorno
      SE dimenticato:
        riapprendimento_costa = 50% originale
```

#### **37.2 Sinergie di Team e Produttività**
```
PRODUTTIVITÀ_TEAM:

conoscenza_team_effettiva(azienda) = {
  // Non è semplice unione!
  
  base = unione(dipendenti.conoscenza_primi)
  
  // Serve copertura completa per produrre
  Per ogni prodotto_target:
    primi_necessari = fattorizzazione(prodotto)
    
    copertura = |primi_necessari ∩ conoscenza_team| / |primi_necessari|
    
    SE copertura < 1:
      produttività *= copertura
      // Non puoi produrre ciò che non conosci!
      
  // Bonus sinergia se conoscenze complementari
  overlap_matrix = Matrix[dipendenti][dipendenti]
  Per ogni coppia:
    overlap = |conoscenza_A ∩ conoscenza_B| / |conoscenza_A ∪ conoscenza_B|
    
    SE overlap ∈ [0.3, 0.7]:  // Complementari ma non ridondanti
      produttività += 10%
      
  // Penalty se troppa ridondanza
  SE overlap_medio > 0.8:
    produttività *= 0.8
    "Troppi fanno la stessa cosa"
    
  // Bonus catena completa
  SE team_copre_sequenza_completa(P₁ to Pₙ):
    produttività += 30%
    "Perfect prime ladder"
}

KNOWLEDGE_TRANSFER:
  // Mentoring interno
  Per ogni senior (conoscenza > junior + 5):
    può_insegnare = senior.conoscenza - junior.conoscenza
    
    velocità_transfer = (
      senior.generosità × 
      junior.intelligenza × 
      affinità_personale
    ) / 10000
    
    ogni_giorno_lavoro_insieme:
      probabilità = velocità_transfer
      SE successo:
        junior.apprende_random(può_insegnare)
        senior.reputazione += 10
```

### **38. ALGORITMI DI MERCATO IMMOBILIARE**

#### **38.1 Valutazione Dinamica Proprietà**
```
PROPERTY_VALUATION_ENGINE:

valore_base_m³(x, y, z, t) = {
  
  // Componenti spaziali (60% peso)
  location_value = {
    centralità: 1 / (distanza_centro + 1),
    accessibilità: Σ(1/distanza_servizi),
    
    // Job accessibility cruciale
    lavoro_score: Σ(
      per ogni azienda in range(5):
        (posti_lavoro × salario_medio) / distanza²
    ),
    
    // Scuole pesano per famiglie
    education_score: SE has_children:
      best_school_quality / distanza_scuola
  }
  
  // Componenti sociali (25% peso)
  social_value = {
    // Homophily effect
    similarità_vicini: correlation(miei_tratti, media_vicini),
    
    // Status signaling
    prestigio: percentile(ricchezza_media_zona),
    
    // Network effects
    amici_vicini: count(relazioni in range(3))
  }
  
  // Componenti temporali (15% peso)
  momentum = {
    trend_3mesi: (prezzo_oggi - prezzo_3mesi) / prezzo_3mesi,
    
    // Self-fulfilling prophecy
    SE trend > 0.2: value *= 1.1,
    SE trend < -0.2: value *= 0.9
  }
  
  return weighted_sum(components) × qualità_edificio × (1 - età/20)
}

BIDDING_MECHANISM:
  // Asta continua con reservation price
  
  seller_reservation = max(
    mutuo_residuo × 1.1,
    valore_stimato × (1 - urgenza_vendita × 0.3)
  )
  
  Per ogni buyer interessato:
    max_bid = min(
      budget_disponibile,
      valore_percepito × (1 + urgenza_acquisto × 0.5)
    )
    
    // Guerre di offerte
    SE multiple_bidders > 3:
      escalation = emotional_attachment × (1 - razionalità)
      max_bid *= (1 + escalation × 0.3)
      
  // Deal or no deal
  SE max_bid >= seller_reservation:
    transazione(prezzo = max_bid × 0.98)  // Piccolo sconto negoziazione
  ALTRIMENTI:
    ogni_settimana: seller_reservation *= 0.97
```

### **39. ENGINE POLITICO E CULTURALE**

#### **39.1 Sistema Elettorale e Propaganda**
```
ELECTION_SYSTEM:

CAMPAIGN_PHASE (30 giorni pre-elezione):
  
  Per ogni candidato:
    budget_campagna = ricchezza_personale × 0.2 + donazioni
    
    allocazione_budget = {
      propaganda_media: 40%,
      eventi_pubblici: 30%,
      vote_buying: 20% (se corrotto),
      ground_game: 10%
    }
    
    reach_giornaliero = √budget × carisma × media_coverage
    
    Per ogni elettore_raggiunto:
      messaggio_efficacia = (
        allineamento_ideologico × 0.3 +
        carisma_candidato × 0.3 +
        promesse_credibili × 0.2 +
        paura_alternative × 0.2
      ) × (1 - elettore.cinismo/100)
      
      SE efficacia > soglia:
        elettore.intenzione_voto.shift_verso(candidato)

VOTE_DECISION:
  
  Per ogni elettore:
    // Componente razionale
    utilità_attesa[candidato] = Σ(
      probabilità_promessa × impatto_personale
    )
    
    // Componente tribale
    pressione_sociale = (
      % amici_supportano × conformismo +
      % quartiere_supporta × localismo
    )
    
    // Componente emotiva
    gut_feeling = (
      carisma_candidato - 
      scandali_recenti × 20 +
      "looks_like_me" × 30
    )
    
    voto_finale = argmax(
      utilità × (intelligenza/100) +
      pressione × (100-indipendenza)/100 +
      gut_feeling × emotività/100
    )
    
    // Astensione
    SE max_score < apatia_threshold:
      non_vota()
```

#### **39.2 Propagazione Memi e Culture Wars**
```
MEME_PROPAGATION_ENGINE:

VIRAL_DYNAMICS:
  
  Per ogni meme_attivo:
    
    R₀ = transmissibilità_base × 
         novità × 
         emotional_resonance ×
         (1 + controversy_score)
         
    SE R₀ > 1:
      growth = exponential
    ALTRIMENTI:
      decay = logarithmic
      
    // Network effects
    Per ogni carrier:
      Per ogni interazione_sociale:
        
        exposure = carrier.evangelismo × 
                  contact_time × 
                  recipient.apertura
                  
        resistance = recipient.current_meme_strength × 
                    (1 + education/100) ×
                    satisfaction_status_quo
                    
        SE exposure > resistance + random_factor:
          recipient.infected(meme)
          
          // Mutation possibile
          SE random() < 0.01:
            meme.mutate(small_random_change)

CULTURE_WAR_DYNAMICS:
  
  Quando due_memi_opposti in stesso_territorio:
    
    tensione = |differenza_valori| × 
               (% popolazione_meme_A × % popolazione_meme_B)
               
    SE tensione > 50:
      polarizzazione.accelera()
      centro.scompare()
      
      azioni_emergenti = [
        boycott_businesses,
        social_ostracism,
        violent_clashes,
        segregazione_volontaria,
        political_extremism
      ]
      
    SE tensione > 80:
      possible_outcomes = [
        one_meme_wins_total,
        territory_splits,
        synthesis_new_meme,
        prolonged_conflict
      ]
```

### **40. SISTEMA DI EVENTI E NARRATIVA**

#### **40.1 Event Generator**
```
EVENT_SYSTEM:

TRIGGER_CONDITIONS:
  
  monitora_continuamente = {
    threshold_triggers: [
      (unemployment > 30%, "mass_protests"),
      (gini > 0.9, "revolution_risk"),
      (happiness < 20, "depression_epidemic"),
      (innovation == 0 for 365d, "stagnation_crisis")
    ],
    
    probabilistic_triggers: [
      (0.001/day, "technological_breakthrough"),
      (0.0001/day, "natural_disaster"),
      (0.01/day, "scandal_revealed"),
      (0.005/day, "new_meme_born")
    ],
    
    narrative_triggers: [
      (star_crossed_lovers_exist, "romeo_juliet"),
      (underdog_succeeds_wildly, "rags_to_riches"),
      (trusted_leader_corrupted, "fall_from_grace"),
      (siblings_rivalry_extreme, "cain_abel")
    ]
  }

NARRATIVE_WEAVING:
  
  // Track interesting individuals
  protagonists = people.filter(
    interestingness > 80
  )
  
  interestingness = (
    |life_trajectory_derivative| +  // Big changes
    relationship_drama_score +
    power_accumulated +
    tragedy_experienced +
    uniqueness_of_path
  )
  
  // Generate micro-stories
  Per protagonist:
    track_major_events()
    identify_antagonists()
    note_ironic_reversals()
    highlight_moral_choices()
    
  // Weave into macro-narrative
  connect_stories_where_intersect()
  identify_themes_emerging()
  generate_chronicle_entries()
```

### **41. OTTIMIZZAZIONI E PERFORMANCE**

#### **41.1 Scalabilità Computazionale**
```
PERFORMANCE_STRATEGIES:

SPATIAL_PARTITIONING:
  // Divide world in chunks
  chunks = Grid[region][district][10x10_cells]
  
  // Process only active chunks
  active = chunks.where(population > 0)
  
  // LOD based on player focus
  detail_level = {
    focus_area: FULL_SIMULATION,
    nearby: SIMPLIFIED_RULES,
    distant: STATISTICAL_ONLY
  }

AGENT_POOLING:
  // Group similar agents
  IF population > 10000:
    cluster_similar_people()
    simulate_clusters_not_individuals()
    
  similarity_threshold = 0.8
  max_cluster_size = 100

TEMPORAL_OPTIMIZATION:
  // Not everything needs daily update
  
  update_frequencies = {
    energy/movement: every_tick,
    work/production: every_tick,
    relationships: every_3_ticks,
    politics: every_7_ticks,
    culture: every_30_ticks,
    infrastructure: every_100_ticks
  }

PARALLEL_PROCESSING:
  // Embarrassingly parallel components
  
  parallel_safe = [
    individual_decisions,
    market_transactions,
    pathfinding,
    culture_propagation
  ]
  
  sequential_required = [
    global_market_clearing,
    political_elections,
    system_wide_events
  ]
```

#### **41.2 Memory Management**
```
DATA_LIFECYCLE:

HISTORY_COMPRESSION:
  // Keep full detail only recent
  
  memory_windows = {
    full_detail: last_100_days,
    daily_summary: last_1000_days,
    monthly_summary: last_10000_days,
    statistical_only: everything_else
  }
  
  // Importante events never forgotten
  permanent_memory = events.filter(
    historical_significance > threshold
  )

CACHING_STRATEGY:
  
  cache_frequently_accessed = {
    pathfinding_routes: LRU_cache(1000),
    market_prices: TTL_cache(1_day),
    relationship_scores: TTL_cache(7_days),
    building_values: TTL_cache(1_day)
  }
  
  invalidate_on_change = [
    infrastructure_updates,
    major_events,
    regime_changes
  ]
```

### **42. BILANCIAMENTO DINAMICO**

#### **42.1 Auto-Tuning Parameters**
```
ADAPTIVE_BALANCING:

monitora_health_metrics = {
  economic: [gdp_growth, gini, unemployment],
  social: [happiness, education, crime],
  political: [participation, stability, freedom],
  systemic: [population, innovation, sustainability]
}

Per ogni metric:
  IF outside_healthy_range:
    
    identify_root_causes()
    
    apply_gentle_corrections = {
      IF unemployment > 40%:
        job_creation_bonus += 10%,
        education_costs *= 0.8,
        
      IF gini > 0.85:
        progressive_tax_pressure += 5%,
        inheritance_tax += 10%,
        
      IF innovation < threshold:
        R&D_returns += 20%,
        patent_duration -= 50_days,
        
      IF population < 100:
        fertility_bonus += 30%,
        immigration_wave.trigger()
    }
    
  // Never overcorrect
  max_adjustment_per_cycle = 10%
  
  // Learn from corrections
  track_intervention_effectiveness()
  adjust_future_responses()
```

### **43. SISTEMA DI SAVE/LOAD E REPLAY**

#### **43.1 State Serialization**
```
SAVE_SYSTEM:

save_game_state = {
  version: SIMULATOR_VERSION,
  timestamp: current_tick,
  
  // Entity states
  people: compress(all_person_objects),
  companies: compress(all_company_objects),
  buildings: compress(all_building_objects),
  
  // Market state
  prices: current_price_matrix,
  contracts: active_contracts,
  
  // Political state
  officials: elected_positions,
  laws: active_legislation,
  
  // Cultural state
  memes: active_memes_and_spread,
  
  // History
  chronicles: compressed_event_log,
  statistics: historical_metrics,
  
  // Random seed for reproducibility
  rng_state: current_seed
}

SAVE_COMPRESSION:
  // Delta compression for time series
  // Clustering for similar entities
  // Prune redundant relationships
  
  typical_save_size = {
    1000_people: ~10MB,
    10000_people: ~80MB,
    100000_people: ~600MB
  }
```

### **44. INTERFACCIA E VISUALIZZAZIONE**

#### **44.1 Key Visualizations Needed**
```
ESSENTIAL_VIEWS:

MAP_VIEW:
  - Heatmaps: wealth, happiness, density
  - Flows: migration, trade, commute
  - Borders: political, cultural
  - Buildings: 3D or symbolic
  
ECONOMY_VIEW:
  - Supply chains graph
  - Price charts over time
  - Company hierarchies
  - Trade flow sankey
  
SOCIAL_VIEW:
  - Relationship networks
  - Meme spread animation
  - Class stratification
  - Life trajectory paths
  
POLITICAL_VIEW:
  - Election maps
  - Ideology compass
  - Power networks
  - Law effects
  
INDIVIDUAL_VIEW:
  - Biography timeline
  - Relationships tree
  - Career path
  - Emotional journey

DATA_DASHBOARDS:
  - Real-time KPIs
  - Historical trends
  - Predictive indicators
  - Alerts and warnings
```

### **45. CONFIGURAZIONE E MODDABILITÀ**

#### **45.1 Exposed Parameters**
```
MODDABLE_CONSTANTS:

// Tutti i parametri chiave esposti in config files

economy.json: {
  base_prime_production,
  nutrition_formulas,
  weight_calculations,
  discovery_costs,
  patent_durations,
  tax_rates
}

social.json: {
  trait_inheritance,
  relationship_formation,
  meme_spread_rates,
  education_costs,
  happiness_factors
}

political.json: {
  election_cycles,
  corruption_thresholds,
  revolution_triggers,
  law_effects
}

balancing.json: {
  auto_correction_strengths,
  crisis_thresholds,
  intervention_triggers,
  feedback_loop_dampening
}

// Mod support
mods_folder/
  ├── total_conversion/
  ├── balance_tweaks/
  ├── new_features/
  └── scenarios/
```

---

**FINE PARTE 5**

Questa parte tecnica fornisce:
- Architettura generale scalabile
- Algoritmi chiave per mercato del lavoro con conoscenze primi
- Sistema di apprendimento e team synergy
- Mercato immobiliare completamente dinamico
- Engine politico e culturale
- Ottimizzazioni per performance
- Sistemi di bilanciamento automatico

Il simulatore è ora completamente specificato con particolare attenzione a:
- **Mercato del lavoro** basato su match tra conoscenze primi dei lavoratori e necessità produttive
- **Apprendimento progressivo** dei primi più complessi
- **Team synergy** dove la combinazione di conoscenze diverse crea valore
- **Sfruttamento e furto** come dinamiche emergenti
- **Valutazione immobiliare** basata su molteplici fattori including job accessibility


## **PARTE FINALE: ESSENZIALI E SPINE DORSALI**
---

### **46. I 10 PILASTRI FONDAMENTALI (NON NEGOZIABILI)**

#### **46.1 Il Cuore Matematico**
```
ESSENZIALE #1: NUTRIZIONE = POSIZIONE, NON VALORE

nutrizione(2) = 1    (primo #1)
nutrizione(3) = 2    (primo #2)  
nutrizione(5) = 3    (primo #3)
nutrizione(7) = 4    (primo #4)

nutrizione(6) = nutrizione(2) + nutrizione(3) = 1 + 2 = 3
nutrizione(30) = nutrizione(2) + nutrizione(3) + nutrizione(5) = 1 + 2 + 3 = 6

PESO cresce quadraticamente con posizione
CONOSCENZA è prerequisita: non puoi studiare P₇ senza conoscere P₁-P₆
```

#### **46.2 Mercato del Lavoro = Match di Conoscenze**
```
ESSENZIALE #2: PRODUTTIVITÀ = INTERSEZIONE CONOSCENZE

Azienda vuole produrre 30 = 2×3×5
SERVE: almeno un dipendente che conosce 2
       + almeno uno che conosce 3  
       + almeno uno che conosce 5
(può essere la stessa persona o team)

Stipendio ∝ rarità della tua conoscenza × necessità aziendale
NON semplicemente "più alto il primo = più pagato"
```

#### **46.3 Nessun Prezzo Fisso**
```
ESSENZIALE #3: TUTTO È MERCATO EMERGENTE

MAI prezzi hardcoded per:
- Numeri/nutrizione
- Case/affitti
- Salari
- Servizi

SEMPRE: domanda ↔ offerta → prezzo
Anche le case sono spazio continuo, non "tipi" discreti
```

#### **46.4 Personalità Non È Flavour**
```
ESSENZIALE #4: I TRATTI GUIDANO TUTTO

Ogni decisione DEVE derivare dai 10 tratti:
- Generosità/Avidità → prezzi, salari, donazioni
- Inventiva/Imitazione → scoperte vs copia
- Sociale/Pragmatico → voto, politiche, scelte vita

NON sono statistiche decorative
SONO il motore decisionale
```

#### **46.5 Conoscenza Decade e Si Trasferisce**
```
ESSENZIALE #5: KNOWLEDGE MANAGEMENT

- Conoscenza NON è permanente (decay se non usata)
- Si trasferisce via mentoring (lentamente)
- Team knowledge ≠ somma individuale
- Sinergie se conoscenze complementari, non identiche
```

---

### **47. LE TRAPPOLE DA EVITARE (ERRORI COMUNI)**

#### **47.1 La Trappola della Crescita Infinita**
```
ERRORE: "Più primi scoperti = sempre meglio"
REALTÀ: Primi alti possono essere TROPPO complessi
        Peso eccessivo, costi trasporto proibitivi
        Mercato può preferire efficienza a innovazione
```

#### **47.2 La Trappola del Determinismo**
```
ERRORE: "Intelligenza alta = successo garantito"
REALTÀ: Genio povero senza network fallisce
        Stupido ricco con connessioni prospera
        Fortuna/timing spesso > capacità
```

#### **47.3 La Trappola dell'Ottimizzazione**
```
ERRORE: "Esiste strategia ottimale"
REALTÀ: Sistema deve essere anti-fragile
        Ogni strategia dominante → contro-strategia emerge
        Cicli, non equilibri
```

#### **47.4 La Trappola della Segregazione Forzata**
```
ERRORE: "Quartieri ricchi/poveri predefiniti"
REALTÀ: Segregazione EMERGE da micro-decisioni
        Homophily + prezzi → clustering naturale
        MA sempre possibilità di gentrification/decline
```

---

### **48. L'ORDINE DI IMPLEMENTAZIONE CRITICO**

```
FASE 1: CORE MINIMO FUNZIONANTE
1. Persone con 10 tratti
2. Bisogno nutrizione giornaliero
3. Produzione/consumo numeri base (1,2,3)
4. Mercato semplice domanda/offerta
5. Nascite/morti base

FASE 2: ECONOMIA PRIMI
6. Scoperta primi progressiva
7. Peso e trasporto
8. Aziende e dipendenti
9. Match conoscenze-lavoro
10. Salari emergenti

FASE 3: TERRITORIO
11. Griglia spaziale
12. Edifici come spazio continuo
13. Valore locazione emergente
14. Commuting e energia

FASE 4: SOCIETÀ
15. Relazioni e famiglie
16. Memi culturali
17. Politica base
18. Eventi narrativi

NON iniziare da grafica/UI
NON iniziare da ottimizzazioni
NON iniziare da features secondarie
```

---

### **49. IL REFERENCE SHEET DEFINITIVO**

#### **49.1 Formule Core (da non modificare)**
```python
# NUTRIZIONE
def nutrizione(n):
    if is_primo(n):
        return posizione_primo(n)
    else:
        return sum(posizione_primo(p) * exp for p, exp in fattorizza(n))

# PESO
def peso(n):
    if is_primo(n):
        return posizione_primo(n) ** 2
    else:
        return sum((posizione_primo(p) * exp) ** 2 for p, exp in fattorizza(n))

# EFFICIENZA
def efficienza(n):
    return nutrizione(n) / peso(n)

# MATCH LAVORO
def può_produrre(azienda, prodotto):
    primi_necessari = set(fattorizza(prodotto).keys())
    conoscenza_team = union(dip.conoscenza for dip in azienda.dipendenti)
    return primi_necessari.issubset(conoscenza_team)

# VALORE CASA
def valore_location(x, y, z, t):
    # MAI hardcoded, sempre funzione di:
    job_accessibility = sum(jobs_nearby / distance²)
    social_fit = correlation(my_traits, neighbors_traits)
    services = count_services_nearby()
    return weighted_sum(factors) * building_quality
```

#### **49.2 Parametri Critici di Bilanciamento**
```
POPOLAZIONE_MIN = 100       # Sotto = spawn automatico
NUTRIZIONE_MIN = 0.3        # Sotto = boost produzione
GINI_MAX = 0.85            # Sopra = instabilità sociale
DISOCCUPAZIONE_MAX = 0.30  # Sopra = crisi sistemica
MONOPOLIO_MAX = 0.80       # Sopra = antitrust automatico

CONOSCENZA_DECAY = 1% / 365 giorni non uso
KNOWLEDGE_TRANSFER = 1 primo / 30 giorni mentoring
MEME_SPREAD_R0 = 1.2 (appena virale)
ELECTION_CYCLE = 365-1095 giorni per livello
```

---

### **50. LA CHECKLIST FINALE DI VALIDAZIONE**

Prima di considerare il simulatore "funzionante", verificare:

#### **50.1 Test di Emergenza**
```
□ I prezzi fluttuano senza intervento esterno?
□ I quartieri si segregano naturalmente?
□ Emergono monopoli e poi crollano?
□ Le mode culturali nascono e muoiono?
□ Storie personali uniche ogni run?
```

#### **50.2 Test di Realismo**
```
□ Geni poveri possono fallire?
□ Stupidi ricchi possono prosperare?
□ Votare contro propri interessi succede?
□ Gentrification spontanea dei quartieri?
□ Bolle speculative e crash?
```

#### **50.3 Test di Bilanciamento**
```
□ Nessuna strategia vince sempre?
□ Sistema recupera da crisi estreme?
□ Popolazione non esplode né collassa?
□ Innovazione continua ma non troppo veloce?
□ Disuguaglianza presente ma non estrema?
```

#### **50.4 Test di Narrativa**
```
□ Ogni persona ha una storia coerente?
□ Le dinastie familiari sono tracciabili?
□ Ascese e cadute drammatiche?
□ Ironie e twist emergenti?
□ Il giocatore si affeziona ai personaggi?
```

---

### **51. IL MANTRA DELL'IMPLEMENTATORE**

> **"Niente è hardcoded, tutto emerge"**
> 
> **"I tratti guidano le decisioni, le decisioni creano patterns"**
> 
> **"La conoscenza dei primi è capitale, il capitale è potere, il potere corrompe"**
> 
> **"Ogni equilibrio è temporaneo, ogni crisi è opportunità"**
> 
> **"Il mercato del lavoro è match di conoscenze, non di titoli"**
> 
> **"Lo spazio è continuo, il valore è emergente, la segregazione è naturale"**
> 
> **"Complessità da regole semplici, storie da interazioni locali"**

---

### **52. PRIORITÀ ASSOLUTE**

Se devi tagliare features per semplicità, mantieni SEMPRE:

1. **I 10 tratti** che guidano ogni decisione
2. **Numeri primi** come unica risorsa (nutrizione = posizione)
3. **Conoscenza specifica** dei primi (non generica "educazione")
4. **Match lavoro** basato su conoscenze necessarie
5. **Prezzi emergenti** per tutto (mai fissi)
6. **Spazio continuo** per abitazioni (non tipi discreti)
7. **Decay e transfer** della conoscenza
8. **Cicli economici** automatici (boom/bust)
9. **Memi culturali** che modificano comportamenti
10. **Nessun game over** (sempre recupero possibile)

---

## **CONCLUSIONE**

Prime Society NON è:
- Un city builder con economia
- Un Sims con numeri primi
- Un simulatore economico puro

Prime Society È:
- Un **laboratorio di dinamiche sociali emergenti**
- Dove **la matematica dei primi crea scarsità naturale**
- Dove **la conoscenza è potere letterale**
- Dove **ogni regola semplice genera complessità infinita**
- Dove **le storie emergono, non sono scritte**

Il simulatore funziona quando un osservatore esterno non può distinguere se una storia emersa è stata scriptata o è davvero emergente.

Il simulatore è perfetto quando genera social commentary senza che sia stato programmato per farlo.

**Build the rules, let the stories emerge.**

---

**FINE DEL MANUALE**

Con questa spina dorsale, l'implementazione dovrebbe rimanere focalizzata sull'essenziale, evitando di perdersi in feature secondarie o meccaniche non-core. I punti controintuitivi sono evidenziati, le priorità sono chiare, e le trappole comuni sono segnalate.

# Referenza essenziale per l'implementazione

# PRIME SOCIETY - MANUALE TECNICO CONCISO

## PARTE 1: SISTEMA CORE

### 1.1 FONDAMENTO MATEMATICO
**Risorsa Base**: Il pianeta produce giornalmente POPOLAZIONE × 1 unità di "1"

**Nutrizione dei Numeri**:
- Numeri primi: nutrizione = posizione nel ranking (2→1, 3→2, 5→3, 7→4...)
- Numeri composti: nutrizione = Σ(posizione dei fattori primi)
- Esempio: 6 (2×3) → nutrizione = 1+2 = 3

**Peso**: 
- Primi: peso = posizione²
- Composti: peso = Σ(posizione × occorrenze)²

**Efficienza**: nutrizione/peso (determina convenienza economica)

### 1.2 PERSONE
**10 Assi di Personalità** (-100 a +100):
1. Generosità ↔ Avidità
2. Inventiva ↔ Imitazione  
3. Diplomazia ↔ Aggressività
4. Umiltà ↔ Ambizione
5. Sociale ↔ Pragmatico
6. Sincerità ↔ Inganno
7. Condivisione ↔ Sfruttamento
8. Riflessività ↔ Impulsività
9. Conservatore ↔ Progressista
10. Materialista ↔ Spirituale

**Attributi Derivati**:
- Intelligenza = 50 + (inventiva×0.3) + (riflessività×0.2) + random(-10,+10)
- Carisma = 50 + (diplomazia×0.3) + (felicità×0.2) + (salute×0.1)
- Conoscenza primi = lista progressiva appresa

**Ciclo Vitale**:
- 0-16: Infanzia (costa 10 risorse/giorno)
- 16-25: Formazione (50% efficienza lavoro)
- 25-55: Produttività piena
- 55-70: Esperienza (+20% decisioni)
- 70+: Anzianità (40% efficienza)

### 1.3 ECONOMIA BASE

**Scoperta Primi**:
- Costo: posizione³ × 100 risorse
- Tempo: posizione² giorni
- Requisito: intelligenza > 30 + (posizione×2)
- Prerequisiti: conoscere tutti i primi precedenti

**Produzione**:
- Input: numeri componenti
- Output: prodotto × 0.95 (entropia 5%)
- Tempo: √peso ore

**Mercato del Lavoro**:
- Aziende richiedono conoscenze specifiche per produrre
- Match: conoscenza_team ⊇ primi_necessari_prodotto
- Salario ∝ rarità_competenza × necessità_aziendale

## PARTE 2: TERRITORIO E SOCIETÀ

### 2.1 SPAZIO
**Struttura**: 5 regioni → 20 distretti → 2000 celle totali
- Ogni cella: 1000 unità cubiche edificabili (verticalmente illimitato)
- Distribuzione iniziale: 70% vuoto, 30% edifici base

**Valore Locazione** (completamente emergente):
```
valore_m³ = f(
  distanza_centro,
  posti_lavoro_vicini,
  servizi_raggiungibili,
  omogeneità_sociale_vicini,
  qualità_edificio,
  età_struttura
)
```

### 2.2 RELAZIONI
**Formazione Coppia**:
- Attrazione = |100 - Σ|differenze_tratti|/10|
- Compatibilità economica = min(ricchezza)/max(ricchezza)
- Probabilità = attrazione×0.4 + compatibilità×0.3 + prossimità×0.2

**Figli**:
- Tratti = (madre+padre)/2 + random(-20,+20)
- Costo: 10×365×18 risorse totali

### 2.3 SISTEMA POLITICO
**Gerarchia** (elezioni bottom-up):
1. Blocco (20-30 persone) → Rappresentante
2. Quartiere (200-300) → Consigliere  
3. Distretto (2000-3000) → Sindaco
4. Regione (8000-12000) → Governatore

**Voto** = razionale×(intelligenza/100) + emotivo×0.5 + sociale×(100-indipendenza)/100

### 2.4 MEMI CULTURALI
- Nascita: random con creatività_sociale
- Propagazione: R₀ = trasmissibilità × novità × risonanza_emotiva
- Effetti: modificano tratti popolazione ±20%
- Decadimento se R₀ < 1

## PARTE 3: ALGORITMI CHIAVE

### 3.1 LOOP PRINCIPALE (1 tick = 1 giorno)
1. **Fase Individuale** (40% CPU): energia, bisogni, decisioni
2. **Fase Lavoro** (25%): matching, produzione, salari
3. **Fase Mercato** (20%): prezzi, transazioni
4. **Fase Sociale** (10%): relazioni, memi
5. **Fase Sistema** (5%): metriche, eventi, bilanciamento

### 3.2 FORMULE CRITICHE

**Job Matching**:
```python
può_produrre = primi_necessari ⊆ conoscenza_team
salario = base × scarsità × (1 + esperienza/10)
```

**Price Discovery** (MAI hardcoded):
```python
prezzo = domanda/offerta × costo_produzione × (1 + margine_desiderato)
```

**Gentrification**:
```python
if quartiere.attrattività > soglia:
    prezzi += 20%/anno
    residenti_poveri.espulsi()
    carattere.perduto()
```

### 3.3 BILANCIAMENTO AUTOMATICO
- Se disoccupazione > 30%: job_creation_bonus +10%
- Se GINI > 0.85: progressive_tax +5%
- Se innovazione < soglia: R&D_returns +20%
- Se popolazione < 100: fertility_bonus +30%

## PARTE 4: CONFIGURAZIONE

### 4.1 PARAMETRI ESSENZIALI
```
POPOLAZIONE_INIZIALE = 1000
PRODUZIONE_BASE_ANNUA = POPOLAZIONE × 365
NUTRIZIONE_GIORNALIERA = 1 unità/persona
CONOSCENZA_DECAY = 1%/anno non uso
KNOWLEDGE_TRANSFER = 1 primo/30 giorni mentoring
```

### 4.2 CONDIZIONI VITTORIA (customizzabili)
- Economiche: GDP target, scoperta P₁₀₀, monopolio
- Sociali: felicità > 80, GINI < 0.3, zero criminalità
- Politiche: democrazia stabile, rivoluzione, unificazione
- Personali: dinastia 10 generazioni, legacy immortale

## IMPLEMENTAZIONE PRIORITARIA

**Fase 1 - Core Minimo**:
1. Persone con 10 tratti
2. Produzione/consumo base (1,2,3)
3. Mercato domanda/offerta
4. Nascite/morti

**Fase 2 - Economia Primi**:
5. Scoperta progressiva
6. Peso e trasporto
7. Aziende e match conoscenze
8. Salari emergenti

**Fase 3 - Territorio**:
9. Griglia spaziale
10. Valore emergente
11. Commuting

**Fase 4 - Società**:
12. Relazioni/famiglie
13. Memi culturali
14. Politica base
15. Eventi narrativi

## PRINCIPI INVIOLABILI

1. **Niente hardcoded**: tutti i prezzi emergono
2. **Tratti guidano tutto**: ogni decisione deriva dai 10 assi
3. **Conoscenza specifica**: non generica "educazione"
4. **Match lavoro preciso**: serve conoscenza esatta dei primi
5. **Spazio continuo**: non "tipi" di case predefiniti
6. **Knowledge decay**: si dimentica se non usata
7. **Nessun game over**: sempre recupero possibile

---

*Build the rules, let the stories emerge.*