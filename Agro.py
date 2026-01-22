import streamlit as st
import pandas as pd
import numpy as np
import time
import urllib.parse

# 1. Configuração
st.set_page_config(layout="wide", page_title="NOAH AGRO | IA PREDICTIVE", initial_sidebar_state="collapsed")

# 2. CSS: Visual Premium com destaque para IA
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    h1, h2, h3, h4, p, span, b, small, label { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    .titulo-noah { color: #00FF7F; text-align: center; font-size: 2.5rem; text-shadow: 0 0 15px #00FF7F; padding: 10px; }
    
    /* Card de Alerta */
    .card-alerta { padding: 15px; border-radius: 12px; margin-bottom: 10px; background-color: #111111; border: 1px solid #333; }
    .critico { border-left: 10px solid #FF0000; }
    .alerta { border-left: 10px solid #FF8C00; }
    .normal { border-left: 10px solid #00FF7F; }
    
    /* Estilo do Módulo de IA */
    .ia-badge { 
        background: linear-gradient(90deg, #00FF7F, #0077ff); 
        color: white !important; padding: 2px 8px; border-radius: 5px; font-size: 0.7rem; font-weight: bold;
    }
    .risk-bar-container { background-color: #333; border-radius: 10px; height: 10px; width: 100%; margin-top: 5px; }
    .risk-bar-fill { height: 10px; border-radius: 10px; transition: width 0.5s; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='titulo-noah'>NOAH AGRO - PREDIÇÃO DE RISCO VIA IA</h1>", unsafe_allow_html=True)

# 3. Lógica de IA Preditiva (Simulação de Machine Learning)
def analise_ia_preditiva(umid, ph, pluv):
    # Simula um modelo que prevê risco nas próximas 24h
    # Se a umidade está caindo e a pluviometria é zero, o risco sobe
    score_risco = (100 - umid) * 0.5 + (abs(6.5 - ph) * 10)
    if pluv < 10: score_risco += 15
    
    risco = min(int(score_risco), 100)
    
    if risco > 75: return risco, "CRÍTICO", "#FF0000"
    if risco > 45: return risco, "MODERADO", "#FF8C00"
    return risco, "BAIXO", "#00FF7F"

def get_data_ia():
    setores = ["SETOR NORTE", "SETOR SUL", "ESTUFA 01", "ÁREA OESTE"]
    lista = []
    for s in setores:
        umid = np.random.randint(15, 70)
        pluv = np.random.randint(0, 50)
        ph = round(np.random.uniform(5.0, 8.5), 1)
        
        risco_val, risco_txt, risco_cor = analise_ia_preditiva(umid, ph, pluv)
        
        # Peso para ordenação (Risco de IA primeiro)
        peso = 1 if risco_val > 75 else (2 if risco_val > 45 else 3)
        
        lista.append({
            "setor": s, "umid": umid, "pluv": pluv, "ph": ph,
            "risco": risco_val, "risco_txt": risco_txt, "risco_cor": risco_cor, "peso": peso
        })
    return sorted(lista, key=lambda x: x['peso'])

dados = get_data_ia()

# 4. Layout
c1, c2 = st.columns([1.2, 1])

with c1:
    st.markdown("### 🌐 MAPA DE CALOR PREDITIVO (24H)")
    df_map = pd.DataFrame(dados)
    df_map['lat'] = [-22.90, -22.95, -22.85, -22.82]
    df_map['lon'] = [-43.20, -43.25, -43.15, -43.12]
    st.map(df_map, latitude='lat', longitude='lon', color='risco_cor', size=500)

with c2:
    st.markdown("### 🧠 ANÁLISE DE PROBABILIDADE (IA)")
    for d in dados:
        st.markdown(f"""
            <div class="card-alerta {'critico' if d['risco'] > 75 else ('alerta' if d['risco'] > 45 else 'normal')}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <b>{d['setor']}</b>
                    <span class="ia-badge">IA PREDICT</span>
                </div>
                <div style="margin-top:10px;">
                    <small>PROBABILIDADE DE INCIDENTE (PRÓX. 24H): <b>{d['risco']}%</b></small>
                    <div class="risk-bar-container">
                        <div class="risk-bar-fill" style="width: {d['risco']}%; background-color: {d['risco_cor']};"></div>
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 10px; font-size: 0.8rem;">
                    <span>💧 Solo: {d['umid']}%</span>
                    <span>🧪 pH: {d['ph']}</span>
                    <span>🌡️ Risco: {d['risco_txt']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if d['risco'] > 45:
            st.button(f"Gerar Relatório Preditivo {d['setor']}", key=d['setor'])

# 5. Refresh
time.sleep(10)
st.rerun()
