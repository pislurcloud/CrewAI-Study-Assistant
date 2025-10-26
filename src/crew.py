"""
Main Crew orchestration for the Personalized Education Assistant.
"""
from crewai import Crew, Process
from src.agents import EducationAgents
from src.tasks import EducationTasks
from typing import Dict, Any


class EducationCrew:
    """Main crew for orchestrating the education assistant workflow."""
    
    def __init__(self, llm_provider: str = None):
        """
        Initialize the education crew.
        
        Args:
            llm_provider: LLM provider to use (openrouter or groq)
        """
        self.agents_factory = EducationAgents(llm_provider)
        self.tasks_factory = EducationTasks()
    
    def run(
        self,
        topic: str,
        expertise_level: str,
        resources_per_category: int = 3,
        num_questions: int = 5,
        num_projects: int = 2
    ) -> Dict[str, Any]:
        """
        Run the complete education assistant workflow.
        
        Args:
            topic: Topic of interest
            expertise_level: User's expertise level (beginner/intermediate/advanced)
            resources_per_category: Number of resources per category
            num_questions: Number of quiz questions
            num_projects: Number of project ideas
        
        Returns:
            Dictionary containing learning materials, quiz, and project suggestions
        """
        print(f"\n{'='*80}")
        print(f"🎓 PERSONALIZED EDUCATION ASSISTANT")
        print(f"{'='*80}")
        print(f"📚 Topic: {topic}")
        print(f"🎯 Expertise Level: {expertise_level.capitalize()}")
        print(f"📊 Parameters: {resources_per_category} resources/category, "
              f"{num_questions} questions, {num_projects} projects")
        print(f"{'='*80}\n")
        
        # Validate expertise level
        valid_levels = ["beginner", "intermediate", "advanced"]
        if expertise_level.lower() not in valid_levels:
            raise ValueError(f"Expertise level must be one of: {', '.join(valid_levels)}")
        
        # Create agents
        print("🤖 Initializing agents...")
        learning_agent = self.agents_factory.learning_material_agent()
        quiz_agent = self.agents_factory.quiz_creator_agent()
        project_agent = self.agents_factory.project_idea_agent()
        print("✓ Agents initialized\n")
        
        # Create tasks
        print("📋 Creating tasks...")
        task1 = self.tasks_factory.curate_learning_materials_task(
            agent=learning_agent,
            topic=topic,
            expertise_level=expertise_level,
            resources_per_category=resources_per_category
        )
        
        task2 = self.tasks_factory.create_quiz_task(
            agent=quiz_agent,
            learning_materials_task=task1,
            num_questions=num_questions
        )
        
        task3 = self.tasks_factory.suggest_projects_task(
            agent=project_agent,
            learning_materials_task=task1,
            topic=topic,
            expertise_level=expertise_level,
            num_projects=num_projects
        )
        print("✓ Tasks created\n")
        
        # Create and run crew
        print("🚀 Starting sequential workflow...\n")
        crew = Crew(
            agents=[learning_agent, quiz_agent, project_agent],
            tasks=[task1, task2, task3],
            process=Process.sequential,
            verbose=True
        )
        
        try:
            # Execute the crew
            result = crew.kickoff()
            
            print(f"\n{'='*80}")
            print("✅ WORKFLOW COMPLETED SUCCESSFULLY!")
            print(f"{'='*80}\n")
            
            # Extract structured outputs from tasks
            learning_materials = task1.output.pydantic
            quiz = task2.output.pydantic
            projects = task3.output.pydantic
            
            return {
                "success": True,
                "topic": topic,
                "expertise_level": expertise_level,
                "learning_materials": learning_materials,
                "quiz": quiz,
                "projects": projects,
                "raw_output": result
            }
            
        except Exception as e:
            print(f"\n{'='*80}")
            print(f"❌ ERROR: {str(e)}")
            print(f"{'='*80}\n")
            
            # Try fallback to Groq if we were using OpenRouter
            if self.agents_factory.active_provider == "openrouter":
                print("🔄 Attempting fallback to Groq...\n")
                self.agents_factory = EducationAgents("groq")
                return self.run(topic, expertise_level, resources_per_category, 
                              num_questions, num_projects)
            
            return {
                "success": False,
                "error": str(e),
                "topic": topic,
                "expertise_level": expertise_level
            }


def create_education_crew(llm_provider: str = None) -> EducationCrew:
    """Factory function to create an EducationCrew instance."""
    return EducationCrew(llm_provider)
