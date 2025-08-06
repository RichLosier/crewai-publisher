#!/usr/bin/env python3
"""
Système de publication automatique avec optimisation d'engagement
"""

import time
import schedule
from datetime import datetime
from engagement_monitor import EngagementMonitor
from test_approval import test_approval_dashboard
import subprocess
import os

class AutoPublisher:
    def __init__(self):
        self.monitor = EngagementMonitor()
        self.is_running = False
    
    def publish_at_optimal_time(self):
        """Publie à l'heure optimale"""
        current_time = datetime.now()
        print(f"\n⏰ {current_time.strftime('%H:%M:%S')} - Vérification de publication...")
        
        if self.monitor.should_publish_now():
            print("🚀 Heure optimale détectée ! Création d'une publication...")
            
            try:
                # Créer une nouvelle publication
                publication_id = test_approval_dashboard()
                
                # Enregistrer dans le système de surveillance
                self.monitor.record_publication(
                    publication_id=publication_id,
                    content="Publication automatique iFiveMe",
                    time_posted=current_time.isoformat(),
                    engagement_score=0.7  # Score par défaut, sera mis à jour après analyse
                )
                
                print(f"✅ Publication créée: {publication_id}")
                print("📊 Publication enregistrée pour analyse d'engagement")
                
                # Analyser l'engagement et optimiser
                self.monitor.analyze_engagement()
                
            except Exception as e:
                print(f"❌ Erreur lors de la publication: {str(e)}")
        else:
            next_time = self.monitor.get_next_publication_time()
            print(f"⏳ Prochaine publication prévue: {next_time}")
    
    def start_monitoring(self):
        """Démarre la surveillance continue"""
        print("🤖 SYSTÈME DE PUBLICATION AUTOMATIQUE")
        print("=" * 50)
        print("📊 Agent de surveillance: ACTIF")
        print("⏰ Optimisation d'engagement: ACTIVE")
        print("🎯 Heures optimales: 9h17, 12h30, 15h45, 19h30, 21h15")
        print("=" * 50)
        
        self.is_running = True
        
        # Programmer les vérifications toutes les 5 minutes
        schedule.every(5).minutes.do(self.publish_at_optimal_time)
        
        # Vérification immédiate
        self.publish_at_optimal_time()
        
        # Boucle principale
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # Vérifier toutes les minutes
    
    def stop_monitoring(self):
        """Arrête la surveillance"""
        self.is_running = False
        print("🛑 Surveillance arrêtée")
    
    def get_status(self):
        """Affiche le statut du système"""
        print("\n📊 STATUT DU SYSTÈME")
        print("=" * 30)
        
        # Heures optimales actuelles
        optimal_hours = self.monitor.optimal_hours
        print("⏰ Heures optimales:")
        for period, time in optimal_hours.items():
            print(f"   {period}: {time}")
        
        # Prochaine publication
        next_pub = self.monitor.get_next_publication_time()
        print(f"\n📅 Prochaine publication: {next_pub}")
        
        # Statistiques
        total_pubs = len(self.monitor.engagement_data)
        print(f"📈 Publications totales: {total_pubs}")
        
        if total_pubs > 0:
            avg_engagement = sum(p.get('engagement_score', 0) for p in self.monitor.engagement_data) / total_pubs
            print(f"📊 Engagement moyen: {avg_engagement:.2f}")
        
        # Recommandations
        recommendations = self.monitor.get_engagement_recommendations()
        print(f"\n💡 Recommandations:")
        for rec in recommendations:
            print(f"   {rec}")

def main():
    """Interface principale"""
    publisher = AutoPublisher()
    
    print("🎯 SYSTÈME DE PUBLICATION AUTOMATIQUE iFiveMe")
    print("=" * 50)
    print("1. Démarrer la surveillance automatique")
    print("2. Voir le statut")
    print("3. Tester une publication")
    print("4. Quitter")
    print("=" * 50)
    
    while True:
        choice = input("\nVotre choix (1-4): ").strip()
        
        if choice == "1":
            print("\n🚀 Démarrage de la surveillance...")
            try:
                publisher.start_monitoring()
            except KeyboardInterrupt:
                print("\n🛑 Arrêt demandé par l'utilisateur")
                publisher.stop_monitoring()
        
        elif choice == "2":
            publisher.get_status()
        
        elif choice == "3":
            print("\n🧪 Test de publication...")
            publication_id = test_approval_dashboard()
            print(f"✅ Publication test créée: {publication_id}")
        
        elif choice == "4":
            print("👋 Au revoir !")
            break
        
        else:
            print("❌ Choix invalide")

if __name__ == "__main__":
    main() 