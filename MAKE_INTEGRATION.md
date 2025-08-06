# 🔗 Guide d'intégration Make.com

## Vue d'ensemble

Ce guide explique comment intégrer CrewAI avec Make.com pour créer un système d'automatisation complet où :
- **CrewAI** = Le cerveau (analyse, décisions, planification)
- **Make.com** = Le bras (exécution des actions concrètes)

## 🏗️ Architecture

```
CrewAI Agents → Outils Make.com → Webhook Make.com → Actions concrètes
```

### Flux de données :
1. **Agent CrewAI** prend une décision
2. **Outil Make.com** envoie les données au webhook
3. **Make.com** exécute l'action (Facebook, Email, CRM, etc.)
4. **Résultat** retourné à CrewAI

## 🛠️ Configuration

### 1. Variables d'environnement

Ajoutez dans votre `.env` :

```env
# Configuration Make.com
MAKE_WEBHOOK_URL=https://your-make-scenario.webhook.com
MAKE_API_KEY=your_make_api_key_here

# Configuration Facebook (pour Make.com)
FACEBOOK_PAGE_ID=your_facebook_page_id
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token

# Configuration Email (pour Make.com)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# Configuration CRM (pour Make.com)
CRM_API_KEY=your_crm_api_key
CRM_BASE_URL=https://your-crm.com/api
```

### 2. Installation des dépendances

```bash
pip install -r requirements.txt
```

## 🧪 Test de l'intégration

### 1. Démarrer le simulateur de webhook

```bash
python make_webhook_example.py
```

### 2. Configurer l'URL du webhook

Dans votre `.env` :
```env
MAKE_WEBHOOK_URL=http://localhost:8080/webhook
```

### 3. Tester le crew

```bash
python main.py
```

## 📋 Actions disponibles

### Publication Facebook
```python
# Via l'agent "Coordinateur de Publication"
facebook_publisher._run(
    post_content="Votre contenu Facebook",
    image_url="https://example.com/image.jpg",
    scheduled_time="2024-01-15T10:00:00Z"
)
```

### Envoi d'email
```python
# Via l'agent "Analyste Performance"
email_sender._run(
    to_email="client@example.com",
    subject="Rapport de performance",
    body="Voici votre rapport..."
)
```

### Actions CRM
```python
# Via l'agent "Stratège Ciblage"
crm_tool._run(
    action="create_lead",
    customer_data={
        "name": "John Doe",
        "email": "john@example.com",
        "source": "facebook_campaign"
    }
)
```

## 🔧 Configuration Make.com

### 1. Créer un scénario Make.com

1. **Déclencheur** : Webhook
2. **Action** : Router (selon le type d'action)
3. **Actions** : Facebook, Email, CRM, etc.

### 2. Structure du webhook

```json
{
  "action": "publish_facebook",
  "data": {
    "post_content": "Contenu du post",
    "image_url": "https://example.com/image.jpg",
    "scheduled_time": "2024-01-15T10:00:00Z",
    "platform": "facebook"
  },
  "timestamp": "2024-01-15T09:00:00Z"
}
```

### 3. Actions supportées

| Action | Description | Agent responsable |
|--------|-------------|-------------------|
| `publish_facebook` | Publie sur Facebook | Coordinateur de Publication |
| `send_email` | Envoie un email | Analyste Performance |
| `crm_action` | Action CRM | Stratège Ciblage |
| `schedule_post` | Programme une publication | Planificateur Intelligent |
| `update_budget` | Met à jour le budget | Optimiseur de Budget |

## 🚀 Déploiement en production

### 1. Webhook Make.com public

Remplacez `http://localhost:8080/webhook` par votre URL Make.com publique.

### 2. Sécurité

- Utilisez des clés API sécurisées
- Validez les données reçues
- Implémentez une authentification

### 3. Monitoring

- Logs des actions exécutées
- Métriques de performance
- Alertes en cas d'erreur

## 🔄 Workflow complet

1. **CrewAI** analyse l'objectif
2. **Stratège Narratif** crée le concept
3. **Rédacteur Persuasif** rédige le contenu
4. **Curateur Visuel** sélectionne l'image
5. **Coordinateur de Publication** envoie à Make.com
6. **Make.com** publie sur Facebook
7. **Analyste Performance** mesure les résultats
8. **Planificateur Intelligent** optimise le timing

## 🎯 Avantages de cette architecture

- ✅ **Séparation des responsabilités** : CrewAI = cerveau, Make.com = exécution
- ✅ **Scalabilité** : Make.com gère les APIs complexes
- ✅ **Fiabilité** : Make.com a une haute disponibilité
- ✅ **Flexibilité** : Facile d'ajouter de nouvelles actions
- ✅ **Monitoring** : Make.com fournit des logs détaillés

## 🐛 Dépannage

### Erreur de connexion au webhook
- Vérifiez l'URL du webhook
- Testez avec `curl` ou Postman
- Vérifiez les logs Make.com

### Action non reconnue
- Vérifiez le nom de l'action dans le webhook
- Ajoutez la nouvelle action dans Make.com
- Mettez à jour les outils CrewAI

### Erreur d'authentification
- Vérifiez les clés API
- Testez les connexions individuellement
- Vérifiez les permissions Make.com 