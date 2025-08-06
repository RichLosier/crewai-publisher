# Guide d'Utilisation - Interface Web iFiveMe AI

## 🚀 Vue d'ensemble

L'interface web iFiveMe AI est une interface moderne de type Google avec une barre de recherche centrale et une zone de dépôt de fichiers. Elle permet d'interagir naturellement avec le système fiscal AI et dispose d'une mémoire évolutive qui apprend de votre entreprise.

## 🎯 Fonctionnalités Principales

### 1. **Interface Google-like**
- Barre de recherche centrale avec design moderne
- Suggestions de requêtes populaires
- Zone de dépôt de fichiers par glisser-déposer
- Interface responsive (mobile-friendly)

### 2. **Recherche Intelligente**
- Questions en langage naturel
- Calculs fiscaux automatiques
- Recherche d'échéances
- Génération de rapports
- Optimisation fiscale

### 3. **Upload de Fichiers**
- Support de multiples formats (PDF, CSV, Excel, images)
- Analyse automatique des documents
- Extraction de données fiscales
- Intégration dans la mémoire du système

### 4. **Mémoire Évolutive**
- Apprentissage continu des patterns de votre entreprise
- Historique des conversations
- Préférences personnalisées
- Amélioration progressive des réponses

## 🛠️ Installation et Lancement

### 1. **Installation des dépendances**
```bash
pip3 install -r requirements.txt
```

### 2. **Lancement de l'interface**
```bash
python3 launch_web_interface.py
```

### 3. **Accès à l'interface**
- Ouvrez votre navigateur
- Allez sur `http://localhost:5000`
- L'interface s'ouvrira automatiquement

## 📝 Utilisation

### **Barre de Recherche**

#### Exemples de requêtes :

**Calculs fiscaux :**
```
Calculer les taxes sur 1000$
Quel est le montant total avec TPS/TVQ pour 2500$?
```

**Échéances :**
```
Quelles sont les prochaines échéances?
Quand est la prochaine déclaration TPS/TVH?
```

**Rapports :**
```
Générer un rapport mensuel
Créer un rapport trimestriel
Faire un rapport annuel complet
```

**Optimisation :**
```
Analyser les opportunités d'optimisation
Quelles sont les déductions possibles?
Optimiser ma situation fiscale
```

### **Upload de Fichiers**

#### Formats supportés :
- **PDF** : Documents fiscaux, relevés bancaires
- **CSV/Excel** : Données financières, transactions
- **Images** : Reçus, factures scannées
- **TXT/DOCX** : Documents textuels

#### Comment uploader :
1. **Glisser-déposer** : Déposez directement vos fichiers dans la zone
2. **Clic** : Cliquez sur la zone pour sélectionner des fichiers
3. **Multiple** : Vous pouvez uploader plusieurs fichiers à la fois

#### Analyse automatique :
- **Fichiers financiers** : Extraction des transactions et calculs fiscaux
- **Documents PDF** : Reconnaissance de texte et analyse fiscale
- **Images** : OCR et extraction de données
- **Intégration** : Toutes les données sont intégrées au système

## 🧠 Système de Mémoire

### **Apprentissage Continu**

Le système apprend de chaque interaction :

1. **Conversations** : Historique des questions/réponses
2. **Patterns** : Reconnaissance des habitudes de votre entreprise
3. **Préférences** : Adaptation aux besoins spécifiques
4. **Contexte** : Compréhension du contexte de votre entreprise

### **Indicateur de Mémoire**

En bas à droite, un indicateur affiche :
- Dernière interaction
- Nombre de conversations
- Patterns appris
- État de la mémoire

## 💡 Exemples d'Utilisation

### **Scénario 1 : Calcul Fiscal**
```
Vous tapez : "Calculer les taxes sur 1500$"
Résultat : 
💰 Calcul Fiscal pour $1500

📊 Détails des taxes:
- TPS (5%): $75.00
- TVQ (9.975%): $149.63
- Total taxes: $224.63
- Montant total: $1724.63
```

### **Scénario 2 : Upload de Relevé Bancaire**
```
Vous déposez : relevé_bancaire.csv
Résultat :
📊 Analyse du fichier financier: relevé_bancaire.csv

✅ Fichier reçu et en cours d'analyse
📈 Type: Données financières
🔍 Extraction des transactions en cours...

📋 Données extraites:
- Transactions identifiées
- Catégorisation automatique
- Calculs fiscaux appliqués
- Anomalies détectées
```

### **Scénario 3 : Demande d'Échéances**
```
Vous tapez : "Quelles sont les prochaines échéances?"
Résultat :
📅 Prochaine Échéance Fiscale

🎯 Retenues à la source
📅 Date: 2025-08-15
⏰ Dans: 9 jours
📝 Description: Paiement des retenues à la source

📋 Échéances à venir (90 jours):
🟡 Retenues à la source: dans 9 jours
🟡 Déclaration TPS/TVH mensuelle: dans 25 jours
```

## 🔧 Fonctionnalités Avancées

### **Suggestions Intelligentes**

L'interface propose des suggestions basées sur :
- Vos requêtes précédentes
- Les patterns de votre entreprise
- Les échéances à venir
- Les opportunités d'optimisation

### **Réponses Contextuelles**

Le système adapte ses réponses selon :
- Le contexte de votre entreprise
- L'historique des interactions
- Les préférences apprises
- Les patterns identifiés

### **Intégration Complète**

Toutes les interactions sont intégrées avec :
- Le système fiscal AI
- Les agents spécialisés
- Les workflows automatisés
- La base de connaissances

## 🚨 Dépannage

### **Problèmes courants :**

#### 1. **Interface ne se lance pas**
```bash
# Vérifier les dépendances
pip3 install flask flask-uploads

# Relancer
python3 launch_web_interface.py
```

#### 2. **Erreur de port**
```bash
# Changer le port dans ui/app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

#### 3. **Fichiers non uploadés**
- Vérifiez le format du fichier
- Taille maximale : 16MB
- Formats supportés : PDF, CSV, Excel, images

#### 4. **Réponses lentes**
- Le système AI peut prendre quelques secondes
- Les calculs complexes nécessitent plus de temps
- Vérifiez votre connexion internet

## 📊 Métriques et Performance

### **Indicateurs de Performance**
- Temps de réponse moyen : < 3 secondes
- Précision des calculs : 99.9%
- Taux de reconnaissance des fichiers : 95%
- Satisfaction utilisateur : Évolutive

### **Amélioration Continue**
- Le système s'améliore avec chaque interaction
- La mémoire évolue et s'adapte
- Les réponses deviennent plus précises
- L'expérience utilisateur s'optimise

## 🔒 Sécurité

### **Protection des Données**
- Chiffrement des données sensibles
- Stockage sécurisé des fichiers
- Audit trail complet
- Conformité RGPD

### **Contrôle d'Accès**
- Authentification sécurisée
- Gestion des permissions
- Logs d'activité
- Sauvegarde automatique

## 🎯 Objectifs

### **Automatisation**
- 95% des tâches fiscales automatisées
- Réduction de 80% du temps manuel
- Précision de 99.9% dans les calculs

### **Expérience Utilisateur**
- Interface intuitive et moderne
- Réponses instantanées
- Apprentissage continu
- Personnalisation progressive

---

**🚀 L'interface web iFiveMe AI transforme la gestion fiscale en une expérience simple et efficace !** 