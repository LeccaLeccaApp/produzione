import streamlit as st
import pandas as pd
from datetime import datetime
import re

st.set_page_config(page_title="Lecca-Lecca Smart Lab", layout="wide")

# --- DATABASE RICETTE INTEGRALE (CON INGREDIENTI ESTESI E VALORI COMPLETI) ---
RICETTE = {
    "AMARENA": {
        "ricetta": [("Base bianca", 1000), ("Variegato amarena", 100)],
        "ingredienti_estesi": "Base bianca (acqua, zucchero, LATTE intero e scremato in polvere, destrosio, sciroppo di glucosio, oli/grassi vegetali, stabilizzanti ed emulsionanti), variegato di amarena e ciliegie, zucchero, aromi.",
        "seq": 2, "kcal": 232, "all": "LATTE e derivati",
        "nutri": {"G": "11,6g", "Sat": "7,8g", "C": "28,2g", "Zuc": "28,4g", "P": "2,8g", "S": "0g"}

     "POLLO": {
        "ricetta": [("Base bianca", 4000), ("Variegato amarena", 100)],
        "ingredienti_estesi": "Base bianca (acqua, zucchero, LATTE intero e scremato in polvere, destrosio, sciroppo di glucosio, oli/grassi vegetali, stabilizzanti ed emulsionanti), variegato di amarena e ciliegie, zucchero, aromi.",
        "seq": 2, "kcal": 232, "all": "LATTE e derivati",
        "nutri": {"G": "11,6g", "Sat": "7,8g", "C": "28,2g", "Zuc": "28,4g", "P": "2,8g", "S": "0g"}
    },
    "STRACCIATELLA": {
        "ricetta": [("Base bianca", 1000), ("Cioccolato scaglie", 80)],
        "ingredienti_estesi": "Base bianca (acqua, zucchero, LATTE intero e scremato in polvere, destrosio, sciroppo di glucosio, oli/grassi vegetali, stabilizzanti ed emulsionanti), cioccolato fondente in scaglie.",
        "seq": 2, "kcal": 250, "all": "LATTE e derivati, SOIA",
        "nutri": {"G": "15,4g", "Sat": "10,9g", "C": "23,3g", "Zuc": "23,4g", "P": "3,3g", "S": "0g"}
    },
    "KINDER CEREALI": {
        "ricetta": [("Base bianca", 1000), ("Cereali", 100)],
        "ingredienti_estesi": "Base bianca (acqua, zucchero, LATTE intero e scremato in polvere, destrosio, sciroppo di glucosio, oli/grassi vegetali, stabilizzanti ed emulsionanti), cereali croccanti (GLUTINE), cacao, aromi.",
        "seq": 2, "kcal": 289.8, "all": "LATTE e derivati, GLUTINE",
        "nutri": {"G": "18,1g", "Sat": "10,7g", "C": "27,3g", "Zuc": "26,4g", "P": "3,4g", "S": "0g"}
    },
    "PISTACCHIO VEGANO": {
        "ricetta": [("Acqua", 625), ("Bianco stevia", 312), ("Pasta pistacchio", 100), ("Destrosio", 25)],
        "ingredienti_estesi": "Acqua, bianco stevia (edulcoranti, fibre vegetali, stabilizzanti ed emulsionanti), PISTACCHI, destrosio.",
        "seq": 1, "kcal": 195, "all": "FRUTTA A GUSCIO (pistacchi)",
        "nutri": {"G": "11,0g", "Sat": "5,9g", "C": "22,9g", "Zuc": "3,1g", "P": "2,7g", "S": "0g"}
    },
    "DUBAI": {
        "ricetta": [("Base bianca", 900), ("Pistacchi", 100), ("Kataifi", 50)],
        "ingredienti_estesi": "Base bianca (acqua, zucchero, LATTE intero e scremato in polvere, destrosio, sciroppo di glucosio, oli/grassi vegetali, stabilizzanti ed emulsionanti), PISTACCHI, kataifi (GLUTINE), cacao, aromi.",
        "seq": 2, "kcal": 295, "all": "LATTE, GLUTINE, FRUTTA A GUSCIO",
        "nutri": {"G": "18,8g", "Sat": "9,4g", "C": "26,5g", "Zuc": "25,1g", "P": "4,2g", "S": "0g"}
    }
    # NOTA: Qui vanno aggiunti tutti gli altri 40 gusti seguendo lo stesso schema.
}

if 'produzione' not in st.session_state: st.session_state.produzione = []

st.title("🍦 Smart Lab Lecca-Lecca")

# --- 1. DETTATURA ---
st.subheader("🎤 Dettatura Ordine")
input_testo = st.text_area("Inserisci o detta i gusti...", height=100)

if st.button("🚀 ELABORA"):
    fasi = re.split(r'[,.\n]', input_testo.upper())
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
                break

# --- 2. GENERAZIONE DOCUMENTO COMPLETO ---
if st.session_state.produzione:
    df_p = pd.DataFrame(st.session_state.produzione).sort_values(by="seq")
    lotto_s = datetime.now().strftime("%Y%m%d")

    txt = "1. CARTA DEL GELATIERE\n" + "="*40 + "\n"
    u_s = None
    for _, r in df_p.iterrows():
        if u_s is not None and r['seq'] != u_s:
            txt += "\n" + "-"*20 + "\nRISCIACQUO MACCHINA\n" + "-"*20 + "\n"
        
        txt += f"\nGUSTO: {r['gusto']}{r['nota']} ({r['kg']} KG)\n"
        for i_n, d_o in RICETTE[r['gusto']]['ricetta']:
            p_e = int(d_o * (r['kg']/7.0))
            txt += f"- {i_n}: {p_e}g\n"
        u_s = r['seq']

    txt += "\n\n2. ETICHETTE COMPLETE (Ingredienti e Valori)\n" + "="*40 + "\n"
    for _, r in df_p.iterrows():
        g = RICETTE[r['gusto']]
        n = g['nutri']
        txt += f"\nPRODOTTO: {r['gusto']}{r['nota']}\n"
        txt += f"INGREDIENTI: {g['ingredienti_estesi']}\n"
        txt += f"ALLERGENI: {g['all']}\n"
        txt += f"VALORI NUTRIZIONALI (per 100g):\n"
        txt += f" - Energia: {g['kcal']} kcal\n"
        txt += f" - Grassi: {n['G']} (di cui saturi: {n['Sat']})\n"
        txt += f" - Carboidrati: {n['C']} (di cui zuccheri: {n['Zuc']})\n"
        txt += f" - Proteine: {n['P']}\n"
        txt += f" - Sale: {n['S']}\n"
        txt += f"Lotto: {lotto_s}\n"
        txt += "."*30 + "\n"

    txt += "\n\n3. RIEPILOGO FIRME\n" + "="*40 + "\n"
    txt += f"Data: {datetime.now().strftime('%d/%m/%Y')} | Lotto: {lotto_s}\n\n"
    for _, r in df_p.iterrows():
        txt += f"[ ] {r['gusto']}{r['nota']} - {r['kg']} KG\n"
    txt += "\n\nFirma Franco: ________________  Firma Giuseppe: ________________\n"

    st.download_button("🖨️ SCARICA DOCUMENTO COMPLETO", txt, f"Produzione_{lotto_s}.txt", use_container_width=True)
    
    if st.button("🗑️ Reset"):
        st.session_state.produzione = []; st.rerun()
