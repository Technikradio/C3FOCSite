#The following things need to be done when the site will be pushed on an production server:

 * change the secret key inside every settings.py file to a randomly generated one
 * disable debug mode for every settings.py file
 * change database engine in settings.py file
 * have a look at the deploying how-to guide
 * have a look at the deploying static files guide

#The following commands need to be executed:
 * python3 manage.py migrate
 * python3 manage.py createsuperuser