# 📍 Où voir vos publications CrewAI

## 🎯 Tableau de bord local (Recommandé)

### **Voir toutes vos publications :**
```bash
python3 dashboard.py
```

### **Voir les données brutes :**
```bash
cat publications.json
```

### **Créer une nouvelle publication :**
```bash
python3 main.py
```

## 🔗 Dans Make.com

### **Où voir :**
1. **Allez dans Make.com**
2. **Ouvrez votre scénario**
3. **Regardez les logs d'exécution**

### **Ce que vous verrez :**
- ✅ **Webhooks reçus** de CrewAI
- ✅ **Données envoyées** (contenu + image)
- ✅ **Statut de publication** sur Facebook
- ✅ **Erreurs éventuelles**

### **Comment activer :**
1. Allez dans Make.com
2. Trouvez votre scénario
3. Cliquez sur **"Activate"**
4. Vérifiez que le webhook est configuré

## 📘 Sur Facebook (Final)

### **Où voir :**
- **Votre page Facebook** (une fois publié)
- **Historique des publications**
- **Statistiques d'engagement**

### **Ce que vous verrez :**
- ✅ **Posts publiés** automatiquement
- ✅ **Images sélectionnées** par CrewAI
- ✅ **Contenu en français** créé par CrewAI
- ✅ **Hashtags** optimisés

## 📊 Fichiers locaux

### **publications.json**
```bash
cat publications.json
```
**Contient :**
- Toutes les publications créées
- Statut de chaque publication
- Images sélectionnées
- Timestamps

### **Images téléchargées**
```bash
ls -la downloaded_*.jpeg
```
**Contient :**
- Images sélectionnées par CrewAI
- Prêtes pour publication

## 🎯 Workflow complet

### **1. Création (CrewAI)**
```bash
python3 main.py
```
- ✅ Crée le contenu en français
- ✅ Sélectionne une image de Google Drive
- ✅ Ajoute au tableau de bord local

### **2. Envoi (Make.com)**
- 🔄 Reçoit le webhook de CrewAI
- 🔄 Publie sur Facebook
- 🔄 Met à jour le statut

### **3. Publication (Facebook)**
- ✅ Post visible sur votre page
- ✅ Image et contenu optimisés
- ✅ Engagement et statistiques

## 🔧 Commandes utiles

### **Voir le tableau de bord :**
```bash
python3 dashboard.py
```

### **Créer une publication :**
```bash
python3 main.py
```

### **Tester Make.com :**
```bash
python3 test_make_webhook.py
```

### **Voir les images disponibles :**
```bash
python3 test_drive_simple.py
```

### **Diagnostic complet :**
```bash
python3 test_complete_integration.py
```

## 📈 Statuts des publications

### **"created"**
- ✅ Créé par CrewAI
- ✅ Ajouté au tableau de bord
- ⏳ En attente d'envoi à Make.com

### **"sent_to_make"**
- ✅ Envoyé à Make.com
- 🔄 En cours de traitement
- ⏳ En attente de publication

### **"published"**
- ✅ Publié sur Facebook
- ✅ Visible sur votre page
- ✅ Engagement disponible

## 🚀 Prochaines étapes

1. **Activez Make.com** pour voir les publications en temps réel
2. **Lancez une publication** : `python3 main.py`
3. **Vérifiez le tableau de bord** : `python3 dashboard.py`
4. **Consultez Facebook** pour voir les posts publiés

---

**Note :** Le tableau de bord local fonctionne déjà parfaitement. Il suffit d'activer Make.com pour avoir l'intégration complète avec Facebook ! 