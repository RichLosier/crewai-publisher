#!/usr/bin/env python3
"""
Tableau de bord local pour voir les publications CrewAI
"""
import os
import json
import datetime
from dotenv import load_dotenv

load_dotenv()

class PublicationDashboard:
    def __init__(self):
        self.publications_file = "publications.json"
        self.load_publications()
    
    def load_publications(self):
        """Charge les publications existantes"""
        if os.path.exists(self.publications_file):
            with open(self.publications_file, 'r', encoding='utf-8') as f:
                self.publications = json.load(f)
        else:
            self.publications = []
    
    def add_publication(self, content, image, status="created"):
        """Ajoute une nouvelle publication"""
        publication = {
            "id": len(self.publications) + 1,
            "timestamp": datetime.datetime.now().isoformat(),
            "content": content,
            "image": image,
            "status": status,  # created, sent_to_make, published
            "make_webhook_url": os.getenv("MAKE_WEBHOOK_URL", ""),
            "google_drive_folder": os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")
        }
        
        self.publications.append(publication)
        self.save_publications()
        return publication
    
    def save_publications(self):
        """Sauvegarde les publications"""
        with open(self.publications_file, 'w', encoding='utf-8') as f:
            json.dump(self.publications, f, indent=2, ensure_ascii=False)
    
    def display_dashboard(self):
        """Affiche le tableau de bord"""
        print("📊 TABLEAU DE BORD CREWAI")
        print("=" * 50)
        
        if not self.publications:
            print("📭 Aucune publication trouvée")
            print("\n💡 Pour créer une publication:")
            print("   python3 main.py")
            return
        
        print(f"📈 Total des publications: {len(self.publications)}")
        print("\n" + "=" * 50)
        
        for pub in self.publications:
            print(f"\n📋 Publication #{pub['id']}")
            print(f"   📅 Date: {pub['timestamp']}")
            print(f"   📊 Statut: {pub['status']}")
            print(f"   🖼️ Image: {pub['image']}")
            print(f"   📝 Contenu: {pub['content'][:100]}...")
            
            if pub['status'] == "published":
                print("   ✅ Publié sur Facebook")
            elif pub['status'] == "sent_to_make":
                print("   🔄 Envoyé à Make.com")
            else:
                print("   📝 Créé par CrewAI")
        
        print("\n" + "=" * 50)
        print("🎯 OÙ VOIR VOS PUBLICATIONS:")
        print("   1. 📊 Ce tableau de bord (local)")
        print("   2. 🔗 Make.com (logs et statut)")
        print("   3. 📘 Facebook (une fois publié)")
        print("   4. 📁 Fichier: publications.json")

def create_sample_publication():
    """Crée une publication d'exemple"""
    dashboard = PublicationDashboard()
    
    # Publication d'exemple
    sample_content = """🎶 Libère ta musique sans interruptions ! 🚀

Tu es passionné de musique et tu veux profiter de tes morceaux préférés sans aucune publicité ? Rejoins notre service de streaming aujourd'hui et découvre une écoute fluide comme jamais auparavant ! 🌐✨

Avec notre abonnement, tu vas bénéficier de :

✅ Accès illimité à des millions de titres
✅ Une expérience d'écoute sans interruptions
✅ La possibilité de créer des playlists personnalisées
✅ Des suggestions basées sur tes goûts musicaux

Ne laisse pas les publicités gâcher ton moment ! Prends un abonnement dès maintenant et plonge dans un univers musical qui t'appartient ! 🥳🎧

👉 Clique ici pour commencer ta période d'essai gratuite et découvre la musique à un tout autre niveau !

#MusicLovers #Streaming #AdFree #JoinUs #MusicWithoutLimits 🎵"""
    
    sample_image = "freepik__crer-une-image-dans-un-style-3d-semiraliste-inspir__48353.jpeg"
    
    publication = dashboard.add_publication(sample_content, sample_image, "created")
    print(f"✅ Publication d'exemple créée: #{publication['id']}")
    
    return dashboard

def main():
    """Fonction principale"""
    print("🎯 TABLEAU DE BORD CREWAI")
    print("=" * 50)
    
    # Créer le tableau de bord
    dashboard = PublicationDashboard()
    
    # Si aucune publication, créer un exemple
    if not dashboard.publications:
        print("📝 Création d'une publication d'exemple...")
        dashboard = create_sample_publication()
    
    # Afficher le tableau de bord
    dashboard.display_dashboard()
    
    print("\n🔧 COMMANDES UTILES:")
    print("   python3 main.py                    # Créer une nouvelle publication")
    print("   python3 dashboard.py               # Voir ce tableau de bord")
    print("   cat publications.json              # Voir les données brutes")
    print("   python3 test_make_webhook.py      # Tester Make.com")

if __name__ == "__main__":
    main() 