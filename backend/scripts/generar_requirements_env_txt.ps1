. ./backend/env/Scripts/activate
if($?){
    pip freeze > ./backend/requirements.env.txt
}