---
layout: post
title: PyAutoGUI
categories: [learning-log]
tags: [python]
---

This is an extension of my [2025 Learning Log]({% link _posts/2025-01-24-2025-learning-log.md %}). 


> PyAutoGUI lets your Python scripts control the mouse and keyboard to automate interactions with other applications. [PyAutoGUI Docs](https://pyautogui.readthedocs.io/en/latest/)

Install `pip install pyautogui`

## Mouse functions
```python
import pyautogui

# screen resolution
print(pyautogui.size())
# current position of the mouse
print(pyautogui.position())
# move to (100,100) position in 3 seconds
pyautogui.moveTo(100, 100, 3)
# move to relative position
pyautogui.moveRel(100, 100, 3)
# move to (500,500) twice in 3 seconds
pyautogui.click(500, 500, 2, 3, button="left")
# other click functions
pyautogui.leftClick()
pyautogui.doubleClick()
pyautogui.tripleClick()

# lift mouse up go to (100,100)
pyautogui.mouseUp(100, 100, button="left")
# hold down mouse using left button go to (500,100)
pyautogui.mouseDown(500, 100, button="left")

```

## Scroll functions
```python
# scroll 500 px up
pyautogui.scroll(500)
# scroll 500 px down
pyautogui.scroll(-500)
```

## Failsafe
- scroll to the corner of the screen to trigger Fail Safe
- tip: add `time.sleep(n)` to have n seconds to move the mouse to the Fail safe position

## Keyboard functions

```python
pyautogui.write("hello") # hello
pyautogui.press("enter") # will press enter button
pyautogui.press("space") # will press space button
```
More functionalities in the [docs](https://pyautogui.readthedocs.io/en/latest/)

## Resources
- [Python Automation with PyAutoGUI](https://www.youtube.com/watch?v=3PekU8OGBCA&t=1011s)
- [PyAutoGUI Docs](https://pyautogui.readthedocs.io/en/latest/)
