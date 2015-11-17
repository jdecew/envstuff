# webserver aliases
alias ws_init="pyenv activate vida-webserver"
alias ws_update="pip install -r requirements.txt && npm install && ./manage.py migrate"
alias ws_start_web="./manage.py runserver"
alias ws_start_back="foreman start -f Procfile.dev"

