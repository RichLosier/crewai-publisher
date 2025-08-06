#!/usr/bin/env python3
"""
Script de test rapide pour le dashboard d'approbation
Simule une publication CrewAI sans lancer tout le processus
"""

import json
import uuid
import os
import shutil
from datetime import datetime
from approval_dashboard import ApprovalDashboard

def test_approval_dashboard():
    """Test rapide du dashboard d'approbation"""
    
    print("🎯 TEST RAPIDE DU DASHBOARD D'APPROBATION")
    print("=" * 50)
    
    # Créer des publications de test avec différents horaires
    import random
    
    publications = [
        {
            'content': """✨ Et si vous donniez une nouvelle dimension à vos connexions matinales ?

La première impression de la journée peut tout changer. Chaque interaction matinale est une opportunité de créer une connexion authentique et mémorable ! 💼

Chez iFiveMe, nous croyons que les vraies connexions se créent dans l'authenticité. C'est pourquoi notre carte d'affaires virtuelle vous permet de partager votre essence professionnelle en un simple clic.

🤝 **Pourquoi choisir la connexion authentique ?**
- **Simplicité** : Partagez votre profil en quelques secondes
- **Mémorabilité** : Laissez une impression durable
- **Accessibilité** : Toujours disponible, partout
- **Innovation** : La technologie au service des relations humaines

Osez l'efficacité au bout des doigts et tissez votre réseau ! 🚀

#iFiveMe #carteaffairesvirtuelle #réseautage #professionnelle #numérique #business #connexion #réseau #partage #entrepreneur #succès""",
            'image': 'downloaded_freepik__crer-une-image-dans-un-style-3d-semiraliste-inspir__48353.jpeg',
            'hashtags': ['#iFiveMe', '#carteaffairesvirtuelle', '#réseautage', '#professionnelle', '#numérique'],
            'time': 'morning'
        },
        {
            'content': """🌞 Et si vous révolutionniez vos pauses pour maximiser votre impact ?

La productivité ne rime pas toujours avec travail acharné. Les vraies pauses sont celles qui vous ressourcent et vous reconnectent avec votre mission ! 💡

Au lieu de scroller sans fin, prenez le temps de :
- **Réfléchir** à vos objectifs du jour
- **Planifier** vos prochaines connexions
- **Apprendre** quelque chose de nouveau
- **Partager** une valeur avec votre réseau

Chaque pause peut devenir un moment de croissance ! 📈

#iFiveMe #productivité #croissance #réseau #innovation #développement #connexion #business #entrepreneur #succès""",
            'image': 'downloaded_freepik__crer-une-image-dans-un-style-3d-semiraliste-lumine__10018.jpeg',
            'hashtags': ['#iFiveMe', '#productivité', '#croissance', '#réseau', '#innovation'],
            'time': 'noon'
        },
        {
            'content': """🌙 Et si vous transformiez la fin de journée en moment de réflexion stratégique ?

Le networking ne s'arrête pas à 18h. Les vraies connexions se cultivent dans la continuité et l'authenticité ! ✨

Prenez quelques minutes pour :
- **Analyser** vos interactions de la journée
- **Planifier** vos prochaines connexions
- **Apprendre** de chaque échange
- **Préparer** demain avec intention

Chaque soir est une opportunité de préparer les connexions de demain ! 🚀

#iFiveMe #réflexion #stratégie #networking #croissance #connexion #innovation #business #entrepreneur #succès""",
            'image': 'downloaded_freepik__crer-une-image-dans-un-style-3d-semiraliste-inspir__48358.jpeg',
            'hashtags': ['#iFiveMe', '#réflexion', '#stratégie', '#networking', '#croissance'],
            'time': 'evening'
        }
    ]
    
    # Charger l'historique des images utilisées
    def load_image_history():
        try:
            with open('image_history.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_image_history(history):
        with open('image_history.json', 'w') as f:
            json.dump(history, f)
    
    # Vérifier quelles images sont disponibles
    available_images = [
        'downloaded_freepik__crer-une-image-dans-un-style-3d-semiraliste-inspir__48353.jpeg',
        'downloaded_freepik__crer-une-image-dans-un-style-3d-semiraliste-lumine__10018.jpeg',
        'downloaded_freepik__crer-une-image-dans-un-style-3d-semiraliste-inspir__48358.jpeg',
        'downloaded_freepik__crer-une-image-dans-un-style-3d-semiraliste-inspir__48355.jpeg',
        'downloaded_freepik__crer-une-image-dans-un-style-3d-semiraliste-inspir__48359.jpeg'
    ]
    
    # Charger l'historique
    image_history = load_image_history()
    
    # Sélectionner une publication aléatoire
    test_publication = random.choice(publications)
    
    # Choisir une image qui n'a pas été utilisée récemment (dans les 50 derniers posts)
    used_images = image_history[-50:] if len(image_history) > 50 else image_history
    available_for_use = [img for img in available_images if img not in used_images]
    
    if available_for_use:
        selected_image = random.choice(available_for_use)
    else:
        # Si toutes les images ont été utilisées récemment, prendre la plus ancienne
        selected_image = image_history[0] if image_history else available_images[0]
    
    # Mettre à jour l'image de la publication
    test_publication['image'] = selected_image
    
    # Ajouter l'image à l'historique
    image_history.append(selected_image)
    save_image_history(image_history)
    
    # Copier l'image dans le dossier static si elle existe
    image_file = test_publication['image']
    if os.path.exists(image_file):
        static_dir = 'static/images'
        os.makedirs(static_dir, exist_ok=True)
        shutil.copy2(image_file, os.path.join(static_dir, image_file))
        print(f"✅ Image copiée: {image_file}")
    
    # Ajouter au dashboard d'approbation
    dashboard = ApprovalDashboard()
    approval_id = dashboard.add_pending_publication(test_publication)
    
    print(f"✅ Publication de test créée avec l'ID: {approval_id[:8]}")
    print("🌐 Ouvrez votre navigateur sur: http://localhost:5001")
    print("📋 Vous devriez voir la publication en attente d'approbation")
    print("🔧 Vous pouvez approuver ou rejeter la publication")
    print("=" * 50)
    
    return approval_id

if __name__ == "__main__":
    test_approval_dashboard() 