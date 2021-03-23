# MovieBlog Website

## Setup

First clone the repository:
```sh
$ git clone https://github.com/nat13ho/django-movieblog.git
$ cd django-movieblog
```

Create a virtual environment to install dependencies in and activate it:
```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Install the dependencies:
```sh
(env)$ pip install -r requirements.txt
```

Once pip has finished downloading the dependencies:
```sh
(env)$ cd project
(env)$ python manage.py runserver
```

Then navigate to `http://127.0.0.1:8000/`

Create superuser:
```sh
(env)$ python manage.py createsuperuser
```

To use email notifications set `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in settings.py.
