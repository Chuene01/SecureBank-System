# setup.py
import subprocess
import sys

def install_packages():
    packages = [
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "motor==3.3.2",
        "passlib==1.7.4",
        "bcrypt==4.1.1",
        "python-jose[cryptography]==3.3.0",
        "python-dotenv==1.0.0",
        "pydantic==2.5.0"
    ]
    
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    print("All packages installed successfully!")

if __name__ == "__main__":
    install_packages()