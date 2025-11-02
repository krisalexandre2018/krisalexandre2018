"""
Sistema de Agentes Inteligentes para GitHub Profile
"""

from .profile import ProfileAgent
from .projects import ProjectsAgent
from .documentation import DocumentationAgent
from .engagement import EngagementAgent
from .insights import InsightsAgent
from .quality import QualityAgent

__all__ = [
    'ProfileAgent',
    'ProjectsAgent',
    'DocumentationAgent',
    'EngagementAgent',
    'InsightsAgent',
    'QualityAgent'
]

__version__ = '1.0.0'
