"""
Example usage script for the Personalized Education Assistant.
Demonstrates how to use the system programmatically.
"""
from src.crew import create_education_crew
import json


def example_basic_usage():
    """Basic usage example."""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Usage")
    print("="*80)
    
    # Create crew
    crew = create_education_crew(llm_provider="openrouter")
    
    # Run with minimal parameters
    result = crew.run(
        topic="Python Programming",
        expertise_level="beginner"
    )
    
    if result["success"]:
        print("\n✅ Success!")
        print(f"Found {len(result['learning_materials'].videos)} videos")
        print(f"Generated {result['quiz'].total_questions} quiz questions")
        print(f"Suggested {result['projects'].total_projects} projects")
    else:
        print(f"\n❌ Error: {result['error']}")


def example_custom_parameters():
    """Example with custom parameters."""
    print("\n" + "="*80)
    print("EXAMPLE 2: Custom Parameters")
    print("="*80)
    
    crew = create_education_crew(llm_provider="openrouter")
    
    result = crew.run(
        topic="Machine Learning",
        expertise_level="intermediate",
        resources_per_category=4,
        num_questions=7,
        num_projects=3
    )
    
    if result["success"]:
        print("\n✅ Generated comprehensive learning plan")
        
        # Access specific data
        materials = result['learning_materials']
        print(f"\nLearning Materials Summary:")
        print(f"- Videos: {len(materials.videos)}")
        print(f"- Articles: {len(materials.articles)}")
        print(f"- Exercises: {len(materials.exercises)}")
        
        # Show first video
        if materials.videos:
            video = materials.videos[0]
            print(f"\nFirst Video:")
            print(f"  Title: {video.title}")
            print(f"  URL: {video.url}")


def example_with_export():
    """Example with JSON export."""
    print("\n" + "="*80)
    print("EXAMPLE 3: With JSON Export")
    print("="*80)
    
    crew = create_education_crew()
    
    result = crew.run(
        topic="Data Structures",
        expertise_level="intermediate",
        resources_per_category=3,
        num_questions=5,
        num_projects=2
    )
    
    if result["success"]:
        # Prepare export data
        export_data = {
            "topic": result["topic"],
            "expertise_level": result["expertise_level"],
            "learning_materials": result["learning_materials"].model_dump(),
            "quiz": result["quiz"].model_dump(),
            "projects": result["projects"].model_dump()
        }
        
        # Save to file
        filename = "example_output.json"
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"\n✅ Results exported to {filename}")


def example_accessing_structured_data():
    """Example showing how to access structured data."""
    print("\n" + "="*80)
    print("EXAMPLE 4: Accessing Structured Data")
    print("="*80)
    
    crew = create_education_crew()
    
    result = crew.run(
        topic="Web Development",
        expertise_level="beginner",
        resources_per_category=2,
        num_questions=3,
        num_projects=1
    )
    
    if result["success"]:
        # Access learning materials
        materials = result['learning_materials']
        print("\n📚 Learning Materials:")
        print(f"Topic: {materials.topic}")
        print(f"Level: {materials.expertise_level}")
        print(f"\nSummary: {materials.summary[:100]}...")
        
        # Access quiz
        quiz = result['quiz']
        print("\n📝 Quiz:")
        print(f"Total Questions: {quiz.total_questions}")
        print(f"Estimated Time: {quiz.estimated_time_minutes} minutes")
        
        # Show first question
        if quiz.questions:
            q1 = quiz.questions[0]
            print(f"\nFirst Question:")
            print(f"  Q: {q1.question}")
            print(f"  Difficulty: {q1.difficulty}")
            print(f"  Correct Answer: {q1.correct_answer}")
        
        # Access projects
        projects = result['projects']
        print("\n🚀 Projects:")
        print(f"Total Projects: {projects.total_projects}")
        
        if projects.projects:
            p1 = projects.projects[0]
            print(f"\nFirst Project:")
            print(f"  Title: {p1.title}")
            print(f"  Duration: {p1.estimated_duration}")
            print(f"  Deliverables: {len(p1.deliverables)}")


def example_error_handling():
    """Example showing error handling."""
    print("\n" + "="*80)
    print("EXAMPLE 5: Error Handling")
    print("="*80)
    
    try:
        crew = create_education_crew(llm_provider="openrouter")
        
        # Invalid expertise level (will raise error)
        result = crew.run(
            topic="Python",
            expertise_level="expert"  # Should be: beginner/intermediate/advanced
        )
    except ValueError as e:
        print(f"\n✓ Caught validation error: {e}")
    
    # Correct usage
    result = crew.run(
        topic="Python",
        expertise_level="advanced"  # Correct
    )
    
    if result["success"]:
        print("\n✓ Valid request processed successfully")


def main():
    """Run all examples."""
    print("\n" + "="*80)
    print("PERSONALIZED EDUCATION ASSISTANT - USAGE EXAMPLES")
    print("="*80)
    print("\nThis script demonstrates various ways to use the system.")
    print("NOTE: Each example will make API calls and may take a few minutes.\n")
    
    # Choose which examples to run
    examples = {
        "1": ("Basic Usage", example_basic_usage),
        "2": ("Custom Parameters", example_custom_parameters),
        "3": ("With JSON Export", example_with_export),
        "4": ("Accessing Structured Data", example_accessing_structured_data),
        "5": ("Error Handling", example_error_handling)
    }
    
    print("Available examples:")
    for key, (name, _) in examples.items():
        print(f"  {key}. {name}")
    print("  0. Run all examples")
    print("  q. Quit")
    
    choice = input("\nSelect an example (0-5, q): ").strip()
    
    if choice == 'q':
        print("Goodbye!")
        return
    
    if choice == '0':
        # Run all
        for name, func in examples.values():
            try:
                func()
            except Exception as e:
                print(f"\n❌ Error in {name}: {e}")
    elif choice in examples:
        # Run selected
        name, func = examples[choice]
        try:
            func()
        except Exception as e:
            print(f"\n❌ Error: {e}")
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    # For quick test without interaction, uncomment one:
    # example_basic_usage()
    # example_custom_parameters()
    # example_with_export()
    # example_accessing_structured_data()
    # example_error_handling()
    
    # For interactive mode:
    main()
