#!/bin/python3

from turtle import position
import pyautogui as pagui
from random import randint
import win32api
import time
import sys

def print_help():
    print("""
Clicker - Mouse Click Automation Script

Usage:
    python main.py [OPTIONS]

Options:
    -h, --help              Show this help message and exit
    -t, --terminate SECONDS Terminate the script after SECONDS seconds

Instructions:
    1. Run the script.
    2. Left-click to record positions (each click is saved).
    3. Press Ctrl+C to stop recording and start the auto-clicker.
    4. The script will click the recorded positions in a loop with random delays.

Example:
    python main.py --terminate 60
    """)

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
    termination_time = float('inf')
    args = sys.argv[1:]
    if len(args) > 0:
        if  (args[0] == "--terminate" or args[0] == "-t"):
            try:
                termination_time = int(args[1])
                print("Script will terminate after %d seconds"%termination_time)
            except (ValueError, IndexError):
                print("Invalid argument for --terminate, expected an integer value")
                print_help()
                sys.exit(1)
        if (args[0] == "--help" or args[0] == "-h"):
            print_help()
            sys.exit(0)
    print("Recording clicks") 
    positions = record_click_sequence()
    assert len(positions) > 0
    print("Positions to click", positions)
    counter = 0
    total_time_slept = 0
    while True:
        delay = randint(2, 10)
        total_time_slept += delay
        print("Sleeping for %s seconds and then clicking (%d, %d) now."%(delay, positions[counter][0], positions[counter][1]))
        click(positions[counter][0], positions[counter][1], delay*1000)
        if total_time_slept >= termination_time:
            print("Total time slept exceeded the termination time, exiting!")
            break
        counter = (counter+1)%len(positions)
except AssertionError:
    print("No clickes were recorded")
except KeyboardInterrupt:
    print("Ctrl+C pressed, stopping the loop")
