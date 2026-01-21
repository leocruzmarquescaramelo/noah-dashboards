import streamlit as st
import pandas as pd
import numpy as np
import time
import urllib.parse

# Configuração da Página
st.set_page_config(layout="wide", page_title="NOAH | COMMAND CENTER", initial_sidebar_state="collapsed")

# --- CSS DE ALTA VISIBILIDADE (SALA DE COMANDO) ---
st.markdown("""
<style>
    /* Fundo Total Preto Profundo */
    .stApp {
        background-color: #000000;
    }
    
    /* Forçar todo texto padrão para Branco */
    div[data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif;
    }

    /* Título com brilho Ciano */
    .titulo-noah {
        color: #00FFFF;
        font-family: 'Orbitron', sans-serif;
        font-size: 2.5rem;
        text-align: center;
        text-shadow: 0 0 15px #00FFFF;
        margin-bottom: 30px;
        letter-spacing: 2px;
    }

    /* Subtítulos em Branco Neve */
    h3, h2, h1 {
        color: #FFFFFF !important;
        font-weight: bold !important;
    }

    /* Estilo dos Cards - Fundo Grafite para destacar do fundo preto */
    .card {
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        background-color: #1A1A1A; /* Cinza muito escuro mas visível sobre o preto */
        border: 1px solid #333333;
    }

    /* Texto dentro dos Cards */
    .card b, .card span, .card small {
        color: #FFFFFF !important; /* Força tudo para branco */
    }

    /* Cores das Bordas Neon */
    .critico { border-left: 12px solid #FF0000; box-shadow: -10px 0 20px rgba(255, 0, 0, 0.4); }
    .alerta { border-left: 12px solid #FF8C00; box-shadow: -10px 0 20px rgba(255, 140, 0, 0.3); }
    .atencao { border-left: 12px solid #FFFF00; box-shadow: -10px 0 20px rgba(255, 255, 0, 0.2); }
    .normal { border-left: 12px solid #00FF00; }

    /* Tags de Status com Contraste Inteligente */
    .status-tag {
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: 900;
        font-size: 0.8em;
        text-transform: uppercase;
    }

    /* Tensão em tamanho grande e branco */
    .tensao-valor {
        font-size: 35px;
        font-family: 'monospace';
        color: #FFFFFF !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 class='titulo-noah'>NOAH COMMAND & CONTROL</h1>", unsafe_allow_html=True)

# --- DADOS E LÓGICA ---
gestores = {
    "Centro": {"nome": "Carlos Silva", "tel": "5521999999999", "email": "carlos@noah.com"},
    "Copacabana": {"nome": "Ana Souza", "tel": "5521888888888", "email": "ana@noah.com"},
    "Barra": {"nome": "Marcos Rocha", "tel": "5521777777777", "email": "marcos@noah.com"},
    "Tijuca": {"nome": "Paula Lima", "tel": "5521666666666", "email": "paula@noah.com"},
    "Madureira": {"nome": "Roberto Cruz", "tel": "5521555555555", "email": "roberto@noah.com"},
}

def get_config(tensao):
    if tensao < 190 or tensao > 240:
        return "CRÍTICO", "#FF0000", "🛑", 1, "critico", "#FFFFFF"
    elif 190 <= tensao <= 200 or 230 <= tensao <= 240:
        return "ALERTA", "#FF8C00", "⚠️", 2, "alerta", "#000000"
    elif 201 <= tensao <= 210:
        return "ATENÇÃO", "#FFFF00", "🟡", 3, "atencao", "#000000"
    else:
        return "NORMAL", "#00FF00", "✅", 4, "normal", "#000000"

ativos = [
    {"setor": "Centro", "lat": -22.904, "lon": -43.178},
    {"setor": "Copacabana", "lat": -22.974, "lon": -43.186},
    {"setor": "Barra", "lat": -23.000, "lon": -43.340},
    {"setor": "Tijuca", "lat": -22.924, "lon": -43.232},
    {"setor": "Madureira", "lat": -22.877, "lon": -43.336},
]

for a in ativos:
    a['tensao'] = np.random.randint(180, 255)
    status, cor, icone, ordem, classe, txt_cor = get_config(a['tensao'])
    a.update({"status": status, "color": cor, "icone": icone, "ordem": ordem, "classe": classe, "txt_cor": txt_cor})

df = pd.DataFrame(ativos).sort_values('ordem')

# --- LAYOUT ---
c_map, c_list = st.columns([1.7, 1])

with c_map:
    st.markdown("### 🌐 GEOPROCESSAMENTO DE REDE")
    st.map(df, latitude='lat', longitude='lon', color='color', size=300)

with c_list:
    st.markdown("### 📋 FILA DE PRIORIDADE")
    for _, r in df.iterrows():
        g = gestores[r['setor']]
        
        st.markdown(f"""
            <div class="card {r['classe']}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <b style="font-size: 1.4em; color: #FFFFFF;">{r['icone']} {r['setor'].upper()}</b>
                    <span class="status-tag" style="background-color: {r['color']}; color: {r['txt_cor']};">
                        {r['status']}
                    </span>
                </div>
                <div style="margin-top: 15px;">
                    <span class="tensao-valor">{r['tensao']}V</span>
                    <p style="margin: 5px 0 0 0; color: #FFFFFF; font-size: 0.9em;">
                        <b>RESPONSÁVEL:</b> {g['nome'].upper()}
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if r['status'] == "CRÍTICO":
            st.link_button(f"🚨 ESCALONAR VIA WHATSAPP", f"https://wa.me/{g['tel']}", use_container_width=True, type="primary")
        elif r['status'] in ["ALERTA", "ATENÇÃO"]:
            st.link_button(f"📧 NOTIFICAR POR E-MAIL", f"mailto:{g['email']}", use_container_width=True)

# Loop de atualização
time.sleep(5)
st.rerun()