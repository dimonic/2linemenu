#!/usr/bin/python

import math
import time

import Adafruit_CharLCD as LCD

lcd = LCD.Adafruit_CharLCDPlate()

buttons = ( (LCD.SELECT,    'Select', (1, 1, 1)),
            (LCD.LEFT,      'Left', (1, 0, 0)),
            (LCD.UP,        'Up',   (0, 0, 1)),
            (LCD.DOWN,      'Down', (0, 1, 0)),
            (LCD.RIGHT,     'Right',(1, 0, 1)) )

menu_data = ['File',
                ['New', 'Open', 'Close', 'Save', 'Quit'],
            'Edit',
                ['Undo', 'Redo', 'Cut', 'Copy', 'Paste', 'Delete'],
            'Help',
                ['Menu help', 'About menu']
            ]
class Menu:
    def __init__(self, data = []):
        self.data = data
        self.selection = [-1, 0]
        self.show_selection()

    # to show a list as a string, with the selection first
    def list_to_string(self, l, sel):
        s = ""
        for index in range(sel, len(l)):
            s = s + l[index] + ' '
        for index in range(0, sel - 1):
            s = s + l[index] + ' '
        return s

    def get_selection(self):
        if self.selection[0] == -1:             # at top level
            print "Getting selection at top level"
            s = self.data[self.selection[1] * 2]
        else:
            print "getting selection at submenu [", self.selection[0], "][", self.selection[1], "]"
            s = self.data[self.selection[0] + 1][self.selection[1]]
        return s

    def top_level_string(self):
        s = ""
        tl_menus = len(self.data)
        for c in range(self.selection[1] * 2, tl_menus, 2):
            s = s + " " + self.data[c]
        for c in range(0, self.selection[1] * 2, 2):
            s = s + " " + self.data[c]
        return s

    def show_selection(self):
        lcd.clear()
        print "selection[0] = ", self.selection[0]
        if self.selection[0] == -1:
            lcd.message("=> " + self.data[self.selection[1] * 2] + "\n" + self.top_level_string())
        elif isinstance(self.data[self.selection[0] * 2], str):
            if isinstance(self.data[self.selection[0] * 2 + 1], list):
                lcd.message(self.data[self.selection[0] * 2] + ' => ' + self.data[self.selection[0] * 2 + 1][self.selection[1]] + "\n" + self.list_to_string(self.data[self.selection[0] * 2 + 1], self.selection[1]))
            else:
                lcd.message(self.data[self.selection[0]] )

    def process_button(self):
        retval = True
        if lcd.is_pressed(LCD.SELECT):
            print "Select button pressed"
            print m.get_selection()
            exit()
        elif lcd.is_pressed(LCD.UP):
            print "Up button pressed"
            if self.selection[0] != -1:
                self.selection[0] -= 1
                self.selection[1] = 0
        elif lcd.is_pressed(LCD.DOWN):
            print "Down button pressed"
            if self.selection[0] == -1:
                self.selection[0] = self.selection[1]
                self.selection[1] = 0
        elif lcd.is_pressed(LCD.LEFT):
            print "Left button pressed"
            if self.selection[1] > 0:
                self.selection[1] -= 1
            else:
                if self.selection[0] == -1:
                    s = len(self.data) / 2
                else:
                    s = len(self.data[self.selection[0] + 1])
                self.selection[1] = s - 1
        elif lcd.is_pressed(LCD.RIGHT):
            print "Right button pressed"
            if self.selection[0] == -1:
                s = len(self.data) / 2
            else:
                s = len(self.data[self.selection[0] + 1])
            if (self.selection[1] + 1) < s:
                self.selection[1] += 1
            else:
                self.selection[1] = 0
        else:
            retval = False
        return retval

m = Menu(menu_data)

print 'Press Ctrl-C to quit.'
while True:
    # loop through each button to see if it was pressed
    if m.process_button() == True:
        m.show_selection()
        time.sleep(1)
