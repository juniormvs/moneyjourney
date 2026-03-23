import pandas as pd
import streamlit as st
import os
import sys

# Adiciona a raiz do projeto ao path para encontrar a pasta utils/
# Isso é necessário porque o dashboard.py está dentro de /pages
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa as funções de gráfico do utils/charts.py
# Cada função recebe um DataFrame e devolve uma figura Plotly

from utils.charts import (
    grafico_latencia,
    grafico_velocidade,
    grafico_tokens_por_interacao,
    grafico_proporcao_tokens,
    grafico_feedbacks
    
)

# ============================================================
# DASHBOARD DE MÉTRICAS — pages/dashboard.py
#
# Responsabilidade ÚNICA deste arquivo:
# Carregar os dados, aplicar filtros e exibir os gráficos.
#
# O que este arquivo NÃO faz:
# - Não define como os gráficos são construídos (isso é o charts.py)
# - Não faz cálculos complexos
# ============================================================

st.set_page_config(
    page_title='Dashboard de Métricas',
    page_icon='📊',
    layout='wide'
)

st.title('📊 Dashboard de Métricas do Agente Money Journey')

ARQUIVO_METRICAS = 'data/metricas.csv'

# ============================================================
# 1. VERIFICAR SE O ARQUIVO DE MÉTRICAS EXISTE
# ============================================================
if not os.path.exists(ARQUIVO_METRICAS):
    st.info('Nenhuma métrica registrada ainda. Faça sua primeira pergunta no chat')
    st.page_link('app.py', label='💬 Ir para o Chat', icon='💬')
    st.stop()


# ============================================================
# 2. CARREGAR O CSV
# ============================================================

def carregar_metricas():
    return pd.read_csv(ARQUIVO_METRICAS, parse_dates=['timestamp'])

df = carregar_metricas()  # ← carrega primeiro
df_completo = df.copy()   # ← copia antes de qualquer filtro




# ============================================================
# 3. SIDEBAR — FILTROS E NAVEGAÇÃO
# ============================================================

with st.sidebar:
    st.header('🔎 Filtros')

    data_min = df['timestamp'].min().date()
    data_max = df['timestamp'].max().date()

    datas = st.date_input(
    'Período',
    value     = (data_min, data_max),
    min_value = data_min,
    max_value = data_max,
)

    # Só aplica o filtro se as duas datas estiverem preenchidas
    if len(datas) == 2:
        data_inicio, data_fim = datas
        df = df[
            (df['timestamp'].dt.date >= data_inicio) &
            (df['timestamp'].dt.date <= data_fim)
        ]
    else:
        st.warning('Selecione as duas datas para filtrar o período.')
        st.stop()


    st.divider()
    st.metric('Total de interações', len(df))
    st.divider()

    # Link para voltar ao chat
    st.markdown('<a href="/" target="_self">💬 Voltar para o Chat</a>', unsafe_allow_html=True)


# ============================================================
# 4. KPIs — CARTÕES DE RESUMO NO TOPO
# ============================================================
st.subheader('📌 Resumo do Período')

col1,col2,col3,col4,col5 = st.columns(5)

col1.metric('⏱️ Latência Média',         f'{df["latencia_s"].mean():.2f}s')
col2.metric('⚡ Tokens/s Médio',          f'{df["tokens_por_segundo"].mean():.1f}')
col3.metric('🔢 Tokens Médios/Interação', f'{df["tokens_total"].mean():.0f}')
col4.metric('👍 Feedbacks Positivos',     len(df[df['feedback'] == 'positivo']))
col5.metric('⚠️ Fora do Escopo',          len(df[df['fora_do_escopo'] == True]))


st.divider()


# ============================================================
# 5. GRÁFICOS
# Cada st.plotly_chart() recebe o retorno da função do charts.py.
# use_container_width=True faz o gráfico ocupar toda a largura disponível.
# ============================================================

# --- Linha 1: Latência e Velocidade lado a lado ---
col_a, col_b = st.columns(2)

with col_a:
    st.plotly_chart(
        grafico_latencia(df),
        use_container_width=True,
    )
with col_b:
    st.plotly_chart(
        grafico_velocidade(df),
        use_container_width=True
    )

# --- Linha 2: Tokens por interação (largura total) ---
st.plotly_chart(
    grafico_tokens_por_interacao(df),
    use_container_width=True
)

# --- Linha 3: Proporção e Feedbacks lado a lado ---
col_c, col_d = st.columns(2)
with col_c:
    st.plotly_chart(
        grafico_proporcao_tokens(df),
        use_container_width=True,
    )
with col_d:
    st.plotly_chart(
        grafico_feedbacks(df),
        use_container_width=True
    )
    #Taxa de satisfação abaixo do gráfico de feedbacks
    positivos = len(df[df['feedback'] == 'positivo'])
    negativos = len(df[df['feedback'] == 'negativo'])
    total_com_feedback = positivos + negativos

    if total_com_feedback > 0:
        taxa = positivos / total_com_feedback * 100
        st.metric('✅ Taxa de Satisfação', f'{taxa:1f}%')
    else:
        st.caption('Nenhum feedback registrado ainda.')

st.divider()


# ============================================================
# 6. TABELA COMPLETA + EXPORTAÇÃO
# ============================================================

with st.expander('🗂️ Ver todos os registros'):
    st.dataframe(
        df_completo.sort_values('timestamp', ascending=False),
        use_container_width=True,
    )

    csv_export = df_completo.to_csv(index=False).encode('utf-8')
    st.download_button(
        label='⬇️ Baixar métricas filtradas (CSV)',
        data = csv_export,
        file_name='metricas_exportadas.csv',
        mime='text/csv'
    )