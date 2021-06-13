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

4. Formulating the evaluation (if/else statements) to decide the game was tough!


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