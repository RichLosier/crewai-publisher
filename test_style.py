#!/usr/bin/env python3
"""
Test du style amélioré des agents
"""

import os
from dotenv import load_dotenv
import yaml
from crewai import Agent, Task, Crew
from crewai.memory import LongTermMemory

# Load environment variables
load_dotenv()

def test_improved_style():
    """Test du style amélioré des agents"""
    
    print("🎨 TEST DU STYLE AMÉLIORÉ")
    print("=" * 50)
    
    # Create agents with improved style
    content_creator = Agent(
        name="Content Creator",
        role="Creator of impactful editorial concepts",
        goal="Generate inspiring and engaging content ideas for iFiveMe that use modern, positive language. Focus on questions like 'Et si vous...?', 'Osez...', 'Découvrez...'. Create concepts that inspire rather than promote. All content must be in French with the iFiveMe style: engaging, modern, benefit-driven.",
        backstory="I am Content Creator, specialized in creating inspiring content concepts for iFiveMe.",
        verbose=True
    )
    
    copywriter = Agent(
        name="Copywriter",
        role="Modern, inspiring copywriter",
        goal="Write compelling French content in the iFiveMe style: inspiring, modern, and engaging. Use questions like 'Et si vous...?', positive language like 'Osez l'efficacité', 'Découvrez la vraie modernité'. Focus on benefits and inspiration, not promotions. Include relevant hashtags like #iFiveMe #carteaffairesvirtuelle #réseautage #professionnelle #numérique #business #connexion #partage #entrepreneur #succès.",
        backstory="I am Copywriter, specialized in writing modern, inspiring content for iFiveMe.",
        verbose=True
    )
    
    # Create tasks
    concept_task = Task(
        description="Create an inspiring content concept for iFiveMe virtual business card",
        agent=content_creator,
        expected_output="An inspiring content concept in the iFiveMe style"
    )
    
    writing_task = Task(
        description="Write a compelling Facebook post based on the concept",
        agent=copywriter,
        expected_output="A complete Facebook post in French with the iFiveMe style"
    )
    
    # Create crew
    crew = Crew(
        agents=[content_creator, copywriter],
        tasks=[concept_task, writing_task],
        verbose=True,
        process="sequential"
    )
    
    # Execute
    print("🚀 Lancement du test avec le style amélioré...")
    result = crew.kickoff()
    
    print("\n" + "=" * 50)
    print("📝 RÉSULTAT DU TEST :")
    print("=" * 50)
    print(str(result))
    print("=" * 50)

if __name__ == "__main__":
    test_improved_style() 