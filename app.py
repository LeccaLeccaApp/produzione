import streamlit as st
import pandas as pd
from datetime import datetime
import re

st.set_page_config(page_title="Lecca-Lecca Smart Lab", layout="wide")

# --- DATABASE RICETTE (Unificato e Integrale) ---
RICETTE = {
    # --- GRUPPO 1: VEGANI / SPECIALI (Sequenza 1) ---
    "PISTACCHIO VEGANO": {"ing": [("Acqua", 625), ("Bianco Stevia", 312), ("Pasta Pistacchio", 100), ("Destrosio", 25)], "seq": 1, "kcal": 195, "all": "FRUTTA A GUSCIO"},
    "SICILY VEGANO": {"ing": [("Acqua", 625), ("Bianco Stevia", 312), ("Pasta Mandorla", 75)], "seq": 1, "kcal": 192, "all": "FRUTTA A GUSCIO"},
    "NOCCIOLA VEGANO": {"ing": [("Acqua", 625), ("Bianco Stevia", 312), ("Pasta Nocciola", 130)], "seq": 1, "kcal": 180, "all": "FRUTTA A GUSCIO"},
    "CIOCCOLATO FONDENTE": {"ing": [("Acqua", 600), ("Fondente Babbi", 450), ("Destrosio", 20)], "seq": 1, "kcal": 176, "all": "SOIA"},
    "BUENO VEGANO": {"ing": [("Acqua", 625), ("Pasta Bueno Veg", 120)], "seq": 1, "kcal": 225, "all": "FRUTTA A GUSCIO"},

    # --- GRUPPO 2: CREME (Sequenza 2) ---
    "AMARENA": {"ing": [("Base bianca", 1000), ("Variegato amarena", 100)], "seq": 2, "kcal": 232, "all": "LATTE"},
    "STRACCIATELLA": {"ing": [("Base bianca", 1000), ("Cioccolato scaglie", 80)], "seq": 2, "kcal": 250, "all": "LATTE, SOIA"},
    "FIOR DI LATTE": {"ing": [("Base bianca", 1000)], "seq": 2, "kcal": 226, "all": "LATTE"},
    "SMARTIES": {"ing": [("Base bianca", 1000), ("Smarties", 100)], "seq": 2, "kcal": 238, "all": "LATTE"},
    "KINDER CEREALI": {"ing": [("Base bianca", 1000), ("Crema Kinder Cereali", 100)], "seq": 2, "kcal": 289, "all": "LATTE, GLUTINE"},
    "KINDER BARRETTA": {"ing": [("Base bianca", 1000), ("Pasta Nocciole/Cacao", 100)], "seq": 2, "kcal": 270, "all": "LATTE, FRUTTA A GUSCIO"},
    "SPAGNOLA": {"ing": [("Base bianca", 1000), ("Variegato amarena", 100)], "seq": 2, "kcal": 245, "all": "LATTE"},
    "CROCCANTE AMARENA": {"ing": [("Base bianca", 1000), ("Variegato amarena", 80), ("Granella", 50)], "seq": 2, "kcal": 296, "all": "LATTE, FRUTTA A GUSCIO"},
    "COSTIERA": {"ing": [("Base bianca", 1000), ("Biscotto sbriciolato", 100)], "seq": 2, "kcal": 246, "all": "LATTE, GLUTINE"},
    "NOCCIOLA": {"ing": [("Base bianca", 900), ("Pasta Nocciola", 130), ("Destrosio", 25)], "seq": 2, "kcal": 286, "all": "LATTE, FRUTTA A GUSCIO"},
    "PISTACCHIO": {"ing": [("Base bianca", 900), ("Pasta Pistacchio", 100), ("Destrosio", 20)], "seq": 2, "kcal": 275, "all": "LATTE, FRUTTA A GUSCIO"},
    "BACIO": {"ing": [("Base bianca", 900), ("Pasta Sorriso", 100)], "seq": 2, "kcal": 276, "all": "LATTE, FRUTTA A GUSCIO"},
    "CIOCCOLATO AL LATTE": {"ing": [("Base bianca", 900), ("Cacao", 100), ("Destrosio", 50)], "seq": 2, "kcal": 254, "all": "LATTE"},
    "DUBAI": {"ing": [("Base bianca", 900), ("Pistacchi", 100), ("Kataifi", 50)], "seq": 2, "kcal": 295, "all": "LATTE, GLUTINE, FRUTTA A GUSCIO"},
    "GALAK": {"ing": [("Base Bianca", 825), ("Pasta Galak", 100)], "seq": 2, "kcal": 260, "all": "LATTE"},

    # --- GRUPPO 3: FRUTTA (Sequenza 3) ---
    "FRAGOLA": {"ing": [("Acqua", 300), ("Polpa Fragola", 375), ("Base Bianca", 200)], "seq": 3, "kcal": 121, "all": "NESSUNO"},
    "LIMONE": {"ing": [("Acqua", 700), ("Lemon Plus", 300)], "seq": 3, "kcal": 119, "all": "NESSUNO"},
    "PESCA": {"ing": [("Acqua", 700), ("Frutta Pesca", 300)], "seq": 3, "kcal": 122, "all": "NESSUNO"},
    "ANGURIA": {"ing": [("Acqua", 700), ("Anguria", 300)], "seq": 3, "kcal": 118, "all": "NESSUNO"},
    "MELONE": {"ing": [("Acqua", 700), ("Melone", 300)], "seq": 3, "kcal": 125, "all": "NESSUNO"},

    # --- GRUPPO 4: ALTRO (Sequenza 4) ---
    "LIQUIRIZIA": {"ing": [("Base bianca", 900), ("Pasta liquirizia", 50)], "seq": 4, "kcal": 228, "all": "LATTE"},
}

