
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# utils/charts.py
#
# Responsabilidade ÚNICA deste arquivo:
# Receber DataFrames e devolver figuras Plotly prontas para exibir.
#
# O que este arquivo NÃO faz:
# - Não importa Streamlit
# - Não lê arquivos CSV
# - Não exibe nada na tela
#
# Isso significa que cada função aqui pode ser testada e reutilizada
# em qualquer contexto — não só no Streamlit.
# ============================================================

def grafico_latencia(df: pd.DataFrame) -> go.Figure:
    """Gráfico de linha - Latêcia ao longo do tempo.

    Mostra como o tempo de resposta variou entre as interações.
    Picos indicam possíveis sobrecargas ao modelo ou na rede.

    Parâmetros:
    df (pd.DataFrame): Dataframe com solunas 'timestamp' e 'latencia_s'         

    Returna:
        go.Figure: fig: Objeto Figure do Plotly
    """
    fig = px.line(
        df,
        x = 'timestamp', #eixo x: momento da interação
        y = 'latencia_s',#eixo y: tempo em segundos
        title = '⏱️ Latência ao Longo do Tempo',
        labels ={
            'timestamp': 'Horário',
            'latencia_s': 'Latência (s)'
        },
        markers = True #exibe um ponto em cada interação
    )

    # Linha de referência horizontal - média do período
    # Ajuda a visualizar se um interação está acima ou abaixo do normal
    media = df['latencia_s'].mean()
    fig.add_hline(
        y= media,
        line_dash = 'dash', #liniha tracejada
        line_color = 'orange',
        annotation_text = f'Média: {media:.2f}s',
        annotation_position = 'top right'
    )

    # CORRETO
    fig.update_layout(
    xaxis_title = 'Horário',   # ← x-a-x-i-s
    yaxis_title = 'Segundos',
    hovermode   = 'x unified',
    )

    return fig
    
def grafico_tokens_por_interacao(df: pd.DataFrame) -> go.Figure:
    """Gráfico de barras agrupadas - Tokens por interação.

    Compara tokens de prompt e de resposta lado a lado.
    Se o prompt consumir muito mais que a resposta,
    o contexto pode estar inflado desnecessariamente.

    Parâmetros:
        df (pd.DataFrame): DataFrame com colunas 'timestamp', 'tokens_prompt', tokens_resposta

    Returna:
        go.Figure: fig objeto Figure do Plotly
    """
    # Plotly Express com múltiplas colunas exige formato "longo" (long format).
    # melt() transforma colunas em linhas — converte:
    #
    # timestamp | tokens_prompt | tokens_resposta
    # 10:00     | 850           | 120
    #
    # Para:
    # timestamp | tipo              | valor
    # 10:00     | tokens_prompt     | 850
    # 10:00     | tokens_resposta   | 120
    #
    # Isso permite que o Plotly separe as barras por 'tipo' automaticamente.

    df_long = df.melt(
        id_vars='timestamp',                             #coluna que permanece
        value_vars=['tokens_prompt', 'tokens_resposta'], #colunas que viram linhas
        var_name= 'tipo',                                # nome da nova coluna por categoria
        value_name='tokens'                              #nome da nova coluna de valor
    )

    #Substitui os nomes técnicos por textos legíveis na legenda
    df_long['tipo'] = df_long['tipo'].map({
    'tokens_prompt':   '📥 Prompt (contexto)',
    'tokens_resposta': '📤 Resposta gerada'   # ← 📤 saída
    })

    fig = px.bar(
        df_long,
        x = 'timestamp',
        y = 'tokens',
        color = 'tipo',     #separa as barras por tipo
        barmode = 'group',  #barras lado a lado (não empilhadas)
        title = '🔢 Tokens por Interação',
        labels = {
            'timestamp': 'Horário',
            'tokens': 'Tokens',
            'tipo': 'Tipo'
        },
    )

    fig.update_layout(
        xaxis_title = 'Horário',
        yaxis_title = 'Tokens',
        hovermode = 'x unified',
        legend_title = 'Tipo'
    )

    return fig

