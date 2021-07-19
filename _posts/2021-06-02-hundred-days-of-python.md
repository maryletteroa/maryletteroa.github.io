---
layout: post
title: 100 Days of Code
categories:
- project
---

<!-- I've finally gotten around to doing the 100 Days of Code Challenge. This was popular a few years back, and as usual, I caught up with the trend just now. 😅 
 -->
This journey is based on the Udemy course [100 Days of Code - The Python Pro Bootcamp](https://www.udemy.com/course/100-days-of-code/) by Dr. Angela Yu.

My code repo is here 👉: [100DaysOfCode-Python](https://github.com/maryletteroa/100DaysOfCode-Python)

I document my progress in this post: programming tasks, and notes about things that made an impression.


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
 - [Sheety](sheety.co)

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