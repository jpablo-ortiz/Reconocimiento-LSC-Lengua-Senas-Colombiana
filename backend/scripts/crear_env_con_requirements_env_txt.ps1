pip install virtualenv
(python3 -m virtualenv ./backend/env || virtualenv ./backend/env) #-p python3.8

if($?){
    . ./backend/env/Scripts/activate
    if($?) {
        pip install -r ./backend/requirements.env.txt
        if($?) {
            # Cambiar "./env/bin/python" por "./env/Scripts/python.exe"
            $content = [IO.File]::ReadAllText("./backend/.vscode/backend.code-workspace")
            $content = $content.Replace("./env/bin/python", "./env/Scripts/python.exe")
            [IO.File]::WriteAllText("./backend/.vscode/backend.code-workspace", $content)
        }
    }
}