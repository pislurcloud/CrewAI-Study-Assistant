"""
Command-line interface for the Personalized Education Assistant.
"""
import argparse
import json
from datetime import datetime
from src.crew import create_education_crew
from src.config import config


def print_separator(char="=", length=80):
    """Print a separator line."""
    print(char * length)


def print_learning_materials(materials):
    """Print learning materials in a formatted way."""
    print("\n" + "="*80)
    print("📚 LEARNING MATERIALS")
    print("="*80)
    
    print(f"\n📝 Learning Path Summary:")
    print(f"{materials.summary}\n")
    
    if materials.videos:
        print("\n🎥 VIDEO RESOURCES:")
        print("-" * 80)
        for i, video in enumerate(materials.videos, 1):
            print(f"\n{i}. {video.title}")
            print(f"   URL: {video.url}")
            print(f"   Description: {video.description}")
    
    if materials.articles:
        print("\n📄 ARTICLE RESOURCES:")
        print("-" * 80)
        for i, article in enumerate(materials.articles, 1):
            print(f"\n{i}. {article.title}")
            print(f"   URL: {article.url}")
            print(f"   Description: {article.description}")
    
    if materials.exercises:
        print("\n💪 PRACTICE EXERCISES:")
        print("-" * 80)
        for i, exercise in enumerate(materials.exercises, 1):
            print(f"\n{i}. {exercise.title}")
            print(f"   URL: {exercise.url}")
            print(f"   Description: {exercise.description}")


def print_quiz(quiz):
    """Print quiz in a formatted way."""
    print("\n" + "="*80)
    print("📝 KNOWLEDGE ASSESSMENT QUIZ")
    print("="*80)
    print(f"\nTotal Questions: {quiz.total_questions}")
    print(f"Estimated Time: {quiz.estimated_time_minutes} minutes\n")
    
    for i, question in enumerate(quiz.questions, 1):
        print(f"\nQuestion {i} (Difficulty: {question.difficulty}):")
        print(f"{question.question}\n")
        
        for option in question.options:
            marker = "✓" if option.option == question.correct_answer else " "
            print(f"  [{marker}] {option.option}) {option.text}")
        
        print(f"\n  💡 Correct Answer: {question.correct_answer}")
        print(f"  📖 Explanation: {question.explanation}")
        print("-" * 80)


def print_projects(projects):
    """Print project suggestions in a formatted way."""
    print("\n" + "="*80)
    print("🚀 PROJECT IDEAS")
    print("="*80)
    print(f"\nTotal Projects: {projects.total_projects}\n")
    
    for i, project in enumerate(projects.projects, 1):
        print(f"\n{'='*80}")
        print(f"PROJECT {i}: {project.title}")
        print(f"{'='*80}")
        
        print(f"\n📋 Description:")
        print(f"{project.description}")
        
        print(f"\n🎯 Expertise Level: {project.expertise_level}")
        print(f"⏱️  Estimated Duration: {project.estimated_duration}")
        
        print(f"\n🔑 Key Concepts:")
        for concept in project.key_concepts:
            print(f"  • {concept}")
        
        print(f"\n📦 Deliverables:")
        for j, deliverable in enumerate(project.deliverables, 1):
            print(f"  {j}. {deliverable.name}")
            print(f"     {deliverable.description}")
        
        print(f"\n🎓 Learning Outcomes:")
        for outcome in project.learning_outcomes:
            print(f"  • {outcome}")


def save_to_file(result, filename=None):
    """Save result to a JSON file."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        topic_slug = result["topic"].replace(" ", "_").lower()
        filename = f"learning_plan_{topic_slug}_{timestamp}.json"
    
    export_data = {
        "topic": result["topic"],
        "expertise_level": result["expertise_level"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "learning_materials": result["learning_materials"].model_dump(),
        "quiz": result["quiz"].model_dump(),
        "projects": result["projects"].model_dump()
    }
    
    with open(filename, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"\n✅ Results saved to: {filename}")
    return filename


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Personalized Education Assistant - Generate customized learning plans",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "topic",
        type=str,
        help="Topic you want to learn about"
    )
    
    parser.add_argument(
        "-l", "--level",
        type=str,
        choices=["beginner", "intermediate", "advanced"],
        default="beginner",
        help="Your expertise level (default: beginner)"
    )
    
    parser.add_argument(
        "-r", "--resources",
        type=int,
        default=config.default_resources_per_category,
        help=f"Number of resources per category (default: {config.default_resources_per_category})"
    )
    
    parser.add_argument(
        "-q", "--questions",
        type=int,
        default=config.default_quiz_questions,
        help=f"Number of quiz questions (default: {config.default_quiz_questions})"
    )
    
    parser.add_argument(
        "-p", "--projects",
        type=int,
        default=config.default_project_count,
        help=f"Number of project ideas (default: {config.default_project_count})"
    )
    
    parser.add_argument(
        "--llm",
        type=str,
        choices=["openrouter", "groq"],
        default="openrouter",
        help="LLM provider to use (default: openrouter)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Output filename for JSON export"
    )
    
    parser.add_argument(
        "--no-display",
        action="store_true",
        help="Don't display results in console (only save to file)"
    )
    
    args = parser.parse_args()
    
    # Validate API keys
    try:
        config.validate_api_keys()
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nPlease set your API keys in the .env file")
        return 1
    
    # Create and run crew
    try:
        print("\n🎓 PERSONALIZED EDUCATION ASSISTANT")
        print_separator()
        print(f"📚 Topic: {args.topic}")
        print(f"🎯 Expertise Level: {args.level.capitalize()}")
        print(f"🤖 LLM Provider: {args.llm}")
        print_separator()
        
        crew = create_education_crew(args.llm)
        result = crew.run(
            topic=args.topic,
            expertise_level=args.level,
            resources_per_category=args.resources,
            num_questions=args.questions,
            num_projects=args.projects
        )
        
        if not result["success"]:
            print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
            return 1
        
        # Display results
        if not args.no_display:
            print_learning_materials(result["learning_materials"])
            print_quiz(result["quiz"])
            print_projects(result["projects"])
        
        # Save to file
        if args.output or args.no_display:
            save_to_file(result, args.output)
        
        print("\n" + "="*80)
        print("✅ LEARNING PLAN GENERATED SUCCESSFULLY!")
        print("="*80 + "\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
