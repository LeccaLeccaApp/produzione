import streamlit as st
import pandas as pd
from datetime import datetime
import re

st.set_page_config(page_title="Lecca-Lecca Smart Lab", layout="wide")

# --- DATABASE RICETTE (Numeri puliti senza zeri iniziali) ---
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
input_testo = st.text_area("Scrivi o detta tutto (es: 'Terminato nocciola, fragola 4kg')", height=100)

if st.button("🚀 ELABORA TUTTO L'ORDINE"):
    # Pulizia testo: toglie punti e divide per virgola
    fasi = input_testo.upper().replace('.', ',').split(',')
    aggiunti = 0
    for frase in fasi:
        for gusto in RICETTE.keys():
            if gusto in frase:
                # Cerca il numero dei KG
                kg_m = re.search(r'(\d+)', frase)
                kg = float(kg_m.group(1)) if kg_m else 7.0
                st.session_state.produzione.append({"gusto": gusto, "kg": kg, "seq": RICETTE[gusto]['seq']})
                aggiunti += 1
    if aggiunti > 0:
        st.success(f"Caricati {aggiunti} gusti!")
    else:
        st.warning("Non ho trovato gusti conosciuti nel testo.")

# --- 2. FOTOCAMERA (LATERALE) ---
with st.sidebar:
    st.header("📸 Foto Fatture")
    st.camera_input("Scatta e salva")

# --- 3. GENERAZIONE DOCUMENTO UNICO ---
if st.session_state.produzione:
    st.divider()
    
    # Ordiniamo per sequenza per gestire i risciacqui
    df_p = pd.DataFrame(st.session_state.produzione).sort_values(by="seq")
    data_s = datetime.now().strftime("%d/%m/%Y")
    lotto_s = datetime.now().strftime("%Y%m%d")

    # COSTRUZIONE DEL TESTO UNICO
    # 1. CARTA GELATIERE
    testo_finale = "--- 1. CARTA DEL GELATIERE ---\n" + "="*35 + "\n"
    u_s = None
    for _, r in df_p.iterrows():
        # Inserimento risciacquo tra sequenze diverse [cite: 2026-02-11]
        if u_s is not None and r['seq'] != u_s:
            testo_finale += "\n🚿 RISCIACQUO MACCHINA\n" + "-"*35 + "\n"
            testo_finale += "risciacquo\n" + "-"*35 + "\n"
        
        testo_finale += f"\n🍦 GUSTO: {r['gusto']} ({r['kg']} KG)\n"
        for i_n, d_o in RICETTE[r['gusto']]['ing']:
            p_e = int(d_o * (r['kg']/7.0))
            testo_finale += f"  - {i_n}: {p_e}g\n"
        u_s = r['seq']

    # 2. ETICHETTE
    testo_finale += "\n\n" + "--- 2. ETICHETTE NUTRIZIONALI ---\n" + "="*35 + "\n"
    for _, r in df_p.iterrows():
        testo_finale += f"\n🏷️ PRODOTTO: {r['gusto']}\nLotto: {lotto_s}\nCalorie: {RICETTE[r['gusto']]['kcal']} kcal/100g\n"
        testo_finale += "."*25 + "\n"

    # 3. RIEPILOGO GIORNALIERO E FIRME
    testo_finale += "\n\n" + "--- 3. RIEPILOGO GIORNALIERO ---\n" + "="*35 + "\n"
    testo_finale += f"Data: {data_s} | Lotto: {lotto_s}\n\n"
    for _, r in df_p.iterrows():
        testo_finale += f"[ ] {r['gusto']} - {r['kg']} KG\n"
    testo_finale += "\n\nFirma Responsabile 1: Franco Antonio ________________\n"
    testo_finale += "Firma Responsabile 2: Quagliozzi Giuseppe ______________\n"

    st.download_button(
        label="🖨️ SCARICA DOCUMENTO PER STAMPA UNICA",
        data=testo_finale,
        file_name=f"Produzione_{lotto_s}.txt",
        mime="text/plain",
        use_container_width=True
    )

    # Anteprima a video
    st.subheader("📋 Gusti in lista:")
    for p in st.session_state.produzione:
        st.write(f"- {p['gusto']} ({p['kg']} KG)")
    
    if st.button("🗑️ Svuota tutto"):
        st.session_state.produzione = []
        st.rerun()
