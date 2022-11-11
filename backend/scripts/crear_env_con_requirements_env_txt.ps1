# Commands Example:
# ./backend/scripts/crear_env_con_requirements_env_txt.ps1 3.10
# ./backend/scripts/crear_env_con_requirements_env_txt.ps1

param(
    [Parameter()]
    [string]$pyver
)

# Function to update pip
function update_pip {
    (pip install --upgrade pip || pip3 install --upgrade pip || python -m pip install --upgrade pip || python3 -m pip install --upgrade pip)
}

# Function to install pipenv
function install_pipenv {
    (pip install pipenv || pip3 install pipenv || python -m pip install pipenv || python3 -m pip install pipenv)
}

# Function to create a new virtual environment
function create_virtualenv {
    # Warning: The python version entered must be installed in the system
    if ($PSBoundParameters.ContainsKey('pyver')) {
            (virtualenv ./env -p python"$pythvers" || python -m virtualenv ./env -p python"$pythvers" || python3 -m virtualenv ./env -p python"$pythvers")
    }
    else {
            (virtualenv ./env || python -m virtualenv ./env || python3 -m virtualenv ./env)
        
    }
}

# Function to install the requirements of requirements.env.txt
function install_requirements {
    (pip install -r ./requirements.env.txt || pip3 install -r ./requirements.env.txt || python -m pip install -r ./requirements.env.txt || python3 -m pip install -r ./requirements.env.txt)
}

# Function to change "bin/python" to "Scripts/python.exe" in the .vscode/backend.code-workspace file (vscode config)
function change_python_path {
    $content = [IO.File]::ReadAllText("./backend/.vscode/backend.code-workspace")
    $content = $content.Replace("bin/python", "Scripts/python.exe")
    [IO.File]::WriteAllText("./backend/.vscode/backend.code-workspace", $content)
}

# Change to the backend directory
Set-Location ./backend
Try {
    # Install pipenv
    install_pipenv
    # Create virtual environment
    # Warning: The python version entered must be installed in the system
    create_virtualenv
    # Activate virtual environment
    ./env/Scripts/activate
    # Update pip
    update_pip  
    # Install the dependencies from the requirements.env.txt file
    install_requirements
    # Change vscode config
    change_python_path
    # Show Success Message
    Write-Host "Success: The virtual environment was created successfully" -ForegroundColor Green
}
Catch {
    Write-Host "Error" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
Finally {
    Set-Location ..
}