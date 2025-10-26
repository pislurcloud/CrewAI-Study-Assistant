"""
Personalized Education Assistant - A CrewAI-powered learning system.
"""
from src.crew import EducationCrew, create_education_crew
from src.models import LearningMaterial, Quiz, ProjectSuggestions

__all__ = [
    'EducationCrew',
    'create_education_crew',
    'LearningMaterial',
    'Quiz',
    'ProjectSuggestions'
]

__version__ = "1.0.0"
