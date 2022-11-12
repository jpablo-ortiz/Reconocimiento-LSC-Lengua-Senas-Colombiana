#!/bin/sh

# Commands Example:
# ./backend/scripts/crear_env_con_requirements_env_txt.ps1 3.10
# ./backend/scripts/crear_env_con_requirements_env_txt.ps1

pythvers=$1
# Change "Scripts/python.exe" to "bin/python" in the .vscode/backend.code-workspace file (vscode config)
cambio_env=$(sed 's/Scripts\/python.exe/bin\/python/g' ./backend/.vscode/backend.code-workspace)

# Function to update pip
update_pip() {
    (pip install --upgrade pip || pip3 install --upgrade pip || python -m pip install --upgrade pip || python3 -m pip install --upgrade pip)
}

# Function to install virtualenv
install_virtualenv() {
    (pip install virtualenv || pip3 install virtualenv || python -m pip install virtualenv || python3 -m pip install virtualenv)
}

# Function to create a new virtual environment
create_virtualenv() {
    # Warning: The python version entered must be installed in the system
    (
        if [ -z "$pythvers" ]; then
            (virtualenv ./backend/env -p python"$pythvers" || python -m virtualenv ./backend/env -p python"$pythvers" || python3 -m virtualenv ./backend/env -p python"$pythvers")
        else
            (virtualenv ./backend/env || python -m virtualenv ./backend/env || python3 -m virtualenv ./backend/env)
        fi
    )
}

# Function to install the requirements of requirements.env.txt
install_requirements() {
    (pip install -r ./backend/requirements.env.txt || pip3 install -r ./backend/requirements.env.txt || python -m pip install -r ./backend/requirements.env.txt || python3 -m pip install -r ./backend/requirements.env.txt)
}

# Install virtualenv
install_virtualenv &&
    # Create a new virtual environment
    # Warning: The python version entered must be installed in the system
    create_virtualenv &&
    # Activate the virtual environment
    . ./backend/env/bin/activate &&
    # Update pip
    update_pip &&
    # Install the dependencies from the requirements.env.txt file
    install_requirements &&
    # Change "Scripts/python.exe" to "bin/python" in the .vscode/backend.code-workspace file (vscode config)
    echo "$cambio_env" > ./backend/.vscode/backend.code-workspace
