import kivy
kivy.require('1.10.0')
import math
from random import randint, shuffle
from functools import partial
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.logger import Logger
from kivy.uix.popup import Popup
import kivy.resources
kivy.resources.resource_add_path('.')

def shuffleChoice(choice):
    # shuffle the list in place and return the index of the true answer
    correct = choice[0]
    shuffle(choice)
    for i, c in enumerate(choice):
        if c == correct:
            Logger.info('{}, {}'.format(i, c))
            return i
