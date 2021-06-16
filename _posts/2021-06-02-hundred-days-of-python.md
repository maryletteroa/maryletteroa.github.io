---
layout: post
title: 100 Days of Code
categories:
- project
---

I've finally gotten around to doing the 100 Days of Code Challenge. This was popular a few years back, and as usual, I caught up with the trend just now. 😅 

I'm following the Udemy course [100 Days of Code - The Python Pro Bootcamp](https://www.udemy.com/course/100-days-of-code/) by Dr. Angela Yu.

My code repo is here 👉: [100DaysOfCode-Python](https://github.com/maryletteroa/100DaysOfCode-Python)

I document my progress in this post: programming tasks, and notes about things that made an impression.

#### Day 14 - Higher-lower

Play my solution 🎮: [higher-lower](https://replit.com/@maryletteroa/higher-lower)

⚠ Might need to refactor this code. Was so sleepy when I wrote this.

#### Day 13 - Debugging

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


#### Day 12 - Guess the number

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


#### Day 11 (Capstone) - Blackjack

Play my solution 🎮: [blackjack](https://replit.com/@maryletteroa/blackjack)

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


#### Day 10 - Calculator
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

#### Day 9 - Blind auction

#### Day 8 - Caesar cipher

TIL That Caesar was into ciphers!

#### Day 7 - Hangman

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

#### Day 6 - Reeborg Maze

The [Reeborg's World](https://reeborg.ca/reeborg.html) website fun coding puzzles! 🤖

#### Day 5 - Password generator

#### Day 4 - Rock paper scissors

#### Day 3 - Treasure Island

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

#### Day 2 - Tip calculator

#### Day 1 - Band name generator