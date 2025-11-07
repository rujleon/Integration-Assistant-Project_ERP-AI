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

# --- Interface principale ---
st.set_page_config(page_title="Écritures comptables + Assistant", layout="wide")
st.title("📘 Liste des écritures comptables")

# --- Disposition en deux colonnes (70% / 30%) ---
col_left, col_right = st.columns([0.7, 0.3])

# ================================
# 🧾 PARTIE GAUCHE : TABLE PRINCIPALE
# ================================
with col_left:
    try:
        df = pd.read_sql("SELECT * FROM ecritures_comptables ORDER BY id_ecriture DESC LIMIT 100;", engine)
        st.success("✅ Données chargées avec succès !")

        c1, c2 = st.columns([6, 1])
        with c1:
            search_query = st.text_input("🔍 Rechercher dans les écritures")
        with c2:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            retour_clicked = st.button("⬅️Back", width="stretch")
            if retour_clicked:
                st.switch_page("app.py")

        # Filtrage
        if search_query:
            mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
            filtered_df = df[mask]
        else:
            filtered_df = df

        st.dataframe(filtered_df, width="stretch")

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des écritures : {e}")

# ================================
# 🤖 PARTIE DROITE : ASSISTANT SQL
# ================================
with col_right:
    st.markdown("#### 🧠 Assistant intelligent")
    st.markdown("<hr>", unsafe_allow_html=True)


    # zone de saisie
    question = st.text_area("💬 Pose une question à propos de la base :", height=100)

    # on déclenche sur Entrée ou bouton
    send_triggered = st.button("Envoyer", key="assistant_btn") or (question and st.session_state.get("last_question") != question)

    if send_triggered and question.strip() != "":
        st.session_state["last_question"] = question  # éviter relance multiple

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

            if not sql_query.lower().startswith("select"):
                st.warning(f"⚠️ Gemini n'a pas généré un SELECT valide :\n\n{sql_query}")
            else:
                try:
                    with engine.connect() as conn:
                        result = conn.execute(text(sql_query))
                        result_df = pd.DataFrame(result.fetchall(), columns=result.keys())

                    # phrase descriptive automatique
                    summary_prompt = f"""
                    Voici les résultats d'une requête SQL sur une base comptable :
                    {result_df.head(5).to_markdown(index=False)}
                    Écris une phrase courte et claire qui résume la réponse à la question suivante :
                    "{question}"
                    Exemple : "La somme totale du débit est de 12 450 €."
                    """

                    summary_response = model.generate_content(summary_prompt)
                    summary_text = summary_response.text.strip()

                    st.success("✅ Requête exécutée avec succès !")
                    st.code(sql_query, language="sql")
                    st.info(summary_text)
                    st.dataframe(result_df, width="stretch")

                except Exception as e:
                    st.error(f"❌ Erreur lors de l'exécution de la requête : {e}")
