import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

#st.button("Retour")

st.title("📘 Ecritures comptables")

# --- Paramètres MySQL ---
host = "localhost"
port = 3307
user = "root"
password = ""  # adapte si besoin
database = "gl_comptable"

# --- Créer le moteur SQLAlchemy ---
engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}")

# --- Initialiser session_state ---
fields = ["date_ecriture", "libelle", "numero_piece", "id_compte", "debit", "credit", "journal"]
for f in fields:
    if f not in st.session_state:
        st.session_state[f] = "0.00" if f in ["debit", "credit"] else ""

# --- Formulaire en colonnes ---
col1, col2 = st.columns(2)

with col1:
    date_ecriture = st.text_input("Date d'écriture", value=st.session_state.date_ecriture, placeholder="Ex : 2025-01-03")
    libelle = st.text_input("Libellé", value=st.session_state.libelle, placeholder="Ex : Achat de fournitures")
    numero_piece = st.text_input("Numéro de pièce", value=st.session_state.numero_piece, placeholder="Ex : FAC001")

with col2:
    id_compte = st.text_input("ID du compte", value=st.session_state.id_compte, placeholder="Ex : 606")
    debit = st.text_input("Montant au débit", value=st.session_state.debit, placeholder="Ex : 500.00")
    credit = st.text_input("Montant au crédit", value=st.session_state.credit, placeholder="Ex : 0.00")

journal = st.text_input("Journal", value=st.session_state.journal, placeholder="Ex : ACH")

# --- Mise à jour session_state ---
for f in fields:
    st.session_state[f] = locals()[f]

# --- Boutons côte à côte ---
col1, col2 = st.columns([7,1])  # Deux colonnes de taille égale

with col1:
    ajouter = st.button("Ajouter l'écriture")

with col2:
    retour = st.button("⬅️ Back")
    #st.switch_page("app.py")

# --- Action du bouton Ajouter ---
if ajouter:
    if not all([date_ecriture, libelle, numero_piece, id_compte, debit, credit, journal]):
        st.warning("Merci de remplir tous les champs.")
    else:
        try:
            with engine.connect() as conn:
                query = text("""
                    INSERT INTO ecritures_comptables
                    (date_ecriture, libelle, numero_piece, id_compte, debit, credit, journal)
                    VALUES (:date_ecriture, :libelle, :numero_piece, :id_compte, :debit, :credit, :journal)
                """)
                conn.execute(query, {
                    "date_ecriture": date_ecriture,
                    "libelle": libelle,
                    "numero_piece": numero_piece,
                    "id_compte": id_compte,
                    "debit": debit,
                    "credit": credit,
                    "journal": journal
                })
                conn.commit()

                st.success("✅ Écriture ajoutée avec succès !")

                # Afficher les 5 dernières lignes
                df = pd.read_sql("SELECT * FROM ecritures_comptables ORDER BY id_ecriture DESC LIMIT 50;", engine)
                st.write("### Derniers enregistrements :")
                st.dataframe(df)

        except Exception as e:
            st.error(f"❌ Erreur lors de l'insertion : {e}")

# --- Action du bouton Retour ---
if retour:
    #st.switch_page("app.py")  # redirection vers la page d’accueil
    st.switch_page("Dashboard.py")


# --- Action du bouton Retour ---
#if retour:
    #st.session_state["page"] = "accueil"  # Exemple : redirection vers une autre page
    #st.experimental_rerun()
