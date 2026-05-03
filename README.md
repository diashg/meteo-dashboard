# Météo Dashboard

**[Voir le site](https://meteo-dashboard.onrender.com)**

Dashboard météo personnel réalisé pour revoir les bases de SQL et Flask.
Recherche une ville et affiche ses prévisions météorologiques sur 14 jours,
stockées en base de données SQLite.

## Stack
- Python + Flask : serveur web
- SQLite : stockage des villes et prévisions
- Open-Meteo API : données météo gratuites, sans clé API

## Installation
```bash
git clone https://github.com/diashg/meteo-dashboard.git
cd meteo-dashboard
pip install -r requirements.txt
python app.py
```
Puis ouvrir http://127.0.0.1:5000 dans le navigateur
