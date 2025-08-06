# 🚀 Déploiement Railway - Guide Manuel

## Étape 1: Créer un compte Railway
1. Allez sur https://railway.app
2. Cliquez sur "Sign Up" et connectez-vous avec GitHub

## Étape 2: Créer un nouveau projet
1. Cliquez sur "New Project"
2. Sélectionnez "Deploy from GitHub repo"
3. Connectez votre repository GitHub

## Étape 3: Configurer le projet
1. Railway détectera automatiquement que c'est un projet Python
2. Il utilisera le `Procfile` et `requirements.txt` existants

## Étape 4: Configurer les variables d'environnement
Dans l'interface Railway, allez dans "Variables" et ajoutez :

```
OPENAI_API_KEY=votre_clé_openai
MAKE_WEBHOOK_URL=https://hook.us2.make.com/cojopjk9yp1vc18zxxlryodv29qfvgqb
GOOGLE_DRIVE_CREDENTIALS_FILE=votre_fichier_credentials
GOOGLE_DRIVE_FOLDER_ID=votre_folder_id
```

## Étape 5: Déployer
1. Railway déploiera automatiquement
2. Vous recevrez une URL comme : `https://votre-projet.railway.app`

## Étape 6: Vérifier le déploiement
1. Allez sur l'URL fournie
2. Votre dashboard devrait être accessible 24h/24 !

## 🔄 Mise à jour automatique
À chaque push sur GitHub, Railway redéploiera automatiquement. 