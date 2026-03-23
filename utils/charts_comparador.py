import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# utils/charts_comparador.py
#
# Responsabilidade ÚNICA deste arquivo:
# Gráficos específicos para comparação entre modelos de LLM.
#
# Separado do charts.py para manter cada arquivo com
# responsabilidade única e facilitar manutenção.
# ============================================================

def grafico_comparacao_latencia(df: pd.DataFrame) -> go.Figure:
    """Gráfico de barras — Latência média por modelo.

    Permite comparar visualmente qual modelo responde mais rápido.

    Parâmetros:
        df (pd.DataFrame): DataFrame com colunas 'modelo' e 'latencia_s'

    Returns:
        go.Figure: objeto Figure do Plotly
    """
    # Agrupa por modelo e calcula a média de latência
    media = df.groupby('modelo')['latencia_s'].mean().reset_index()
    media.columns = ['modelo', 'latencia_media']
    media = media.sort_values('latencia_media') # ordena do mais rápido ao mais lento

    fig = px.bar(
        media,
        x = 'modelo',
        y = 'latencia_media',
        title = '⏱️ Latência Média por Modelo (segundos)',
        labels={
            'modelo': 'Modelo',
            'latencia_media':'Latência Média (s)',
        },
        color = 'modelo', # cada modelo com uma cor diferente
        color_discrete_sequence = px.colors.qualitative.Set2,
        text_auto = '.2f', #exibe o valor em cima de cada barra
    )

    fig.update_layout(
        showlegend = False, #Legenda desnecessária, o eixo X já identifica
        xaxis_title = 'Modelo',
        yaxis_title = 'Segundos',
    )

    return fig

def grafico_comparacao_velocidade(df: pd.DataFrame) -> go.Figure:
    """
    Gráfico de barras — Velocidade média (tokens/segundo) por modelo.

    Diferente da latência — mede a velocidade de geração real,
    independente do tamanho da resposta.

    Parâmetros:
        df: DataFrame com colunas 'modelo' e 'tokens_por_segundo'

    Retorna:
        fig: objeto Figure do Plotly
    """
    media = df.groupby('modelo')['tokens_por_segundo'].mean().reset_index()
    media.columns = ['modelo', 'velocidade_media']
    media = media.sort_values('velocidade_media', ascending=False) # mais rápido primeiro

    fig = px.bar(
        media,
        x = 'modelo',
        y = 'velocidade_media',
        title = '⚡ Velocidade Média por Modelo (tokens/s)',
        labels = {
            'modelo': 'Modelo',
            'velocidade_media': 'Tokens/Segundo',
        },
        color = 'modelo',
        color_discrete_sequence = px.colors.qualitative.Set2,
        text_auto = '.1f',
    )

    fig.update_layout(
        showlegend = False,
        xaxis_title = 'Modelo',
        yaxis_title = 'Tokens/segundo'
    )
    
    return fig

def grafico_comparacao_tokens(df: pd.DataFrame) -> go.Figure:
    """
    Gráfico de barras agrupadas — Tokens médios por modelo.

    Compara prompt e resposta lado a lado para cada modelo.
    Útil para entender qual modelo é mais "econômico".

    Parâmetros:
        df: DataFrame com colunas 'modelo', 'tokens_prompt', 'tokens_resposta'

    Retorna:
        fig: objeto Figure do Plotly
    """
    # Calcula média por modelo
    media = df.groupby('modelo')[['tokens_prompt', 'tokens_resposta']].mean().reset_index()

    # Converte para formato longo para o Plotly separar as barras por tipo
    df_long = media.melt(
        id_vars = 'modelo',
        value_vars = ['tokens_prompt', 'tokens_resposta'],
        var_name = 'tipo',
        value_name ='tokens',
    )

    df_long['tipo'] = df_long['tipo'].map({
        'tokens_prompt': '📥 Prompt',
        'tokens_resposta': '📤 Resposta',
    })

    fig = px.bar(
        df_long,
        x = 'modelo',
        y= 'tokens',
        color= 'tipo',
        barmode='group',
        title= '🔢 Tokens Médios por Modelo',
        labels= {
            'modelo': 'Modelo',
            'tokens': 'Tokens',
            'tipo': 'Tipo',
        },
        color_discrete_map={
            '📥 Prompt':   '#636EFA',
            '📤 Resposta': '#EF553B',
        },
        text_auto= '.0f',
    )

    fig.update_layout(
        xaxis_title = 'Modelo',
        yaxis_title = 'Tokens',
        legend_title = 'Tipo',
    )

    return fig

