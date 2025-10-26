"""
Agent definitions for the Personalized Education Assistant.
"""
from crewai import Agent, LLM
from src.tools import search_tool, project_tool
from src.config import config


def create_llm(provider: str = None):
    """Create LLM instance with fallback support."""
    try:
        llm_config = config.get_llm_config(provider)
        
        # Use CrewAI's LLM class which handles LiteLLM integration
        # LiteLLM will automatically route based on provider prefix in model name
        llm = LLM(
            model=llm_config["model"],
            api_key=llm_config["api_key"],
            temperature=0.7
        )
        return llm, llm_config["provider"]
    except Exception as e:
        print(f"Error creating LLM with {provider}: {e}")
        # Try fallback
        if provider != "groq":
            print("Attempting fallback to Groq...")
            return create_llm("groq")
        raise


class EducationAgents:
    """Factory class for creating education assistant agents."""
    
    def __init__(self, llm_provider: str = None):
        """Initialize agents with specified LLM provider."""
        self.llm, self.active_provider = create_llm(llm_provider)
        print(f"✓ Using LLM provider: {self.active_provider}")
    
    def learning_material_agent(self):
        """Create the Learning Material Agent."""
        return Agent(
            role="Educational Content Curator",
            goal="Find and curate the highest quality learning resources (videos, articles, exercises) "
                 "for the specified topics and expertise level",
            backstory="You are an expert educational content curator with years of experience "
                     "in identifying the best learning resources across the internet. "
                     "You have a keen eye for quality, relevance, and pedagogical value. "
                     "You understand how different expertise levels require different types of content "
                     "and always prioritize authoritative sources like official documentation, "
                     "reputable educational platforms, and well-known experts in the field.",
            tools=[search_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def quiz_creator_agent(self):
        """Create the Quiz Creator Agent."""
        return Agent(
            role="Assessment Designer",
            goal="Create engaging and educational multiple-choice quizzes that test understanding "
                 "of the key concepts from the learning materials",
            backstory="You are an experienced educator and assessment designer who specializes in "
                     "creating effective multiple-choice questions. You understand learning psychology "
                     "and know how to craft questions that truly test comprehension rather than just "
                     "memorization. Your questions are clear, unambiguous, and include helpful "
                     "explanations that reinforce learning. You carefully align difficulty levels "
                     "with the user's expertise level, ensuring questions are challenging but fair.",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def project_idea_agent(self):
        """Create the Project Idea Agent."""
        return Agent(
            role="Project Advisor and Mentor",
            goal="Recommend practical, hands-on project ideas that allow learners to apply "
                 "their knowledge and build a portfolio",
            backstory="You are a seasoned mentor and project advisor who has guided hundreds of "
                     "learners through their educational journey. You excel at designing projects "
                     "that are both educational and practical, with clear deliverables and learning "
                     "outcomes. You understand how to scale project complexity based on expertise "
                     "level and always ensure projects are achievable yet challenging. Your project "
                     "suggestions are well-structured with clear deliverables and emphasize real-world "
                     "applications that will help learners build impressive portfolios.",
            tools=[project_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        