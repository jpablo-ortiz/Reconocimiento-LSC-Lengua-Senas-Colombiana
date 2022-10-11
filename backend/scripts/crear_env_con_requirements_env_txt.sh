# ./backend/scripts/crear_env_con_requirements_env_txt.ps1 3.10
# ./backend/scripts/crear_env_con_requirements_env_txt.ps1

pythvers=$1 
cambio_env=$(sed 's/\.\/env\/Scripts\/python\.exe/\.\/env\/bin\/python/g' ./backend/.vscode/backend.code-workspace)

# Instalar virtualenv si no esta instalado
pip install virtualenv &&
# Crear un nuevo env python (si no se ingresa una version, se instala la 3.10)
# AVISO: La versión del python que se ingrese debe estar instalada en el sistema
(

    if [[ -z "$pythvers" ]] 
    then
        (python3 -m virtualenv ./backend/env -p python$pythvers || virtualenv ./backend/env -p python$pythvers)
    else
        (python3 -m virtualenv ./backend/env || virtualenv ./backend/env)
    fi 
) &&
# Activar el env virtual
source ./backend/env/bin/activate &&
# Instalar los requerimientos de requirements.env.txt
pip install -r ./backend/requirements.env.txt &&
# Cambiar "./env/Scripts/python.exe" por "./env/bin/python" en el archivo .vscode/backend.code-workspace (config para vscode)
echo $cambio_env > ./backend/.vscode/backend.code-workspace