def grafico_radar_modelos(df: pd.DataFrame) -> go.Figure:
    """
    Gráfico radar — Comparação geral entre modelos.

    Normaliza as métricas para uma escala de 0 a 1 e plota
    cada modelo como um polígono. Quanto maior a área, melhor.

    Métricas usadas:
    - Velocidade (tokens/s) → maior é melhor
    - Tokens de resposta    → maior é melhor (mais detalhado)
    - Latência invertida    → menor latência = maior pontuação

    Parâmetros:
        df: DataFrame com colunas 'modelo', 'tokens_por_segundo',
            'tokens_resposta', 'latencia_s'

    Retorna:
        fig: objeto Figure do Plotly
    """
    # Calcula médias por modelo
    media = df.groupby('modelo').agg(
        velocidade = ('tokens_por_segundo', 'mean'),
        resposta   = ('tokens_resposta',    'mean'),
        latencia   = ('latencia_s',         'mean'),
    ).reset_index()

    # Normaliza cada métrica para 0-1
    # Velocidade e resposta: maior = melhor → divide pelo máximo
    # Latência: menor = melhor → inverte (1 - normalizado)
    def normalizar(serie, inverter=False):
        min_v = serie.min()
        max_v = serie.max()
        if max_v == min_v:          # evita divisão por zero se todos iguais
            return pd.Series([0.5] * len(serie))
        norm = (serie - min_v) / (max_v - min_v)
        return 1 - norm if inverter else norm

    media['vel_norm']  = normalizar(media['velocidade'])
    media['resp_norm'] = normalizar(media['resposta'])
    media['lat_norm']  = normalizar(media['latencia'], inverter=True)

    categorias = ['Velocidade', 'Detalhe da Resposta', 'Baixa Latência']

    fig = go.Figure()

    # Adiciona um polígono para cada modelo
    for _, row in media.iterrows():
        valores = [row['vel_norm'], row['resp_norm'], row['lat_norm']]
        valores += [valores[0]]          # fecha o polígono repetindo o primeiro valor
        cats    = categorias + [categorias[0]]

        fig.add_trace(go.Scatterpolar(
            r    = valores,
            theta= cats,
            fill = 'toself',
            name = row['modelo'],
        ))

    fig.update_layout(
        title = '🕸️ Comparação Geral entre Modelos (Radar)',
        polar = dict(
            radialaxis = dict(
                visible = True,
                range   = [0, 1],
            )
        ),
        showlegend = True,
    )

    return fig


def grafico_historico_comparativo(df: pd.DataFrame) -> go.Figure:
    """
    Gráfico de linhas — Latência ao longo do tempo por modelo.

    Mostra a evolução da latência de cada modelo nas comparações
    realizadas, permitindo ver consistência e variação.

    Parâmetros:
        df: DataFrame com colunas 'timestamp', 'modelo', 'latencia_s'

    Retorna:
        fig: objeto Figure do Plotly
    """
    fig = px.line(
        df,
        x       = 'timestamp',
        y       = 'latencia_s',
        color   = 'modelo',      # uma linha por modelo
        markers = True,
        title   = '📈 Histórico de Latência por Modelo',
        labels  = {
            'timestamp':  'Horário',
            'latencia_s': 'Latência (s)',
            'modelo':     'Modelo',
        },
    )

    fig.update_layout(
        xaxis_title  = 'Horário',
        yaxis_title  = 'Segundos',
        hovermode    = 'x unified',
        legend_title = 'Modelo',
    )

    return fig
