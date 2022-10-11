# ./backend/scripts/crear_env_con_requirements_env_txt.ps1 -pyver 3.10pyver
# ./backend/scripts/crear_env_con_requirements_env_txt.ps1

param(
    [Parameter()]
    [string]$pyver
)

# Instalar virtualenv si no esta instalado
pip install virtualenv
Try {
    # Crear un nuevo env python (si no se ingresa una version, se instala la 3.10)
    # AVISO: La versión del python que se ingrese debe estar instalada en el sistema
    if ($PSBoundParameters.ContainsKey('pyver')) {
        (python3 -m virtualenv ./backend/env -p python$pyver || virtualenv ./backend/env -p python$pyver)
    } else {
        (python3 -m virtualenv ./backend/env || virtualenv ./backend/env)
    }
    # Activar el env virtual
    . ./backend/env/scripts/activate
    # Instalar los requerimientos de requirements.env.txt
    pip install -r ./backend/requirements.env.txt
    # Cambiar "./env/bin/python" por "./env/Scripts/python.exe" en el archivo .vscode/backend.code-workspace (config para vscode)
    $content = [IO.File]::ReadAllText("./backend/.vscode/backend.code-workspace")
    $content = $content.Replace("./env/bin/python", "./env/Scripts/python.exe")
    [IO.File]::WriteAllText("./backend/.vscode/backend.code-workspace", $content)
} Catch {
    Write-Host "Error" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
