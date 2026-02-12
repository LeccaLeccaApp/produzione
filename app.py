import streamlit as st
import pandas as pd
from datetime import datetime
import re

st.set_page_config(page_title="Lecca-Lecca Smart Lab", layout="wide")

# --- DATABASE RICETTE ---
RICETTE = {
    "NOCCIOLA VEGANO": {"ing": [("Acqua", 4375), ("Pasta Nocciola", 910), ("Zuccheri", 2450)], "seq": 1, "kcal": 210},
    "BUENO VEGANO": {"ing": [("Acqua", 625), ("Pasta Bueno Veg", 120)], "seq": 1, "kcal": 225},
    "STRACCIATELLA": {"ing": [("Base Lecca lecca", 7000), ("Cioccolato scaglie", 560)], "seq": 2, "kcal": 240},
    "GALAK": {"ing": [("Base Bianca", 825), ("Pasta Galak", 100)], "seq": 2, "kcal": 260},
    "FRAGOLA": {"ing": [("Acqua", 2100), ("Polpa Fragola", 2625), ("Base", 1400)], "seq": 3, "kcal": 150},
    "LIMONE": {"ing": [("Acqua", 700), ("Succo Limone", 300)], "seq": 3, "kcal": 130},
    "LIQUIRIZIA": {"ing": [("Acqua", 5000), ("Liquirizia", 500)], "seq": 4, "kcal": 180},
}

if 'produzione' not in st.session_state: st.session_state.produzione = []

st.title("🍦 Smart Lab Lecca-Lecca")

# --- 1. INSERIMENTO VOCALE / TESTO ---
st.subheader("🎤 Dettatura Ordine")
input_testo = st.text_area("Dì: 'Terminato nocciola, Galak mancano 2kg, non più idoneo limone'", height=120)

if st.button("🚀 ELABORA TUTTO L'ORDINE"):
    fasi = re.split(r'[,.\n]', input_testo.upper())
    aggiunti = 0
    
    for f in fasi:
        f = f.strip()
        if not f: continue
        
        for g_nome in RICETTE.keys():
            if g_nome in f:
                # Controlla se è stato detto "NON IDONEO"
                stato_idoneo = "**(NON IDONEO)**" if "IDONEO" in f else ""
                
                # Cerca i KG
                kg_m = re.search(r'(\d+)', f)
                kg_ok = float(kg_m.group(1)) if kg_m else 7.0
                
                st.session_state.produzione.append({
                    "gusto": g_nome, 
                    "kg": kg_ok, 
                    "seq": RICETTE[g_nome]['seq'],
                    "nota": stato_idoneo
                })
                aggiunti += 1
                break
                
    if aggiunti > 0:
        st.success(f"Caricati {aggiunti} gusti!")

# --- 2. GENERAZIONE DOCUMENTO UNICO ---
if st.session_state.produzione:
    st.divider()
    df_p = pd.DataFrame(st.session_state.produzione).sort_values(by="seq")
    lotto_s = datetime.now().strftime("%Y%m%d")

    # COSTRUZIONE TESTO
    # 1. CARTA GELATIERE
    txt = "1. CARTA DEL GELATIERE\n" + "="*30 + "\n"
    u_s = None
    for _, r in df_p.iterrows():
        # Risciacquo [cite: 2026-02-11]
        if u_s is not None and r['seq'] != u_s:
            txt += "\nRISCIACQUO MACCHINA\n" + "-"*30 + "\nrisciacquo\n" + "-"*30 + "\n"
        
        # Aggiunge (NON IDONEO) se presente (senza asterischi nel TXT per pulizia)
        nota_txt = r['nota'].replace('*', '') 
        txt += f"\nGUSTO: {r['gusto']} {nota_txt} ({r['kg']} KG)\n"
        for i_n, d_o in RICETTE[r['gusto']]['ing']:
            p_e = int(d_o * (r['kg']/7.0))
            txt += f"- {i_n}: {p_e}g\n"
        u_s = r['seq']

    # 2. ETICHETTE
    txt += "\n\n2. ETICHETTE NUTRIZIONALI\n" + "="*30 + "\n"
    for _, r in df_p.iterrows():
        txt += f"\nPRODOTTO: {r['gusto']}\nLotto: {lotto_s}\nCalorie: {RICETTE[r['gusto']]['kcal']} kcal/100g\n"
        txt += "."*25 + "\n"

    # 3. RIEPILOGO E FIRME
    txt += "\n\n3. RIEPILOGO GIORNALIERO\n" + "="*30 + "\n"
    txt += f"Data: {datetime.now().strftime('%d/%m/%Y')} | Lotto: {lotto_s}\n\n"
    for _, r in df_p.iterrows():
        nota_txt = r['nota'].replace('*', '')
        txt += f"[ ] {r['gusto']} {nota_txt} - {r['kg']} KG\n"
    txt += "\n\nFirma Franco Antonio: ________________\nFirma Quagliozzi Giuseppe: ______________\n"

    st.download_button("🖨️ SCARICA DOCUMENTO UNICO", txt, f"Prod_{lotto_s}.txt", use_container_width=True)

    # Anteprima elenco con grassetto
    st.subheader("📋 Riepilogo Caricato:")
    for p in st.session_state.produzione:
        st.write(f"🔹 {p['gusto']} {p['nota']}: **{p['kg']} KG**")
    
    if st.button("🗑️ Svuota Tutto"):
        st.session_state.produzione = []; st.rerun()
