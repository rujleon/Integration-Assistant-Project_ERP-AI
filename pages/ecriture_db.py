import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

from pathlib import Path


st.title("📘 Liste des écritures comptables")


# --- Paramètres MySQL ---
host = "localhost"
port = 3307
user = "root"
password = ""  
database = "gl_comptable"

# --- Créer le moteur SQLAlchemy ---
engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}")

try:
    # --- Charger les données directement ---
    df = pd.read_sql("SELECT * FROM ecritures_comptables ORDER BY id_ecriture DESC LIMIT 100;", engine)
    st.success("✅ Données chargées avec succès !")
    st.write("#### Dernières écritures comptables :")
    
    # --- Barre de recherche + Bouton Retour sur la même ligne ---
    col1, col2 = st.columns([6, 1])  # col1 pour le champ texte, col2 pour le bouton
    with col1:
        search_query = st.text_input("🔍 Rechercher dans les écritures")
    with col2:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)  # petit décalage vertical
            retour_clicked = st.button("⬅️ Back",use_container_width=True)
            if retour_clicked:
                #st.switch_page("app.py")
                st.switch_page("Dashboard.py")
    
    # --- Filtrer le DataFrame selon la recherche ---
    if search_query:
        mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
        filtered_df = df[mask]
    else:
        filtered_df = df
    
    st.dataframe(filtered_df, width="stretch")

except Exception as e:
    st.error(f"❌ Erreur lors du chargement des écritures : {e}")
