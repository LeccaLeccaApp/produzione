import streamlit as st
import pandas as pd

st.set_page_config(page_title="Lecca-Lecca Laboratorio", layout="wide")

# --- DATABASE COMPLETO (Gusti + Basi per Etichette) ---
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

st.title("🍦 Produzione & Etichette Lecca-Lecca")

# --- LATERALE: INSERIMENTO ---
with st.sidebar:
    st.header("🛒 Selezione Gusti")
    gusto_scelto = st.selectbox("Scegli Gusto", list(RICETTE.keys()))
    quantita = st.number_input("KG da produrre", value=7.0, step=0.5)
    
    if st.button("AGGIUNGI ALLA LISTA"):
        st.session_state.produzione.append({"gusto": gusto_scelto, "kg": quantita, "seq": RICETTE[gusto_scelto]['seq']})
        st.session_state.attiva = False

    if st.session_state.produzione and not st.session_state.attiva:
        st.divider()
        # IL TASTO CHE TI SERVE
        if st.button("🚀 AVVIA PRODUZIONE", use_container_width=True):
            st.session_state.attiva = True

# --- AREA CENTRALE ---
if st.session_state.attiva:
    st.header("👨‍🍳 SCHEDE TECNICHE E ETICHETTE")
    
    # Ordina per sequenza per i risciacqui
    df = pd.DataFrame(st.session_state.produzione).sort_values(by="seq")
    ultimo_s = None
    
    for _, row in df.iterrows():
        # Messaggio Risciacquo tra categorie diverse [cite: 2026-02-11]
        if ultimo_s is not None and row['seq'] != ultimo_s:
            st.error("🚿 RISCIACQUO MACCHINA OBBLIGATORIO")
            
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.expander(f"📖 RICETTA: {row['gusto']} ({row['kg']} KG)", expanded=True):
                for ing, dose in RICETTE[row['gusto']]['ing']:
                    st.write(f"- {ing}: **{int(dose * row['kg'])}g**")
        
        with col2:
            with st.container(border=True):
                st.caption("🏷️ ETICHETTA NUTRIZIONALE")
                st.write(f"**Gusto:** {row['gusto']}")
                st.write(f"Valore energetico: {RICETTE[row['gusto']]['kcal']} kcal / 100g")
                st.button("🖨️ Stampa", key=f"print_{row['gusto']}_{_}")

        ultimo_s = row['seq']

    if st.button("✅ FINISCI E PULISCI"):
        st.session_state.produzione = []
        st.session_state.attiva = False
        st.rerun()
else:
    if not st.session_state.produzione:
        st.info("👋 Ciao Nicola! Inizia aggiungendo i gusti dal menu a sinistra.")
    else:
        st.warning("Hai dei gusti pronti! Clicca '🚀 AVVIA PRODUZIONE' a sinistra.")
