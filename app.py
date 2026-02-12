import streamlit as st
import pandas as pd
from datetime import datetime
import re

st.set_page_config(page_title="Lecca-Lecca Smart Lab", layout="wide")

# --- DATABASE RICETTE INTEGRALE (TUTTI I GUSTI INVIATI) ---
RICETTE = {
    "AMARENA": {"ing": [("Base bianca", 1000), ("Variegato amarena", 100)], "seq": 2, "kcal": 232, "all": "LATTE e derivati", "nutri": "Grassi: 11,6g | Carb: 28,2g | Prot: 2,8g | Sale: 0g"},
    "STRACCIATELLA": {"ing": [("Base bianca", 1000), ("Cioccolato scaglie", 80)], "seq": 2, "kcal": 250, "all": "LATTE e derivati, SOIA", "nutri": "Grassi: 15,4g | Carb: 23,3g | Prot: 3,3g | Sale: 0g"},
    "FIOR DI LATTE": {"ing": [("Base bianca", 1000)], "seq": 2, "kcal": 226.6, "all": "LATTE e derivati", "nutri": "Grassi: 13,1g | Carb: 22,9g | Prot: 3,2g | Sale: 0g"},
    "SMARTIES": {"ing": [("Base bianca", 1000), ("Confetti cioccolato", 100)], "seq": 2, "kcal": 238.1, "all": "LATTE e derivati", "nutri": "Grassi: 13,3g | Carb: 25,3g | Prot: 3,2g | Sale: 0g"},
    "KINDER CEREALI": {"ing": [("Base bianca", 1000), ("Cereali croccanti", 100), ("Cacao", 20)], "seq": 2, "kcal": 289.8, "all": "LATTE e derivati, GLUTINE", "nutri": "Grassi: 18,1g | Carb: 27,3g | Prot: 3,4g | Sale: 0g"},
    "KINDER BARRETTA": {"ing": [("Base bianca", 1000), ("Nocciole", 50), ("Cacao", 30)], "seq": 2, "kcal": 270.8, "all": "LATTE e derivati, FRUTTA A GUSCIO", "nutri": "Grassi: 16,2g | Carb: 26,9g | Prot: 3,4g | Sale: 0g"},
    "SPAGNOLA": {"ing": [("Base bianca", 1000), ("Variegato amarena", 100), ("Cacao", 20)], "seq": 2, "kcal": 245, "all": "LATTE e derivati", "nutri": "Grassi: 14,0g | Carb: 24,5g | Prot: 3,2g | Sale: 0g"},
    "CROCCANTE AMARENA": {"ing": [("Base bianca", 1000), ("Variegato amarena", 80), ("Croccante", 50)], "seq": 2, "kcal": 296.6, "all": "LATTE, FRUTTA A GUSCIO, GLUTINE", "nutri": "Grassi: 15,7g | Carb: 34,2g | Prot: 3,6g | Sale: 0g"},
    "COSTIERA": {"ing": [("Base bianca", 1000), ("Biscotto sbriciolato", 100)], "seq": 2, "kcal": 246, "all": "LATTE e derivati, GLUTINE", "nutri": "Grassi: 13,5g | Carb: 26,0g | Prot: 3,0g | Sale: 0g"},
    "NOCCIOLA": {"ing": [("Base bianca", 900), ("Pasta nocciola", 130), ("Destrosio", 25)], "seq": 2, "kcal": 286.2, "all": "LATTE, FRUTTA A GUSCIO", "nutri": "Grassi: 19,0g | Carb: 22,8g | Prot: 4,6g | Sale: 0g"},
    "PISTACCHIO": {"ing": [("Base bianca", 900), ("Pasta pistacchio", 100), ("Destrosio", 20)], "seq": 2, "kcal": 275.9, "all": "LATTE, FRUTTA A GUSCIO", "nutri": "Grassi: 17,4g | Carb: 23,0g | Prot: 5,5g | Sale: 0g"},
    "BACIO": {"ing": [("Base bianca", 900), ("Pasta sorriso amaro", 100)], "seq": 2, "kcal": 276.5, "all": "LATTE, FRUTTA A GUSCIO", "nutri": "Grassi: 17,9g | Carb: 23,0g | Prot: 4,3g | Sale: 0g"},
    "CIOCCOLATO AL LATTE": {"ing": [("Base bianca", 900), ("Cacao", 100), ("Destrosio", 50), ("Cioccolato puro", 30)], "seq": 2, "kcal": 254.8, "all": "LATTE e derivati", "nutri": "Grassi: 13,8g | Carb: 25,8g | Prot: 4,8g | Sale: 0g"},
    "CIOCCOLATO FONDENTE": {"ing": [("Acqua", 600), ("Fondente babbi", 450), ("Destrosio", 20)], "seq": 1, "kcal": 176.1, "all": "Può contenere LATTE e SOIA", "nutri": "Grassi: 4,1g | Carb: 29,2g | Prot: 3,1g | Sale: 0g"},
    "FRAGOLA": {"ing": [("Acqua", 300), ("Polpa fragola", 375), ("Base bianca", 200), ("Destrosio", 40), ("Saccarosio", 75), ("Pasta fragolina", 50)], "seq": 3, "kcal": 121.3, "all": "Può contenere LATTE", "nutri": "Grassi: 2,4g | Carb: 23,8g | Prot: 0,8g | Sale: 0g"},
    "LIMONE": {"ing": [("Acqua", 700), ("Lemon plus", 300)], "seq": 3, "kcal": 119, "all": "—", "nutri": "Grassi: 1,3g | Carb: 27,0g | Prot: 0,3g | Sale: 0g"},
    "PESCA": {"ing": [("Acqua", 700), ("Frutta pesca gialla", 300)], "seq": 3, "kcal": 122, "all": "—", "nutri": "Grassi: 1,8g | Carb: 26,7g | Prot: 0g | Sale: 0g"},
    "ANGURIA": {"ing": [("Acqua", 700), ("Anguria 300", 300)], "seq": 3, "kcal": 118, "all": "—", "nutri": "Grassi: 0,2g | Carb: 27,0g | Prot: 0,3g | Sale: 0g"},
    "MELONE": {"ing": [("Acqua", 700), ("Melone 300", 300)], "seq": 3, "kcal": 125, "all": "—", "nutri": "Grassi: 1,1g | Carb: 28,7g | Prot: 0g | Sale: 0g"},
    "ANANAS": {"ing": [("Acqua", 700), ("Frutta ananas", 300)], "seq": 3, "kcal": 120, "all": "—", "nutri": "Grassi: 0,2g | Carb: 27,5g | Prot: 0,4g | Sale: 0g"},
    "COCCO": {"ing": [("Base bianca", 900), ("Cocco Giuso", 70)], "seq": 2, "kcal": 255, "all": "LATTE e derivati", "nutri": "Grassi: 15,5g | Carb: 24,5g | Prot: 3,0g | Sale: 0g"},
    "MENTA E CIOCCOLATO": {"ing": [("Base bianca", 900), ("Pasta menta", 50), ("Cacao", 20)], "seq": 2, "kcal": 238, "all": "LATTE e derivati, SOIA", "nutri": "Grassi: 13,0g | Carb: 26,2g | Prot: 3,0g | Sale: 0g"},
    "PUFFO": {"ing": [("Base bianca", 900), ("Pasta fiocco azzurro", 50)], "seq": 2, "kcal": 244, "all": "LATTE e derivati", "nutri": "Grassi: 14,3g | Carb: 24,6g | Prot: 3,3g | Sale: 0g"},
    "LIQUIRIZIA": {"ing": [("Base bianca", 900), ("Pasta liquirizia", 50)], "seq": 4, "kcal": 228, "all": "LATTE e derivati", "nutri": "Grassi: 12,5g | Carb: 24,9g | Prot: 3,0g | Sale: 0g"},
    "CAFFÈ": {"ing": [("Base bianca", 900), ("Caffè arabica", 25)], "seq": 2, "kcal": 228, "all": "LATTE e derivati", "nutri": "Grassi: 12,4g | Carb: 24,8g | Prot: 3,1g | Sale: 0g"},
    "PAN DI STELLE": {"ing": [("Base bianca", 900), ("Biscotto Pan di Stelle", 100)], "seq": 2, "kcal": 269, "all": "LATTE, GLUTINE, FRUTTA A GUSCIO", "nutri": "Grassi: 14,7g | Carb: 29,2g | Prot: 3,9g | Sale: 0g"},
    "OREO": {"ing": [("Base bianca", 900), ("Pasta cookies black", 50)], "seq": 2, "kcal": 263, "all": "LATTE, GLUTINE", "nutri": "Grassi: 14,9g | Carb: 27,9g | Prot: 3,2g | Sale: 0g"},
    "NUTELLA BISCUITS": {"ing": [("Base bianca", 900), ("Pasta cookies", 50)], "seq": 2, "kcal": 248, "all": "LATTE, FRUTTA A GUSCIO", "nutri": "Grassi: 14,1g | Carb: 25,6g | Prot: 3,3g | Sale: 0g"},
    "SNICKERS": {"ing": [("Base bianca", 900), ("Arachidi e caramello", 100)], "seq": 2, "kcal": 304, "all": "LATTE, ARACHIDI, FRUTTA A GUSCIO", "nutri": "Grassi: 19,6g | Carb: 25,2g | Prot: 5,5g | Sale: 0g"},
    "POP CORN": {"ing": [("Latte", 750), ("Popcorn/caramello", 312)], "seq": 2, "kcal": 163, "all": "LATTE e derivati", "nutri": "Grassi: 5,2g | Carb: 26,6g | Prot: 2,5g | Sale: 0g"},
    "PLASMON": {"ing": [("Base bianca", 900), ("Biscotto Plasmon", 100)], "seq": 2, "kcal": 262, "all": "LATTE, GLUTINE", "nutri": "Grassi: 12,2g | Carb: 32,7g | Prot: 4,2g | Sale: 0g"},
    "RED VELVET": {"ing": [("Base bianca", 900), ("Pasta cookies black", 50)], "seq": 2, "kcal": 238, "all": "LATTE, GLUTINE, UOVA", "nutri": "Grassi: 12,3g | Carb: 27,7g | Prot: 3,1g | Sale: 0g"},
    "YOGURT FRUTTI DI BOSCO": {"ing": [("Base", 900), ("Peryo", 30)], "seq": 2, "kcal": 215, "all": "LATTE e derivati", "nutri": "Grassi: 10,8g | Carb: 24,6g | Prot: 3,4g | Sale: 0g"},
    "TIRAMISÙ": {"ing": [("Base bianca", 900), ("Pasta tiramisù special", 50)], "seq": 2, "kcal": 235, "all": "LATTE, UOVA", "nutri": "Grassi: 12,9g | Carb: 25,1g | Prot: 3,4g | Sale: 0g"},
    "MANDORLA": {"ing": [("Base bianca", 900), ("Pasta mandorla", 75)], "seq": 2, "kcal": 257, "all": "LATTE, FRUTTA A GUSCIO", "nutri": "Grassi: 15,6g | Carb: 25,1g | Prot: 4,2g | Sale: 0g"},
    "LOTUS": {"ing": [("Base bianca", 900), ("Pasta speculous", 100)], "seq": 2, "kcal": 316, "all": "LATTE, GLUTINE", "nutri": "Grassi: 19,9g | Carb: 30,0g | Prot: 3,3g | Sale: 0g"},
    "FERRERO ROCHER": {"ing": [("Base bianca", 900), ("Pasta nocciola", 50)], "seq": 2, "kcal": 290, "all": "LATTE, FRUTTA A GUSCIO", "nutri": "Grassi: 19,2g | Carb: 23,9g | Prot: 4,1g | Sale: 0g"},
    "HAPPY HIPPO": {"ing": [("Base bianca", 900), ("Pasta nocciola", 50)], "seq": 2, "kcal": 278, "all": "LATTE, FRUTTA A GUSCIO", "nutri": "Grassi: 17,5g | Carb: 24,6g | Prot: 3,7g | Sale: 0g"},
    "KINDER BUENO": {"ing": [("Base bianca", 900), ("Pasta nocciola", 50)], "seq": 2, "kcal": 282, "all": "LATTE, FRUTTA A GUSCIO", "nutri": "Grassi: 18,5g | Carb: 23,8g | Prot: 3,9g | Sale: 0g"},
    "KINDER CARDS": {"ing": [("Base bianca", 1000)], "seq": 2, "kcal": 280, "all": "LATTE, FRUTTA A GUSCIO", "nutri": "Grassi: 17,2g | Carb: 26,8g | Prot: 3,7g | Sale: 0g"},
    "PISTACCHIO VEGANO": {"ing": [("Acqua", 625), ("Bianco stevia", 312), ("Pasta pistacchio", 100), ("Destrosio", 25)], "seq": 1, "kcal": 195, "all": "FRUTTA A GUSCIO", "nutri": "Grassi: 11,0g | Carb: 22,9g | Prot: 2,7g | Sale: 0g"},
    "SICILY VEGANO": {"ing": [("Acqua", 625), ("Bianco stevia", 312), ("Pasta mandorla", 75)], "seq": 1, "kcal": 192, "all": "FRUTTA A GUSCIO", "nutri": "Grassi: 10,7g | Carb: 25,3g | Prot: 2,0g | Sale: 0g"},
    "NOCCIOLA VEGANO": {"ing": [("Acqua", 625), ("Bianco stevia", 312), ("Pasta nocciola", 130)], "seq": 1, "kcal": 180, "all": "FRUTTA A GUSCIO", "nutri": "Grassi: 10,5g | Carb: 21,8g | Prot: 1,5g | Sale: 0g"},
    "DUBAI": {"ing": [("Base bianca", 900), ("Cacao", 100), ("Destrosio", 50), ("Pistacchi", 100), ("Kataifi", 50)], "seq": 2, "kcal": 295, "all": "LATTE, GLUTINE, FRUTTA A GUSCIO", "nutri": "Grassi: 18,8g | Carb: 26,5g | Prot: 4,2g | Sale: 0g"},
    "CANNOLO SICILIANO": {"ing": [("Base bianca", 825), ("Panna suldy", 50), ("Base cannolo", 50)], "seq": 2, "kcal": 245, "all": "LATTE, GLUTINE", "nutri": "Grassi: 13,4g | Carb: 26,4g | Prot: 3,4g | Sale: 0g"},
    "CHEESECAKE LAMPONE": {"ing": [("Base bianca", 900), ("Base cheesecake", 40)], "seq": 2, "kcal": 242, "all": "LATTE, GLUTINE", "nutri": "Grassi: 13,0g | Carb: 26,8g | Prot: 3,3g | Sale: 0g"},
    "CARAMELLO SALATO": {"ing": [("Latte", 750), ("Caramello salato", 312)], "seq": 2, "kcal": 260, "all": "LATTE e derivati", "nutri": "Grassi: 14,5g | Carb: 28,0g | Prot: 3,4g | Sale: 0,1g"},
    "COOKIES & CARAMEL": {"ing": [("Base bianca", 900), ("Pasta coockies caramel", 50)], "seq": 2, "kcal": 255, "all": "LATTE, GLUTINE", "nutri": "Grassi: 14,0g | Carb: 27,5g | Prot: 3,3g | Sale: 0g"},
    "BENVENUTI AL SUD": {"ing": [("Base bianca", 900), ("Pasta mandorla", 75)], "seq": 2, "kcal": 270, "all": "LATTE, GLUTINE, FRUTTA A GUSCIO", "nutri": "Grassi: 16,0g | Carb: 26,0g | Prot: 3,8g | Sale: 0g"},
    "BOUNTY": {"ing": [("Base bianca", 900), ("Cocco Giuso", 70)], "seq": 2, "kcal": 255, "all": "LATTE e derivati", "nutri": "Grassi: 15,5g | Carb: 24,5g | Prot: 3,0g | Sale: 0g"},
    "MERENDERO": {"ing": [("Crema da banco", 1000)], "seq": 2, "kcal": 574, "all": "LATTE, FRUTTA A GUSCIO", "nutri": "Grassi: 37,5g | Carb: 53,5g | Prot: 4,8g | Sale: 0g"},
    "NUTELLA": {"ing": [("Crema da banco", 1000)], "seq": 2, "kcal": 562, "all": "LATTE, FRUTTA A GUSCIO", "nutri": "Grassi: 36,0g | Carb: 53,0g | Prot: 5,0g | Sale: 0g"},
    "AMORE PISTACCHIO": {"ing": [("Crema banco pistacchio", 1000)], "seq": 2, "kcal": 589, "all": "LATTE, FRUTTA A GUSCIO", "nutri": "Grassi: 40,5g | Carb: 44,5g | Prot: 10,2g | Sale: 0g"}
}

if 'produzione' not in st.session_state: st.session_state.produzione = []

st.title("🍦 Smart Lab Lecca-Lecca")

# --- 1. DETTATURA ---
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
        if u_s is not None and r['seq'] != u_s:
            txt += "\nRISCIACQUO MACCHINA\n" + "-"*30 + "\nrisciacquo\n" + "-"*30 + "\n"
        
        txt += f"\nGUSTO: {r['gusto']}{r['nota']} ({r['kg']} KG)\n"
        for i_n, d_o in RICETTE[r['gusto']]['ing']:
            p_e = int(d_o * (r['kg']/7.0))
            txt += f"- {i_n}: {p_e}g\n"
        u_s = r['seq']

    # 2. ETICHETTE
    txt += "\n\n2. ETICHETTE NUTRIZIONALI\n" + "="*30 + "\n"
    for _, r in df_p.iterrows():
        g = RICETTE[r['gusto']]
        txt += f"\nPRODOTTO: {r['gusto']}{r['nota']}\nALLERGENI: {g['all']}\nLotto: {lotto_s}\n"
        txt += f"Calorie: {g['kcal']} kcal/100g\n{g['nutri']}\n"
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
    
    if st.button("🗑️ Reset"):
        st.session_state.produzione = []; st.rerun()
