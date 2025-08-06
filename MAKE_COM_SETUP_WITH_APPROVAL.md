# 🎯 Configuration Make.com avec Processus d'Approbation

## 📋 **Vue d'ensemble du processus**

```
CrewAI → Dashboard d'Approbation → Make.com → Facebook
```

1. **CrewAI** crée le contenu
2. **Dashboard d'Approbation** (interface web) pour approuver/rejeter
3. **Make.com** reçoit les publications approuvées
4. **Facebook** publie automatiquement

## 🚀 **Étapes de configuration**

### **Étape 1 : Lancer le Dashboard d'Approbation**

```bash
python3 approval_dashboard.py
```

Ouvrez : http://localhost:5000

### **Étape 2 : Configurer Make.com**

#### **2.1 Créer le scénario Make.com**

1. **Allez sur Make.com**
2. **Cliquez sur "Create a new scenario"**
3. **Nommez-le :** "CrewAI Facebook Publisher"

#### **2.2 Ajouter le Webhook**

1. **Cliquez sur le "+" pour ajouter un module**
2. **Recherchez "Webhook"**
3. **Sélectionnez "Webhooks"**
4. **Cliquez sur "Add"**

#### **2.3 Configurer le Webhook**

1. **Cliquez sur le module Webhook**
2. **Dans "URL" :** Copiez l'URL fournie par Make.com
3. **Dans "Method" :** Sélectionnez "POST"
4. **Cliquez sur "Save"**

#### **2.4 Ajouter un Router (Condition)**

1. **Cliquez sur le "+" après le Webhook**
2. **Recherchez "Router"**
3. **Sélectionnez "Router"**
4. **Cliquez sur "Add"**

#### **2.5 Configurer le Router**

1. **Cliquez sur le Router**
2. **Dans "Add a new route" :**
   - **Label :** "Publish Facebook"
   - **Condition :** `{{1.action}} = "publish_facebook"`

#### **2.6 Ajouter l'action Facebook**

1. **Cliquez sur le "+" dans la route "Publish Facebook"**
2. **Recherchez "Facebook"**
3. **Sélectionnez "Facebook"**
4. **Cliquez sur "Add"**

#### **2.7 Configurer Facebook**

1. **Cliquez sur le module Facebook**
2. **Dans "Connection" :** Connectez votre compte Facebook
3. **Dans "Page" :** Sélectionnez votre page iFiveMe
4. **Dans "Message" :** `{{1.data.content}}`
5. **Dans "Image" :** `{{1.data.image}}`
6. **Cliquez sur "Save"**

#### **2.8 Ajouter une route par défaut**

1. **Cliquez sur le "+" dans "Default"**
2. **Recherchez "Text aggregator"**
3. **Sélectionnez "Text aggregator"**
4. **Cliquez sur "Add"**
5. **Dans "Text" :** `Publication non reconnue: {{1.action}}`

### **Étape 3 : Tester le processus**

#### **3.1 Créer une publication test**

```bash
python3 main.py
```

#### **3.2 Approuver dans le dashboard**

1. **Ouvrez :** http://localhost:5000
2. **Cliquez sur "✅ Approuver"**
3. **Vérifiez dans Make.com que le webhook est reçu**

#### **3.3 Vérifier sur Facebook**

1. **Allez sur votre page Facebook**
2. **Vérifiez que la publication apparaît**

## 🔧 **Configuration avancée**

### **Ajouter des notifications par email**

1. **Dans Make.com, ajoutez un module "Email"**
2. **Configurez-le pour envoyer un email de confirmation**
3. **Placez-le après l'action Facebook**

### **Ajouter des logs détaillés**

1. **Ajoutez un module "Google Sheets"**
2. **Configurez-le pour logger toutes les publications**
3. **Placez-le après l'action Facebook**

## 📊 **Structure des données**

### **Données envoyées par le Dashboard d'Approbation**

```json
{
  "action": "publish_facebook",
  "data": {
    "content": "🎶 Libère ta musique sans interruptions ! 🚀\n\nTu es passionné de musique et tu veux profiter de tes morceaux préférés sans publicités ? Notre plateforme de streaming premium t'offre une expérience musicale exceptionnelle !\n\n✨ Écoute sans limites\n🎵 Qualité audio premium\n🚫 Zéro publicité\n📱 Compatible tous appareils\n\n👉 Essaie gratuitement pendant 30 jours !\n\n#MusicLovers #Streaming #AdFree #PremiumMusic #iFiveMe",
    "image": "freepik__crer-une-image-dans-un-style-3d-semiraliste-inspir__48353.jpeg",
    "hashtags": ["#iFiveMe", "#Facebook", "#Marketing"],
    "timestamp": "2025-08-03T10:54:20.495847"
  }
}
```

### **Variables disponibles dans Make.com**

- `{{1.action}}` : Type d'action
- `{{1.data.content}}` : Contenu du post
- `{{1.data.image}}` : Nom de l'image
- `{{1.data.hashtags}}` : Liste des hashtags
- `{{1.data.timestamp}}` : Timestamp

## 🚨 **Dépannage**

### **Problème : Webhook non reçu**

1. **Vérifiez l'URL du webhook dans `.env`**
2. **Testez avec :** `python3 test_make_webhook.py`
3. **Vérifiez que le scénario est activé dans Make.com**

### **Problème : Publication non publiée sur Facebook**

1. **Vérifiez la connexion Facebook dans Make.com**
2. **Vérifiez les permissions de la page**
3. **Testez manuellement l'action Facebook**

### **Problème : Dashboard non accessible**

1. **Vérifiez que Flask est installé :** `pip3 install flask`
2. **Relancez :** `python3 approval_dashboard.py`
3. **Vérifiez le port 5000 n'est pas utilisé**

## 📱 **Interface mobile**

Le dashboard est responsive et fonctionne sur mobile :
- **Ouvrez :** http://localhost:5000 sur votre téléphone
- **Approuvez/rejetez** depuis n'importe où

## 🔄 **Automatisation complète**

Une fois configuré, le processus est entièrement automatisé :

1. **CrewAI** crée le contenu automatiquement
2. **Vous approuvez** via le dashboard web
3. **Make.com** publie automatiquement sur Facebook
4. **Vous recevez** une notification de confirmation

## 🎯 **Prochaines étapes**

1. **Testez le processus complet**
2. **Personnalisez les templates de contenu**
3. **Ajoutez d'autres réseaux sociaux**
4. **Configurez des notifications avancées** 