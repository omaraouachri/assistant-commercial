# Assistant Commercial Ketil Media

Ce projet propose une application Python développée avec Streamlit, permettant de créer un assistant commercial reposant sur le modèle Gemini de google.  
L'application utilise une base de connaissances extraite de fichiers PDF et Word pour fournir des réponses pertinentes et adaptées.

---

## Fonctionnalités

- **Extraction de texte** : Analyse et extraction automatique de texte à partir de fichiers PDF et DOCX.
- **Génération de réponses intelligentes** : Intégration de l'API OpenAI pour fournir des réponses cohérentes et contextuelles.
- **Interface utilisateur interactive** : Déployée via Streamlit pour une expérience utilisateur simple et intuitive.

---

## Prérequis

Pour exécuter cette application, vous aurez besoin de :

- **Python** : Version 3.8 ou ultérieure.
- **Clé API OpenAI** : Une clé valide pour accéder au service.
- **Base de connaissances** : Fichiers PDF et DOCX stockés dans le dossier `base de connaissance`.
- **Logos** : Les fichiers `ketil_media_logo.png` et `athling_logo.png` doivent être placés dans le répertoire principal.

---

## Installation

Suivez les étapes ci-dessous pour configurer et exécuter l'application :

### Étape 1 : Activer un environnement virtuel

Créez et activez un environnement virtuel pour isoler les dépendances du projet :

```bash
# Créer un environnement virtuel
python -m venv env

# Activer l'environnement virtuel (Windows)
env\Scripts\activate

# Activer l'environnement virtuel (Mac/Linux)
source env/bin/activate 
```
### Étape 2 : Installer les dépendances

```bash
pip install -r requirements.txt
```

### Étape 3 : Préparer les fichiers nécessaires

Assurez-vous que les fichiers PDF et Word sont bien placés dans le dossier base de connaissance.

Vérifiez que les images ketil_media_logo.png et athling_logo.png sont présentes à la racine du projet.

### Étape 4 : Lancer l'application
```bash

streamlit run main_app.py
```
