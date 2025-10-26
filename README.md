# 🎓 Personalized Education Assistant

A powerful CrewAI-powered system that generates personalized educational recommendations, including curated learning materials, interactive quizzes, and hands-on project ideas tailored to your expertise level.

## ✨ Features

- **🔍 Intelligent Content Curation**: Finds the best videos, articles, and exercises from across the web
- **📝 Custom Quiz Generation**: Creates personalized multiple-choice quizzes to test understanding
- **🚀 Project Recommendations**: Suggests practical projects with clear deliverables and learning outcomes
- **🤖 Multi-Agent System**: Uses specialized AI agents working sequentially for optimal results
- **🌐 Web Interface**: Beautiful Streamlit UI for easy interaction
- **💻 CLI Support**: Command-line interface for automation and scripting
- **🔄 LLM Fallback**: Automatic fallback from OpenRouter to Groq for reliability
- **📊 Structured Outputs**: Uses Pydantic models for consistent, validated results

## 🏗️ Architecture

### Sequential Multi-Agent Workflow

```
User Input (Topic + Expertise Level)
           ↓
┌─────────────────────────────────────┐
│  Agent 1: Learning Material Agent   │
│  - Searches web for resources       │
│  - Curates videos, articles, etc.   │
│  - Uses SerperDev search tool       │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│  Agent 2: Quiz Creator Agent        │
│  - Analyzes learning materials      │
│  - Creates MCQ questions            │
│  - Provides explanations            │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│  Agent 3: Project Idea Agent        │
│  - Designs practical projects       │
│  - Uses custom project tool         │
│  - Aligns with expertise level      │
└─────────────────────────────────────┘
           ↓
    Structured Output
```

### Key Components

1. **3 Specialized Agents**:
   - Learning Material Agent (Web Search)
   - Quiz Creator Agent (Assessment Design)
   - Project Idea Agent (Project Planning)

2. **3 Sequential Tasks**:
   - Task 1: Curate learning materials
   - Task 2: Create quiz (context from Task 1)
   - Task 3: Suggest projects (context from Task 1)

3. **Custom Tools**:
   - SerperDev Web Search Tool
   - Project Suggestion Tool (LLM-based logic)

4. **Structured Outputs**:
   - LearningMaterial (Pydantic model)
   - Quiz (Pydantic model)
   - ProjectSuggestions (Pydantic model)

## 📋 Prerequisites

- Python 3.9+
- API Keys:
  - OpenRouter API Key
  - Groq API Key
  - SerperDev API Key

## 🚀 Installation

### 1. Clone or Download the Project

```bash
cd personalized-education-assistant
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# API Keys
OPENROUTER_API_KEY=your_openrouter_key_here
GROQ_API_KEY=your_groq_key_here
SERPER_API_KEY=your_serper_key_here

# LLM Configuration (default settings)
DEFAULT_LLM=openrouter
OPENROUTER_MODEL=meta-llama/llama-4-scout:free
GROQ_MODEL=meta-llama/llama-4-scout-17b-16e-instruct

# Default Parameters
DEFAULT_RESOURCES_PER_CATEGORY=3
DEFAULT_QUIZ_QUESTIONS=5
DEFAULT_PROJECT_COUNT=2
```

### 5. Get Your API Keys

