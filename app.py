import streamlit as st
import pandas as pd
from datetime import datetime
import re

st.set_page_config(page_title="Lecca-Lecca Smart Lab", layout="wide")

# --- DATABASE RICETTE AGGIORNATO ---
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
input_testo = st.text_area("Scrivi o detta (es: 'Terminato stracciatella, Galak mancano 2kg, limone')", height=120)

if st.button("🚀 ELABORA TUTTO L'ORDINE"):
    # Divide il testo in pezzi basandosi su virgole, punti o a capo
    pezzi = re.split(r'[,.\n]', input_testo.upper())
    aggiunti = 0
    
    for pezzo in pezzi:
        pezzo = pezzo.strip()
        if not pezzo: continue
        
        for gusto_nome in RICETTE.keys():
            if gusto_nome in pezzo:
                # CERCA I KG SOLO IN QUESTO PEZZO DI FRASE
                kg_match = re.search(r'(\d+)', pezzo)
                
                # Se trova un numero in QUESTO pezzo usa quello, altrimenti TORNA A 7
                if kg_match:
                    kg_da_usare = float(kg_match.group(1))
                else:
                    kg_da_usare = 7.0
                
                st.session_state.produzione.append({
                    "gusto": gusto_nome, 
                    "kg": kg_da_usare, 
                    "seq": RICETTE[gusto_nome]['seq']
                })
                aggiunti += 1
                break # Trovato il gusto, passa al pezzo successivo
                
    if aggiunti > 0:
        st.success(f"Caricati {aggiunti} gusti con quantità specifiche!")
    else:
        st.warning("Non ho riconosciuto gusti. Controlla i nomi.")

# --- 2. GENERAZIONE DOCUMENTO UNICO ---
if st.session_state.produzione:
    st.divider()
    df_p = pd.DataFrame(st.session_state.produzione).sort_values(by="seq")
    lotto_s = datetime.now().strftime("%Y%m%d")

    # COSTRUZIONE TESTO SENZA CARATTERI SPECIALI (EVITA ERRORI STAMPA)
    # 1. CARTA GELATIERE
    txt = "1. CARTA DEL GELATIERE\n" + "="*30 + "\n"
    u_s = None
    for _, r in df_p.iterrows():
        # Risciacquo tra sequenze [cite: 2026-02-11]
        if u_s is not None and r['seq'] != u_s:
            txt += "\nRISCIACQUO MACCHINA\n" + "-"*30 + "\n"
            txt += "risciacquo\n" + "-"*30 + "\n"
        
        txt += f"\nGUSTO: {r['gusto']} ({r['kg']} KG)\n"
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
        txt += f"[ ] {r['gusto']} - {r['kg']} KG\n"
    txt += "\n\nFirma Franco Antonio: ________________\n"
    txt += "Firma Quagliozzi Giuseppe: ______________\n"

    st.download_button("🖨️ SCARICA DOCUMENTO UNICO", txt, f"Prod_{lotto_s}.txt", use_container_width=True)

    # Anteprima elenco
    st.subheader("📋 Riepilogo Caricato:")
    for p in st.session_state.produzione:
        st.write(f"🔹 {p['gusto']}: **{p['kg']} KG**")
    
    if st.button("🗑️ Svuota Tutto"):
        st.session_state.produzione = []; st.rerun()
