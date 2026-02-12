import streamlit as st
import pandas as pd
from datetime import datetime
import re

st.set_page_config(page_title="Lecca-Lecca Smart Lab", layout="wide")

# --- DATABASE RICETTE INTEGRALE (Base originale + Integrazioni PDF) ---
RICETTE = {
    # --- GOLOSITÀ & NUOVI ---
    "AMARENA": {"ing": [("Base bianca", 1000), ("Variegato amarena", 100)], "seq": 2, "kcal": 232, "all": "LATTE", "nutri": "G: 11.6g | C: 28.2g | P: 2.8g"},
    "STRACCIATELLA": {"ing": [("Base bianca", 1000), ("Cioccolato scaglie", 80)], "seq": 2, "kcal": 250, "all": "LATTE, SOIA", "nutri": "G: 15.4g | C: 23.3g | P: 3.3g"},
    "FIOR DI LATTE": {"ing": [("Base bianca", 1000)], "seq": 2, "kcal": 226.6, "all": "LATTE", "nutri": "G: 13.1g | C: 22.9g | P: 3.2g"},
    "SMARTIES": {"ing": [("Base bianca", 1000), ("Confetti cioccolato", 100)], "seq": 2, "kcal": 238.1, "all": "LATTE", "nutri": "G: 13.3g | C: 25.3g | P: 3.2g"},
    "KINDER CEREALI": {"ing": [("Base bianca", 1000), ("Crema Kinder Cereali", 100)], "seq": 2, "kcal": 289.8, "all": "LATTE, GLUTINE", "nutri": "G: 18.1g | C: 27.3g | P: 3.4g"},
    "KINDER BARRETTA": {"ing": [("Base bianca", 1000), ("Pasta Nocciola/Cacao", 100)], "seq": 2, "kcal": 270.8, "all": "LATTE, FRUTTA A GUSCIO", "nutri": "G: 16.2g | C: 26.9g | P: 3.4g"},
    "ZUPPA INGLESE": {"ing": [("Base bianca", 1000), ("Bagna Alchermes", 100), ("Pan di Spagna", 50)], "seq": 2, "kcal": 243.2, "all": "LATTE, UOVA, GLUTINE", "nutri": "G: 15.7g | C: 20.2g | P: 2.9g"},
    "DUBAI": {"ing": [("Base bianca", 900), ("Pasta Pistacchio", 100), ("Kataifi", 50)], "seq": 2, "kcal": 295, "all": "LATTE, GLUTINE, FRUTTA A GUSCIO", "nutri": "G: 18.8g | C: 26.5g | P: 4.2g"},
    "NUTELLA": {"ing": [("Crema da banco", 1000)], "seq": 2, "kcal": 562, "all": "LATTE, FRUTTA A GUSCIO, SOIA", "nutri": "G: 36g | C: 53g | P: 5g"},
    "SNICKERS": {"ing": [("Base bianca", 900), ("Pasta Arachidi", 100), ("Arachidi tostate", 50)], "seq": 2, "kcal": 303.6, "all": "LATTE, ARACHIDI, SOIA", "nutri": "G: 19.5g | C: 25.1g | P: 5.5g"},
    "LOTUS": {"ing": [("Base bianca", 900), ("Pasta Speculoos", 100), ("Biscotto Lotus", 50)], "seq": 2, "kcal": 316, "all": "LATTE, GLUTINE, SOIA", "nutri": "G: 19.9g | C: 30g | P: 3.3g"},
    
    # --- CLASSICI ---
    "NOCCIOLA": {"ing": [("Base bianca", 900), ("Pasta Nocciola", 130), ("Destrosio", 25)], "seq": 2, "kcal": 286.2, "all": "LATTE, FRUTTA A GUSCIO", "nutri": "G: 19.0g | C: 22.8g | P: 4.6g"},
    "PISTACCHIO": {"ing": [("Base bianca", 900), ("Pasta Pistacchio", 100), ("Destrosio", 20)], "seq": 2, "kcal": 275.9, "all": "LATTE, FRUTTA A GUSCIO", "nutri": "G: 17.4g | C: 23.0g | P: 5.5g"},
    "BACIO": {"ing": [("Base bianca", 900), ("Pasta Sorriso Amaro", 100)], "seq": 2, "kcal": 276.5, "all": "LATTE, FRUTTA A GUSCIO", "nutri": "G: 17.9g | C: 23.0g | P: 4.3g"},
    "CAFFÈ": {"ing": [("Base bianca", 900), ("Caffè Arabica", 25)], "seq": 2, "kcal": 228, "all": "LATTE", "nutri": "G: 12.4g | C: 24.8g | P: 3.1g"},
    "TIRAMISÙ": {"ing": [("Base bianca", 900), ("Pasta Tiramisù Special", 50)], "seq": 2, "kcal": 235, "all": "LATTE, UOVA", "nutri": "G: 12.9g | C: 25.1g | P: 3.4g"},
    
    # --- FRUTTA & SORBETTI ---
    "FRAGOLA": {"ing": [("Acqua", 300), ("Polpa Fragola", 375), ("Base Bianca", 200), ("Destrosio", 40), ("Saccarosio", 75)], "seq": 3, "kcal": 121.3, "all": "Può contenere LATTE", "nutri": "G: 2.4g | C: 23.8g"},
    "LIMONE": {"ing": [("Acqua", 700), ("Lemon Plus", 300)], "seq": 3, "kcal": 119, "all": "Nessuno", "nutri": "C: 27.0g"},
    "PESCA": {"ing": [("Acqua", 700), ("Frutta Pesca", 300)], "seq": 3, "kcal": 122, "all": "Nessuno", "nutri": "C: 26.7g"},
    
    # --- VEGANI ---
    "PISTACCHIO VEGANO": {"ing": [("Acqua", 625), ("Bianco Stevia", 312), ("Pasta Pistacchio", 100), ("Destrosio", 25)], "seq": 1, "kcal": 195, "all": "FRUTTA A GUSCIO", "nutri": "G: 11.0g | C: 22.9g"},
    "SICILY VEGANO": {"ing": [("Acqua", 625), ("Bianco Stevia", 312), ("Pasta Mandorla", 75)], "seq": 1, "kcal": 192, "all": "FRUTTA A GUSCIO", "nutri": "G: 10.7g | C: 25.3g"},
    "CIOCCOLATO FONDENTE": {"ing": [("Acqua", 600), ("Fondente Babbi", 450), ("Destrosio", 20)], "seq": 1, "kcal": 176.1, "all": "SOIA, Può contenere LATTE", "nutri": "G: 4.1g | C: 29.2g"},
}

