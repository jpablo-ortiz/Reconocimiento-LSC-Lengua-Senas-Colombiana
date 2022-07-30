pip install virtualenv && 
(python3 -m virtualenv ./backend/env || virtualenv ./backend/env || venv ./backend/env) && 
source ./backend/env/bin/activate && 
pip install -r ./backend/requirements.env.txt &&
# Cambiar "./env/Scripts/python.exe" por "./env/bin/python"
texto=$(sed 's/\.\/env\/Scripts\/python\.exe/\.\/env\/bin\/python/g' ./backend/.vscode/backend.code-workspace) &&
echo $texto > ./backend/.vscode/backend.code-workspace