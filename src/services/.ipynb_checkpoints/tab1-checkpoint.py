#==> Importando bibliotecas
from statsbombpy import sb
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def _tab1(events_id):
    eventos = pd.DataFrame(events_id)
    resultado = eventos[['team_id', 'shot_outcome', 'team']].groupby(['shot_outcome', 'team']).count().reset_index()
    dt = resultado.loc[resultado['shot_outcome'] == 'Goal', :]
    
    st.subheader('Gols')
    #==> Criando duas colunas para os gráficos de pizza
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label=dt.loc[dt.index[0],'team'], value=dt.loc[dt.index[0],'team_id'])
    with col2:
        if dt.shape[0] > 1:
            st.metric(label=dt.loc[dt.index[1],'team'], value=dt.loc[dt.index[1],'team_id'])

    st.markdown('---')
    #==> Criando duas colunas para os gráficos de pizza
    col1, col2 = st.columns(2)

    #==> Grafico pizza de posse de bola
    with col1:
        st.subheader('Posse de bola')
        team_counts = eventos[['possession', 'team']].groupby('team').team.count()
        fig, ax = plt.subplots(figsize=(15, 15))
        fig.patch.set_facecolor('#2D694D')
        ax.pie(team_counts, labels=team_counts.index, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 50})
        ax.axis('equal')
        st.pyplot(fig);

    #==> Grafico pizza de jogadas
    with col2:
        st.subheader('Jogada Predominante')
        duel_count = eventos.groupby('duel_type').size()
        #==> Grafico pizza de jogadas
        fig.patch.set_facecolor('#2D694D')
        ax.pie(duel_count, labels=duel_count.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig);

    st.markdown('---')
    st.subheader('Jogadores mais Requisitados em Campo')
    player_team_count = eventos[['player_id', 'player', 'team']].groupby(['player', 'team']).count().sort_values(by='player_id', ascending=False)

    #==> Grafico de barras
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#2D694D')
    ax.set_facecolor('#2D694D')
    player_team_count['player_id'].plot(kind='bar', ax=ax, figsize=(10, 6))
    ax.set_xlabel('Jogador e Equipe')
    ax.set_ylabel('Contagem de Eventos')
    ax.set_title('Eventos por Jogador e Equipe')
    plt.xticks(rotation=90)
    st.pyplot(fig);

    st.markdown('---')