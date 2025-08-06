#!/usr/bin/env python3
"""
Agent de surveillance pour analyser l'engagement et optimiser les heures de publication
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import random

class EngagementMonitor:
    def __init__(self):
        self.engagement_data_file = 'engagement_data.json'
        self.optimal_hours_file = 'optimal_hours.json'
        self.load_data()
    
    def load_data(self):
        """Charge les données d'engagement et les heures optimales"""
        try:
            with open(self.engagement_data_file, 'r') as f:
                self.engagement_data = json.load(f)
        except FileNotFoundError:
            self.engagement_data = []
        
        try:
            with open(self.optimal_hours_file, 'r') as f:
                self.optimal_hours = json.load(f)
        except FileNotFoundError:
            # Heures optimales par défaut basées sur les études
            self.optimal_hours = {
                'morning': '09:17',
                'noon': '12:30',
                'afternoon': '15:45',
                'evening': '19:30',
                'night': '21:15'
            }
    
    def save_data(self):
        """Sauvegarde les données"""
        with open(self.engagement_data_file, 'w') as f:
            json.dump(self.engagement_data, f, indent=2)
        
        with open(self.optimal_hours_file, 'w') as f:
            json.dump(self.optimal_hours, f, indent=2)
    
    def record_publication(self, publication_id: str, content: str, time_posted: str, 
                          engagement_score: float = None):
        """Enregistre une nouvelle publication avec son score d'engagement"""
        publication_data = {
            'id': publication_id,
            'content': content,
            'time_posted': time_posted,
            'engagement_score': engagement_score,
            'timestamp': datetime.now().isoformat(),
            'hour': datetime.fromisoformat(time_posted).hour,
            'day_of_week': datetime.fromisoformat(time_posted).strftime('%A')
        }
        
        self.engagement_data.append(publication_data)
        self.save_data()
        
        print(f"📊 Publication enregistrée: {publication_id} à {time_posted}")
    
    def analyze_engagement(self) -> Dict:
        """Analyse les données d'engagement pour optimiser les heures"""
        if not self.engagement_data:
            return self.optimal_hours
        
        # Analyser les performances par heure
        hourly_performance = {}
        for pub in self.engagement_data:
            hour = pub['hour']
            score = pub.get('engagement_score', 0.5)  # Score par défaut si non disponible
            
            if hour not in hourly_performance:
                hourly_performance[hour] = {'total_score': 0, 'count': 0}
            
            hourly_performance[hour]['total_score'] += score
            hourly_performance[hour]['count'] += 1
        
        # Calculer les moyennes
        for hour in hourly_performance:
            hourly_performance[hour]['average'] = (
                hourly_performance[hour]['total_score'] / 
                hourly_performance[hour]['count']
            )
        
        # Trouver les meilleures heures
        best_hours = sorted(
            hourly_performance.items(), 
            key=lambda x: x[1]['average'], 
            reverse=True
        )
        
        # Mettre à jour les heures optimales
        if best_hours:
            self.optimal_hours = {
                'morning': f"{best_hours[0][0]:02d}:17",
                'noon': f"{best_hours[1][0] if len(best_hours) > 1 else 12:02d}:30",
                'afternoon': f"{best_hours[2][0] if len(best_hours) > 2 else 15:02d}:45",
                'evening': f"{best_hours[3][0] if len(best_hours) > 3 else 19:02d}:30",
                'night': f"{best_hours[4][0] if len(best_hours) > 4 else 21:02d}:15"
            }
        
        self.save_data()
        
        print("🎯 Analyse d'engagement terminée")
        print(f"📈 Meilleures heures: {best_hours[:3] if best_hours else 'Pas assez de données'}")
        
        return self.optimal_hours
    
    def get_next_publication_time(self) -> str:
        """Détermine la prochaine heure de publication optimale"""
        current_time = datetime.now()
        current_hour = current_time.hour
        
        # Déterminer la période de la journée
        if 6 <= current_hour < 12:
            period = 'morning'
        elif 12 <= current_hour < 16:
            period = 'noon'
        elif 16 <= current_hour < 19:
            period = 'afternoon'
        elif 19 <= current_hour < 22:
            period = 'evening'
        else:
            period = 'night'
        
        # Obtenir l'heure optimale pour cette période
        optimal_time = self.optimal_hours.get(period, '09:17')
        hour, minute = map(int, optimal_time.split(':'))
        
        # Calculer la prochaine publication
        next_publication = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # Si l'heure est déjà passée aujourd'hui, programmer pour demain
        if next_publication <= current_time:
            next_publication += timedelta(days=1)
        
        return next_publication.isoformat()
    
    def should_publish_now(self) -> bool:
        """Vérifie s'il est temps de publier maintenant"""
        current_time = datetime.now()
        next_time = datetime.fromisoformat(self.get_next_publication_time())
        
        # Publier si on est dans la fenêtre de 5 minutes autour de l'heure optimale
        time_diff = abs((current_time - next_time).total_seconds())
        return time_diff <= 300  # 5 minutes
    
    def get_engagement_recommendations(self) -> List[str]:
        """Génère des recommandations basées sur l'analyse d'engagement"""
        recommendations = []
        
        if len(self.engagement_data) < 5:
            recommendations.append("📊 Collectez plus de données d'engagement pour optimiser les heures")
            recommendations.append("⏰ Utilisez les heures par défaut pour commencer")
        else:
            best_hour = max(self.engagement_data, key=lambda x: x.get('engagement_score', 0))
            recommendations.append(f"🎯 Heure optimale: {best_hour['hour']}h")
            recommendations.append("📈 Continuez à publier aux heures de forte engagement")
        
        return recommendations

def main():
    """Test de l'agent de surveillance"""
    monitor = EngagementMonitor()
    
    print("🤖 AGENT DE SURVEILLANCE ENGAGEMENT")
    print("=" * 50)
    
    # Simuler quelques publications
    test_publications = [
        ("pub_001", "Contenu test 1", "2025-08-03T09:17:00", 0.8),
        ("pub_002", "Contenu test 2", "2025-08-03T12:30:00", 0.6),
        ("pub_003", "Contenu test 3", "2025-08-03T15:45:00", 0.9),
        ("pub_004", "Contenu test 4", "2025-08-03T19:30:00", 0.7),
    ]
    
    for pub_id, content, time, score in test_publications:
        monitor.record_publication(pub_id, content, time, score)
    
    # Analyser l'engagement
    optimal_hours = monitor.analyze_engagement()
    
    print(f"\n⏰ Heures optimales actuelles:")
    for period, time in optimal_hours.items():
        print(f"   {period}: {time}")
    
    print(f"\n📅 Prochaine publication: {monitor.get_next_publication_time()}")
    
    recommendations = monitor.get_engagement_recommendations()
    print(f"\n💡 Recommandations:")
    for rec in recommendations:
        print(f"   {rec}")

if __name__ == "__main__":
    main() 