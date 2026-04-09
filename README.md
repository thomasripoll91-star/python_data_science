# Projet Data Science - Prédiction de Désabonnement (Churn)
**Auteurs :** DIALLO Bintou & RIPOLL Thomas

Ce projet se divise en deux grandes parties : un **Notebook d'analyse** (pour la recherche et la création du modèle) et une **API REST** (pour rendre le modèle utilisable en temps réel).

---

##  1. Le Notebook de Data Science
Le fichier Jupyter Notebook contient toute la démarche analytique du projet :
* **Analyse Exploratoire (EDA) :** Visualisation et compréhension du comportement des clients.
* **Préparation des données :** Nettoyage, sélection des variables (Feature Engineering) et équilibrage des classes.
* **Modélisation :** Entraînement et optimisation de plusieurs algorithmes (Régression Logistique, Random Forest).
* **Choix final :** Sélection et configuration du modèle **XGBoost**, qui offre le meilleur compromis pour identifier les clients à risque.

---

##  2. L'API REST (Déploiement)
L'API est construite avec FastAPI. Elle charge notre modèle XGBoost pré-entraîné pour évaluer instantanément la probabilité de départ d'un client donné.

###  Installation

Ouvrez votre terminal et exécutez ces commandes :

\`\`\`bash
# 1. Cloner le projet
git clone <votre-lien-github>
cd <nom-du-dossier>

# 2. Créer et activer l'environnement virtuel
python -m venv env
source env/bin/activate  # Sur Windows : env\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt
\`\`\`

###  Démarrage

**Important :** Le serveur doit être lancé depuis le dossier `API`.

\`\`\`bash
# 1. Entrer dans le dossier contenant l'API
cd API

# 2. Lancer le serveur local
uvicorn app:app --reload
\`\`\`
 L'API tourne maintenant sur : **http://127.0.0.1:8000**

### Tester le modèle

#### Option A : Interface Visuelle (Recommandé)
1. Ouvrez  **http://127.0.0.1:8000/docs**
2. Déroulez la route `POST /predict` et cliquez sur **"Try it out"**.
3. Remplissez les infos du client et cliquez sur **"Execute"**.

#### Option B : Terminal (cURL)
\`\`\`bash
curl -X 'POST' 'http://127.0.0.1:8000/predict' \
  -H 'Content-Type: application/json' \
  -d '{
  "ord__Contract": "Month-to-month",
  "ord__InternetService": "Fiber optic",
  "num__tenure": 5,
  "num__MonthlyCharges": 85.50
}'
\`\`\`