if 'produzione' not in st.session_state: st.session_state.produzione = []

st.title("🍦 Smart Lab Lecca-Lecca - Database Unificato")

# --- 1. INSERIMENTO VOCALE / TESTO ---
st.subheader("🎤 Dettatura Ordine")
input_testo = st.text_area("Dì: 'Terminato Smarties, non idoneo Kinder Cereali, Nocciola 2'", height=120)

if st.button("🚀 ELABORA TUTTO L'ORDINE"):
    fasi = re.split(r'[,.\n]', input_testo.upper())
    aggiunti = 0
    for f in fasi:
        f = f.strip()
        if not f: continue
        for g_nome in RICETTE.keys():
            if g_nome in f:
                nota_stato = " (NON IDONEO)" if "IDONEO" in f else ""
                kg_m = re.search(r'(\d+)', f)
                peso_tot_base = sum(val for nome, val in RICETTE[g_nome]['ing'])
                kg_val = float(kg_m.group(1)) if kg_m else (7.0 if peso_tot_base > 2000 else 1.0)
                st.session_state.produzione.append({
                    "gusto": g_nome, "kg": kg_val, "seq": RICETTE[g_nome]['seq'], "nota": nota_stato
                })
                aggiunti += 1
                break
    if aggiunti > 0: st.success(f"Caricati {aggiunti} gusti!")

# --- 2. GENERAZIONE DOCUMENTO UNICO ---
if st.session_state.produzione:
    st.divider()
    df_p = pd.DataFrame(st.session_state.produzione).sort_values(by="seq")
    lotto_s = datetime.now().strftime("%Y%m%d")

    txt = "1. CARTA DEL GELATIERE\n" + "="*30 + "\n"
    u_s = None
    for _, r in df_p.iterrows():
        # Risciacquo [cite: 2026-02-11]
        if u_s is not None and r['seq'] != u_s:
            txt += "\nRISCIACQUO MACCHINA\n" + "-"*30 + "\nrisciacquo\n" + "-"*30 + "\n"
        
        peso_ricetta_base = sum(val for nome, val in RICETTE[r['gusto']]['ing'])
        label_quantita = "KG" if peso_ricetta_base > 2000 else "DOSI"
        txt += f"\nGUSTO: {r['gusto']}{r['nota']} ({r['kg']} {label_quantita})\n"
        
        fattore = r['kg'] / (7.0 if label_quantita == "KG" else 1.0)
        for i_n, d_o in RICETTE[r['gusto']]['ing']:
            p_e = int(d_o * fattore)
            txt += f"- {i_n}: {p_e}g\n"
        u_s = r['seq']

    txt += "\n\n2. ETICHETTE, ALLERGENI & NUTRIZIONE\n" + "="*30 + "\n"
    for _, r in df_p.iterrows():
        g = RICETTE[r['gusto']]
        txt += f"\nPRODOTTO: {r['gusto']}{r['nota']}\n"
        txt += f"ALLERGENI: {g.get('all', 'Vedere ingredienti')}\n"
        txt += f"VALORI x 100g: {g['kcal']} kcal | {g.get('nutri', '')}\n"
        txt += f"Lotto: {lotto_s}\n"
        txt += "."*25 + "\n"

    txt += "\n\n3. RIEPILOGO GIORNALIERO\n" + "="*30 + "\n"
    txt += f"Data: {datetime.now().strftime('%d/%m/%Y')} | Lotto: {lotto_s}\n\n"
    for _, r in df_p.iterrows():
        txt += f"[ ] {r['gusto']}{r['nota']} - {r['kg']} unità\n"
    txt += "\n\nFirma Franco Antonio: ________________\nFirma Quagliozzi Giuseppe: ______________\n"

    st.download_button("🖨️ SCARICA DOCUMENTO UNICO", txt, f"Prod_{lotto_s}.txt", use_container_width=True)

    if st.button("🗑️ Svuota Tutto"):
        st.session_state.produzione = []; st.rerun()
