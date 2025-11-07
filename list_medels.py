import os
from dotenv import load_dotenv
import google.generativeai as genai

# Charger la clé depuis .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("❌ Vérifie que ta clé GOOGLE_API_KEY est bien dans .env")

# Configurer l'API
genai.configure(api_key=api_key)

# Lister les modèles disponibles
models = genai.list_models()
print("Modèles disponibles :")
for m in models:
    print("-", m.name)
