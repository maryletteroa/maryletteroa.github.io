---
layout: post
title: 100 Days of Code
categories: [project]
tags: [python]
---

<!-- I've finally gotten around to doing the 100 Days of Code Challenge. This was popular a few years back, and as usual, I caught up with the trend just now. 😅 
 -->
This journey is based on the Udemy course [100 Days of Code - The Python Pro Bootcamp](https://www.udemy.com/course/100-days-of-code/) by Dr. Angela Yu.

My code repo is here 👉: [100DaysOfCode-Python](https://github.com/maryletteroa/100DaysOfCode-Python)

I document my progress in this post: programming tasks, and notes about things that made an impression.


## Day 72 - Visualization

[Programming Languages](https://github.com/maryletteroa/100DaysOfCode-Python/blob/main/72/Programming_Languages.ipynb)

Converting string to date 

`pd.to_datetime(df.DATE)`

Pivot pandas dataframe

`df.pivot(index = 'DATE', columns = 'TAG', values = 'POST')`


Data visualization with matplotlib

```py
plt.figure(figsize=(16,20))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of post', fontsize=14)
plt.ylim(0, 35000)

for column in df.columns:
    plt.plot(df.index, df[column],
        linewidth=3, label=df[column].name)

plt.legend(fontsize=16)
```


## Day 71 - Data Exploration with Pandas

This day starts the Data Analytics exercises.

Pandas 🐼

The notebook is here [Data Exploration Pandas College Major](https://github.com/maryletteroa/100DaysOfCode-Python/blob/main/71/Data_Exploration_Pandas_College_Major.ipynb)

Noteworthy Pandas functions include: 

- `.findna()` - Looks for NaN (not a number)
- `.dropna()` - drops the NaN
- `df[['col1','col2']]` - access multiple columns
- `.idxmax()` - gets row index of the max value
- `.idxmin()` - gets row index of the min value

## Day 70 - Deployed blog in Heroku

Deployed blog 📝: [Blog](https://dawn-leaf-1474.herokuapp.com).

The Github repo is here 👉: [my-blog-flask](https://github.com/maryletteroa/my-blog-flask)

Since I've done this part ahead, it's only a matter of changing the underlying database from SQLite to PostgreSQL. This ensures that the data will not be wiped out periodically. More information [here](https://devcenter.heroku.com/articles/sqlite3).

A Postgres database was added from the Resources in Heroku. Databases can be viewed in [Heroku Data](https://data.heroku.com). The Postgres database URL (`DATABASE_URL`) is automatically added as a variable in Config Vars; hence the script should be modified as:

```python
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///blog.db")
```

The second argument in `os.environ.get` is the default value if `DATABASE_URL` is not available, i.e. in the local deployment.

I also removed the SQLAlchemy binding for the two other tables since these tables will be created in the Postgres database and not in separate databases (unlike in SQLite which is text based). Not doing so resulted in this error `(psycopg2.errors.UndefinedTable) relation "table_name" does not exist`. (This actually took a while to figure out 😅)

I also learned how to write a [custom flask CLI command](https://flask.palletsprojects.com/en/1.0.x/cli/#application-context) while digging around for a solution to this error. 
```python
import click
from flask.cli import with_appcontext

@click.command(name="create_tables")
@with_appcontext
def create_tables():
    db.create_all()
    
app.cli.add_command(create_tables)
```

Rename `main.py` to `app.py`.

In Heroku, run the custom Flask CLI command using the console:
```bash
flask create_tables
```

This turned out unnecessary but convenient when doing multiple deploys; I don't have to comment and uncomment `db.create_all()` in the script since I can just do this using the Heroku commandline.


## Day 69 (Capstone Part 4) - Blog with Users

Added authentication and users to blog 📝: [Blog](https://dawn-leaf-1474.herokuapp.com)

Multiple databases declared in Flask
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config["SQLALCHEMY_BINDS"] = {
        'db2': 'sqlite:///users.db'
    }

class User(UserMixin, db.Model):
    __bind_key__ = "db2"
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
```

Create an `admin_only` decorator. Patterned from the [`login_required` decorator](https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/#login-required-decorator). Error pages using [`abort()`](https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages)

```python
from functools import wraps
from flask import abort
def admin_only(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return function(*args, **kwargs)
    return wrapper
```

Define a one-to-many relationship between user (author) and posts using `relationship()`

```python
class User(UserMixin, db.Model):
    __bind_key__ = "db2"
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    posts = relationship("BlogPost", back_populates="author") 
            # connection

class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id")) 
            # Foreign Key to user.id
    author = relationship("User", back_populates="posts") 
            # connection
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

```

Since `post.author` is now a `User` object, access author name as `post.author.name`
{% raw %}
```html
  <p class="post-meta">Posted by
    <a href="#">{{post.author.name}}</a>
    on {{post.date}}
```
{% endraw %}

[Flask gravatar](https://pythonhosted.org/Flask-Gravatar) to show image by email
{% raw %}
```html
<img src="{{ post.author.email | gravatar }}"/>
```
{% endraw %}


## Day 68 - Flask with Authentication

Flask website with authentication 🔐: [Flask with Authentication](https://replit.com/@maryletteroa/flask-with-authentication)

Why authenticate
- Create / login users
- Restrict access

Levels of encryption
- 1: Storing the password as plain text in the database
- 2: Encryption - scrambling the original message with a key to decode it i.e. password + key (cipher method) -> cipher text; weak, easy to figure out the original text even without a key (think Mary, Queen of Scots but methaphorically. Still 🙅‍♀️)
- 3: Hashing - removes the need for an encryption key; hash function turns the password into a hash and the hash is stored in the database; Hashes are mathematical equations that make it almost impossible (far too long) to turn a hash back to a password; e.g. MD5 or bcrypt (the latter takes longer to hash out; industry standard)
- 4: Hashing and Salting - salt or random string of characters is appended to the password which generates different hashes for the same passwords; salt is stored in the database along with the hash; bcrypt has salt-rounds or how many times the password is salted e.g. hash from round 1 gets salted with the same salt then repeat; increase rounds to overcome Moore's Law (every year computing power increases)


A hash table of passwords can be created from:
- Common passwords
- All words from a dictionary (approxo 150,000) -> dictionary attack
- All numbers form a telephone book (approx 5,000,000)
- All combinations of characters up to 6 places (19,770,609,664)

❌ Total: 19,775,759,664 combinations which only takes 0.9s seconds to generate the hash for using one of the latest GPUs

☝ But as the number of characters of your password increases, the combination of times it takes to crack it increases exponentialy.

Hash password using [Werkzeug helper function](https://werkzeug.palletsprojects.com/en/1.0.x/utils/#module-werkzeug.security)
```python
from werkzeug.security import generate_password_hash

new_user = User(
    email = request.form.get("email"),
    password = generate_password_hash(request.form.get("password"), \
        method='pbkdf2:sha256', salt_length=8),
    name = request.form.get("name")
```

Login authentication using [Flask_Login package](https://flask-login.readthedocs.io/en/latest/). The User class is implemented with UserMixin. Mixin is a way to provide multiple inheritance in Python
```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
```

Configure the flask app to use Flask_login
```python
app = Flask(__name__)

# more configs ...

login_manager = LoginManager()
login_manager.init_app(app)
```

Create a user loader function. Flask_Login creates a cookie 🍪 that contains the `user.id`. Flask uses this to create a `User` object to access information in the succeeding pages. eg. printing the user's name `secrets.html`. This function is in fact used in every page even though it was not explicitly called in `main.py`
```python
@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))
```

Check password agains the database. Unhash using `check_password_hash`
```python
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("secrets"))
    return render_template("login.html")
```

Some pages are only viewable when authenticated using `@login_required`. Loggin user is identified by `current_user.is_authenticated`. `current_user ` is imported from `flask_login`. `is_authenticated` is from the Mixin

[`send_from_directory()`](https://flask.palletsprojects.com/en/1.1.x/api/#flask.send_from_directory) method is used to download files

```python
@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html", name=current_user.name, \
        logged_in=current_user.is_authenticated)

@app.route('/download')
@login_required
def download():
    return send_from_directory("static", filename="files/cheat_sheet.pdf")
```

Immediately login user after registration using `login_user()`
```python
# add new_user to the db...

db.session.add(new_user)
db.session.commit()
login_user(new_user)
```

Use `flash` to display feedback on forms
```python
flash("Password incorrect, please try again")
```
and in the HTML code
{% raw %}
```html
{% with messages = get_flashed_messages() %}
{% if messages %}
  {% for message in messages %}
    <p>{{ message }}<p>
  {% endfor %}
{% endif %}
{% endwith %}
```
{% endraw %}
Resources
- [Cryptii](https://cryptii.com); works just like the Caesar Cipher (Letter substitution by shifting the letters)
- [How the Enigma Machine Works](https://www.youtube.com/watch?v=G2_Q9FoD-oQ)
- [The Flaw in the Enigma Machine](https://www.youtube.com/watch?v=V4V2bpZlqx8)
- [Plain Text Offenders](https://plaintextoffenders.com)
- [Have I been Pawned Passwords](https://haveibeenpwned.com/Passwords)
- [Most common passwords](https://en.wikipedia.org/wiki/List_of_the_most_common_passwords); usually gleaned from attacks
- [Password complexity checker](http://password-checker.online-domain-tools.com); also gives the time it takes for the password to be cracked (brute force)
- [Hacker Typer](https://hackertyper.net)

## Day 67 (Capstone Part 3) - Blog with RESTful Routing

Added SQL database and CRUD functionalities to the blog project 📝: [Blog](https://dawn-leaf-1474.herokuapp.com)

New features:
- Add new post
- Edit post
- Delete post

Flask-CDKEditor renders styling toolbar in the body text area

{% raw %}
```python
from flask_ckeditor import CKEditor, CKEditorField

# more code ...

app.config['CKEDITOR_PKG_TYPE'] = "basic"
ckeditor = CKEditor(app)

class CreatePostForm(FlaskForm):
    # some code ..
    body = CKEditorField("Blog Content", validators=[DataRequired()])

```
{% endraw %}

And in the html
{% raw %}
```html
{% import "bootstrap/wtf.html" as wtf %}

#...more html code ..
 
# Load ckeditor
{{ ckeditor.load() }}

# Configure the ckeditor to tell it which field in WTForm will need to be a CKEditor.
{{ ckeditor.config(name="body") }}    

# Add WTF quickfor
# button_map to render "primary" button styling to the submit button
{{ wtf.quick_form(form, novalidate=True, button_map={"submit": "primary"}) }}
```
{% endraw %}

Remove HTML tags from CDK editor using the [Jinja filter: safe](https://jinja.palletsprojects.com/en/2.11.x/templates/#safe) 

{% raw %} 
```html
{{ Jinja expression | Jinja filter }}
```
{% endraw %}

as in 

{% raw %}
```html
{{post.body|safe}}
```
{% endraw %}

Write date with month as string
```python
from datetime import datetime

date = datetime.now().strftime("%B %d, %Y"),
    # August 14, 2021
```

Also `if form.validate_on_submit():` as opposed to `if request.method == "POST"`, and using `form.body.data` as opposed to `request.form.get("body")` when `form` is supplied in `render_template` as in:
```python
form = CreatePostForm()

# more code ..

return render_template("make-post.html", form=form)
```

## Day 66 - Cafe and Wifi with REST API

An update to the Cafe and Wifi Project ☕📶: [Cafe and Wifi with RESTful API](https://replit.com/@maryletteroa/cafe-and-wifi-restful-api)


Skipped Day 65 on design since I've picked up that course a few months back. And also because I'm excited about this Day's topic 😅

Analogy:
- customer: client
- order: request
- api: language (can take many forms)
- waiter: server

Other examples of protocols are HTTP, HTTPS, and FTP.

REST stands for REpresentational State Transfer and is the gold standard guidelines to communicate with a web API / A set of rules that web developers can follow when building web APIs. A RESTful website follows the REST principles.

Serialization is the process of turning an SQL object into JSON -- the structure of the data returned by the endpoints.

Two important features of REST:
- Use HTTP Request Verbs
    - GET, POST, PUT, PATCH (new!), DELETE
- Use Specific Pattern of Routes/Endpoint URLs
    - e.g. `/artiles`, `/articles/about-me` the latter is a specific article

Resources: Postman to manage API calls and make documentations!
- [Postman](https://www.postman.com)
- [Learning Postman](https://learning.postman.com/)

My take at the [Cafe & Wifi documentation](https://documenter.getpostman.com/view/17076610/Tzz7NxgS)

I'm still confused about when to use `request.args.get()` and `request.form.get()`. The former is for parsing a URL e.g. `/search/?loc=Peckham` or `/update-cafe/<int:id>`.. `def update_cafe(id)`. The latter is for `POST` when a form is created even if it's implicit (e.g. when using Postman) e.g. `Cafe(location=request.form.get("location"))` where the equivalent HTML has an attribute `name` with value `location` as in `<input type="text" name="location"/>`.

☝ Use of `request.form.get("key")` returns None if `key` is not present. This is preferrable to `request.form["key"]` which returns an error if `key` is not found.

Get a variable from link e.g. `http://127.0.0.1:5000/search/?loc=Peckham`
```python
loc = request.args.get("loc")
```

A method to convert a Model to a dictionary 
```python
class Cafe ()
    # more code here
    
    def to_dict(self):
        cafe_dictionary = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return cafe_dictionary
```

```python
@app.route("/random", methods=["GET"]) # can also remove methods because all routes have GET
def get_random_cafe():
    cafes = Cafe().query.all()
    random_cafe = choice(cafes)
    return jsonify(cafe = random_cafe.to_dict())
```

For `POST`:
```python
from distutils.utils import strtobool
    # strtobool converts a string to a boolean 
        # (e.g. "false" and"False" are False or 0, "true" & "True" is True or 1)

@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url")
        has_sockets=strtobool(request.form.get("has_sockets")),
        # more code
    )
```
Example of a `PATCH`
```python
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def path_update_price(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    if cafe:
        cafe.coffee_price = request.args.get("new_price")
        db.session.commit()
```

Example of responses
```python
return jsonify(response={"success": "Successfully deleted the cafe."}), 200
return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database"}), 404
return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct API key"}), 403
```

## Day 64 - My Top Movies

Here is the app 📽: [My top Movies - Deployed](https://damp-meadow-5145.herokuapp.com/)

Features:
- Displays movies according to rating, top-rated first
- Can edit both rating and review
- Can delete entries
- Movie details populated through the [The Movie Database (TMDB) API](https://www.themoviedb.org/documentation/api)

I populated it with my favorite movies (see below 👇) but the db might get deleted or changed overtime.

The code in Replit: [My Top Movies](https://replit.com/@maryletteroa/my-top-movies) and the Github repo: [my-top-movies](https://github.com/maryletteroa/my-top-movies). In the deployed and the github repo, I changed the view of the cards to be in a responsive grid.

This project has some interconnectedness that was a bit confusing. So when I got stuck, I found that back-tracking and thinking about each connection one at a time helped. 

Order database entries by column
```python
movies = Movie.query.order_by(Movie.rating).all()
```

My top movies! These are my go-to movies when I'm bored, sad, or just in general. I like animations (Studio Ghibli), horror (The Conjuring Universe), rom-com (yep!), and the Hunger Games!

<img src="https://lh3.googleusercontent.com/Pv96FXfAUvwh5fySRleK2w68VqWP1KhgDg7J66qp62znLS4MHZOeJbOnBmFDpArg1IQ9nxUsdr4af4_V-OhMp9uvnPefmnj1leHc15xl4l4zpjN51Dp2Z7U4UMHcH0JmGuHolkGCK5mIL4sq2-XGrwYz4m-2TkthRK86bSwYJXocZlkaNzt0rRsPf97NaBBpi_fib65hgs8wnwAID6DLSSed9U1UzQIKmVyQIuSOT3vzjpv62XV5CDMLC1sR9Kfja451wjCcmsHnYqrSJRaygUNMpJjSXwjdHlwvG4rIHjMGfWuX7bUrzJrGaDbWpRt5pLXfKDot-Ixd_zDiuoEWsWiFFnf9XrNIbzg5u2g4Wqoen12Zf4Nc2WINVWsgQU4NY0X3WRjvuPTHPZrL9li3pc-NXNAK1vYcEZ0_Bb78PkXZz4QCmbIFtyB7WQWh0RM-2yATdqRg2d_Dq5dQXZjIMCpP32S10WnQohft1UuiTT0uccfIiEBPPLwEfOxODaJ-oKc1ttgTfxI3CDZTDkYxUrO8reUb15I8_5sBeKsTuUooE6g6tBSSoIYakqMwn0U8JLGapvzqzZ_9yfC9fKHjIEcuRaF0TNWLrScnfjZrBb5twgo2lmxspIPBon6czX9gVitE_axTwOQVZb4eDVPAAM_ahIP0kNFgM43dyvq4QAdyPZfRQBNsQ2uBpN02oSgFLEy4dIqOF3veXzqFxH4gBLZeSQ=w602-h881-no?authuser=2" height="500" alt="my top movies">

## Day 63 - Library

Flask with SQL functionality using SQL Alchemy 📚: [Library](https://replit.com/@maryletteroa/library)

A model using SQL Alchemy
```python
from flask import Flask, render_template, request, redirect, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/ new-books-collection.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

# create the database
db.create_all()

# output contents of the database
Books.query.all()
```

CRUD functions:

Create an entry
```python
def add():
    if request.method == "POST":
        book = Books(title = request.form["title"], 
            author = request.form["author"], 
            rating = request.form["rating"])
        db.session.add(book)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html")
```

Update an entry
```python
@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_rating(id):
    book_to_update = Books.query.get(id)
    if request.method == "POST":
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for("home"))
```

Read
{% raw %}
```python
Books.query.all()
```
then in the HTML, use curly braces and dot notation
```html
<form action="{{ url_for('edit_rating', id=book.id) }}", method="post">
    <h1>Book name: {{ book.title }}</h1>
    <h1>Current rating: {{book.rating }} </h1>
    <input type="text" placeholder="New Rating" name="rating">
    <button>Change Rating</button>
</form>
```
{% endraw %}


Delete an entry
{% raw %}
```html
<a href="{{ url_for('delete', id=book.id) }}">Delete </a>
```
{% endraw %}

```python
id = request.args.get("id")
book_to_delete = Books.query.get(id)
db.session.delete(book_to_delete)
db.session.commit()
```

Resources:
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart)

Redirects are a bit confusing

## Day 62 - Coffee & Wifi

Cofee and Wifi ☕📶: [Coffee & WiFi](https://replit.com/@maryletteroa/coffee-and-wifi)

Useful Jinja feature that I discovered while digging: [For loop index and attributes in Jinja](https://jinja.palletsprojects.com/en/3.0.x/templates/#for)

## Day 61 - Flask-WTForms

Template code using Flask-WTForms and Flask-Bootstrap: [flask-wtforms](https://replit.com/@maryletteroa/flask-wtf-forms)

Resources:
- [Flask-WTForm](https://flask-wtf.readthedocs.io/en/0.15.x)
- [Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/)

Quick form

{% raw %}
```html
{% extends "bootstrap/base.html"%}
{% import "bootstrap/wtf.html" as wtf %}
{{ wtf.quick_form(form, novalidate=True) }}
```
{% endraw %}

## Day 60 - Contact Form

Added functionality to the contact form for the blog: 📝[Blog](https://dawn-leaf-1474.herokuapp.com)

Template contact form with some functions: [Contact Form](https://replit.com/@maryletteroa/contact-form)

Using Flask `request`

```python
from flask import request

@app.route("/login", methods=["POST"])
def received_data():
    username = request.form["username"]
    password = request.form["password"]
    return f"<h1>Name: {username}, Password: {password}</h1>"

```

In the HTML file, add `action="<redirect>" method=<"get" or "post">`. Add value for name in input tag: `name="username"`

```html
<form action="/login" method="post">
    <labe >Name</label>
    <input type="text" placeholder="name" name="username">
    <label >Pasword</label>
    <input type="text" placeholder="password" name="password">
    <button type="submit">Ok</button>    
</form>
```

## Day 59 (Capstone Part 2) - Blog with Styling

Stub Blog using Flask / Jinja and deployed using Heroku: 📝[Blog](https://dawn-leaf-1474.herokuapp.com)


The repo for this project is here: [my-blog-flask](https://github.com/maryletteroa/my-blog-flask)


Ways to serve static files:
{% raw %}
```python
url({{ url_for('static', filename='assets/img/home-bg.jpg')}})
```
{% endraw %}
also
```python
app = Flask(__name__,
        static_url_path = "",
        static_folder = "static",
        templates_folder = "templates")
```

Resources:
- [Bootstrap Made](https://bootstrapmade.com/)
- [Creative Tim Bootstrap Themes](https://www.creative-tim.com/bootstrap-themes/free)


Useful resource on how to setup a flask app to deploy in Heroku:
- [Deploying Flask app on Heroku using GitHub](https://dev.to/lordofdexterity/deploying-flask-app-on-heroku-using-github-50nh)
- [Flask Heroku example](https://github.com/franccesco/flask-heroku-example)


## Day 58 - Tindog

<small>I've come around to front-end web development (again!) and, admittedly, I sat on this for <em>days</em>... But here it is! 🌞</small> 👇

Landing page for a dating site for dogs 🐶: [Tindog](https://maryletteroa.github.io/tindog)

The repo for this project is here: [tindog](https://github.com/maryletteroa/tindog)

CDN - Content Delivery Network; Instead of hosting a website in just one location, there are multiple locations that can deliver the website; Cuts down on the latency i.e. how long the website will load up

Bootstrap uses `maxcdn`; Look for the shortest route to download the CSS file; Browser caches (saves local copy) so browser does not have to download it again which further cuts down the latency

Workflow: 
1. Plan first! 
2. Wireframe - low-fidelity representation of a website  
3. Mockup (optional) - high-fidelity representation of the your app or web design  
4. Prototype (optional) - animated version of your website

Resources:
- [Awwwards](https://www.awwwards.com/websites/com)
- [UI Patterns](http://ui-patterns.com/patterns)
- [Dribble](https://dribbble.com/search/website)
- [Sneak Peek It](https://sneakpeekit.com)
- [Balsamiq](https://sneakpeekit.com)
- [Fonts](https://fonts.google.com)
- [Font awesome](https://fontawesome.com)
- [Bootstrap examples](https://getbootstrap.com/docs/4.5/examples)
- [Bootsnipp](https://bootsnipp.com)
- [Mobile-friendly](https://search.google.com/test/mobile-friendly)

[How to install bootstrap](https://getbootstrap.com/docs/4.5/getting-started/introduction)

Javascript is responsible for the behaviour of the website; CSS for the appearance.

Responsive does not mean fast; it means that the website respond to the size of the viewport i.e. desktop, tablet, or phone.

Positioning:
- Sequential (top is closer to the back)
- Heirarchical (child sits over parents)
- `position`
    - absolute - take divs outside of the flow, bottom div at the top
    - z-index - positive: forwards; negative: backwards; only works with `position` at the parent div; by default all elements have a z-index of 0

Refactoring: neat, tidy, readable code
By order of importance
- Readability
- Modularity
- Efficiency
- Length

[Code Golf](https://codegolf.stackexchange.com/questions/157546/create-a-magic-8-ball)

`.container.title` - targets an element with two classes `class="container title"`
`.container .title` - targets an element with class `.title` inside another element with class `.container`

Consider using classes for specific styling rather than targetting a tag itself.

## Day 57 (Capstone Part 1) - Blog

Simple blog template 📝: [Blog](https://replit.com/@maryletteroa/blog)

[Rendering Templates in Flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/#rendering-templates)

[Jinja](https://jinja.palletsprojects.com/en/2.11.x/templates) - used for templating in Python; already installed with Flask

{% raw %}
```html
<h1>{{ 5 * 6 }}</h1>
<h1>Hey {{ name.title() }},</h1>
```
{% endraw %}

```python
from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route("/")
def home():
    random_number = random.randint(1,10)
    return render_template("index.html", num=random_number)
```
{% raw %}
```html
<h3>Random Number: {{ num }}</h3>
```
{% endraw %}

Multi-line python codes in HTML
{% raw %}
```html
{% for blog_post in posts: %}
    {% if blog_post["id"] == 2: %}
        <h1>{{ blog_post["title"] }}</h1>
        <h2>{{ blog_post["subtitle"] }}</h2>
    {% endif %}
{% endfor %}
```
{% endraw %}

URL building
{% raw %}
```html
<a href="{{ url_for('get_blog', num=3) }}">Go to blog</a>
```
{% endraw %}

Where `get_blog` is a function in `app.py` that renders a page, and `num` is a keyword argument that can be passed:
```python
@app.route("/blog/<num>")
def get_blog(num):
    # some code here
    return render_template("blog.html", posts=all_posts)
```

Resources:
- [Update your footer](https://updateyourfooter.com)
- [Genderize.io](https://genderize.io) - predict the gender of a name
- [Agify.io](https://agify.io) - predict the age of a name
- [Npoint.io](https://www.npoint.io/) - create own API endpoint


## Day 56 - Name Card

Name card flask template: [Name Card](https://replit.com/@maryletteroa/name-card)

HTML Source: [Identity](https://github.com/html5up/identity)

How to render HTML and statifiles:

HTML files should be inside the folder `templates`.

Static files like images, CSS, videos etc should be in the folder `static` and linked accordingly in the HTML files e.g. `static/<image_name>.png` 
```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
```

Chrome tends to cache static files so in order to view changes in CSS, need to do a hard reload: `Shift + Reload`

Free templates: [HTML5](https://html5up.net)

How to trigger editing a webpage in Chrome developer: 

In console (JS):
```javascript
document.body.contentEditable = true
```
Then save the webpage.

Resource for images: [Unsplash](https://unsplash.com)


## Day 55 - Higher Lower Web Game

Higher-lower game in web form: [Higher Lower Web Game](https://replit.com/@maryletteroa/higher-lower-game-web)

Parse a URL in Flask
```python
@app.route("/username/<name>/1") # can add before or after or leave as /<name>
def greet(name):
    return f"Hello {name}"
```

Run on debug mode to reload server automatically; Errors are outputed in View
```python
if __name__ == "__main__":
    app.run(debug=True)
```
Can open an interactive shell (via icon on right), enter debugging PIN to continue.

Converter - converts url variable name to a datatype
```python
@app.route("/username/<path:name>")
def greet(name):
    return f"Hello there {name}"
# <local:5000>/name/1
# Hello there name/1

@app.route("/username/<name>/<int:number>")
def greet(name, number):
    return f"Hello there {name}, you are {number} years old"
#<local:5000>/name/2
# Hello there name, you are 2 years old
```

Render HTML
```python
@app.route("/")
def hello_world():
    return "<h1 style='text-align: center'>Hello, World!</h1> \
    <p>This is a paragraph</p> \
    <img width=200px src='https://media.giphy.com/media/3oriO0OEd9QIDdllqo/giphy.gif'>"
```

Render HTML tags in decorators
```python
def make_bold(function):
    def wrapper():
        return f"<b>{function()}</b>"
    return wrapper
def make_emphasis(function):
    def wrapper():
        return f"<em>{function()}</em>"
    return wrapper
def make_underlined(function):
    def wrapper():
        return f"<u>{function()}</u>"
    return wrapper

@app.route("/bye")
@make_bold
@make_emphasis
@make_underlined
def say_bye():
    return "Bye"
```

Advanced decorator - pass arguments as `*args` and/or `**kwargs` to wrapper function 
```python
class User:
    def __init__(self, name):
        self.name = name
        self.is_logged_in = False

def is_authenticated_decorator(function):
    def wrapper(*args, **kwargs):
        if args[0].is_logged_in == True:
            function(args[0])
    return wrapper

@is_authenticated_decorator
def create_blog_post(user):
    print(f"This is {user.name}'s new blog post.")

new_user = User("my_name")
new_user.is_logged_in = True
create_blog_post(new_user)
```

Another example
```python
# Create the logging_decorator() function
def logging_decorator(function):
    def wrapper(*args):
        result = function(*args)
        print(f"Function name: {function.__name__}, arguments: {args} ")
        print(f"Result: {result}")
    return wrapper

# Use the decorator
@logging_decorator
def sum(n1, n2):
    return n1 + n2
# Call function
sum(3,2)

# Function name: sum, arguments: (3, 2)
# Result: 5
```

## Day 54 - Introduction to Flask

Starting code here 👉: [Introduction to Flask](https://replit.com/@maryletteroa/introduction-to-flask)

[Flask documentation](https://flask.palletsprojects.com/en/1.1.x/quickstart)

Full Stack = Front-End + Back-End  
Front: HTML, CSS, JS; Frameworks: Angular, React ...  
Back-end: JS, Python, Ruby, etc..; Frameworks: Node, Flask ...  

Frameworks: Tools with pre-built functionalities

Examples of frameworks in Python:
 - Flask
 - Django
 - Cherrypy
 - Pyramid

Backend:
 - Client
 - Server
 - Datbase 


`app.py`
```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/bye")
def say_bye():
    return "Bye"

if __name__ == "__main__":
    app.run()
```

Run as:
```bash
flask run
```

`__name__` is a Special Attribute in Python which corresponds to the current class or module name; `__main__` is the name of the scope in which the top-level code runs.

Python functions can be treated as first-class objects - they can be passed around as arguments e.g. int/string/float etc

```python
def add(n1, n2):
    return n1 + n2

def subtract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return n1 * n2

def divide(n1, n2):
    return n1 / n2
```

Functions as first-class objects
```python
def calculate(calc_function, n1, n2):
    return calc_function(n1, n2)

result = calculate(add, 2, 3)
print(result)
    # 5
```

Nested functions
```python
def outer_function():
    print("I'm outer")

    def nested_function():
        print("I'm inner")

    nested_function()

outer_function()

    # I'm outer
    # I'm inner
```

Functions can be returned from other functions
```python
def outer_function():
    print("I'm outer")

    def nested_function():
        print("I'm inner")

    return nested_function

inner_function = outer_function()
inner_function() # add parenthesis (calls variable as a function)
    # I'm outer
    # I'm inner
```

Simple decorator
```python
import time
current_time = time.time()
print(current_time)

def speed_calc_decorator(function):
    def wrapper_function():
        start_time = time.time()
        function()
        end_time = time.time()
        print(f"{function.__name__} run speed: {end_time - start_time}s")
    return wrapper_function

@speed_calc_decorator
def fast_function():
    for i in range(10000000):
        i * i
        
@speed_calc_decorator
def slow_function():
    for i in range(100000000):
        i * i

fast_function()
slow_function()
```


## Day 53 (Capstone) - Data Entry Automation

Automated data entry 🏦: [Data entry automation](https://replit.com/@maryletteroa/data-entry-automation)

Goes through Zillow (a website containing listings of properties), scrapes all results for a certain search, then fills up a Google Form with these information.

Pass a `header` in requests in order to access the website without CAPTCHA. Supply headers of the default browser.

Since BeautifulSoup can only parse the first 9 listings, I've used Selenium all throughout:
 - Clicked / unclicked an element on the right panel (I used the dropdown element since it's clickable; trying this on any other element raises an exception)
 - Scrolled down using `Key.DOWN` for n seconds (this hopefully gets the page to load until the end; otherwise increase n)
    - I tried scrolling until an element but all the listing information do not tend to load with the speed of the scroll
- Maximizing the window also helped with the speed

I also scraped until the end of the results (e.g. until page 20). I can only get until page 20 (800 listings) even though Zillow indicates there are >1,600 properties.

Time:
```bash
real    32m40.976s
user    0m18.578s
sys     0m3.234s
```

Zillow still checks for a human now and again so the script above fails when that happens.

I skipped Days 50-52 because I didn't want to deal with social media right now. Here's some interesting links:
- [Does Tweeting at Companies Really Work?](https://time.com/4894182/twitter-company-complaints)
- [This person does not exist](https://www.thispersondoesnotexist.com)
- Translate URL to human-readable form: [URL Decoder/Encoder](https://meyerweb.com/eric/tools/dencoder)


## Day 49 - Automate Job Application

Automate LinkedIn job application (template) code 💼:  [Automate Job Applications](https://replit.com/@maryletteroa/automate-job-applications)


Used XPaths generously, and also `time.sleep()` function which waits for the page to load before executing the next part of the code

## Day 48 - Game Clicker Bot

Cookie world domination here 🍪: [Game Clicker Bot](https://replit.com/@maryletteroa/game-cliker-bot)

Automates the game (click and purchase) for five minutes.

Got the following score:
```bash
Total score: 1239
Cookies per second: cookies/second : 97.4
```

Uses [Selenium](https://www.Selenium.dev) web driver.

Download the Chrome Driver that matches Chrome browser's version: [ChromeDriver WebDriver for Chrome](https://chromedriver.chromium.org/downloads)

Read the docs for [locating elements in Selenium](https://Selenium-python.readthedocs.io/locating-elements.html)

```python
chrome_driver_path="/path/to/exec"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
url = "https://www.amazon.com/Legend-Zelda-Skyward-Sword-Nintendo-Switch/dp/B08WWFWRY6"

# open the url in browser
driver.get(url)

# get element
price = driver.find_element_by_id("priceblock_ourprice")
print(price.text)

# quit tab or program
# driver.close() # quits particular tab
driver.quit() # quits entire program
```

BeautifulSoup scrapes data from website HTML/XML but gets stuck if website uses Javascript to load (or other conditions) whereas Selenium would do the same thing as humans i.e. opening websites, grabbing the needed info. Can do a lot more using Selenium.

```python
# url = "python.org"

search_bar = driver.find_element_by_name("q")
print(search_bar) # a Selenium object

print(search_bar.tag_name)
print(search_bar.get_attribute("placeholder"))

logo = driver.find_element_by_class_name("logo")
print(logo.size)

documentation_link = driver.find_elements_by_css_selector(".documentation-widget a") # list
print(documentation_link.text)
```

XPath - [What is XPath](https://www.w3schools.com/xml/xpath_intro.asp)

```python
bug_link = driver.find_element_by_xpath('//*[@id="site-map"]/div[2]/div/ul/li[3]/a')
print(bug_link.text)
```

To get more than one elements, use `find_elments*` in method name, as in e.g. `.find_elements_by_xpath` or `find_elements_by_name`

Interactions
```python
from Selenium import webdriver
from Selenium.webdriver.common.keys import Keys

chrome_driver_path="/mnt/d/Programs/Chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
url = "https://en.wikipedia.org/wiki/Main_Page"
driver.get(url)

# selecting through tag
article_count = driver.find_element_by_css_selector("#articlecount a")
article_count.click()


# selecting through linked text (text inside link tag)
all_portals = driver.find_element_by_link_text("All portals")
all_portals.click()

# write in input bar
search = driver.find_element_by_name("search")
search.send_keys("Python")
# enter in keyboard
search.send_keys(Keys.ENTER)


```

## Day 47 - Amazon Price Tracker

Get sales alert here 🛒: [Amazon Price Tracker](https://replit.com/@maryletteroa/amazon-price-tracker)

Sends an email when an item in Amazon is equal to or below a price. (May be adapted to other websites.)

See current browser's headers here: [MY HTTP Header](http://myhttpheader.com/). Pass the entire string as values in headers.

Web article on [the difference between HTML and XML](https://techdifferences.com/difference-between-xml-and-html.html).

## Day 46 - Music Time Machine

Travel back in time through music! 🎵: [Music Time Machine](https://replit.com/@maryletteroa/music-time-machine)

This is so cool! ⭐ And I get to have new playlists while working.

This code uses the `spotipy` library. I had some hiccups with authentication (my systems' config). Otherwise the [documentation](https://spotipy.readthedocs.io) is pretty good.

This is the [Developer page](https://developer.spotify.com) for Spotify.

Here's the [`spotipy` Github repo](https://github.com/plamere/spotipy) which contains [code examples](https://github.com/plamere/spotipy/tree/master/examples).


## Day 45 - Greatest Movies

Top 100 Greatest Movies according to Empire Online 📽: [Greatest Movies](https://replit.com/@maryletteroa/greatest-movies)

(I actually haven't been able to sit through The Godfather try as I may 😅)

The script is a bit complex because the source website has transitioned out of vanilla HTML -- essentially, contents were loaded using Javascript on an almost empty HTML plate. Movie names had to be parsed from the `<script>` tag, and then further re-formatted.

I've skipped over several days since days 41-44 were about HTML and CSS (which I feel at this point I'm already familiar with).

Is Web Scraping legal? 🤔
 - [Web scraping is now legal: Here's what that means for Data Scientists](https://medium.com/@tjwaterman99/web-scraping-is-now-legal-6bf0e5730a78)  
 - ✅ Publicly available  
 - ✅ Not copyrighted   
 - ✅ Using data privately  
 - ❌ Using data for commercial purposes (business)  
 - ❌ Data behind authentication (e.g. scraping  from social media sites where you need to login - see fine print)

❗ Just because it's legal, doesn't mean you can do it - CAPTCHA / reCAPTCHA  

💭 Ethics: think about if it's right or wrong; putting aside whether it's legal or not.

👍 Go for the API if possible  
👍 Respect the owner - don't scrape every few ms  (e.g. try < 1 per minute)  
👍 Check `<website>/robots.txt`. e.g `https://news.ycombinator.com/robots.txt` specifies which endpoints are not allowed to be scraped

```
User-Agent: * # person or bot scraping
Disallow: /x?
Disallow: /r?
Disallow: /vote?
Disallow: /reply?
Disallow: /submitted?
Disallow: /submitlink?
Disallow: /threads?
Crawl-delay: 30 
    # the number of seconds that to wait each time 
    # the website is accessed
```
Compare this to [LinkIn's `robot.txt`](https://www.linkedin.com/robots.txt) statement


Read a website using `requests`
```python
response = requests.get("https://news.ycombinator.com")
yc_combinator = response.text
soup = BeautifulSoup(yc_webpage, "html.parser")
```

👇 Can use `html.parser` or `lxml`  which needs to be imported `import lxml`; sometimes `lxml` works better than `html.parser` 

Some syntax reference:
```python
from bs4 import BeautifulSoup
# import lxml

with open("./website.html") as file:
    contents = file.read()

soup = BeautifulSoup(contents, "html.parser") #or "lxml"
print(soup.title)
    # <title>Angela's Personal Site</title
print(soup.title.name)
    # title
print(soup.title.string)
    # Angela's Personal Site

# matches first instance
print(soup.p)

# pretty printing
print(soup.prettify())

# list of all anchor tags
all_anchor_tags = soup.find_all(name="a")
for tag in all_anchor_tags:
    print(tag.getText())
    print(tag.get("href"))

# isolate by name tag
heading = soup.find(name="h1", id="name")
print(heading)
    # <h1 id="name">Angela Yu</h1>

# same for isolating by class name
section_heading = soup.find(name="h3", class_="heading") 
    # "class" is a reserved word in Python
print(section_heading)
    # <h3 class="heading">Books and Teaching</h3>

# using selector
company_url = soup.select_one(selector="p a")
print(company_url)
    # <a href="https://www.appbrewery.co/">The App Brewery</a>

# using selector
name = soup.select_one(selector="#name")
print(name)
    # <h1 id="name">Angela Yu</h1>
headings = soup.select(".heading")
print(headings)
    # [<h3 class="heading">Books and Teaching</h3>, 
    # <h3 class="heading">Other Pages</h3>]
```



## Day 40 (Capstone Part 2) - Flight club

Join the flight club here 🤜🛫: [Flight club](https://replit.com/@maryletteroa/flight-club)

This sends a text and an email (a user can be added) when there are flights cheaper than a certain price. If direct flights are not avialable, it looks for flights with at most one (1) stop-over.

Flights are limited at the moment, so testing was challenging. 

I also encountered a weird bug because I was passing an entire class as an argument.

⚠ Sheety has a cap of 200 requests per month in its free tier.


Historic low prices for airfare: [Fare Detective](https://www.faredetective.com/farehistory)


## Day 39 (Capstone Part 1) - Flight deal finder

Flight deal finder 🛫: [Flight deal finder](https://replit.com/@maryletteroa/flight-deal-finder)

Sends a message when flights are equal to or cheaper than a set price

This took longer than I thought: getting through the API documentation and writing models.

Flight search API: [Tequila](https://tequila.kiwi.com/)


## Day 38 - Workout Tracker

Workout tracker using Google Sheets 🏊‍♀️ : [Workout tracker](https://replit.com/@maryletteroa/workout-tracker)

This tracker uses NLP capabilities from [OpenAI API](https://openai.com/blog/openai-api/).

This was a lot of fun to make and certainly challenging in terms of reading documentations.


API resources:
 - [Nutritionix](https://www.nutritionix.com/business/api)
 - [Sheety](https://sheety.co/)

Storing `.env` in Replit: [Storing secrets in .env](https://docs.replit.com/archive/secret-keys)

## Day 37 - Pixela Habit Tracker

Template for the Pixela habit tracker here🧘‍♀️: [Pixela habit tracker](https://replit.com/@maryletteroa/pixela-habit-tracker)

Advanced authentication and POST / PUT / DELETE Requests

```python
# get data
requests.get()
# post data
requests.post(url=endpoint, json=params)
# update a piece of data
requests.put()
# delete a piece of data
requests.delete()
```

Website: [Pixela](https://pixe.la), [API Documentation](https://docs.pixe.la/)

`.strftime()` to specific date string formats

```python
today = datetime.now().strftime("%Y%m%d")
yesterday = datetime(year=2020, month=7, day=12).strftime("%Y%m%d")
```

## Day 36 - Stock Trading News Alert

A script to send stock updates 📈: [Stock trading news alert](https://replit.com/@maryletteroa/stock-trading-news-alert)

\* sends a text when stock price of a certain company changes 5% or more between the present day and the day before

API sources:
- [Alphavantage](https://www.alphavantage.co)
- [NewsAPI](https://newsapi.org/)

## Day 35 - Rain Alert App

Rain Alert app ☔: [Rain Alert](https://replit.com/@maryletteroa/rain-alert)

API authentication using API key: way for API providers to track usage and/or deny access past limit

Weather related websites:
- [Open Weather Map](https://openweathermap.org)
- [OWM Weather Conditions ID](https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2)
- [Live Weather](https://www.ventusky.com)

Visual parsing of JSON texts: [Online JSON Viewer](http://jsonviewer.stack.hu)

Send text messages using [Twillio](https://www.twilio.com/try-twilio)

Retrieve variables from environment
```python
import os

API_KEY = os.environ.get("API_KEY")
```
In the commandline
```shell
export API_KEY="thisIsASecret"
```

## Day 34 - Quizzler App

Play the Quizzler App here 🎓: [Quizzler app](https://replit.com/@maryletteroa/quizzler-app)

[Open Trivia Database](https://opentdb.com/api_config.php)

[HTML Entities](https://www.w3schools.com/html/html_entities.asp) - a way to replace characters in text so they are not confused with HTML characters

[HTML Escape](https://www.freeformatter.com/html-escape.html) to convert into human-readable format

Or using the `html` module
```python
import html
text = "It's <tag>"
q_text = html.unescape(text)
```

Specify paramater as type: 'Class'
```python
from quiz_brain import QuizBrain

def __init__(self, quiz_brain: QuizBrain):
    # code here
```
Usage in `main.py`
```python
quiz = QuizBrain()
quiz_ui = QuizInterface(quiz)

```

Type hints
```python
age: int
name: str
height: float
is_human: bool

def police_check(age: int) -> bool:
    if age > 18:
        can_drive = True
    else:
        can_drive = False
    return can_drive

if print(police_check(19)):
    print("You may pass")
else:
    print("Pay a fine")


# will crash code
if print(police_check("twelve")):
    print("You may pass")
else:
    print("Pay a fine")
```

## Day 33 - ISS Overhead

Send an email if the International Space Station is overhead 🌟: [ISS Overhead](https://replit.com/@maryletteroa/iss-overhead)

API (Application Programming Interface): a set of commands, functions, protocols, and objects that programmers can use to create software or interact with an external system

API Endpoint: where to extract data; e.g. url `api.coinbase.com`

API Request: get a piece of data from a website 

API Parameters: inputs

[International Space Station Current Location](http://open-notify.org/Open-Notify-API/ISS-Location-Now)

[Kanye Quotes API](https://kanye.rest/)

[Sunrise-Sunset API](https://sunrise-sunset.org/api)

[JSON Viewer Chrome plugin](https://chrome.google.com/webstore/detail/json-viewer/gbmdgpbipfallnflgajpaliibnhdgobh/related)

[HTTP Status Codes](https://httpstatuses.com)
 - 1xx: Hold on
 - 2xx: Here you go
 - 3xx: Go away
 - 4xx: You screwed up
 - 5xx: I screwed up

[Latitude-Longitude To Address](https://www.latlong.net/Show-Latitude-Longitude.html)
[Address to Latitude-Longitude](https://www.latlong.net)

## Day 32 - Birthday Greeting

Email a birthday greeting 🎂: [Birthday greeting](https://replit.com/@maryletteroa/birthday-greeting)

SMTP stands for Simple Mail Transfer Protocol
```sh
Gmail(smtp.gmail.com)
Yahoo(smtp.mail.yahoo.com) 
Hotmail(smtp.live.com)
Outlook(smtp-mail.outlook.com)
```

Template code for sending an email
```python
import smtplib

my_email = "test@gmail.com"
password = "abc123()"

with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendemail(
        from_addr=my_email, 
        to_addrs="test@yahoo.com", 
        msg="Subject:Hello\n\nThis is the body of my email."
    )
```


Some `datetime` codes
```python
import datetime as dt

now = dt.datetime.now()
year = now.year
print(year)
print(now.weekday())
date_of_birth = dt.datetime(year = 1995, month = 12, day = 15, hour=4)
print(date_of_birth)
```

[101 Monday Motivation Quotes](https://www.positivityblog.com/monday-motivation-quotes)

Host code in [Python Anywhere](https://www.pythonanywhere.com)


## Day 31 - Flash Card App

Flash card app: [Flash card](https://replit.com/@maryletteroa/flash-card)

It's another capstone project! 

Timer in `tkinter`
```python
# set the timer
flip_timer = window.after(3000, func=flip_card)
# stop the timer
window.after_cancel(flip_timer)
```

## Day 30 - Password Manager with Search

🔒🔎 [Password manager with search](https://replit.com/@maryletteroa/password-manager-with-search)

Catching exceptions

```python
try:
    # something that might cause an exception
except:
    # do this if there was an exception
else:
    # do this if there were no exceptions
finally:
    # do this no matter what happens
```

Use Exceptions if there is no other way (i.e. an easy alternative) to handle an error or if the error happens in *exceptional* cases. Otherwise, an `if-else` statement can be used.

Error handling with recursions
```python
def generate_phonetic():
    word = input("Enter a word: ").upper()
    try:
        output_list = [phonetic_dict[letter] for letter in word]
    except KeyError:
        print("Sorry, only letters in the alphabet please.")
        generate_phonetic()
    else:
        print(output_list)
generate_phonetic()
```

JSON - `update()` and `dump()` are a bit confusing 
```python
import json
new_file = {"key":"value"}
with open("file.json") as data_file:
    # read a json file
    data = json.load(data_file)
    # update a json file
    data.update(new_data) 
    # write in a json file
    json.dump(new_data, data_file) 
```


## Day 29 - Password Manager

Password manager/ generator 🔒 : [Password manager](https://replit.com/@maryletteroa/password-manager)

Also learned about [pyperclip](https://pypi.org/project/pyperclip), a clipboard module in Python.


## Day 28 - Pomodoro Timer

Tomato timer here 🍅: [Pomodoro](https://replit.com/@maryletteroa/pomodoro)

Event Driven programs watch the screen -- a while loop before the `mainloop()` program will result in an error since the program will stop listening when it encounters the while loop.

Recursion
```python
def count_down(count):
    print(count)
    if count > 0:
        window.after(1000, count_down, count-1)
```

Dynaminc typing
```python
count_down = 0
count_down = "00"
    # change type from int to str
```

[Python is a **strongly, dynamically typed** language](https://stackoverflow.com/questions/11328920/is-python-strongly-typed)

## Day 27 - Miles to Kilometer Converter

Convert miles to kilometer 🛣: [Miles to Kilometer](https://replit.com/@maryletteroa/miles-to-kilometer)

Moving on to GUI✨ using [tKinter](https://docs.python.org/3/library/tkinter.htm)

Tk commands: [Tk commands](http://tcl.tk/man/tcl8.6/TkCmd/contents.htm)

Steps to add components on the screen:
1. Make a component
2. Specify how that component will be laid out on the screen
```python
my_label = tkinter.Label(text="I am a label")
my_label.pack() # The Packer
```

tkinter layouts:
1. Pack
2. Place
3. Grid
```python
my_label.pack(side="left")
my_label.place(x=0,y=0)
my_label.place(x=100, y=100) # x moves to right, y moves down
my_label.grid(column=0, row=0)
```
Pack and place are incompatible

Advanced arguments 😡💢😠
<iframe src="https://giphy.com/embed/1w2vvSVgAu3Ti" width="250" height="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/fighting-power-rangers-argument-1w2vvSVgAu3Ti">via GIPHY</a></p>

Unlimited positional arguments: `*args` -> tuple
```python
def add(*args):
    print(sum(args))
add(3,5,8,10,12) # 38
```

Unlimited keyword arguments: `**kwargs` -> dictionary
```python
def calculate(n, **kwargs):
    n += kwargs["add"]
    n *= kwargs["multiply"]
    print(n)

calculate(2, add=3, multiply=5) # (2+3)*5 = 25
```
Use in a class:
```python
class Car:
    def __init__(self, **kw) :
        self.make = kw.get("make")
        self.model = kw.get("model")
        self.color = kw.get("color")
        self.seats = kw.get("seats")

my_car = Car(make="Nissan", model="Skyline")
print(my_car.color)
    # None
```

Mixed
```python
def all_aboard(a, *args, **kw): 
    print(a, args, kw)
 
all_aboard(4, 7, 3, 0, x=10, y=64)
    # 4 (7,3,5) {'x: 10, 'y': 64}
```


## Day 26 - NATO Alphabet

Translate any word to the NATO alphabet here: [NATO alphabet](https://replit.com/@maryletteroa/nato-alphabet)

This is actually helpful for me! (Also, isn't spelling out the letters easier?)

List comprehension

```python
new_list  = [new_item for item in list if test]
```

Dictionary comprehension
```python
new_dict = {new_key:new_value for (key,value) in dict.items if test}

```

Iterate over a Pandas DataFrame: use `iterrows()`
```python
for (index, row) in df.iterrows():
    print(index)
    print(row)
        # each row is a pandas.Series object so dot-notation can be used
    print(row.col1)
    print(row.col2)
```


## Day 25 - Guess US States

Guess US States here 👉: [US States](https://replit.com/@maryletteroa/us-states)

Website for quizzes: [Sporkle](https://www.sporcle.com/)

Code to get coordinates of mouseclick in `turtle`

```python
def get_mouse_click_coor(x,y):
    print(x,y)
turtle.onscreenclick(get_mouse_click_coor)
turtle.mainloop() # instead of `exitonclick()`
```


## Day 24 - Snake with High Score

🐍 Snake but you can retain the high scores:  [Snake High Score](https://replit.com/@maryletteroa/snake-high-score)  
📧 Mail merge - an automatic letter generator: [Mail merge](https://replit.com/@maryletteroa/mail-merge)

Mail merge reminds me of the time I wrote a script in Python/Latex that created name tags automatically. It took a bit to generate the code but worth the effort for the number of events x participants that we had.

Optimized readability > Premature optimization (Efficient code as soon as possible)

"You write so that people understand what you say."


## Day 23 (Capstone) - Turtle crossing

🛣🐢: [Turtle crossing](https://replit.com/@maryletteroa/turtle-crossing)

It's another capstone, another landmark! 🎉 This game brings back a lot of memories!

💡 Using random chance to slow down the generation of cars can be done this way:
```python
    def create_car(self):
        random_chance = random.randint(1, 6)
        if random_chance == 1:
            # generate cars
```
Needed help on the car manager bit.. but it was interesting. Got confused about when to inherit or not. 

Programming is a way to test one's thinking! 😵💫

## Day 22 - Pong

Play Pong here 🎮: [Pong](https://replit.com/@maryletteroa/pong)

To dos for this game:

- [x] Create the screen
- [x] Create and move a paddle
- [x] Create another paddle
- [x] Create the ball and make it move
- [x] Detect collision with wall and bounce
- [x] Detect collision with paddle
- [x] Detect when paddle misses
- [x] Keep score

## Day 21 - Snake Game Part 2

The full Snake Game here 🐍: [Snake game](https://replit.com/@maryletteroa/snake-game)

- [x] Detect collision with food
- [x] Create a scoreboard
- [x] Detect collision with wall
- [x] Detect collision with tail


Inheritance 
```python
class Fish(Animal):
    def __init__(self):
        super().__init__()
    def breathe(self):
        super().breathe()
        # add something
```


## Day 20 - Snake Game Part 1

Snake Game Part 1 here 🐍: [Snake game Part 1](https://replit.com/@maryletteroa/snake-game-part-1)

To dos for this game:

- [x] Create a body
- [x] Move the snake
- [x] Control the snake
- [ ] Detect collision with food
- [ ] Create a scoreboard
- [ ] Detect collision with wall
- [ ] Detect collision with tail

💡 Focus on understanding, not on memorising.

Getting the hangout of OOP. Also need to consider how to make future modifications of the code easier -- CONSTANTS (at the top of the code) help!

## Day 19 - Etch-A-Sketch App

🐢 [Turtle Race](https://replit.com/@maryletteroa/turtle-race)  
[Etch-A-Sketch](https://replit.com/@maryletteroa/etch-a-sketch)



I had a great time making the turtle race game! 🐢

Higher order functions

```python
def calculator(n1, n2, func):
    return func(n1, n2)
```

States, different versions of the same Object
```python
timmy.color = green
tommy.color = purple

```


## Day 18 - Hirst Painting

See it here 🎨: [Hirst painting](https://replit.com/@maryletteroa/hirst-painting)

[Trinket](https://trinket.io/docs/colors)  
[Colorgram.py](https://pypi.org/project/colorgram.py/)  
[RGB Calculator](https://www.w3schools.com/colors/colors_rgb.asp)

## Day 17 - Quiz Game
Play the game here: [quiz-game](https://replit.com/@maryletteroa/quiz-game)

Generate trivia questions here 👉 [Open Trivia Database](https://opentdb.com)

Run for the bus! 🚌🏃‍

Different types of cases:
- PascalCase
- camelCase
- snake_case

Attaching an attribute to an object
```python
class User:
    speed = 4

user_1 = User()
user_1.id = "001"
user_1.username = "angela"
print(user_1.username)
```

Constructor function `__init__(self)` initializes the Classes:
```python
class Car:
    def __init__(self, seats):
    self.seats = seats

my_car = Car(5)
```

Classes, attributes, methods, objects

```python
class User:
    def __init__(self, user_id, username):
        # attributes
        self.id = user_id
        self.username = username
        self.followers = 0 # default value
        self.following = 0

    # method
    def follow(self, user):
        user.followers += 1
        user.following += 1

# objects
user_1 = User("001", "angela")
user_2 = User("002", "jack")

user_1.follow(user_2)
print(user_1.followers)
print(user_1.following)
print(user_2.followers)
print(user_2.following)

```

## Day 16 - OOP Coffee Machine

Code here: [oop-coffee-machine](https://replit.com/@maryletteroa/oop-coffee-machine)

This day was a bit more challenging. But I've ventured into the Intermediate level so 🙌. Between going over the stub code and reading the documentation, there were a few snags. But the main program looks clean with the help of Python classes.

There's this article about the [Four Programming Styles in Python](https://newrelic.com/blog/nerd-life/python-programming-styles):

1. Functional
2. Imperative
3. Object-oriented
4. Procedural

When I work, I tend to use 1, 2, and 4, and seldom object-oriented. Today (and until September/October this year 2021), we are learning about [web development using Django in WWCode Manila](https://wwcodemanila.github.io/WWCodeManila-Python/#/django/01_introduction). The codes are heavily OOP because we are using a framework. 

So, this lesson and a few more after this, is something that I look forward to. There is also an element of code design which is fun.

## Day 15 - Coffee Machine

Get your own coffee here ☕: [coffee-machine](https://replit.com/@maryletteroa/coffee-machine)

Imagine the amount of coffee I ordered to get this to work. Had a hard time ordering "cappuccino" since the spelling is difficult (I then added a condition). I thought about being in a real café -- what would the transactions be -- and wrote that in the code.

Ahh 💭 good times.

## Day 14 - Higher-lower

Play my solution 🎮: [higher-lower](https://replit.com/@maryletteroa/higher-lower)

⚠ Might need to refactor this code. Was so sleepy when I wrote this.

## Day 13 - Debugging

🐞🚫 Tips: 
1. Describe the problem, challenge your assumptions!
2. Reproduce the error, notice when it happens! See if the code can be changed so it reproduces the error.
3. Play computer. Evaluate each line to figure out the problem.
4. Fix the erros as they come. Watch out the red underlines. Watch out for silent errors.
5. Use your friend `print()`
6. Use a debugger e.g. [Python Tutor](http://www.pythontutor.com/visualize.html#mode=edit)
7. Take a break. 😴
8. Ask a real human friend (not `print()`).
9. Run your code often. Confirm that the code runs like it's intended.
10. Ask StackOverflow (other developers) but only if you think that the bug is unique. Otherwise, check existing solutions.

☝ The more bugs you solve, the better you get at it.


## Day 12 - Guess the number

Play my solution 🎮: [guess the number](https://replit.com/@maryletteroa/guess-the-number)

Today's topic is scope: Global, local, block (same as enclosed scope?).

See Figures [1](https://res.cloudinary.com/dyd911kmh/image/upload/f_auto,q_auto:best/v1588956604/code_dmeddc.png) & [2](https://res.cloudinary.com/dyd911kmh/image/upload/f_auto,q_auto:best/v1588956604/Scope_fbrzcw.png).

1. Using and not using `global`
    ```py
    enemies = 1
    def increase_enemies():
       global enemies
       enemies +=1
       return enemies

    print(increase_enemies())
    ```
    ```py
    enemies = 1
    def increase_enemies():
         return enemies + 1
    enemies = increase_enemies()
    ```
    For the first version of the code, I was able to use `global` but final version went for a functional code which looks like the second one. Because of enclosed scoping, I cannot call the variable out of a nested function.

2. Constants written in capital letters. 👈 Something that still does not come to me automatically.
    ```py
    PI = 3.14159
    URL = "google.com"
    ```

3. [ASCII fonts](http://patorjk.com/software/taag/#p=display&f=Graffiti&t=Guess%20the%20number) 👍


4. ✨Functional coding✨, and writing Docstrings!


## Day 11 (Capstone) - Blackjack

Play my solution 🎮: [blackjack](https://replit.com/@maryletteroa/blackjack)

<iframe
    src="https://replit.com/@maryletteroa/blackjack?embed=True&outputonly=1"
    style="width:600px; height:400px;"
></iframe>

You win if you score 21 or closer to 21 than the dealer. You lose if you score over 21. Full game rules are [here](https://bicyclecards.com/how-to-play/blackjack/). In this version, the deck is infinite.

1. Sample without replacement:

    ```python
    random.sample(seq, n)
```
2. Difference between append and extend:
    - both add to the end of a list, but e.g. given a list `l = [1,2]`
    - `l.append([3]])` adds the object as is e.g. `[1,2,[3]]`
    - `l.extend(3)` unpacks the object and will result in `[1,2,3]`
    - `.extend()` only accepts iterables

    In the code I used `.extend()` to add a card since the result of `random.sample(seq,n)` from a list is a list.

3. While loops, should still be wary of while loops! 

4. Formulating the `evaluation` function (if/else statements) to decide the game was nuanced.


## Day 10 - Calculator
 💡 Functions inside dictionaries.

The functions:
```py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

```
The dictionary:
```py
operators = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}
```

Finally, calling the functions
```py
result = operators[operator](a, b)
```

## Day 9 - Blind auction

## Day 8 - Caesar cipher

TIL That Caesar was into ciphers!

## Day 7 - Hangman

Importing from an external python code

```py
from hangman_art import stages, logo
from hangman_words import word_list
```

and using them inside the code 

```py
print(logo)
print(stages[lives])
chosen_word = random.choice(word_list)
```

## Day 6 - Reeborg Maze

The [Reeborg's World](https://reeborg.ca/reeborg.html) website fun coding puzzles! 🤖

## Day 5 - Password generator

## Day 4 - Rock paper scissors

## Day 3 - Treasure Island

[Asci art ](https://ascii.co.uk/art) 🎨

```sh
    ___ __ 
   (_  ( . ) )__                  '.    \   :   /    .'
     '(___(_____)      __           '.   \  :  /   .'
                     /. _\            '.  \ : /  .'
                .--.|/_/__      -----____   _  _____-----
_______________''.--o/___  \_______________(_)___________
       ~        /.'o|_o  '.|  ~                   ~   ~
  ~            |/    |_|  ~'         ~
               '  ~  |_|        ~       ~     ~     ~
      ~    ~          |_|O  ~                       ~
             ~     ___|_||_____     ~       ~    ~
   ~    ~      .'':. .|_|A:. ..::''.
             /:.  .:::|_|.\ .:.  :.:\   ~
  ~         :..:. .:. .::..:  .:  ..:.       ~   ~    ~
             \.: .:  :. .: ..:: .lcf/
    ~      ~      ~    ~    ~         ~
               ~           ~    ~   ~             ~
        ~         ~            ~   ~                 ~
   ~                  ~    ~ ~                 ~

```

## Day 2 - Tip calculator

## Day 1 - Band name generator