- **OpenRouter**: [https://openrouter.ai/](https://openrouter.ai/)
- **Groq**: [https://console.groq.com/](https://console.groq.com/)
- **SerperDev**: [https://serper.dev/](https://serper.dev/)

## 💻 Usage

### Web Interface (Streamlit)

Launch the Streamlit app:

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

**Features:**
- Interactive topic input
- Expertise level selection (beginner/intermediate/advanced)
- Configurable parameters (resources, questions, projects)
- Beautiful tabbed interface for results
- JSON export functionality
- Session history tracking

### Command-Line Interface

Basic usage:

```bash
python main.py "Machine Learning"
```

With options:

```bash
python main.py "Python Programming" \
  --level intermediate \
  --resources 4 \
  --questions 7 \
  --projects 3 \
  --llm openrouter \
  --output ml_plan.json
```

**CLI Arguments:**

```
positional arguments:
  topic                 Topic you want to learn about

optional arguments:
  -h, --help            Show help message
  -l, --level {beginner,intermediate,advanced}
                        Your expertise level (default: beginner)
  -r, --resources N     Number of resources per category (default: 3)
  -q, --questions N     Number of quiz questions (default: 5)
  -p, --projects N      Number of project ideas (default: 2)
  --llm {openrouter,groq}
                        LLM provider to use (default: openrouter)
  -o, --output FILE     Output filename for JSON export
  --no-display          Don't display results in console
```

### Python API

You can also use it programmatically:

```python
from src.crew import create_education_crew

# Create crew instance
crew = create_education_crew(llm_provider="openrouter")

# Run the workflow
result = crew.run(
    topic="Data Structures and Algorithms",
    expertise_level="intermediate",
    resources_per_category=4,
    num_questions=6,
    num_projects=2
)

# Access structured results
if result["success"]:
    learning_materials = result["learning_materials"]
    quiz = result["quiz"]
    projects = result["projects"]
    
    # Access specific data
    print(f"Found {len(learning_materials.videos)} videos")
    print(f"Generated {quiz.total_questions} questions")
    print(f"Suggested {projects.total_projects} projects")
```

## 📂 Project Structure

```
personalized-education-assistant/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── agents.py            # Agent definitions
│   ├── tasks.py             # Task definitions
│   ├── tools.py             # Custom tools
│   ├── models.py            # Pydantic models
│   ├── crew.py              # Main crew orchestration
│   └── config.py            # Configuration management
├── app.py                   # Streamlit web interface
├── main.py                  # CLI interface
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── .env                    # Your API keys (create this)
└── README.md               # This file
```

## 🎯 Example Outputs

### Learning Materials Output

```json
{
  "topic": "Machine Learning",
  "expertise_level": "beginner",
  "videos": [
    {
      "title": "Machine Learning Crash Course",
      "url": "https://youtube.com/...",
      "description": "Comprehensive introduction to ML concepts",
      "resource_type": "video"
    }
  ],
  "articles": [...],
  "exercises": [...],
  "summary": "A structured learning path covering fundamentals..."
}
```

### Quiz Output

```json
{
  "topic": "Machine Learning",
  "total_questions": 5,
  "questions": [
    {
      "question": "What is supervised learning?",
      "options": [
        {"option": "A", "text": "Learning with labeled data"},
        {"option": "B", "text": "Learning without labels"},
        {"option": "C", "text": "Reinforcement learning"},
        {"option": "D", "text": "Unsupervised clustering"}
      ],
      "correct_answer": "A",
      "explanation": "Supervised learning uses labeled data...",
      "difficulty": "easy"
    }
  ],
  "estimated_time_minutes": 10
}
```

### Project Output

```json
{
  "topic": "Machine Learning",
  "total_projects": 2,
  "projects": [
    {
      "title": "Movie Recommendation System",
      "description": "Build a basic recommendation engine...",
      "expertise_level": "beginner",
      "estimated_duration": "2-3 days",
      "key_concepts": ["Collaborative Filtering", "Data Preprocessing"],
      "deliverables": [
        {
          "name": "Working Python Script",
          "description": "Functional recommendation algorithm"
        }
      ],
      "learning_outcomes": ["Understand recommendation algorithms..."]
    }
  ]
}
```

## 🔧 Configuration

### LLM Models

The system uses Llama 4 Scout models:

- **OpenRouter**: `meta-llama/llama-4-scout:free` (free tier)
- **Groq**: `meta-llama/llama-4-scout-17b-16e-instruct`

You can modify these in `.env` or `src/config.py`.

### Fallback Mechanism

The system automatically falls back to Groq if OpenRouter fails:

1. Tries OpenRouter first (primary)
2. If error occurs, switches to Groq (fallback)
3. Displays warning to user
4. Continues execution seamlessly

### Parameter Tuning

Adjust these parameters for different use cases:

- **resources_per_category**: More resources = better coverage (1-10)
- **num_questions**: More questions = thorough assessment (3-15)
- **num_projects**: More projects = more options (1-5)

## 🎨 Streamlit Interface Features

### Main Page
- Topic input field
- Expertise level dropdown
- Real-time parameter adjustment
- Generate button with progress indicator

### Results Display
- **Tab 1 - Learning Materials**: Organized by type (videos/articles/exercises)
- **Tab 2 - Quiz**: Interactive question display with correct answers
- **Tab 3 - Projects**: Detailed project cards with all information
- **Tab 4 - Export**: JSON download capability

### Sidebar
- API key status indicator
- LLM provider selection
- Parameter sliders
- Session history
- Clear history button

## 🔍 How It Works

### 1. User Input
- Enter a topic (e.g., "Machine Learning")
- Select expertise level (beginner/intermediate/advanced)
- Configure parameters (optional)

### 2. Agent 1: Learning Material Agent
- Searches web using SerperDev API
- Finds videos (YouTube, educational platforms)
- Finds articles (blogs, documentation, guides)
- Finds exercises (coding challenges, practice problems)
- Returns structured LearningMaterial output

### 3. Agent 2: Quiz Creator Agent
- Receives learning materials as context
- Analyzes key concepts covered
- Generates multiple-choice questions
- Creates 4 options per question (A, B, C, D)
- Provides explanations for correct answers
- Returns structured Quiz output

### 4. Agent 3: Project Idea Agent
- Receives learning materials as context
- Uses custom Project Suggestion Tool
- Designs practical projects aligned with expertise level
- Defines clear deliverables and learning outcomes
- Returns structured ProjectSuggestions output

## 🛠️ Troubleshooting

### Common Issues

**1. API Key Errors**
```
Error: Missing required API keys: OPENROUTER_API_KEY
```
**Solution**: Ensure all API keys are set in `.env` file

**2. Import Errors**
```
ModuleNotFoundError: No module named 'crewai'
```
**Solution**: Install dependencies: `pip install -r requirements.txt`

**3. LLM Connection Errors**
```
Error creating LLM with openrouter: ...
```
**Solution**: Check API key validity and network connection. System will auto-fallback to Groq.

**4. SerperDev Errors**
```
SerperDev API error: ...
```
**Solution**: Verify SerperDev API key and check rate limits

### Debug Mode

For verbose output, the system already has `verbose=True` enabled in agents. Check console logs for detailed execution flow.

## 📊 Performance Tips

1. **Start with default parameters** (3-4 resources, 5-6 questions, 1-2 projects)
2. **Use OpenRouter** for better quality (Groq is faster but may be less detailed)
3. **Be specific with topics** (e.g., "Python Web Scraping" vs "Python")
4. **Match expertise level honestly** for best-tailored results
5. **Increase resources gradually** if you need more comprehensive coverage

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Additional custom tools
- More LLM provider support
- Enhanced error handling
- Additional output formats
- User authentication for Streamlit
- Database persistence for session history

## 📝 License

This project is provided as-is for educational purposes.

## 🙏 Acknowledgments

- **CrewAI**: Multi-agent orchestration framework
- **Anthropic/Meta**: LLM models
- **SerperDev**: Web search API
- **Streamlit**: Web interface framework

## 📧 Support

For issues or questions:
1. Check this README thoroughly
2. Review error messages in console
3. Verify API keys are correct
4. Ensure all dependencies are installed

## 🚀 Future Enhancements

- [ ] Support for more LLM providers (Claude, GPT-4, etc.)
- [ ] Integration with learning platforms (Udemy, Coursera)
- [ ] User progress tracking
- [ ] Collaborative features
- [ ] Mobile app version
- [ ] Advanced analytics dashboard
- [ ] Community-shared learning plans

---

**Built with ❤️ using CrewAI**

*Empowering personalized learning through AI agents*
