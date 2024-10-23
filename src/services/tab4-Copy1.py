import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsbombpy import sb

# Função para carregar os competições e jogos disponíveis
def load_competitions():
    competitions = sb.competitions()
    return competitions

# Função para carregar jogos de uma competição específica
def load_matches(competition_id, season_id):
    matches = sb.matches(competition_id=competition_id, season_id=season_id)
    return matches

# Função para carregar eventos de um jogo específico
def load_events(match_id):
    events = sb.events(match_id=match_id)
    return events


def dados_jogador(nome_competicao):
    # Carregando dados das competições
    st.title("Análise de Métricas de Jogadores - StatsBomb")
    competitions = load_competitions()
    
    # Selecionar competição
    competition_name = nome_competicao
    selected_competition = competitions[competitions['competition_name'] == competition_name].iloc[0]
    season_id = selected_competition['season_id']
    # competition_name = st.selectbox("Selecione a competição", competitions['competition_name'].unique(), key=10)
    # selected_competition = competitions[competitions['competition_name'] == competition_name].iloc[0]
    # season_id = selected_competition['season_id']
    
    # Carregar jogos da competição selecionada
    matches = load_matches(selected_competition['competition_id'], season_id)
    match_date = st.session_state.data_partida
    match_date = matches['match_date'].unique()
    # match_date = st.selectbox("Selecione o jogo pela data", matches['match_date'].unique(),key=11)
    selected_match = matches[matches['match_date'] == match_date].iloc[0]
    
    # Carregar eventos do jogo selecionado
    events = load_events(selected_match['match_id'])
    player_names = events['player'].dropna().unique()
    selected_player = st.selectbox("Selecione o jogador", player_names, key=12)
    
    # Filtrar eventos do jogador selecionado
    player_events = events[events['player'] == selected_player]
    
    # Mostrar estatísticas básicas
    st.subheader(f"Estatísticas de {selected_player}")
    st.write(player_events.groupby('type')['type'].count())

