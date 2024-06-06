#!/bin/python3

from turtle import position
import pyautogui as pagui
from random import randint
import win32api
import time

def click(x, y, delay_ms=0, move_first=True):
    while delay_ms > 0:
        delay_ms -= 1000
        time.sleep(1)
    if move_first:
        pagui.move(x, y)
    pagui.click(x, y)

def record_click_sequence():
    positions = []
    state_left = win32api.GetKeyState(0x01)
    state_right = win32api.GetKeyState(0x02)
    try:
        while True:
            a = win32api.GetKeyState(0x01)
            b = win32api.GetKeyState(0x02)
            if a != state_left:  # Button state changed
                state_left = a
                if a < 0:
                    position = win32api.GetCursorPos()
                    print('Adding', position, 'to queue')
                    positions.append(position)
                else:
                    pass

            if b != state_right:  # Button state changed
                pass
                state_right = b
                if b < 0:
                    print('Right Button Pressed')
                else:
                    print('Right Button Released')
            time.sleep(0.001)
    except KeyboardInterrupt:
        print("Ctrl+C pressed, stopped recording")
    return positions
        
try:
    print("Recording clicks")
    positions = record_click_sequence()
    assert len(positions) > 0
    print("Positions to click", positions)
    counter = 0
    while True:
        delay = randint(2, 10)
        print("Sleeping for %s seconds and then clicking (%d, %d) now."%(delay, positions[counter][0], positions[counter][1]))
        click(positions[counter][0], positions[counter][1], delay*1000)
        counter = (counter+1)%len(positions)
except AssertionError:
    print("No clickes were recorded")
except KeyboardInterrupt:
    print("Ctrl+C pressed, stopping the loop")
