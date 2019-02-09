Django Tutorial  

# Python: Django tutorial  

This application supports the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.  

## Running Locally  

Make sure you have Python [installed properly](http://install.python-guide.org). Also, install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) and [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).  

```sh
$ mkdir mysite
$ cd mysite
$ python3 -m venv venv
$ source venv/bin/activate.fish
(venv) $ pip install django django-heroku gunicorn
(venv) $ django-admin.py startproject mysite .
(venv) $ pip freeze > requirements.txt
```

Add following in settings.py  

```sh
TIME_ZONE = 'Asia/Tokyo'

LANGUAGE_CODE = 'ja-JP'

STATIC_ROOT = '/static/'
# Configure Django App for Heroku.
import django_heroku
    django_heroku.settings(locals())
```

```sh
(venv) $ set -x DATABASE=postgres://yoka@localhost/mysite
(venv) 
(venv) $ python manage.py runserver
```

Add Procfile following.  

```sh
web: gunicorn mysite.wsgi --reload --log-file -
```

#Push to Bitbucket

Make .gitignore  

```sh
*.pyc
*~
__pycache__
myvenv
db.sqlite3
/static
.DS_Store
```

```sh
$ git init
$ git add -A
$ git commit -m "Initialize repository"

git remote add origin git@bitbucket.org:<username>/mysite.git
git push -u origin --all
````

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
