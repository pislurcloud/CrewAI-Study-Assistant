# 🚀 Quick Start Guide

Get up and running with the Personalized Education Assistant in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Up API Keys

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:
```env
OPENROUTER_API_KEY=sk-or-v1-...
GROQ_API_KEY=gsk_...
SERPER_API_KEY=...
```

### Where to Get API Keys?

- **OpenRouter**: Sign up at [openrouter.ai](https://openrouter.ai/)
  - Go to Keys section
  - Create new key
  - Free tier available with `meta-llama/llama-4-scout:free`

- **Groq**: Sign up at [console.groq.com](https://console.groq.com/)
  - Go to API Keys
  - Create new key
  - Fast inference, free tier available

- **SerperDev**: Sign up at [serper.dev](https://serper.dev/)
  - Go to API Key section
  - Copy your key
  - 2,500 free searches

## Step 3: Verify Setup

```bash
python verify_setup.py
```

This will check:
- ✓ Python version (3.9+)
- ✓ All dependencies installed
- ✓ .env file exists
- ✓ API keys configured
- ✓ Project structure intact

## Step 4: Run Your First Query

### Option A: Web Interface (Recommended for Beginners)

```bash
streamlit run app.py
```

Then:
1. Open browser to http://localhost:8501
2. Enter a topic (e.g., "Python Programming")
3. Select expertise level
4. Click "Generate Learning Plan"
5. Wait 2-3 minutes for results

### Option B: Command Line (For Quick Tests)

```bash
python main.py "Machine Learning" --level beginner
```

## Example Usage Scenarios

### 1. Complete Beginner Learning Path

```bash
python main.py "Web Development" \
  --level beginner \
  --resources 4 \
  --questions 7 \
  --projects 2
```

### 2. Intermediate Skill Enhancement

```bash
python main.py "Data Structures and Algorithms" \
  --level intermediate \
  --resources 5 \
  --questions 10 \
  --projects 3
```

### 3. Advanced Deep Dive

```bash
python main.py "Distributed Systems" \
  --level advanced \
  --resources 6 \
  --questions 12 \
  --projects 2 \
  --output advanced_systems.json
```

## What You'll Get

For each topic, the system generates:

### 📚 Learning Materials
- 3-4 **Videos** (YouTube, tutorials)
- 3-4 **Articles** (blogs, documentation)
- 3-4 **Exercises** (coding challenges, practice)

### 📝 Quiz
- 5-6 **Multiple choice questions**
- Clear **explanations** for each answer
- **Difficulty levels** (easy/medium/hard)
- Estimated completion time

### 🚀 Projects
- 1-2 **Practical project ideas**
- Clear **deliverables**
- **Learning outcomes**
- Time estimates
- Key concepts covered

## Tips for Best Results

### 1. Be Specific with Topics
❌ "Programming"
✅ "Python Web Scraping with BeautifulSoup"

### 2. Choose Correct Expertise Level
- **Beginner**: New to the topic
- **Intermediate**: Some experience, want to deepen
- **Advanced**: Experienced, looking for mastery

### 3. Start Small
First time? Use default parameters:
- 3 resources per category
- 5 questions
- 2 projects

### 4. Iterate and Refine
Run multiple queries on related topics to build a comprehensive learning path.

## Common Issues & Solutions

### Issue: "Missing required API keys"
**Solution**: 
1. Make sure .env file exists
2. Check API keys are not placeholder text
3. No quotes around values in .env

### Issue: "Module not found"
**Solution**: 
```bash
pip install -r requirements.txt
```

### Issue: "API rate limit exceeded"
**Solution**: 
- Wait a few minutes
- Try fallback LLM: `--llm groq`
- Check your API quotas

### Issue: Slow response
**Solution**: 
- Normal! Each run takes 2-5 minutes
- Uses multiple AI agents sequentially
- Searches web in real-time

## Pro Tips

### 1. Use JSON Export for Study Plans

```bash
python main.py "React Development" \
  --output react_plan.json \
  --no-display
```

Save results for later review or sharing.

### 2. Combine Multiple Topics

Create comprehensive learning paths:
```bash
# Week 1
python main.py "Python Basics" --level beginner

# Week 2
python main.py "Python OOP" --level intermediate

# Week 3
python main.py "Python Web APIs" --level intermediate
```

### 3. Use for Course Planning

Generate quiz questions for your students:
```bash
python main.py "Linear Algebra" \
  --level beginner \
  --questions 15 \
  --output algebra_quiz.json
```

### 4. Project Portfolio Building

Get project ideas aligned with job requirements:
```bash
python main.py "Full Stack Development" \
  --level advanced \
  --projects 5
```

## Next Steps

1. ✅ **Complete this quick start**
2. 📖 **Read the full [README.md](README.md)** for detailed documentation
3. 🎯 **Try different topics** and expertise levels
4. 🔧 **Customize parameters** to your needs
5. 🚀 **Build your learning portfolio**

## Need Help?

- Check the [README.md](README.md) for comprehensive documentation
- Review error messages carefully
- Verify all API keys are valid
- Ensure you have internet connection
- Check API rate limits on your accounts

## Sample Output Structure

```
📚 LEARNING MATERIALS
  └─ Videos (3-4 with links)
  └─ Articles (3-4 with links)
  └─ Exercises (3-4 with links)
  └─ Learning path summary

📝 QUIZ
  └─ Questions (5-6 MCQs)
      ├─ Question text
      ├─ 4 options (A, B, C, D)
      ├─ Correct answer
      └─ Explanation

🚀 PROJECTS
  └─ Project Ideas (1-2)
      ├─ Title & description
      ├─ Expertise level
      ├─ Duration estimate
      ├─ Key concepts
      ├─ Deliverables (3-5)
      └─ Learning outcomes (3-5)
```

---

**Ready to learn? Run your first query now! 🎓**

```bash
streamlit run app.py
# or
python main.py "Your Favorite Topic"
```
