---
layout: post
title: Learning Django
categories:
- blog
---

Here are some of the things I learned and how I devised my 'workflow' when writing a Django project. *This is really a braindump for myself in the future.*

* Set up the environment using `virtualenv -p python3.6` outside the working directory. This could just be in my case but I ran into conflict error with a dependency when [deleting migrations files](https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html) and this was my work around. 
* Set the `SECRET_KEY` as an environmental variable in the virtual environment using:

    ```python
    import os 
    SECRET_KEY = os.environ['SECRET_KEY']
```
instead of leaving it inside the settings file. This is a secure way of handling the secret key just remember to load it into the environment variables of the platform you're launching on (e.g. inside `~/.bashrc`) or in Heroku using 

    ```
    heroku config:set SECRET_KEY="<this-is-the-secret>"
    ```

<!--more-->

*  Make a `local_settings.py` script for development.
*  Use [`django-livereload-server`](https://github.com/tjwalch/django-livereload-server). Because I was also working on the static files using CSS, I did this at some point so I didn't have to manually refresh the web browser to load any changes.
* Use [`dj-static`](https://github.com/heroku-python/dj-static) to serve static files in Heroku's Gunicorn. With PythonAnywhere, I did not have to do this. It's just that Heroku handles static files differently.
* Because some tasks are repetitive, I wrote small bash scripts to help me set-up each directory, delete the migrations files, etc.
<!-- * As for making sure my views are working, I went from writing/ checking `forms.py` -> `views.py` -> `urls.py` , and lastly the templates.  -->
* In the views and templates, use `request.POST` and `request.FILES` + `enctype="multipart/form-data` to receive user inputs including images and files
* Lastly, use [`django_extensions`](https://github.com/django-extensions/django-extensions) to generate graphviz UML diagrams of each app or the entire project. Aside from an image output, it also generated [DOT files](https://www.graphviz.org/doc/info/lang.html) in `STDOUT` which I parsed using a Python script.  This made generating documentations a lot easier.


## Impressions

Django is sublined as a ["web-framework for perfectionists with deadlines"](https://www.djangoproject.com/). I'm not sure about being a perfectionist but I was most definitely with deadlines. I'm still trying to learn web development on an inconsistent basis and chose Django because it's built using the language I'm comfortable with - Python.

I read different tutorials on-line for beginners, including the [Django Girls tutorial](https://tutorial.djangogirls.org/en) which helped me tremendously starting out. What I really appreciated about this resource is that it included how to deploy the app in popular platforms such as [Heroku](https://www.heroku.com/) and [PythonAnywhere](https://www.pythonanywhere.com/), and explained how to connect the application to a PostGres database. I would be using a PostGres database because of the requirements of my project, although SQLite is lightweight and simple enough to manage for anyone starting out.


Overall, compared to my experience with [`flask`](http://flask.pocoo.org/) and [`bottle`](https://bottlepy.org/docs/dev/) which are both micro-webframeworks (also in Python), I found working with Django to be easier because it has a lot more built-in functions and more extensive documentation ([I mean, really!](https://docs.djangoproject.com)). It was a pleasant surprise to finish the prototype web application I was making in so short a time (hurray deadlines). I also enjoyed coding the models and learned a lot about data fields, tables, and relations, specially that I can see them implemented immediately when the code runs. It was a bit nuanced to troubleshoot though since this sometimes involved managing the database as well (SQLite is more straight-forward to manage than PostGres because it's essentially just a file. For PostGres, I used [PgAdmin](https://www.pgadmin.org/)). But most of the time, with Django, you can perform the database connections in pure Python without a single line of SQL. Lastly, what I also liked about Django is the immense community behind the framework. It's really easy to find a Stack Overflow discussion about common setbacks  I encountered - which in turn helped me better understand what's going on under the hood. 

See sample project [mysite](https://github.com/maryletteroa/practice-space/tree/master/mysite) based on the Django Girls Tutorial.






