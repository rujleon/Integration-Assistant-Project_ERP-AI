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
st.title("Assistant intelligent pour DB")
st.write("Pose une question en langage naturel, et l'assistant génèrera une reponse.")

# Initialisation de l'état de la session
if 'last_question' not in st.session_state:
    st.session_state.last_question = ""
if 'show_sql' not in st.session_state:
    st.session_state.show_sql = False

# Séparer le formulaire pour la question seulement
with st.form(key="query_form"):
    question = st.text_input("💬 Question :", value="", key="question_input")
    submitted = st.form_submit_button("Exécuter", use_container_width=True)

# Bouton Retour en dehors du formulaire
retour_clicked = st.button(" ⬅️ Retour ")


# Gestion du bouton Retour
if retour_clicked:
    st.switch_page("Dashboard.py")

# Gestion de l'exécution (bouton Envoyer ou touche Entrée)
if submitted and question.strip() != "":
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

                # ✅ SUCCÈS - Affichage avec réponse rédigée
                st.success("✅ Requête exécutée avec succès !")
                
                # Afficher la requête SQL seulement si la case est cochée
                if st.session_state.show_sql:
                    st.code(sql_query, language="sql")
                
                # Générer une réponse rédigée avec Gemini
                with st.spinner("📝 Rédaction de la réponse..."):
                    response_prompt = f"""
                    Tu es un assistant qui explique les résultats d'une requête SQL de manière naturelle et professionnelle.
                    
                    Question de l'utilisateur : "{question}"
                    Requête SQL exécutée : "{sql_query}"
                    Résultats obtenus : {df.to_dict('records')}
                    
                    Donne une réponse rédigée et naturelle qui répond à la question de l'utilisateur en utilisant les données obtenues.
                    Sois concis mais informatif.
                    """
                    
                    try:
                        response_text = model.generate_content(response_prompt)
                        st.write(" Résultat :")
                        st.write(response_text.text)
                    except Exception as e:
                        st.warning("⚠️ Impossible de générer une réponse rédigée, affichage des données brutes :")
                        st.dataframe(df)
                
                # Afficher aussi le dataframe complet en dessous
                with st.expander("🔍 Voir les données brutes", expanded=False):
                    st.dataframe(df)
                    
            except Exception as e:
                st.error(f"❌ Erreur lors de l'exécution de la requête : {e}")