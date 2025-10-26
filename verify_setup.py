"""
Setup verification script for the Personalized Education Assistant.
Checks if all dependencies and configurations are correctly set up.
"""
import sys
import os
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")


def check_python_version():
    """Check if Python version is 3.9 or higher."""
    print("\n🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"   ✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.9+)")
        return False


def check_dependencies():
    """Check if required packages are installed."""
    print("\n📦 Checking dependencies...")
    required_packages = [
        'crewai',
        'crewai_tools',
        'pydantic',
        'openai',
        'dotenv',
        'streamlit',
        'requests',
        'langchain',
        'langchain_openai'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✓ {package}")
        except ImportError:
            print(f"   ✗ {package} (missing)")
            missing.append(package)
    
    if missing:
        print(f"\n   ⚠️  Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    return True


def check_env_file():
    """Check if .env file exists and has required keys."""
    print("\n🔑 Checking environment configuration...")
    env_path = Path('.env')
    
    if not env_path.exists():
        print("   ✗ .env file not found")
        print("   Run: cp .env.example .env")
        print("   Then edit .env with your API keys")
        return False
    
    print("   ✓ .env file exists")
    
    # Check if keys are set
    required_keys = [
        'OPENROUTER_API_KEY',
        'GROQ_API_KEY',
        'SERPER_API_KEY'
    ]
    
    from dotenv import load_dotenv
    load_dotenv()
    
    missing_keys = []
    for key in required_keys:
        value = os.getenv(key)
        if not value or value == f"your_{key.lower()}_here":
            print(f"   ✗ {key} (not set)")
            missing_keys.append(key)
        else:
            # Show partial key for verification
            masked = value[:8] + '...' + value[-4:] if len(value) > 12 else '***'
            print(f"   ✓ {key} ({masked})")
    
    if missing_keys:
        print(f"\n   ⚠️  Missing API keys: {', '.join(missing_keys)}")
        print("   Edit .env file and add your API keys")
        return False
    
    return True


def check_project_structure():
    """Check if all required files exist."""
    print("\n📁 Checking project structure...")
    required_files = [
        'src/__init__.py',
        'src/agents.py',
        'src/tasks.py',
        'src/tools.py',
        'src/models.py',
        'src/crew.py',
        'src/config.py',
        'app.py',
        'main.py',
        'requirements.txt',
        '.env.example'
    ]
    
    all_exist = True
    for file in required_files:
        path = Path(file)
        if path.exists():
            print(f"   ✓ {file}")
        else:
            print(f"   ✗ {file} (missing)")
            all_exist = False
    
    return all_exist


def test_imports():
    """Test if project modules can be imported."""
    print("\n🧪 Testing project imports...")
    
    try:
        from src.config import config
        print("   ✓ config module")
    except Exception as e:
        print(f"   ✗ config module: {e}")
        return False
    
    try:
        from src.models import LearningMaterial, Quiz, ProjectSuggestions
        print("   ✓ models module")
    except Exception as e:
        print(f"   ✗ models module: {e}")
        return False
    
    try:
        from src.tools import search_tool, project_tool
        print("   ✓ tools module")
    except Exception as e:
        print(f"   ✗ tools module: {e}")
        return False
    
    try:
        from src.agents import EducationAgents
        print("   ✓ agents module")
    except Exception as e:
        print(f"   ✗ agents module: {e}")
        return False
    
    try:
        from src.tasks import EducationTasks
        print("   ✓ tasks module")
    except Exception as e:
        print(f"   ✗ tasks module: {e}")
        return False
    
    try:
        from src.crew import create_education_crew
        print("   ✓ crew module")
    except Exception as e:
        print(f"   ✗ crew module: {e}")
        return False
    
    return True


def validate_api_keys():
    """Validate API keys if everything else is OK."""
    print("\n🔐 Validating API keys...")
    
    try:
        from src.config import config
        config.validate_api_keys()
        print("   ✓ All API keys are configured")
        return True
    except ValueError as e:
        print(f"   ✗ {e}")
        return False
    except Exception as e:
        print(f"   ✗ Error validating API keys: {e}")
        return False


def main():
    """Run all checks."""
    print_header("PERSONALIZED EDUCATION ASSISTANT - SETUP VERIFICATION")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment File", check_env_file),
        ("Project Structure", check_project_structure),
        ("Module Imports", test_imports),
        ("API Key Validation", validate_api_keys)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n   ⚠️  Error during {name} check: {e}")
            results.append((name, False))
    
    # Summary
    print_header("SETUP VERIFICATION SUMMARY")
    all_passed = True
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"   {status}: {name}")
        if not result:
            all_passed = False
    
    print()
    if all_passed:
        print("   🎉 All checks passed! You're ready to go!")
        print("\n   Next steps:")
        print("   - Run web interface: streamlit run app.py")
        print("   - Run CLI: python main.py 'Your Topic'")
    else:
        print("   ⚠️  Some checks failed. Please fix the issues above.")
        print("\n   Common fixes:")
        print("   - Install dependencies: pip install -r requirements.txt")
        print("   - Create .env file: cp .env.example .env")
        print("   - Add your API keys to .env file")
    
    print()
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
