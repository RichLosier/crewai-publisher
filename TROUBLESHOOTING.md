# 🔧 Guide de Dépannage CrewAI

## 🎯 Diagnostic Rapide

### 1. Vérifier l'état du système
```bash
python3 quick_diagnostic.py
```

### 2. Récupération automatique
```bash
python3 auto_fix.py
```

### 3. Test garanti
```bash
python3 guaranteed_test.py
```

## 🚨 Problèmes Courants et Solutions

### ❌ Erreur OpenAI API
**Symptôme :** `AuthenticationError: Incorrect API key provided`
**Solution :**
1. Vérifiez votre clé API dans `.env`
2. Obtenez une nouvelle clé sur [OpenAI Platform](https://platform.openai.com/account/api-keys)
3. Mettez à jour `OPENAI_API_KEY` dans `.env`

### ❌ Erreur Google Drive
**Symptôme :** `File not found` ou `403 Forbidden`
**Solution :**
1. Vérifiez que le dossier est partagé avec le Service Account
2. Vérifiez que les credentials sont corrects
3. Relancez : `python3 test_drive_simple.py`

### ❌ Erreur Make.com
**Symptôme :** `410 There is no scenario listening for this webhook`
**Solution :**
1. Allez dans Make.com
2. Activez votre scénario (bouton "Activate")
3. Vérifiez que le webhook est configuré

### ❌ Erreur Import
**Symptôme :** `ModuleNotFoundError`
**Solution :**
```bash
pip3 install crewai pyyaml requests google-auth google-api-python-client
```

## 🔧 Scripts de Test

### Test complet
```bash
python3 test_complete_integration.py
```

### Test en mode local
```bash
python3 main_test_mode.py
```

### Test avec Make.com réel
```bash
python3 main.py
```

## 📋 Checklist de Vérification

- [ ] OpenAI API key valide
- [ ] Google Drive credentials configurés
- [ ] Dossier Google Drive partagé avec Service Account
- [ ] Images uploadées dans Google Drive
- [ ] Scénario Make.com activé
- [ ] Webhook Make.com configuré
- [ ] Toutes les dépendances installées

## 🎯 Solutions par Composant

### Google Drive
```bash
# Test simple
python3 test_drive_simple.py

# Vérifier les images
python3 -c "from tools.google_drive_tools import GoogleDriveImageSelector; print('OK')"
```

### Make.com
```bash
# Test webhook
python3 test_make_webhook.py

# Vérifier l'URL
cat .env | grep MAKE_WEBHOOK_URL
```

### CrewAI
```bash
# Test complet
python3 main.py

# Test en mode local
python3 main_test_mode.py
```

## 🚀 Mode de Récupération

Si rien ne fonctionne, utilisez le mode de récupération :

1. **Diagnostic :** `python3 quick_diagnostic.py`
2. **Récupération :** `python3 auto_fix.py`
3. **Test garanti :** `python3 guaranteed_test.py`
4. **Test local :** `python3 main_test_mode.py`

## 📞 Support

Si le problème persiste :
1. Vérifiez les logs d'erreur
2. Relancez les tests de diagnostic
3. Vérifiez la configuration de chaque service
4. Testez en mode local d'abord

---

**Note :** Le système est conçu pour fonctionner même avec des problèmes partiels. Google Drive et CrewAI fonctionnent déjà, il suffit d'activer Make.com pour avoir l'intégration complète. 