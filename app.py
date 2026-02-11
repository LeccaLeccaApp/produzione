import streamlit as st
import pandas as pd
from datetime import datetime

# Configurazione Pagina
st.set_page_config(page_title="Lecca-Lecca ERP Master", layout="wide")

# --- 1. DATABASE RICETTE COMPLETO ---
# Qui ho inserito i gusti con le dosi corrette e le categorie per il risciacquo
RICETTE = {
    "NOCCIOLA VEGANO": {"ing": [("Acqua", 4375), ("Pasta Nocciola", 910), ("Zuccheri", 2450)], "seq": 1, "kcal": 210},
    "BUENO VEGANO": {"ing": [("Acqua", 625), ("Pasta Bueno Veg", 120)], "seq": 1, "kcal": 225},
    "STRACCIATELLA": {"ing": [("Base Lecca lecca", 7000), ("Cioccolato scaglie", 560)], "seq": 2, "kcal": 240},
    "GALAK": {"ing": [("Base Bianca", 825), ("Pasta Galak", 100)], "seq": 2, "kcal": 260},
    "FRAGOLA": {"ing": [("Acqua", 2100), ("Polpa Fragola", 2625), ("Base", 1400)], "seq": 3, "kcal": 150},
    "LIMONE": {"ing": [("Acqua", 700), ("Succo Limone", 300)], "seq": 3, "kcal": 130},
    "FONDENTE": {"ing": [("Acqua", 600), ("Fondente 70%", 450)], "seq": 12, "kcal": 280},
    "TORTA SEMIFREDDO": {"ing": [("Panna", 500), ("Meringa", 500)], "seq": 13, "kcal": 310},
    "TRONCHETTO": {"ing": [("Base Semifreddo", 1000)], "seq": 13, "kcal": 290}
}

# --- 2. GESTIONE MEMORIA (Session State) ---
if 'produzione' not in st.session_state: st.session_state.produzione = []
if 'attiva' not in st.session_state: st.session_state.attiva = False
if 'spese' not in st.session_state: st.session_state.spese = []

st.title("🍦 Gestione Totale Laboratorio")

# --- 3. MENU LATERALE (Input Dati) ---
with st.sidebar:
    st.header("📝 Pianificazione")
    g_scelto = st.selectbox("Seleziona Gusto", sorted(list(RICETTE.keys())))
    kg = st.number_input("Quantità (KG)", value=7.0, step=0.5)
    
    if st.button("➕ AGGIUNGI A LISTA"):
        st.session_state.produzione.append({"gusto": g_scelto, "kg": kg, "seq": RICETTE[g_scelto]['seq']})
        st.session_state.attiva = False
        st.toast(f"{g_scelto} aggiunto!")

    if st.session_state.produzione and not st.session_state.attiva:
        st.divider()
        if st.button("🚀 AVVIA PRODUZIONE", use_container_width=True):
            st.session_state.attiva = True

    st.divider()
    st.header("📸 Contabilità")
    foto = st.camera_input("Scatta Fattura")
    if foto:
        with st.form("fm_spesa"):
            forn = st.text_input("Fornitore")
            euro = st.number_input("Importo €", step=0.01)
            if st.form_submit_button("SALVA IN STORICO"):
                st.session_state.spese.append({"f": forn, "e": euro, "d": datetime.now().strftime("%d/%m/%y")})
                st.success("Fattura salvata!")

# --- 4. AREA PRINCIPALE (Tab) ---
tab_prod, tab_cont = st.tabs(["🚀 PRODUZIONE & STAMPA", "📊 STORICO SPESE"])

with tab_prod:
    if st.session_state.attiva:
        # Costruzione Report Unificato per Stampa
        report_stampa = f"REPORT PRODUZIONE - {datetime.now().strftime('%d/%m/%Y')}\n"
        report_stampa += "="*40 + "\n"
        
        df = pd.DataFrame(st.session_state.produzione).sort_values(by="seq")
        u_s = None
        
        # Generazione testo per il file di stampa
        for _, row in df.iterrows():
            if u_s is not None and row['seq'] != u_s:
                report_stampa += "\n🚿 RISCIACQUO MACCHINA OBBLIGATORIO\n" [cite: 2026-02-11]
                report_stampa += "-"*40 + "\n"
            
            report_stampa += f"\n🍦 {row['gusto']} ({row['kg']} KG)\n"
            for ing, dose in RICETTE[row['gusto']]['ing']:
                peso = int(dose * (row['kg']/7.0)) if row['kg'] != 7.0 else int(dose)
                report_stampa += f"  - {ing}: {peso}g\n"
            report_stampa += f"🏷️ Calorie: {RICETTE[row['gusto']]['kcal']} kcal/100g\n"
            u_s = row['seq']

        # Tasto Stampa Unica (File di testo leggibile da iPhone)
        st.download_button(
            label="🖨️ STAMPA TUTTA LA LISTA (Unico Foglio)",
            data=report_stampa,
            file_name=f"Produzione_{datetime.now().strftime('%d_%m')}.txt",
            mime="text/plain",
            use_container_width=True
        )
        
        st.divider()
        
        # Visualizzazione Schede a schermo
        u_s = None
        for _, row in df.iterrows():
            if u_s is not None and row['seq'] != u_s:
                st.error("🚿 RISCIACQUO MACCHINA") [cite: 2026-02-11]
            
            with st.expander(f"📖 {row['gusto']} - {row['kg']} KG", expanded=True):
                c1, c2 = st.columns([2,1])
                with c1:
                    for ing, dose in RICETTE[row['gusto']]['ing']:
                        peso = int(dose * (row['kg']/7.0)) if row['kg'] != 7.0 else int(dose)
                        st.write(f"- {ing}: **{peso}g**")
                with c2:
                    st.caption("ETICHETTA")
                    st.write(f"{RICETTE[row['gusto']]['kcal']} kcal")
            u_s = row['seq']
            
        if st.button("✅ FINE SESSIONE (Svuota tutto)"):
            st.session_state.produzione = []
            st.session_state.attiva = False
            st.rerun()
    else:
        st.info("Pianifica i gusti nel menu a sinistra e clicca il Razzo 🚀")

with tab_cont:
    st.subheader("Archivio Fatture")
    if st.session_state.spese:
        df_spese = pd.DataFrame(st.session_state.spese)
        st.table(df_spese)
        
        # Report per mail
        testo_mail = "RIEPILOGO SPESE:\n"
        for s in st.session_state.spese:
            testo_mail += f"- {s['d']} | {s['f']}: €{s['e']}\n"
        st.text_area("Testo per Email/WhatsApp:", testo_mail)
    else:
        st.write("Nessuna fattura salvata oggi.")
