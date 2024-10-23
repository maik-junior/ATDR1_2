#==> Importando bibliotecas
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsbombpy import sb

#==> Carrega competicoes e jogos diponiveis
@st.cache_data
def load_competitions():
    competitions = sb.competitions()
    return competitions

#==> Carrega jogos de um competicao especifica
@st.cache_data
def load_matches(competition_id, season_id):
    matches = sb.matches(competition_id=competition_id, season_id=season_id)
    return matches

#==> Carrega eventos de um jogo especifico
@st.cache_data
def load_events(match_id):
    events = sb.events(match_id=match_id)
    return events

def dados_jogador(nome_competicao):
    #==> Carregando dados das competicoes
    st.title("Análise de Métricas de Jogadores - StatsBomb")
    competitions = load_competitions()
    
    #==> Definindo competicao
    competition_name = nome_competicao
    selected_competition = competitions[competitions['competition_name'] == competition_name].iloc[0]
    season_id = selected_competition['season_id']
    
    #==> Carregar jogos da competicao
    matches = load_matches(selected_competition['competition_id'], season_id)
    match_date = st.session_state.data_partida
    match_date = matches['match_date'].unique()
    selected_match = matches[matches['match_date'] == match_date].iloc[0]
    
    #==> Carregar eventos do jogo
    events = load_events(selected_match['match_id'])
    player_names = events['player'].dropna().unique()
    selected_player = st.selectbox("Selecione o jogador", player_names, key=12)
    
    #==> Eventos do jogador selecionado
    player_events = events[events['player'] == selected_player]
    
    #==> Mostrar estatisticas basicas
    st.subheader(f"Estatísticas de {selected_player}")
    st.write(player_events.groupby('type')['type'].count())



