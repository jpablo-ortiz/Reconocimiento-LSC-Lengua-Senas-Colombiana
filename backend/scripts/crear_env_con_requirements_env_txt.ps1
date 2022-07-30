pip install virtualenv
python3 -m virtualenv ./backend/env
if(! $?) { 
    virtualenv ./backend/env #-p python3.8
    if(! $?) { 
        venv ./backend/env #-p python3.8
    }
}

if($?){
    . ./backend/env/Scripts/activate
    if($?) {
        pip install -r ./backend/requirements.env.txt
    }
}
