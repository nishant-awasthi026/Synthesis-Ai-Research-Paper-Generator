"""
Quick setup script for Synthesis AI Research Paper Generator
Run this first to set up the project
"""
import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_ollama():
    """Check if Ollama is installed"""
    success, output = run_command("ollama list")
    return success

def main():
    print_header("Synthesis AI Research Paper Generator - Quick Setup")
    
    base_dir = Path(__file__).parent.parent
    
    # Step 1: Check Ollama
    print("📦 Step 1: Checking Ollama installation...")
    if check_ollama():
        print("✅ Ollama is installed")
    else:
        print("❌ Ollama is not installed or not running")
        print("   Please install from: https://ollama.ai")
        print("   Then run: ollama pull llama3.1:8b")
        return
    
    # Step 2: Create .env file
    print("\n📝 Step 2: Creating .env file...")
    env_example = base_dir / ".env.example"
    env_file = base_dir / ".env"
    
    if not env_file.exists() and env_example.exists():
        import shutil
        shutil.copy(env_example, env_file)
        print("✅ Created .env file")
    else:
        print("ℹ️  .env file already exists")
    
    # Step 3: Create Python virtual environment
    print("\n🐍 Step 3: Setting up Python virtual environment...")
    venv_dir = base_dir / "venv"
    
    if not venv_dir.exists():
        print("   Creating virtual environment...")
        success, _ = run_command(f"{sys.executable} -m venv venv", cwd=base_dir)
        if success:
            print("✅ Virtual environment created")
        else:
            print("❌ Failed to create virtual environment")
            return
    else:
        print("ℹ️  Virtual environment already exists")
    
    # Step 4: Install Python dependencies
    print("\n📥 Step 4: Installing Python dependencies...")
    
    if os.name == 'nt':  # Windows
        pip_path = venv_dir / "Scripts" / "pip.exe"
    else:
        pip_path = venv_dir / "bin" / "pip"
    
    requirements = base_dir / "backend" / "requirements.txt"
    
    if requirements.exists():
        print("   Installing packages (this may take a few minutes)...")
        success, output = run_command(f'"{pip_path}" install -r "{requirements}"')
        if success:
            print("✅ Python dependencies installed")
        else:
            print("⚠️  Some packages may have failed to install")
    
    # Step 5: Initialize database
    print("\n🗄️  Step 5: Initializing database...")
    init_script = base_dir / "backend" / "init_db.py"
    
    if init_script.exists():
        if os.name == 'nt':
            python_path = venv_dir / "Scripts" / "python.exe"
        else:
            python_path = venv_dir / "bin" / "python"
        
        success, _ = run_command(f'"{python_path}" "{init_script}"')
        if success:
            print("✅ Database initialized")
    
    # Step 6: Frontend setup
    print("\n⚛️  Step 6: Setting up frontend...")
    frontend_dir = base_dir / "frontend"
    
    if frontend_dir.exists():
        package_json = frontend_dir / "package.json"
        if package_json.exists():
            print("   Installing npm packages (this may take a few minutes)...")
            success, _ = run_command("npm install", cwd=frontend_dir)
            if success:
                print("✅ Frontend dependencies installed")
            else:
                print("⚠️  Frontend setup incomplete - run 'npm install' manually in frontend/")
    
    # Final instructions
    print_header("Setup Complete!")
    
    print("🚀 Next Steps:\n")
    print("1. Activate virtual environment:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate\n")
    else:
        print("   source venv/bin/activate\n")
    
    print("2. Pull Ollama model (if not done):")
    print("   ollama pull llama3.1:8b\n")
    
    print("3. Run initial data ingestion (optional, 4-6 hours):")
    print("   python backend/scripts/bulk_ingest.py --total-target 2000\n")
    
    print("4. Start the backend:")
    print("   cd backend")
    print("   uvicorn main:app --reload\n")
    
    print("5. Start the frontend (new terminal):")
    print("   cd frontend")
    print("   npm run dev\n")
    
    print("6. Access the application:")
    print("   Frontend: http://localhost:5173")
    print("   Backend API: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs\n")
    
    print("📚 For more information, see README.md\n")

if __name__ == "__main__":
    main()