if 'produzione' not in st.session_state: st.session_state.produzione = []

st.title("🍦 Smart Lab Lecca-Lecca")

# --- 1. INSERIMENTO VOCALE / TESTO ---
st.subheader("🎤 Dettatura Ordine")
input_testo = st.text_area("Dì i gusti (es: 'Smarties, non idoneo Kinder Cereali, Nocciola 2kg')", height=120)

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
                kg_val = float(kg_m.group(1)) if kg_m else 7.0
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

    # 1. CARTA GELATIERE
    txt = "1. CARTA DEL GELATIERE\n" + "="*30 + "\n"
    u_s = None
    for _, r in df_p.iterrows():
        # Risciacquo [cite: 2026-02-11]
        if u_s is not None and r['seq'] != u_s:
            txt += "\nRISCIACQUO MACCHINA\n" + "-"*30 + "\nrisciacquo\n" + "-"*30 + "\n"
        
        txt += f"\nGUSTO: {r['gusto']}{r['nota']} ({r['kg']} KG)\n"
        # Calcolo proporzionale basato su 7kg (come nel codice buono)
        for i_n, d_o in RICETTE[r['gusto']]['ing']:
            p_e = int(d_o * (r['kg']/7.0))
            txt += f"- {i_n}: {p_e}g\n"
        u_s = r['seq']

    # 2. ETICHETTE
    txt += "\n\n2. ETICHETTE NUTRIZIONALI\n" + "="*30 + "\n"
    for _, r in df_p.iterrows():
        txt += f"\nPRODOTTO: {r['gusto']}{r['nota']}\nALLERGENI: {RICETTE[r['gusto']]['all']}\nLotto: {lotto_s}\nCalorie: {RICETTE[r['gusto']]['kcal']} kcal/100g\n"
        txt += "."*25 + "\n"

    # 3. RIEPILOGO E FIRME
    txt += "\n\n3. RIEPILOGO GIORNALIERO\n" + "="*30 + "\n"
    txt += f"Data: {datetime.now().strftime('%d/%m/%Y')} | Lotto: {lotto_s}\n\n"
    for _, r in df_p.iterrows():
        txt += f"[ ] {r['gusto']}{r['nota']} - {r['kg']} KG\n"
    txt += "\n\nFirma Franco Antonio: ________________\nFirma Quagliozzi Giuseppe: ______________\n"

    st.download_button("🖨️ SCARICA DOCUMENTO UNICO", txt, f"Prod_{lotto_s}.txt", use_container_width=True)

    st.subheader("📋 Gusti in lista:")
    for p in st.session_state.produzione:
        nota_video = f" **{p['nota']}**" if p['nota'] else ""
        st.write(f"🔹 {p['gusto']}{nota_video}: **{p['kg']} KG**")
    
    if st.button("🗑️ Svuota Tutto"):
        st.session_state.produzione = []; st.rerun()
