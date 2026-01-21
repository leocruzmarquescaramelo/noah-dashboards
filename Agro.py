import streamlit as st
import pandas as pd
import numpy as np
import time
import urllib.parse

# 1. Configuração de Interface
st.set_page_config(layout="wide", page_title="NOAH AGRO | CONTROL CENTER", initial_sidebar_state="collapsed")

# 2. CSS: Visual Sala de Comando (Letras Brancas e Fundo Preto)
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    h1, h2, h3, h4, p, span, b, small, .stMarkdown, label { 
        color: #FFFFFF !important; 
        font-family: 'Inter', sans-serif; 
    }
    .titulo-noah { 
        color: #00FF7F; 
        text-align: center; 
        font-size: 2.5rem; 
        text-shadow: 0 0 15px #00FF7F; 
        padding: 20px; 
    }
    .card-alerta { 
        padding: 20px; 
        border-radius: 12px; 
        margin-bottom: 15px; 
        background-color: #111111; 
        border: 1px solid #333; 
    }
    .critico { border-left: 15px solid #FF0000; box-shadow: -10px 0 20px rgba(255, 0, 0, 0.4); }
    .alerta { border-left: 15px solid #FF8C00; box-shadow: -10px 0 20px rgba(255, 140, 0, 0.3); }
    .normal { border-left: 15px solid #00FF7F; }
    .sensor-box { 
        display: flex; 
        justify-content: space-between; 
        margin-top: 15px; 
        padding: 10px; 
        background: #1A1A1A; 
        border-radius: 8px; 
    }
    .sensor-label { font-size: 0.8rem; color: #888 !important; }
    .sensor-valor { font-size: 1.4rem; font-weight: bold; color: #FFF !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='titulo-noah'>NOAH AGRO - CONTROLE DE PRIORIDADE</h1>", unsafe_allow_html=True)

# --- GESTORES ---
gestores = {
    "SETOR NORTE": {"nome": "RICARDO", "tel": "5521999999999"},
    "SETOR SUL": {"nome": "ANA PAULA", "tel": "5521888888888"},
    "ESTUFA 01": {"nome": "MARCOS", "tel": "5521777777777"},
    "ÁREA OESTE": {"nome": "BEATRIZ", "tel": "5521666666666"}
}

# 3. Lógica de Dados e Ordenação (Critico primeiro)
def get_data():
    pontos = ["SETOR NORTE", "SETOR SUL", "ESTUFA 01", "ÁREA OESTE"]
    lista = []
    for p in pontos:
        umid = np.random.randint(10, 85)
        pluv = np.random.randint(0, 100)
        ph = round(np.random.uniform(4.0, 9.0), 1)
        
        if umid < 20 or ph < 4.8 or ph > 8.2:
            status, classe, cor, peso = "CRÍTICO", "critico", "#FF0000", 1
        elif umid < 40:
            status, classe, cor, peso = "ALERTA", "alerta", "#FF8C00", 2
        else:
            status, classe, cor, peso = "NORMAL", "normal", "#00FF7F", 3
            
        lista.append({
            "setor": p, "umid": umid, "pluv": pluv, "ph": ph, 
            "status": status, "classe": classe, "cor": cor, "peso": peso
        })
    # Ordena pelo peso (1 Crítico, 2 Alerta, 3 Normal)
    return sorted(lista, key=lambda x: x['peso'])

dados = get_data()

# 4. Exibição em Colunas
c1, c2 = st.columns([1.3, 1])

with c1:
    st.markdown("### 🌐 MAPA OPERACIONAL")
    df_mapa = pd.DataFrame(dados)
    # Coordenadas fixas para evitar erros de lista
    df_mapa['lat'] = [-22.90, -22.95, -22.85, -22.82]
    df_mapa['lon'] = [-43.20, -43.25, -43.15, -43.12]
    st.map(df_mapa, latitude='lat', longitude='lon', color='cor', size=500)

with c2:
    st.markdown("### 🚨 FILA DE PRIORIDADE")
    for d in dados:
        g = gestores[d['setor']]
        st.markdown(f"""
            <div class="card-alerta {d['classe']}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <b style="font-size:1.2rem;">{d['setor']}</b>
                    <b style="color: {d['cor']} !important;">{d['status']}</b>
                </div>
                <div class="sensor-box">
                    <div><small class="sensor-label">UMIDADE</small><br><span class="sensor-valor">{d['umid']}%</span></div>
                    <div><small class="sensor-label">PLUVIO.</small><br><span class="sensor-valor">{d['pluv']}mm</span></div>
                    <div><small class="sensor-label">pH</small><br><span class="sensor-valor">{d['ph']}</span></div>
                </div>
                <p style="margin-top:10px; font-size:0.8rem; color:#888 !important;">GESTOR: {g['nome']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if d['status'] != "NORMAL":
            msg = urllib.parse.quote(f"🚨 ALERTA NOAH: {d['setor']} em {d['status']}! Umid: {d['umid']}%, pH: {d['ph']}.")
            st.link_button(f"📲 ACIONAR {g['nome']}", f"https://wa.me/{g['tel']}?text={msg}", use_container_width=True)

# 5. Download e Refresh
st.sidebar.markdown("### 📊 RELATÓRIOS")
df_rel = pd.DataFrame(dados).drop(columns=['classe', 'cor', 'peso'])
st.sidebar.download_button("📥 BAIXAR LOG CSV", df_rel.to_csv(index=False).encode('utf-8'), "noah_agro.csv")

time.sleep(5)
st.rerun()