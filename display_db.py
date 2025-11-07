import streamlit as st
import mysql.connector
import pandas as pd

# Configuration
st.title("📊 Visualisation de la base MySQL")

host = st.text_input("Hôte", "localhost")
user = st.text_input("Utilisateur", "root")
password = st.text_input("Mot de passe", type="password")
database = st.text_input("Nom de la base de données")

if st.button("Se connecter"):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=gl_comptable
        )
        st.success("✅ Connexion réussie !")

        # Afficher les tables
        tables = pd.read_sql("SHOW TABLES;", conn)
        st.sidebar.write("Tables disponibles :", tables)

        table_name = st.selectbox("Choisir une table à afficher :", tables.iloc[:, 0])

        if table_name:
            df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
            st.write(f"### Contenu de la table `{table_name}`")
            st.dataframe(df)

        conn.close()
    except Exception as e:
        st.error(f"❌ Erreur de connexion : {e}")
