import streamlit as st
import pandas as pd

st.set_page_config(page_title="Lecca-Lecca Lab", layout="wide")

# Database con calorie per etichette
RICETTE = {
    "NOCCIOLA VEGANO": {"ing": [("Acqua", 625), ("Pasta Nocciola", 130), ("Zuccheri", 350)], "seq": 1, "kcal": 210},
    "BUENO VEGANO": {"ing": [("Acqua", 625), ("Pasta Bueno Veg", 120)], "seq": 1, "kcal": 225},
    "STRACCIATELLA": {"ing": [("Base Latte", 1000), ("Cioccolato", 80)], "seq": 2, "kcal": 240},
    "GALAK": {"ing": [("Base Bianca", 825), ("Pasta Galak", 100)], "seq": 2, "kcal": 260},
    "FRAGOLA": {"ing": [("Acqua", 300), ("Polpa Fragola", 375), ("Base Frutta", 200)], "seq": 3, "kcal": 150},
    "LIMONE": {"ing": [("Acqua", 700), ("Succo Limone", 300)], "seq": 3, "kcal": 130},
    "FONDENTE": {"ing": [("Acqua", 600), ("Fondente 70%", 450)], "seq": 12, "kcal": 280},
    "TORTA SEMIFREDDO": {"ing": [("Panna", 500), ("Meringa", 500)], "seq": 13, "kcal": 310},
    "TRONCHETTO": {"ing": [("Base Semifreddo", 1000)], "seq": 13, "kcal": 290}
}

if 'produzione' not in st.session_state: st.session_state.produzione = []
if 'attiva' not in st.session_state: st.session_state.attiva = False

st.title("🍦 Produzione & Etichette")

with st.sidebar:
    st.header("🛒 Selezione")
    gusto_scelto = st.selectbox("Gusto", list(RICETTE.keys()))
    quantita = st.number_input("KG", value=7.0, step=0.5)
    
    if st.button("AGGIUNGI"):
        st.session_state.produzione.append({"gusto": gusto_scelto, "kg": quantita, "seq": RICETTE[gusto_scelto]['seq']})
        st.session_state.attiva = False

    if st.session_state.produzione and not st.session_state.attiva:
        st.divider()
        if st.button("🚀 AVVIA PRODUZIONE", use_container_width=True):
            st.session_state.attiva = True

if st.session_state.attiva:
    df = pd.DataFrame(st.session_state.produzione).sort_values(by="seq")
    ultimo_s = None
    
    for i, row in df.iterrows():
        # Risciacquo [cite: 2026-02-11]
        if ultimo_s is not None and row['seq'] != ultimo_s:
            st.error("🚿 RISCIACQUO MACCHINA OBBLIGATORIO")
            
        c1, c2 = st.columns([2, 1])
        with c1:
            with st.expander(f"📖 RICETTA: {row['gusto']} ({row['kg']} KG)", expanded=True):
                for ing, dose in RICETTE[row['gusto']]['ing']:
                    st.write(f"- {ing}: **{int(dose * row['kg'])}g**")
        
        with c2:
            with st.container(border=True):
                st.caption("🏷️ ETICHETTA")
                info_etichetta = f"GUSTO: {row['gusto']}\nValore Energetico: {RICETTE[row['gusto']]['kcal']} kcal/100g"
                st.write(info_etichetta)
                
                # TASTO CHE FUNZIONA SU IPHONE
                st.download_button(
                    label="💾 SALVA ETICHETTA",
                    data=info_etichetta,
                    file_name=f"etichetta_{row['gusto']}.txt",
                    key=f"dl_{i}"
                )
        ultimo_s = row['seq']

    if st.button("✅ FINISCI E PULISCI"):
        st.session_state.produzione = []; st.session_state.attiva = False; st.rerun()
