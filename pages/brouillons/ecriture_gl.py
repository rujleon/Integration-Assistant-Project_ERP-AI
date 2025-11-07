import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.title("📘 Liste des écritures comptables")

# --- Paramètres MySQL ---
host = "localhost"
port = 3307
user = "root"
password = ""  # adapte si besoin
database = "gl_comptable"

# --- Créer le moteur SQLAlchemy ---
engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}")

# --- Boutons ---
col1, col2 = st.columns([6, 1])

with col1:
    afficher = st.button("📄 Afficher les écritures")

with col2:
    retour = st.button("⬅️ Retour")

# --- Action du bouton Afficher ---
if afficher:
    try:
        df = pd.read_sql("SELECT * FROM ecritures_comptables ORDER BY id_ecriture DESC LIMIT 20;", engine)
        st.success("✅ Données chargées avec succès !")
        st.write("### Dernières écritures comptables :")
        #st.dataframe(df, use_container_width=True)
        st.dataframe(df,width="stretch")
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des écritures : {e}")

# --- Action du bouton Retour ---
if retour:
    st.switch_page("app.py")
