import google.generativeai as genai
import os

# --- ÉTAPE 1 : CONFIGURATION GLOBALE ---
# Configure l'API avec la clé stockée dans les variables d'environnement api.env
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# --- ÉTAPE 2 : INITIALISATION DU CLIENT ---
# Création de l'objet client au niveau du module
client = genai.Client()

def query_gemini(prompt):
    # 'client' est maintenant accessible car il est défini dans le module
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=prompt
    )
    return response.text

