"""
Streamlit web interface for the Personalized Education Assistant.
"""
import streamlit as st
import json
from datetime import datetime
from src.crew import create_education_crew
from src.config import config

# Page configuration
st.set_page_config(
    page_title="Personalized Education Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .resource-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .quiz-question {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid #1f77b4;
    }
    .project-card {
        background-color: #f9f9f9;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
        border: 2px solid #4CAF50;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = []
if 'current_result' not in st.session_state:
    st.session_state.current_result = None


def display_learning_materials(materials):
    """Display learning materials in a formatted way."""
    st.subheader("📚 Learning Materials")
    
    # Summary
    with st.expander("📝 Learning Path Summary", expanded=True):
        st.write(materials.summary)
    
    # Videos
    if materials.videos:
        st.markdown("### 🎥 Video Resources")
        for video in materials.videos:
            with st.container():
                st.markdown(f"""
                <div class="resource-card">
                    <h4>📹 {video.title}</h4>
                    <p>{video.description}</p>
                    <a href="{video.url}" target="_blank">🔗 Watch Video</a>
                </div>
                """, unsafe_allow_html=True)
    
    # Articles
    if materials.articles:
        st.markdown("### 📄 Article Resources")
        for article in materials.articles:
            with st.container():
                st.markdown(f"""
                <div class="resource-card">
                    <h4>📰 {article.title}</h4>
                    <p>{article.description}</p>
                    <a href="{article.url}" target="_blank">🔗 Read Article</a>
                </div>
                """, unsafe_allow_html=True)
    
    # Exercises
    if materials.exercises:
        st.markdown("### 💪 Practice Exercises")
        for exercise in materials.exercises:
            with st.container():
                st.markdown(f"""
                <div class="resource-card">
                    <h4>✏️ {exercise.title}</h4>
                    <p>{exercise.description}</p>
                    <a href="{exercise.url}" target="_blank">🔗 Try Exercise</a>
                </div>
                """, unsafe_allow_html=True)


def display_quiz(quiz):
    """Display quiz in an interactive format."""
    st.subheader("📝 Knowledge Assessment Quiz")
    
    st.info(f"**Total Questions:** {quiz.total_questions} | "
            f"**Estimated Time:** {quiz.estimated_time_minutes} minutes")
    
    for idx, question in enumerate(quiz.questions, 1):
        with st.container():
            st.markdown(f"""
            <div class="quiz-question">
                <h4>Question {idx}</h4>
                <p style="font-size: 1.1rem; font-weight: 500;">{question.question}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display options
            for option in question.options:
                is_correct = option.option == question.correct_answer
                emoji = "✅" if is_correct else "❌"
                color = "#d4edda" if is_correct else "#f8d7da"
                
                st.markdown(f"""
                <div style="background-color: {color}; padding: 0.5rem; 
                     border-radius: 0.3rem; margin: 0.3rem 0;">
                    {emoji} <strong>{option.option})</strong> {option.text}
                </div>
                """, unsafe_allow_html=True)
            
            # Show explanation
            with st.expander(f"💡 Explanation (Difficulty: {question.difficulty})"):
                st.write(f"**Correct Answer:** {question.correct_answer}")
                st.write(question.explanation)
            
            st.divider()


def display_projects(projects):
    """Display project suggestions."""
    st.subheader("🚀 Project Ideas")
    
    st.info(f"**Total Projects:** {projects.total_projects}")
    
    for idx, project in enumerate(projects.projects, 1):
        with st.container():
            st.markdown(f"""
            <div class="project-card">
                <h3>Project {idx}: {project.title}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("**Description:**")
                st.write(project.description)
                
                st.markdown("**Learning Outcomes:**")
                for outcome in project.learning_outcomes:
                    st.write(f"• {outcome}")
            
            with col2:
                st.markdown(f"**Level:** `{project.expertise_level}`")
                st.markdown(f"**Duration:** `{project.estimated_duration}`")
                
                st.markdown("**Key Concepts:**")
                for concept in project.key_concepts:
                    st.write(f"🔹 {concept}")
            
            st.markdown("**Deliverables:**")
            for deliverable in project.deliverables:
                with st.expander(f"📦 {deliverable.name}"):
                    st.write(deliverable.description)
            
            st.divider()


def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">🎓 Personalized Education Assistant</h1>', 
                unsafe_allow_html=True)
    st.markdown("*Powered by CrewAI - Your AI-driven learning companion*")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key validation
        st.subheader("🔑 API Keys Status")
        try:
            config.validate_api_keys()
            st.success("✓ All API keys configured")
        except ValueError as e:
            st.error(f"❌ {str(e)}")
            st.info("Please set your API keys in the .env file")
            return
        
        # LLM Provider selection
        llm_provider = st.selectbox(
            "LLM Provider",
            ["openrouter", "groq"],
            index=0,
            help="Select the LLM provider. Groq will be used as fallback if OpenRouter fails."
        )
        
        st.divider()
        
        # Parameters
        st.subheader("📊 Parameters")
        
        resources_per_category = st.slider(
            "Resources per category",
            min_value=1,
            max_value=10,
            value=config.default_resources_per_category,
            help="Number of videos, articles, and exercises to find"
        )
        
        num_questions = st.slider(
            "Number of quiz questions",
            min_value=3,
            max_value=15,
            value=config.default_quiz_questions,
            help="Number of questions in the quiz"
        )
        
        num_projects = st.slider(
            "Number of project ideas",
            min_value=1,
            max_value=5,
            value=config.default_project_count,
            help="Number of project suggestions"
        )
        
        st.divider()
        
        # Session history
        if st.session_state.results:
            st.subheader("📜 Session History")
            st.write(f"Total generations: {len(st.session_state.results)}")
            if st.button("🗑️ Clear History"):
                st.session_state.results = []
                st.session_state.current_result = None
                st.rerun()
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        topic = st.text_input(
            "📚 What would you like to learn?",
            placeholder="e.g., Machine Learning, Python Programming, Data Structures",
            help="Enter the topic you want to learn about"
        )
    
    with col2:
        expertise_level = st.selectbox(
            "🎯 Your Expertise Level",
            ["beginner", "intermediate", "advanced"],
            help="Select your current level of knowledge in this topic"
        )
    
    # Generate button
    if st.button("🚀 Generate Learning Plan", type="primary"):
        if not topic:
            st.error("Please enter a topic to learn about!")
            return
        
        # Show progress
        with st.spinner("🔍 Creating your personalized learning plan... This may take a few minutes."):
            try:
                # Create and run crew
                crew = create_education_crew(llm_provider)
                result = crew.run(
                    topic=topic,
                    expertise_level=expertise_level,
                    resources_per_category=resources_per_category,
                    num_questions=num_questions,
                    num_projects=num_projects
                )
                
                if result["success"]:
                    # Store result
                    result["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.session_state.results.append(result)
                    st.session_state.current_result = result
                    
                    st.success("✅ Learning plan generated successfully!")
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                    return
                    
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                return
    
    # Display current result
    if st.session_state.current_result:
        result = st.session_state.current_result
        
        st.divider()
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4 = st.tabs([
            "📚 Learning Materials", 
            "📝 Quiz", 
            "🚀 Projects",
            "💾 Export"
        ])
        
        with tab1:
            display_learning_materials(result["learning_materials"])
        
        with tab2:
            display_quiz(result["quiz"])
        
        with tab3:
            display_projects(result["projects"])
        
        with tab4:
            st.subheader("💾 Export Results")
            
            # Create export data
            export_data = {
                "topic": result["topic"],
                "expertise_level": result["expertise_level"],
                "timestamp": result.get("timestamp", "N/A"),
                "learning_materials": result["learning_materials"].model_dump(),
                "quiz": result["quiz"].model_dump(),
                "projects": result["projects"].model_dump()
            }
            
            # JSON download
            json_str = json.dumps(export_data, indent=2)
            st.download_button(
                label="📥 Download as JSON",
                data=json_str,
                file_name=f"learning_plan_{result['topic'].replace(' ', '_')}.json",
                mime="application/json"
            )
            
            # Display raw JSON
            with st.expander("👁️ View Raw JSON"):
                st.json(export_data)


if __name__ == "__main__":
    main()
