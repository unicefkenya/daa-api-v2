git add --all;git commit -m "Initial" ;git push heroku master;heroku ps:scale web=1 worker=1;heroku run ./manage.py migrate 