def grafico_velocidade(df: pd.DataFrame) -> go.Figure:
    """Gráfico de área - Velocidade de geração (tokens/segundo).

    Mede a velocidade real do modelo independente do tamanho da resposta.
    O preenchimento da área comunica 'volume de performance' visualmente

    Parâmetros:
        df (pd.DataFrame): df: Dataframe com colunas 'timestamp' e 'tokens_por_segundo'

    Returns:
        go.Figure: Objeto Figure do Plotly
    """

    fig = px.area(
        df,
        x = 'timestamp',
        y = 'tokens_por_segundo',
        title = '⚡ Velocidade de Geração (tokens/s)',
        labels = {
            'timestamp':'Horário',
            'tokens_por_segundo': 'Tokens/Segundo'
        },
    )

    #Personaliza a cor de preenchimento da área
    fig.update_traces(
        fillcolor = 'rgba(99, 110, 250, 0.2)', #azul translúcido
        line = dict(color='rgba(99,110,250,1)'),
    )

    fig.update_layout(
        xaxis_title = 'Horário',
        yaxis_title = 'Tokens/Segundo',
        hovermode = 'x unified',
    )

    return fig

def grafico_proporcao_tokens(df: pd.DataFrame) -> go.Figure:
    """
    Gráfico de rosca (donut) -> Proporção prompt vs Resposta.

    Mostra a relação percentual entre tokens gasto no contexto e
    tokens gerados na resposta. Rosca é mais legível que pizza
    para apenas duas categorias.

    Parâmetros:
        df (pd.DataFrame): df: DataFrame com colunas 'tokens_prompt' e 'tokens_resposta'

    Returna:
        go.Figure: Objeto Figure do Plotly
    """

    media_prompt = df['tokens_prompt'].mean()
    media_resposta = df['tokens_resposta'].mean()

    #go.Pie com hole > 0 vira um gráfico de rosca (donut)
    fig = go.Figure(
        go.Pie(
            labels = ['📥 Prompt (contexto)', '📤 Resposta gerada'],
            values = [media_prompt, media_resposta],
            hole = 0.5, #0 = pizza, 0.5 = rosca (donut), 1 = invisível
            textinfo = 'label+percent', #exibe label e percentual em cada fatia

        )
    )

    fig.update_layout(
        title = '📊 Proporção Média: Prompt vs Resposta',
        # Anotação central dentro do buraco da rosca
        annotations = [dict(
            text = f'{media_prompt + media_resposta:.0f}<br>tokens',
            x = 0.5,
            y = 0.5,
            font_size = 14,
            showarrow = False,   
        )]
    )

    return fig

def grafico_feedbacks(df: pd.DataFrame) -> go.Figure:
    """
    Gráfico de barras horizontais - Hisórico de feedbacks.

    Barras horizontais funcionam melhor que verticais quando
    os rótulos do eixo são textos longos - evita sobreposição.

    Parâmetros:
        df (pd.DataFrame): df Datrame com coluna 'feedback'

    Returna:
        go.Figure: Objeto Figure do Plotly
    """

    # Conta quantas vezes cada valor aparece na coluna feedback
    contagem = df['feedback'].value_counts().reset_index()

    contagem.columns = ['feedback', 'quantidade']

    # Mapa de cores por tipo de feedback
    # Plotly aceita um dicionário mapeando valor -> cor
    color_map = {
        'positivo': '#2ecc71',    # verde
        'negativo': '#e74c3c',    #vermelho
        'sem_feedback': '#95a5a6' #cinza
    }

    # Substitui os valores técnicos por textos amigáveis
    emoji_map={
        'positivo': '👍 Positivo',
        'negativo': '👎 Negativo',
        'sem_feedback': '➖ Sem Feedback',
    }
    contagem['feedback_label'] = contagem['feedback'].map(
        lambda x: emoji_map.get(x, x)
    )

    contagem['cor'] = contagem['feedback'].map(
        lambda x: color_map.get(x, '#95a5a6')
    )

    # Orientation='h' vira as barras na horizontal
    #x e y são invertidos em relação ao gráfico vertical
    fig = go.Figure(
    go.Bar(
        x            = contagem['quantidade'].tolist(),
        y            = contagem['feedback_label'].tolist(),
        orientation  = 'h',
        marker_color = contagem['cor'].tolist(),        # ← .tolist()
        text         = contagem['quantidade'].tolist(),
        textposition = 'auto',
    )
)
    # Se quer esconder completamente o título do eixo Y
    fig.update_layout(
        title       = '💬 Distribuição de Feedbacks',
        xaxis_title = 'Quantidade',
        yaxis       = dict(title=''),  # ← se precisar usar yaxis diretamente
    )

    return fig