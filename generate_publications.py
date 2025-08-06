#!/usr/bin/env python3
"""
Génère immédiatement 10 publications pour le dashboard
"""

import json
import uuid
from datetime import datetime

def generate_publications():
    """Génère 10 publications avec le style amélioré"""
    
    print("🚀 GÉNÉRATION IMMÉDIATE DE PUBLICATIONS")
    print("=" * 50)
    
    # Contenu avec le style amélioré
    content = """🌟 **Découvrez la carte de visite virtuelle iFiveMe : L'outil essentiel pour un networking captivant !** 🌟

Saviez-vous que votre première impression peut se jouer en une fraction de seconde ? Et si chaque rencontre devenait une opportunité d'échanger, d'inspirer et de créer des connexions authentiques ? Avec la carte de visite virtuelle iFiveMe, transformez la façon dont vous vous présentez au monde.

**Osez la modernité !** Dites adieu aux cartes en papier qui se perdent dans le fond de vos poches. Nous vivons à l'ère numérique, où la durabilité et l'innovation vont de pair. Offrez à vos contacts une expérience enrichissante en leur permettant de découvrir votre univers en un clic !

**Et si vous pouviez captiver avec créativité ?** Personnalisez votre carte de visite virtuelle pour qu'elle reflète votre personnalité, votre style et votre vision. Ajoutez des vidéos, des liens vers vos réseaux sociaux ou même vos réalisations. Chaque élément devient un point de conversation, un moyen de vous démarquer de la foule.

**Embarquez dans l'avenir du networking !** Imaginez pouvoir partager votre carte de visite via un simple QR code. Il n'a jamais été aussi simple d'initier une connexion, où que vous vous trouviez. En partageant votre histoire, vos compétences et vos passions, vous laissez une empreinte mémorable dans l'esprit de vos contacts.

Ne sous-estimez jamais le pouvoir d'une présentation soignée. Avec la carte de visite virtuelle iFiveMe, chaque aspect de votre identité professionnelle est à portée de main. Explorez les possibilités infinies qui s'offrent à vous et commencez à bâtir un réseau solide qui vous propulsera vers de nouveaux sommets.

**Alors, êtes-vous prêt à révolutionner votre façon de vous présenter ?** Osez faire le premier pas vers une communication inspirante et engageante. Découvrez iFiveMe et libérez le potentiel illimité de votre réseau dès aujourd'hui ! 🌟

#iFiveMe #carteaffairesvirtuelle #réseautage #professionnelle #numérique #business #connexion #partage #entrepreneur #succès"""

    # Créer 10 publications
    publications = []
    
    for i in range(10):
        publication = {
            "id": str(uuid.uuid4())[:8],
            "content": content,
            "image": "downloaded_freepik__crer-une-image-dans-un-style-3d-semiraliste-inspir__48353.jpeg",
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "agents": ["Content Creator", "Copywriter"],
            "style": "improved_inspiring"
        }
        publications.append(publication)
        print(f"✅ Publication {i+1}/10 créée - ID: {publication['id']}")
    
    # Sauvegarder
    with open('pending_approvals.json', 'w', encoding='utf-8') as f:
        json.dump(publications, f, ensure_ascii=False, indent=2)
    
    print("=" * 50)
    print(f"🎯 {len(publications)} publications générées avec succès !")
    print("🌐 Va voir ton dashboard : https://web-production-ad2cc.up.railway.app")
    print("=" * 50)

if __name__ == "__main__":
    generate_publications() 