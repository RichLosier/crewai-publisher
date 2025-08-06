#!/usr/bin/env python3
"""
Script de lancement pour l'interface web du système fiscal AI
"""
import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """Vérifier que toutes les dépendances sont installées"""
    print("🔍 Vérification des dépendances...")
    
    try:
        import flask
        import flask_uploads
        print("✅ Flask et extensions installées")
    except ImportError:
        print("❌ Flask manquant. Installation...")
        subprocess.run([sys.executable, "-m", "pip", "install", "flask", "flask-uploads"])
    
    try:
        from main import FiscalAICrew
        print("✅ Système fiscal AI chargé")
    except ImportError as e:
        print(f"❌ Erreur lors du chargement du système: {e}")
        return False
    
    return True

def create_directories():
    """Créer les répertoires nécessaires"""
    directories = [
        'uploads',
        'data',
        'ui/templates'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Répertoire créé/vérifié: {directory}")

def launch_web_interface():
    """Lancer l'interface web"""
    print("🚀 Lancement de l'interface web...")
    
    # Lancer l'application Flask
    try:
        # Changer vers le répertoire ui et importer
        ui_dir = os.path.join(os.getcwd(), 'ui')
        sys.path.insert(0, ui_dir)
        os.chdir(ui_dir)
        
        from app import app
        print("✅ Application Flask chargée")
        print("🌐 Interface disponible sur: http://localhost:5001")
        print("📱 Ouvrez votre navigateur pour accéder à l'interface")
        
        # Ouvrir automatiquement le navigateur après 2 secondes
        def open_browser():
            time.sleep(2)
            webbrowser.open('http://localhost:5001')
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Lancer l'application
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        return False
    
    return True

def main():
    """Fonction principale"""
    print("🤖 Lancement de l'Interface Web - Système Fiscal AI")
    print("=" * 60)
    
    # Vérifier les dépendances
    if not check_dependencies():
        print("❌ Impossible de lancer l'interface. Vérifiez les dépendances.")
        return False
    
    # Créer les répertoires
    create_directories()
    
    # Lancer l'interface
    return launch_web_interface()

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Interface arrêtée par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        sys.exit(1) 