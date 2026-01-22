import streamlit as st
import pandas as pd
import numpy as np
import time
import urllib.parse

# 1. Configuração de Interface
st.set_page_config(layout="wide", page_title="NOAH AGRO | IA PREDICTIVE", initial_sidebar_state="collapsed")

# 2. CSS: Visual Sala de Comando Premium (Sem botões extras)
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    h1, h2, h3, h4, p, span, b, small, label { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    .titulo-noah { color: #00FF7F; text-align: center; font-size: 2.2rem; text-shadow: 0 0 15px #00FF7F; padding: 10px; }
    
    /* Quadrantes de Alerta */
    .card-alerta { padding: 18px; border-radius: 12px; margin-bottom: 12px; background-color: #111111; border: 1px solid #333; }
    .critico { border-left: 12px solid #FF0000; box-shadow: -5px 0 15px rgba(255, 0, 0, 0.3); }
    .alerta { border-left: 12px solid #FF8C00; }
    .normal { border-left: 12px solid #00FF7F; }
    
    /* Badge de IA */
    .ia-badge { 
        background: linear-gradient(90deg, #00FF7F, #0077ff); 
        color: white !important; padding: 3px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: bold;
    }
    
    /* Barra de Risco Preditivo */
    .risk-bar-container { background-color: #222; border-radius: 10px; height: 12px; width: 100%; margin-top: 8px; border: 1px solid #444; }
    .risk-bar-fill { height: 100%; border-radius: 10px; transition: width 0.8s ease-in-out; }
    
    .sensor-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-top: 15px; background: #000; padding: 10px; border-radius: 8px; }
    .sensor-val { font-size: 1.1rem; font-weight: bold; color: #00FF7F !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='titulo-noah'>NOAH AGRO - CONTROLE OPERACIONAL PREDITIVO</h1>", unsafe_allow_html=True)

# 3. Lógica de IA e Priorização
def calcular_risco_ia(umid, ph, pluv):
    base_risco = (75 - umid) * 0.6 + (abs(6.5 - ph) * 12)
    if pluv < 5: base_risco += 20
    risco_final = max(5, min(int(base_risco), 98))
    
    if risco_final > 70: return risco_final, "CRÍTICO", "#FF0000", "critico"
    if risco_final > 40: return risco_final, "MODERADO", "#FF8C00", "alerta"
    return risco_final, "BAIXO", "#00FF7F", "normal"

def obter_dados():
    setores = [
        {"nome": "SETOR NORTE", "lat": -22.90, "lon": -43.20, "gestor": "RICARDO", "tel": "5521999999999"},
        {"nome": "SETOR SUL", "lat": -22.95, "lon": -43.25, "gestor": "ANA", "tel": "5521888888888"},
        {"nome": "ESTUFA 01", "lat": -22.85, "lon": -43.15, "gestor": "MARCOS", "tel": "5521777777777"},
        {"nome": "ÁREA OESTE", "lat": -22.82, "lon": -43.12, "gestor": "BEATRIZ", "tel": "5521666666666"}
    ]
    data = []
    for s in setores:
        u, p, ph = np.random.randint(15, 80), np.random.randint(0, 40), round(np.random.uniform(4.5, 8.5), 1)
        r_val, r_txt, r_cor, r_cls = calcular_risco_ia(u, ph, p)
        peso = 1 if r_val > 70 else (2 if r_val > 40 else 3)
        s.update({"umid": u, "pluv": p, "ph": ph, "risco": r_val, "risco_txt": r_txt, "risco_cor": r_cor, "classe": r_cls, "peso": peso})
        data.append(s)
    return sorted(data, key=lambda x: x['peso'])

df_final = obter_dados()

# 4. Interface
c1, c2 = st.columns([1.3, 1])

with c1:
    st.markdown("### 🌐 MONITORAMENTO GEOGRÁFICO")
    map_df = pd.DataFrame(df_final)
    st.map(map_df, latitude='lat', longitude='lon', color='risco_cor', size=550)

with c2:
    st.markdown("### 🧠 FILA DE INTERVENÇÃO (IA)")
    for d in df_final:
        st.markdown(f"""
            <div class="card-alerta {d['classe']}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <b style="font-size: 1.1rem;">{d['nome']}</b>
                    <span class="ia-badge">IA PREDICT</span>
                </div>
