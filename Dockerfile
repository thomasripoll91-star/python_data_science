# 1) base python d'où on part "légère"
FROM python:3.11-slim

# 2) on dit qu le dossier principale de notre travail est celui ci
WORKDIR /app

# 3) on copie le fichier des dépendances en premier
COPY requirements.txt .

# 4) Installation de toutes les librairies
RUN pip install --no-cache-dir -r requirements.txt

# 5.Copie de tout le reste de ton projet dans le conteneur
COPY . .

#6) on se déplace dans le dossier API
WORKDIR /app/API

# 7) On indique que l'API va communiquer sur le port 8000
EXPOSE 8000

# 8) La commande finale pour allumer le serveur
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]