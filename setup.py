import os
import subprocess
import sys


def create_virtualenv():
    # Check if a virtual environment already exists
    if os.path.exists("venv"):
        print("Virtual environment already exists in this folder.")
        return

    print("Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    print("Virtual environment created.")


def install_requirements():
    # Activate the virtual environment
    if os.name == "nt":  # Windows
        activate_script = ".\\venv\\Scripts\\activate"
        pip_exec = ".\\venv\\Scripts\\pip"
    else:  # macOS/Linux
        activate_script = "./venv/bin/activate"
        pip_exec = "./venv/bin/pip"

    # Check for requirements.txt
    if not os.path.exists("requirements.txt"):
        print("No requirements.txt file found in the current folder.")
        return

    print(f"Installing requirements from requirements.txt using {pip_exec}...")
    subprocess.run([pip_exec, "install", "-r", "requirements.txt"], check=True)
    print("Dependencies installed.")


if __name__ == "__main__":
    try:
        create_virtualenv()
        install_requirements()
        print("Setup completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
