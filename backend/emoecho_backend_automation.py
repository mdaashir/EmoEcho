import os
import subprocess
import sys
import venv


def run_command(command):
    """Run a shell command and handle output."""
    try:
        subprocess.run(command, shell=True, check=True, text=True)
        print(f"Command '{command}' executed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error while executing '{command}': {e}")
        sys.exit(1)


def create_virtual_environment(env_name=".venv"):
    """Create a virtual environment."""
    if not os.path.exists(env_name):
        print(f"Creating a virtual environment in '{env_name}'...")
        venv.EnvBuilder(with_pip=True).create(env_name)
        print(f"Virtual environment '{env_name}' created successfully!")
    else:
        print(f"Virtual environment '{env_name}' already exists.")


def activate_virtual_env(env_name=".venv"):
    """Activate the virtual environment."""
    activate_script = os.path.join(env_name, "Scripts", "activate") if os.name == "nt" else os.path.join(env_name, "bin", "activate")
    if not os.path.exists(activate_script):
        print(f"Error: Cannot find the activation script for the virtual environment '{env_name}'.")
        sys.exit(1)
    print(f"Virtual environment '{env_name}' activated!")
    return activate_script


def install_requirements(env_name=".venv"):
    """Install requirements from requirements.txt in the virtual environment."""
    print("Installing requirements from 'requirements.txt'...")
    pip_install_command = f"{os.path.join(env_name, 'Scripts', 'pip')} install -r requirements.txt" if os.name == "nt" else f"{os.path.join(env_name, 'bin', 'pip')} install -r requirements.txt"
    run_command(pip_install_command)


def main():
    # Define variables
    env_name = ".venv"
    server_dir = "server"  # Backend folder location
    dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")

    # Step 1: Create the virtual environment
    create_virtual_environment(env_name=env_name)

    # Step 2: Activate the virtual environment
    activate_virtual_env(env_name=env_name)

    # Step 3: Install requirements
    install_requirements(env_name=env_name)

    # Step 4: Import dotenv after installing dependencies
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("Error: 'dotenv' package is not found even after installing dependencies.")
        sys.exit(1)

    # Step 5: Load the environment variables from the .env file
    if not os.path.exists(dotenv_path):
        print(f"Error: The .env file '{dotenv_path}' does not exist.")
        sys.exit(1)

    load_dotenv(dotenv_path=dotenv_path)

    # Fetch the port from the .env file; default to 8000 if not set
    port = os.getenv('BACKEND_PORT', '8000')

    # Step 6: Change to the "server" directory
    if not os.path.exists(server_dir):
        print(f"Error: The project directory '{server_dir}' does not exist.")
        sys.exit(1)
    os.chdir(server_dir)
    print(f"Changed directory to '{server_dir}'...")

    # Step 7: Run Django management commands
    print("Running make migrations...")
    run_command('python manage.py makemigrations')

    print("Running migrations...")
    run_command('python manage.py migrate')

    print("Running tests...")
    run_command('python manage.py test')

    # Step 8: Start the development server with the specified port
    print(f"Starting the development server on port {port}...")
    run_command(f'python manage.py runserver {port}')


if __name__ == "__main__":
    main()
