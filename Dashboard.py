import streamlit as st

from dotenv import load_dotenv  # charger les variables d'environnement depuis un fichier .env

# Load la clé d'API dans api.env
load_dotenv()

st.set_page_config(page_title="Ask Your Database", page_icon="🧠", layout="wide")

st.title("💬 Assistant et Base de Données")

st.write("Bienvenue dans votre assistant intelligent connecté à une base SQL.")
st.write("Choisissez une action ci-dessous 👇")

col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Add (Afficher / Ajouter des données)"):
        st.switch_page("pages/add_data.py")

with col2:
    if st.button("🤖 Assistant (Interroger la base)"):
        st.switch_page("pages/assistant.py")

st.markdown("---")
st.caption("Application réalisée avec Streamlit 💡 developé par Rojo")
