. env/Scripts/activate
if($?){
    pip freeze > requirements.env.txt
}