#The following things need to be done when the site will be pushed on an production server:

 * change the secret key inside every settings.py file to a randomly generated one
 * disable debug mode for every settings.py file
 * change database engine in settings.py file
 * set CSRF_COOKIE_SECURE and SESSION_COOKIE_SECURE to True in settings.py file
 * have a look at the deploying how-to guide
 * have a look at the deploying static files guide
 * change body.py SERVER_ROOT
 * In file <code>c3shop/frontpage/management/media_actions.py</code> change the variable
   <code>PATH_TO_UPLOAD_FOLDER_ON_DISK</code> to something useful.

#The following commands need to be executed:
 * python3 manage.py migrate
 * python3 manage.py createsuperuser
 * python3 manage.py collectstatic
