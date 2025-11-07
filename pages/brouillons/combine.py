import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import google.generativeai as genai
import re

# --- Charger les variables d'environnement ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
db_uri = os.getenv("DB_URI")

# --- Configuration de Gemini ---
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-2.0-flash-exp")

# --- Connexion à MySQL ---
host = "localhost"
port = 3307
user = "root"
password = ""
database = "gl_comptable"

engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}")

# --- Interface Streamlit principale ---
st.set_page_config(page_title="Écritures comptables + Assistant", layout="wide")
st.title("📘 Liste des écritures comptables")

# --- Charger les données ---
try:
    df = pd.read_sql("SELECT * FROM ecritures_comptables ORDER BY id_ecriture DESC LIMIT 100;", engine)
    st.success("✅ Données chargées avec succès !")

    # Barre de recherche et bouton retour
    col1, col2, col3 = st.columns([5, 1, 2])
    with col1:
        search_query = st.text_input("🔍 Rechercher dans les écritures")
    with col2:
        retour_clicked = st.button("⬅️ Back")
        if retour_clicked:
            st.switch_page("app.py")
    with col3:
        assistant_open = st.toggle("🧠 Assistant intelligent")

    # Filtrage des données
    if search_query:
        mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
        filtered_df = df[mask]
    else:
        filtered_df = df

    st.dataframe(filtered_df, width="stretch")

except Exception as e:
    st.error(f"❌ Erreur lors du chargement des écritures : {e}")

# --- Assistant intégré ---
if assistant_open:
    st.markdown("---")
    st.subheader("🧠 Assistant intelligent SQL")

    question = st.text_input("💬 Pose une question à propos de la base :")

    if st.button("Envoyer", key="assistant_btn") and question.strip() != "":
        with st.spinner("💡 Génération et exécution de la requête SQL..."):
            prompt = f"""
            Transforme la question suivante en une requête SQL MySQL valide, uniquement de lecture (SELECT).
            Base : gl_comptable
            Table : ecritures_comptables
            Colonnes : id_ecriture, date_ecriture, libelle, numero_piece, id_compte, debit, credit, journal
            Question : {question}
            Ne donne pas d'explications, seulement la requête SQL correcte.
            """

            try:
                response = model.generate_content(prompt)
                sql_query = re.sub(r"```sql|```", "", response.text.strip(), flags=re.IGNORECASE).strip()
            except Exception as e:
                st.error(f"❌ Erreur lors de la génération de la requête : {e}")
                st.stop()

            # Vérifier que c'est bien un SELECT
            if not sql_query.lower().startswith("select"):
                st.warning(f"⚠️ Gemini n'a pas généré un SELECT valide :\n\n{sql_query}")
            else:
                try:
                    with engine.connect() as conn:
                        result = conn.execute(text(sql_query))
                        result_df = pd.DataFrame(result.fetchall(), columns=result.keys())

                    st.success("✅ Requête exécutée avec succès !")
                    st.code(sql_query, language="sql")
                    st.dataframe(result_df, use_container_width=True)
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'exécution de la requête : {e}")
