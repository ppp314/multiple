===============
Mysite
===============


Running Locally
===============
Make sure you have Python installed properly http://install.python-guide.org.

Also, install the Heroku CLI https://devcenter.heroku.com/articles/heroku-cli and

Install Postgres::

  brew install postgresql.


Installation
------------
1. Setup local environment using python3::

     $ mkdir mysite
     $ cd mysite
     $ python3 -m venv venv
     $ source venv/bin/activate.fish
     (venv) $ pip install --upgrade pip
     (venv) $ pip install ipython
     (venv) $ pip install django-extensions
     (venv) $ pip install django django-heroku gunicorn 

#. If you create your source tree from scratch, you need to django project first.::

     (venv) $ django-admin.py startproject mysite .
     (venv) $ pip freeze > requirements.txt

#. Add following in ``settings.py``::

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
     """ Configure Django App for Heroku."""
     django_heroku.settings(locals())

#. Remove secret key from settings.py

#. Set global environment variable::

     (venv) $ set -x SECRET_KEY 'f!%)$s04lc1rr*ea#@tkp#em^24mh295+_=zl)4)bdm!!3q@o^'

#. Setup the database.::

     (venv) $ createdb mysite
     (venv) $ set -x DATABASE_URL 'postgres://$user@localhost/mysite'

#. Run server locally::

     (venv) $ python manage.py runserver

#. Use ipython::

     (venv) $ python manage.py shell_plus -i 

Push to github
==============

1. Make .gitignore::

     *.pyc
     *~
     __pycache__
     myvenv
     db.sqlite3
     /static
     .DS_Store

2. Setup git::

     $ git init
     $ git add -A
     $ git commit -m "Initialize repository"
  
     $ git remote add origin https://github.com/<username>/mysite.git
     $ git push -u origin --all

#. Make Procfile in the top directory and add following::

     web: gunicorn mysite.wsgi --reload --log-file -
  

heroku setup
------------
1. Setup heroku locally::

     $ heroku local web

Your app should now be running on http://localhost:5000/.

Deploying to Heroku
-------------------

2. heroku setup::

     $ heroku create
     $ git push heroku master

     $ heroku run python manage.py migrate
     $ heroku open


Documentation
-------------
For more information about using Python on Heroku, see these Dev Center articles:
https://devcenter.heroku.com/categories/python

LICENSE
=======
GPL-3


URL organization
================


+------------+---------------+-----------------------+----------------+
| Model      | View          | Which Form?           | URL name       |
+============+===============+=======================+================+
|Exam        | create        |ModelFormSetView       |exam-create     |
|            +---------------+-----------------------+----------------+
|            | list answer   |generic.ListView       |(Not yet)       |
|            +---------------+-----------------------+----------------+
|            | list drill    |generic.ListView       |exam-drill-list |
|            +---------------+-----------------------+----------------+
|            | update        |ModelFormSetView       |exam-update     |
|            +---------------+-----------------------+----------------+
|            | delete        |generic.DeleteView     |exam-delete     |
+------------+---------------+-----------------------+----------------+
| Answer     | create        | CreateWithInlinesView | answer-create  |
|            +---------------+-----------------------+----------------+
|            | list          | CreateWithInlinesView | answer-list    |
|            +---------------+-----------------------+----------------+
|            | update        | UpdateWithInlinesView | answer-update  |
|            +---------------+-----------------------+----------------+
|            | delete        | generic.DeleteView    | answer-delete  |
+------------+---------------+-----------------------+----------------+
| Drill      | create        | UpdateWithInlinesView | drill-create   |
|            +---------------+-----------------------+----------------+
|            | list          | generic.ListView      | drill-list     |
+            +---------------+-----------------------+----------------+
|            | update        | UpdateWithInlinesView | drill-update   |
|            +---------------+-----------------------+----------------+
|            | delete        | generic.DeleteView    | drill-delete   |
+------------+---------------+-----------------------+----------------+
| Mark       | create        | (NA)                  | mark-create    |
|            +---------------+-----------------------+----------------+
|            | list          | (NA)                  | mark-list      |
+------------+---------------+-----------------------+----------------+
|            | update        | UpdateWithInlinesView | mark-update    |
|            +---------------+-----------------------+----------------+
|            | delete        | (NA)                  | mark-delete    |
+------------+---------------+-----------------------+----------------+
| Grade      | list          | generic.ListView      | grade-list     |
|            +---------------+-----------------------+----------------+
|            | delete        | generic.DeleteView    | grade-delete   |
+------------+---------------+-----------------------+----------------+

