===============
Mysite
===============


Running Locally
===============
Make sure you have Python installed properly http://install.python-guide.org).

Also, install the Heroku CLI https://devcenter.heroku.com/articles/heroku-cli and

Postgres https://devcenter.heroku.com/articles/heroku-postgresql#local-setup


Setup::
  $ mkdir mysite
  $ cd mysite
  $ python3 -m venv venv
  $ source venv/bin/activate.fish
  (venv) $ pip install --upgrade pip
  (venv) $ pip install ipython
  (venv) $ pip install django-extensions
  (venv) $ pip install django django-heroku gunicorn django-multiselectfield

If you create your source tree from scratch, you need to django project first.::
  (venv) $ django-admin.py startproject mysite .


  (venv) $ pip freeze > requirements.txt


Add following in settings.py::
  import django_heroku

  INSTALLED_APPS = (
  ...
  ...
  'django_extensions', #<--- Insert this line
  ...
  )

  TIME_ZONE = 'Asia/Tokyo'

  LANGUAGE_CODE = 'ja-JP'

  STATIC_ROOT = '/static/'
  # Configure Django App for Heroku.
    django_heroku.settings(locals())


Remove secret key from settings.py

Set global environment variable::
  (venv) $ set -x SECRET_KEY 'f!%)$s04lc1rr*ea#@tkp#em^24mh295+_=zl)4)bdm!!3q@o^'


Setup the database.::
  (venv) $ createdb mysite
  (venv) $ set -x DATABASE_URL 'postgres://$user@localhost/mysite'

Run server locally::
  (venv) $ python manage.py runserver


Use ipython::
  (venv) $ python manage.py shell -i ipython

Push to github
==============
Make .gitignore  


*.pyc
*~
__pycache__
myvenv
db.sqlite3
/static
.DS_Store


Setup git::
  $ git init
  $ git add -A
  $ git commit -m "Initialize repository"
  
  $ git remote add origin https://github.com/<username>/mysite.git
  $git push -u origin --all

Make Procfile in the top directory and add following::
  web: gunicorn mysite.wsgi --reload --log-file -
  

heroku setup
============
  $ heroku local web

Your app should now be running on http://localhost:5000/).

Deploying to Heroku
===================

heroku setup::
  $ heroku create
  $ git push heroku master

  $ heroku run python manage.py migrate
  $ heroku open


Documentation
=============
For more information about using Python on Heroku, see these Dev Center articles:
https://devcenter.heroku.com/categories/python

LICENSE
=======
GPL-3
