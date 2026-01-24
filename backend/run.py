#!/usr/bin/env python3
"""
AI Studio Backend Setup Script
Sets up the development environment and runs the server
"""
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.11 or higher"""
    if sys.version_info < (3, 11):
        print(f"❌ Python 3.11+ required, found {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def create_env_file():
    """Create .env file from example if it doesn't exist"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        print("\n📝 Creating .env file from template...")
        env_file.write_text(env_example.read_text())
        print("✅ .env file created - please configure as needed")
    else:
        print("✅ .env file already exists")


def create_data_directories():
    """Create data directories"""
    print("\n📁 Creating data directories...")
    directories = [
        "data",
        "data/models",
        "data/vector_store",
        "data/database",
        "data/uploads",
        "data/logs",
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Data directories created")


def run_server(dev_mode=True):
    """Run the FastAPI server"""
    print("\n🚀 Starting AI Studio Backend...\n")
    
    try:
        if dev_mode:
            # Development mode with hot reload
            subprocess.check_call([
                sys.executable, "-m", "uvicorn",
                "main:app",
                "--reload",
                "--host", "127.0.0.1",
                "--port", "8000",
            ])
        else:
            # Production mode
            subprocess.check_call([
                sys.executable, "-m", "uvicorn",
                "main:app",
                "--host", "127.0.0.1",
                "--port", "8000",
            ])
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to start server: {e}")
        return False
    
    return True


def main():
    """Main setup and run function"""
    print("=" * 60)
    print("AI Studio Backend Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if "--skip-install" not in sys.argv:
        if not install_dependencies():
            sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Create data directories
    create_data_directories()
    
    # Run server
    if "--no-run" not in sys.argv:
        print("\n" + "=" * 60)
        print("Setup complete! Starting server...")
        print("=" * 60)
        print("\n📖 API Documentation: http://localhost:8000/docs")
        print("🏥 Health Check: http://localhost:8000/health\n")
        
        dev_mode = "--prod" not in sys.argv
        run_server(dev_mode=dev_mode)
    else:
        print("\n✅ Setup complete!")
        print("\nTo start the server, run:")
        print("  python run.py")


if __name__ == "__main__":
    main()
