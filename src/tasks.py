"""
Task definitions for the Personalized Education Assistant.
"""
from crewai import Task
from src.models import LearningMaterial, Quiz, ProjectSuggestions


class EducationTasks:
    """Factory class for creating education assistant tasks."""
    
    @staticmethod
    def curate_learning_materials_task(
        agent,
        topic: str,
        expertise_level: str,
        resources_per_category: int = 3
    ):
        """
        Task 1: Curate learning materials from the web.
        
        Args:
            agent: The Learning Material Agent
            topic: The topic to search for
            expertise_level: User's expertise level
            resources_per_category: Number of resources per category
        """
        return Task(
            description=f"""
            Search and curate high-quality learning materials for the topic: "{topic}"
            Target audience expertise level: {expertise_level}
            
            Your task:
            1. Search for the BEST learning resources online
            2. Find {resources_per_category} high-quality videos (YouTube, educational platforms, tutorials)
            3. Find {resources_per_category} comprehensive articles (blog posts, documentation, guides)
            4. Find {resources_per_category} practical exercises (coding challenges, practice problems, worksheets)
            
            Quality criteria:
            - Prioritize authoritative sources (official docs, reputable platforms, known experts)
            - Ensure content matches the {expertise_level} expertise level
            - Look for recent, up-to-date content (prefer content from last 2 years)
            - Verify links are accessible and functional
            - Ensure good mix of different learning styles (visual, reading, practical)
            
            For each resource provide:
            - Exact title
            - Direct URL
            - Clear description of what it covers
            - Resource type (video/article/exercise)
            
            Also provide a brief summary of the recommended learning path.
            """,
            expected_output=f"""
            A structured collection of {resources_per_category} videos, {resources_per_category} articles, 
            and {resources_per_category} exercises, with complete details (title, URL, description) 
            for each resource, plus an overall learning path summary.
            """,
            agent=agent,
            output_pydantic=LearningMaterial
        )
    
    @staticmethod
    def create_quiz_task(
        agent,
        learning_materials_task,
        num_questions: int = 5
    ):
        """
        Task 2: Create quiz based on learning materials.
        
        Args:
            agent: The Quiz Creator Agent
            learning_materials_task: The previous task to get context from
            num_questions: Number of quiz questions to generate
        """
        return Task(
            description=f"""
            Based on the learning materials curated in the previous task, create a comprehensive 
            multiple-choice quiz with {num_questions} questions.
            
            Your task:
            1. Analyze the learning materials provided
            2. Identify the key concepts and learning objectives
            3. Create {num_questions} multiple-choice questions that test understanding
            
            Question guidelines:
            - Each question should have exactly 4 options (A, B, C, D)
            - Questions should range from easy to medium difficulty
            - Focus on understanding and application, not just memorization
            - Ensure only ONE option is clearly correct
            - Avoid trick questions or ambiguous wording
            - Cover different aspects of the topic
            
            For each question provide:
            - Clear, well-formulated question text
            - 4 distinct options labeled A, B, C, D
            - The correct answer (A, B, C, or D)
            - A helpful explanation of why that answer is correct
            - Difficulty level (easy, medium, or hard)
            
            Also estimate the total time needed to complete the quiz.
            """,
            expected_output=f"""
            A complete quiz with {num_questions} multiple-choice questions, each with 4 options, 
            correct answer, explanation, and difficulty level. Include estimated completion time.
            """,
            agent=agent,
            context=[learning_materials_task],
            output_pydantic=Quiz
        )
    
    @staticmethod
    def suggest_projects_task(
        agent,
        learning_materials_task,
        topic: str,
        expertise_level: str,
        num_projects: int = 2
    ):
        """
        Task 3: Suggest project ideas based on learning materials.
        
        Args:
            agent: The Project Idea Agent
            learning_materials_task: The previous task to get context from
            topic: The main topic
            expertise_level: User's expertise level
            num_projects: Number of project ideas to suggest
        """
        return Task(
            description=f"""
            Based on the learning materials and quiz from previous tasks, suggest {num_projects} 
            practical project ideas for the topic: "{topic}"
            Target expertise level: {expertise_level}
            
            Your task:
            1. Analyze the learning materials to understand what concepts were covered
            2. Design {num_projects} hands-on project ideas that apply these concepts
            3. Ensure projects are appropriate for {expertise_level} level
            
            Project design principles:
            - Projects should be practical and build real, tangible outcomes
            - Include clear, measurable deliverables
            - Specify what the learner will gain from completing the project
            - Provide realistic time estimates
            - List key concepts that will be applied
            
            For each project provide:
            - Compelling, descriptive title
            - High-level description (what needs to be built)
            - Expertise level confirmation
            - Estimated duration (hours or days)
            - List of 3-5 key concepts covered
            - 3-5 specific deliverables (what will be produced)
            - 3-5 learning outcomes (what skills/knowledge will be gained)
            
            Ensure projects are:
            - Beginner: Simple, focused on fundamentals, completable in 1-3 days
            - Intermediate: Multi-faceted, require integration of concepts, 3-7 days
            - Advanced: Complex, real-world scenarios, optimization focused, 1-2 weeks
            """,
            expected_output=f"""
            {num_projects} well-structured project ideas, each with title, description, 
            key concepts, detailed deliverables, learning outcomes, and time estimate.
            """,
            agent=agent,
            context=[learning_materials_task],
            output_pydantic=ProjectSuggestions
        )
