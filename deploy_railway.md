# 🚀 Guide de déploiement Railway

## Étape 1: Installer Railway CLI
```bash
npm install -g @railway/cli
```

## Étape 2: Se connecter à Railway
```bash
railway login
```

## Étape 3: Initialiser le projet
```bash
railway init
```

## Étape 4: Configurer les variables d'environnement
```bash
railway variables set OPENAI_API_KEY=votre_clé_openai
railway variables set MAKE_WEBHOOK_URL=votre_url_make
railway variables set GOOGLE_DRIVE_CREDENTIALS_FILE=votre_fichier_credentials
railway variables set GOOGLE_DRIVE_FOLDER_ID=votre_folder_id
```

## Étape 5: Déployer
```bash
railway up
```

## Étape 6: Obtenir l'URL
```bash
railway domain
```

Votre dashboard sera accessible à l'URL fournie par Railway ! 