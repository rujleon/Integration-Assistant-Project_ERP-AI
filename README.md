# 🧠 ERP-Assist : L'Intelligence au Cœur de Votre ERP

[![Version](https://img.shields.io/badge/Version-v1.0.0-blue)](https://github.com/rujleon/Integration-Assistant-Project_ERP-AI)
[![Licence](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 📄 Description

Ce projet intègre une **interface d'assistance intelligente** (via un modèle de langage) directement dans les données de votre ERP. Il utilise [Streamlit](https://streamlit.io/) pour une interface utilisateur conviviale et se connecte à votre base de données [MySQL](https://www.mysql.com/).

### Objectifs

Permettre aux utilisateurs d'interroger la base de données ERP en **langage naturel** et d'obtenir des analyses instantanées sans écrire une seule ligne de SQL.

---

## 🛠️ Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés :

* **Python** (Version 3.8+)
* **XAMPP** (ou un équivalent Apache/MySQL)
* Une clé API pour le modèle de langage utilisé (OpenAI, Gemini, etc.) — à spécifier dans un fichier `.env`.

## 🚀 Installation

### 1. Cloner le dépôt
```bash
git clone git@github.com:rujleon/Integration-Assistant-Project_ERP-AI.git
cd Integration-Assistant-Project_ERP-AI 
```


### 2. Configurer l'Environnement
``` bash
python -m venv venv
source venv/bin/activate    # Sous Linux/macOS
venv\Scripts\activate     # Sous Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration des identifiants (Base de Données & API)
```.env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=votre_db_erp
API_KEY=votre_cle_secrete_ici
```


### 5. Utilisation
```bash
streamlit run app.py
```

## Mode d'Emploi
Saisissez votre question en langage naturel dans la barre de texte (ex: "Quel est le total des ventes du mois dernier par catégorie de produit ?").

L'assistant vous fournira la réponse ou l'analyse demandée, en interrogeant la base de données.


## Contribution
Les contributions, les rapports de bugs et les suggestions d'amélioration sont les bienvenus !

* Signaler un Bug : Ouvrez une nouvelle Issue sur ce dépôt GitHub.

* Proposer une Fonctionnalité :

* Faites un fork de ce dépôt.

* Créez une nouvelle branche (git checkout -b feature/nom-de-la-feature).

* Committez vos modifications (git commit -m 'feat: ajoute la fonctionnalité X').

* Poussez votre branche (git push origin feature/nom-de-la-feature).

* Ouvrez une Pull Request claire et détaillée.

