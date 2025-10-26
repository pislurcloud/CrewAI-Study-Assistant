"""
Custom tools for the CrewAI agents.
"""
from crewai_tools import SerperDevTool
from crewai.tools import tool
from typing import List
from src.config import config


class EducationTools:
    """Collection of custom tools for the education assistant."""
    
    @staticmethod
    def get_search_tool():
        """Get configured SerperDev search tool."""
        return SerperDevTool(
            api_key=config.serper_api_key,
            n_results=10
        )
    
    @staticmethod
    @tool("Project Suggestion Tool")
    def project_suggestion_tool(topic: str, expertise_level: str, learning_context: str) -> str:
        """
        Generate project ideas tailored to the user's expertise level and topics of interest.
        
        Args:
            topic: The main topic for the project
            expertise_level: User's expertise level (beginner, intermediate, advanced)
            learning_context: Context from the learning materials to inform project suggestions
        
        Returns:
            A string with project suggestions and guidelines
        """
        # This tool provides context and guidelines for the LLM to generate projects
        guidelines = f"""
        Based on the following information, suggest practical project ideas:
        
        Topic: {topic}
        Expertise Level: {expertise_level}
        Learning Context: {learning_context}
        
        Guidelines for project suggestions:
        
        For BEGINNER level:
        - Focus on foundational concepts and simple implementations
        - Projects should be completable in 1-3 days
        - Emphasize learning core principles over complexity
        - Include clear, achievable deliverables
        - Suggest projects with plenty of online resources
        
        For INTERMEDIATE level:
        - Combine multiple concepts learned
        - Projects should take 3-7 days
        - Include some challenging aspects that require problem-solving
        - Encourage best practices and proper documentation
        - Add real-world application elements
        
        For ADVANCED level:
        - Focus on complex, real-world scenarios
        - Projects should take 1-2 weeks
        - Emphasize optimization, scalability, and architecture
        - Include integration with multiple technologies
        - Encourage innovation and creative solutions
        
        Each project should include:
        1. Clear, descriptive title
        2. High-level description of what needs to be built
        3. List of specific deliverables
        4. Key concepts that will be applied
        5. Expected learning outcomes
        6. Estimated duration
        """
        
        return guidelines


# Create tool instances
search_tool = EducationTools.get_search_tool()
project_tool = EducationTools.project_suggestion_tool
