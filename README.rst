#  Demo

This application is inspired by the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.  

## Running Locally  

Make sure you have Python [installed properly](http://install.python-guide.org). Also, install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) and [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).  

```sh
$ mkdir mysite
$ cd mysite
$ python3 -m venv venv
$ source venv/bin/activate.fish
(venv) $ pip install --upgrade pip
(venv) $ pip install ipython
(venv) $ pip install django-extensions
(venv) $ pip install django django-heroku gunicorn django-multiselectfield
```
If you create your source tree from scratch, you need to django project first.
```sh
(venv) $ django-admin.py startproject mysite .
```

```sh
(venv) $ pip freeze > requirements.txt
```

Add following in settings.py  

```sh

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
import django_heroku
    django_heroku.settings(locals())
```
Remove secret key

Create file "local_settings.py" with secret key
```sh
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f!%)$s04lc1rr*ea#@tkp#em^24mh295+_=zl)4)bdm!!3q@o^'
```


```sh
(venv) $ createdb mysite
(venv) $ set -x DATABASE_URL 'postgres://$user@localhost/mysite'
(venv) $ python manage.py runserver
```

Use ipython

```sh
(venv) $ python manage.py shell -i ipython
```


#Push to github

Make .gitignore  

```sh
*.pyc
*~
__pycache__
myvenv
db.sqlite3
/static
.DS_Store
local_settings.py
```

```sh
$ git init
$ git add -A
$ git commit -m "Initialize repository"

git remote add origin https://github.com/<username>/mysite.git
git push -u origin --all
````


Add Procfile following.  

```sh
web: gunicorn mysite.wsgi --reload --log-file -
```



```sh
$ heroku local web
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)

## LICENSE
GPL-3
