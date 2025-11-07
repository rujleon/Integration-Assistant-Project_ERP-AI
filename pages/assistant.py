import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from sqlalchemy import create_engine, text
import pandas as pd
import re

# --- Charger variables d'environnement depuis .env ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
db_uri = os.getenv("DB_URI")

# Vérification des variables
if not api_key or not db_uri:
    st.error("❌ Vérifie que ton fichier .env contient GOOGLE_API_KEY et DB_URI")
    st.stop()

# --- Configurer Gemini ---
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-2.0-flash-exp")

# --- Connexion à la base SQL ---
try:
    engine = create_engine(db_uri)
except Exception as e:
    st.error(f"❌ Impossible de se connecter à la base : {e}")
    st.stop()

# --- Interface Streamlit ---
st.title("🤖 Assistant intelligent pour DB")
st.write("Pose une question en langage naturel, et l'assistant génèrera et exécutera la requête SQL correspondante.")

question = st.text_input("💬 Question :")

# Créer deux colonnes pour les boutons EN DESSOUS du input
col1, col2 = st.columns([1, 1])

with col1:
    retour_clicked = st.button(" ⬅️ Retour ", use_container_width=True)
    
with col2:
    envoyer_clicked = st.button("🚀 Envoyer", use_container_width=True)

if retour_clicked:
    #st.switch_page("app.py")
    st.switch_page("Dashboard.py")

if envoyer_clicked and question.strip() != "":
    with st.spinner("💡 Génération de la requête SQL et exécution..."):
        # 1️⃣ Générer la requête SQL
        prompt = f"""
        Transforme la question suivante en une requête SQL MySQL valide, uniquement pour lecture (SELECT).
        Base : gl_comptable
        Table : ecritures_comptables
        Question : {question}
        Ne mets pas de texte explicatif, donne seulement la requête SQL correcte.
        """

        try:
            response = model.generate_content(prompt)
            sql_query = response.text.strip()
        except Exception as e:
            st.error(f"❌ Erreur lors de la génération de la requête : {e}")
            st.stop()


        # Nettoyage : retirer ```sql et autres balises
        sql_query = re.sub(r"```sql|```", "", sql_query, flags=re.IGNORECASE).strip()

        # 2️⃣ Vérifier si c'est bien un SELECT
        if not sql_query.lower().startswith("select"):
            st.warning(f"⚠️ Gemini n'a pas généré un SELECT valide.\n\nRequête générée :\n{sql_query}")
        else:
            # 3️⃣ Exécuter la requête SQL
            try:
                with engine.connect() as conn:
                    result = conn.execute(text(sql_query))
                    df = pd.DataFrame(result.fetchall(), columns=result.keys())

                st.success("✅ Requête exécutée avec succès !")
                st.code(sql_query, language="sql")
                st.dataframe(df)
            except Exception as e:
                st.error(f"❌ Erreur lors de l'exécution de la requête : {e}")