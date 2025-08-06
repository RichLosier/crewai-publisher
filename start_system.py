#!/usr/bin/env python3
"""
Démarre le système complet : générateur automatique + dashboard
"""

import subprocess
import time
import threading
import os
from auto_generator import AutoPublicationGenerator

def start_generator():
    """Démarre le générateur automatique"""
    print("🚀 Démarrage du générateur automatique...")
    generator = AutoPublicationGenerator()
    generator.start_auto_generation()

def start_dashboard():
    """Démarre le dashboard"""
    print("🌐 Démarrage du dashboard...")
    os.system("python3 approval_dashboard.py")

def main():
    """Démarre le système complet"""
    print("🎯 SYSTÈME COMPLET CREWAI PUBLISHER")
    print("=" * 50)
    print("🚀 Générateur automatique de publications")
    print("🌐 Dashboard d'approbation")
    print("⏰ Maintient 10-20 publications en attente")
    print("🔄 Génération automatique lors des approbations")
    print("=" * 50)
    
    # Démarrer le générateur dans un thread séparé
    generator_thread = threading.Thread(target=start_generator, daemon=True)
    generator_thread.start()
    
    # Attendre un peu pour la première génération
    print("⏳ Attente de la première génération...")
    time.sleep(10)
    
    # Démarrer le dashboard
    start_dashboard()

if __name__ == "__main__":
    main() 