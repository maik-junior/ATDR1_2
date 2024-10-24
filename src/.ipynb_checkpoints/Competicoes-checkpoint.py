#==> Importando bibliotecas
import streamlit as st
import matplotlib.pyplot as plt
from statsbombpy import sb
import pandas as pd
from services.tab1 import _tab1
from services.tab4 import dados_jogador

#==> Configuração de página
st.set_page_config(
    page_title='Página Inicial',
    page_icon='⚽',
    layout='centered',
    initial_sidebar_state='expanded'
)

import os
import streamlit as st

# Obtendo o caminho absoluto
image_path = os.path.join(os.getcwd(), 'data/image/image1.jpeg')
st.sidebar.image(image_path, width=280)

# st.sidebar.image('data/image/image1.jpeg', width=280)

#==> Carregando em cache
@st.cache_data
def get_competitions():
    return sb.competitions()

@st.cache_data
def get_matches(competition_id, season_id):
    return sb.matches(competition_id=competition_id, season_id=season_id)

@st.cache_data
def get_events(match_id):
    return sb.events(match_id=match_id)

@st.cache_data
def get_lineups(match_id, team):
    return pd.DataFrame(sb.lineups(match_id=match_id)[team]).drop(columns=['player_nickname', 'cards'])

#==> Inicializa o estado de sessão
def init_session_state(dataframe):
    if 'matches' not in st.session_state:
        st.session_state.matches = dataframe

    if 'selected_columns' not in st.session_state:
        st.session_state.selected_columns = dataframe.columns.tolist() if not dataframe.empty else []

#==> Função principal
def Competicoes():
    #==> Criando sidebar
    competitions = get_competitions()
    competition = st.sidebar.selectbox("Selecione a competição", competitions["competition_name"].unique())
    
    #==> Nome da competição
    st.title(competition)
    
    #==> Recuperando id da competição
    competition_id = competitions[competitions["competition_name"] == competition]["competition_id"].values[0]

    with st.form('form'):
        
        col1, col2 = st.columns(2)
            
        with col1:
            seasons = competitions[competitions["competition_name"] == competition]["season_name"].unique()           
            season_name = st.selectbox('Selecione a temporada', seasons, key=2)                                      
            season_id = competitions[competitions["season_name"] == season_name]["season_id"].values[0]
                   
        with col2:
            def get_match_label(matches, match_id):
                row = matches[matches["match_id"] == match_id].iloc[0]
                return f"{row['match_date']} - {row['home_team']} vs {row['away_team']}"
        
            matches = get_matches(competition_id=competition_id, season_id=season_id)  # Usando cache
            id = st.selectbox('Selecione o jogo', matches["match_id"], format_func=lambda idx: get_match_label(matches, idx), key=3) 
            date = matches.loc[0,'match_date']
            #==> Armazenando data na sessao
            if 'data_partida' not in st.session_state:
                st.session_state.data_partida = date

        submit_btn = st.form_submit_button('Confirmar')
        
    
    #==> Criando DataFrame da partida
    df_partida = pd.DataFrame(matches[['match_id', 'home_team', 'away_team']])
    df_partida = df_partida.reset_index(drop=False)
    df_partida = df_partida.loc[df_partida['match_id'] == id, :]
    
    index = int(df_partida[['index']][:1].values)
    
    #==> Recuperando dados
    _id = df_partida['match_id'][index]
    home_team = df_partida['home_team'][index]
    away_team = df_partida['away_team'][index]
    
    #==> Abas
    tab1, tab2, tab3, tab4 = st.tabs(['Partida', 'Time Mandante', 'Time Visitante', 'Dados do jogador'])
    
    with tab1:
        _tab1(get_events(_id))

        matches = matches[['match_id', 'match_date', 'kick_off', 'competition', 'season', 'home_team', 'away_team', 'home_score', 'away_score']]
        
        #==> Partidas da temporada
        st.header('Todas Partidas da Temporada')
        
        #==> Selecionar colunas
        selected_columns = st.multiselect(
            'Selecione os dados desejados',
            options=matches.columns,
            default=matches.columns.tolist()
        )
        
        #==> Inicializando o estado da sessão
        init_session_state(matches)
        
        #==> Atualiza as colunas selecionadas
        st.session_state.selected_columns = selected_columns
        
        #==> Exibe o DataFrame
        st.dataframe(matches[st.session_state.selected_columns])
   
    with tab2:
        #==> Time mandante
        st.title(f'Time: {home_team} - Mandante')
        time_mandante = get_lineups(_id, home_team)  # Usando cache
        time_mandante['positions'] = time_mandante['positions'].apply(lambda x: x[0]['position'] if isinstance(x, list) and len(x) > 0 else None)
        time_mandante['player_id'] = time_mandante['player_id'].astype(str)
        st.write(time_mandante)

    
    with tab3:
        #==> Time visitante
        st.title(f'Time: {away_team} - Visitante')
        time_vistante = get_lineups(_id, away_team)  # Usando cache
        time_vistante['positions'] = time_vistante['positions'].apply(lambda x: x[0]['position'] if isinstance(x, list) and len(x) > 0 else None)
        time_vistante['player_id'] = time_vistante['player_id'].astype(str)
        st.write(time_vistante)

    with tab4:
        dados_jogador(competition)
    
if __name__ == "__main__":
    Competicoes()