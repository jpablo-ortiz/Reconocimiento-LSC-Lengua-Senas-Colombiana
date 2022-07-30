pip install virtualenv
python3 -m virtualenv env
if(! $?) { 
    virtualenv env #-p python3.8
    if(! $?) { 
        venv env #-p python3.8
    }
}

if($?){
    . env/Scripts/activate
    if($?) {
        pip install -r requirements.env.txt
    }
}
