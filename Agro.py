import streamlit as st
import pandas as pd
import numpy as np
import time
import urllib.parse

# 1. Configuração inicial (Deve ser a primeira linha)
st.set_page_config(layout="wide", page_title="NOAH AGRO | REAL-TIME", initial_sidebar_state="collapsed")

# 2. Estilo Visual Sala de Comando (Fundo Preto / Letras Brancas)
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    h1, h2, h3, h4, p, span, b, small, label { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    .titulo-noah { color: #00FF7F; text-align: center; font-size: 2rem; text-shadow: 0 0 10px #00FF7F; padding-bottom: 20px; }
    
    .card-alerta { padding: 15px; border-radius: 12px; margin-bottom: 10px; background-color: #111111; border: 1px solid #333; }
    .critico { border-left: 12px solid #FF0000; }
    .alerta { border-left: 12px solid #FF8C00; }
    .normal { border-left: 12px solid #00FF7F; }
    
    .ia-badge { background: linear-gradient(90deg, #00FF7F, #0077ff); color: white !important; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; }
    .sensor-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-top: 10px; }
    .sensor-val { font-weight: bold; color: #00FF7F !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='titulo-noah'>NOAH AGRO - MONITORAMENTO PREDITIVO</h1>", unsafe_allow_html=True)

# 3. Lógica de IA e Geração de Dados (Muda a cada refresh)
def gerar_dados_vivos():
    setores = [
        {"nome": "SETOR NORTE", "lat": -22.90, "lon": -43.20, "gestor": "RICARDO", "tel": "5521999999999"},
        {"nome": "SETOR SUL", "lat": -22.95, "lon": -43.25, "gestor": "ANA", "tel": "5521888888888"},
        {"nome": "ESTUFA 01", "lat": -22.85, "lon": -43.15, "gestor": "MARCOS", "tel": "5521777777777"},
        {"nome": "ÁREA OESTE", "lat": -22.82, "lon": -43.12, "gestor": "BEATRIZ", "tel": "5521666666666"}
    ]
    data = []
    for s in setores:
        # Valores aleatórios para simular sensores em tempo real
        u = np.random.randint(15, 85)
        p = np.random.randint(0, 50)
        ph = round(np.random.uniform(4.5, 8.5), 1)
        
        # Cálculo de Risco Preditivo
        risco = max(5, min(98, int((80 - u) * 0.8 + (abs(6.5 - ph) * 15))))
        
        if risco > 70: info = ["CRÍTICO", "#FF0000", "critico", 1]
        elif risco > 40: info = ["MODERADO", "#FF8C00", "alerta", 2]
        else: info = ["NORMAL", "#00FF7F", "normal", 3]
            
        s.update({"umid": u, "pluv": p, "ph": ph, "risco": risco, "status": info[0], "cor": info[1], "classe": info[2], "peso": info[3]})
        data.append(s)
    # Ordenar por prioridade (Peso 1 primeiro)
    return sorted(data, key=lambda x: x['peso'])

# 4. Execução e Layout
dados = gerar_dados_vivos()
col_mapa, col_cards = st.columns([1.2, 1])

with col_mapa:
    st.markdown("### 🌐 LOCALIZAÇÃO EM TEMPO REAL")
    df_mapa = pd.DataFrame(dados)
    st.map(df_mapa, latitude='lat', longitude='lon', color='cor', size=500)

with col_cards:
    st.markdown("### 🚨 ALERTAS E GESTÃO")
    for d in dados:
        # Card Visual
        st.markdown(f"""
            <div class="card-alerta {d['classe']}">
                <div style="display: flex; justify-content: space-between;">
                    <b>{d['nome']}</b>
                    <span class="ia-badge">IA PREDICT</span>
                </div>
                <div style="margin-top:8px;">
                    <small>PROBABILIDADE DE RISCO (24H): {d['risco']}%</small>
                    <div style="background:#222; height:8px; border-radius:5px; margin-top:5px;">
                        <div style="width:{d['risco']}%; background:{d['cor']}; height:8px; border-radius:5px;"></div>
                    </div>
                </div>
                <div class="sensor-grid">
                    <div><small>UMID.</small><br><span class="sensor-val">{d['umid']}%</span></div>
                    <div><small>PH</small><br><span class="sensor-val">{d['ph']}</span></div>
                    <div><small>STATUS</small><br><span style="color:{d['cor']} !important;">{d['status']}</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # BOTÃO DE CONTATO (Aparece se o risco for acima de 40%)
        if d['risco'] > 40:
            texto = urllib.parse.quote(f"🚨 ALERTA NOAH AGRO: {d['nome']} com risco de {d['risco']}%. Status: {d['status']}.")
            st.link_button(f"📲 FALAR COM {d['gestor']}", f"https://wa.me/{d['tel']}?text={texto}", use_container_width=True)

# 5. LOOP DE ATUALIZAÇÃO (Faz o sistema "viver")
time.sleep(8)
st.rerun()
