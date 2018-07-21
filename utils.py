import kivy
kivy.require('1.10.0')
import math, time
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
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.logger import Logger
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.clock import Clock
import kivy.resources
kivy.resources.resource_add_path('.')

school_locations = ['起點', '校門口', 'N號館', '傅鐘', '校史館', '行政大樓', '文學院', '機會', 
'溫州街', '社科院', '小福', '工綜', '農業陳列館', '醉月湖', '水源校區', '機會', '法學院', '活大', 
'118巷', '機會', '土木系館', '總圖', '機會', '教學館', '城中校區', '體育館', '公館商圈', 
'實驗林場', '臺大農場', '舟山路', '小小福', '二活', '機會', '椰林小舖', '宿舍區', '桃花心木道']
default_font = 'data/DroidSansFallback.ttf'
colors = [(1, 0, 0, 1), (1, 1, 0, 1), (0, 1, 0, 1), (0, 1, 1, 1), (0, 0, 1 ,1), (1, 0, 1, 1)]
questions = {}

def shuffleChoice(choice):
    # shuffle the list in place and return the index of the true answer
    correct = choice[0]
    shuffle(choice)
    for i, c in enumerate(choice):
        if c == correct:
            Logger.info('{}, {}'.format(i, c))
            return i

def auto_close(my_callback, sec):
    Clock.schedule_once(my_callback, sec)

class block(object):
    location_name = ''
    id = -1
    current_player = set()
    dominator = -1
    status = 0
    def __init__(self, i, name):
        self.id = i
        self.location_name = name
    
    def update(self, player_id):
        if self.dominator==player_id and self.status<3:
            self.status += 1
            if self.status == 3:    # dominated
                #self.status = 100
                pass
        elif self.status != 3:
            self.dominator = player_id
            self.status = 1
        else:
            Logger.info('{} is dominated by team {}'.format(self.location_name, self.dominator))
        return [self.dominator, self.status, self.id]

class player(object):
    id = -1
    current_location = -1
    score = 0
    def __init__(self, i):
        self.id = i
        self.color = colors[self.id]
        self.current_location = 0
    def __str__(self):
        return str((self.id, self.current_location, self.score))
    def __repr__(self):
        return str((self.id, self.current_location, self.score))

class board(object):
    blocks = []
    players = []
    def __init__(self, locations):
        for i, loc in enumerate(locations):
            self.blocks.append(block(i, loc))
            for j in range(6):  # all player at starting point
                self.blocks[0].current_player.add(j)
        for i in range(6):
            self.players.append(player(i))

    def move_chess(self, player_id, moves):
        # player on old block leave
        self.blocks[self.players[player_id].current_location].current_player.remove(player_id)
        self.players[player_id].current_location += moves
        self.players[player_id].current_location %= len(self.blocks)
        # player arrive on new block
        self.blocks[self.players[player_id].current_location].current_player.add(player_id)
        Logger.info(self.players)
    
    def updateScore(self):
        for player in self.players:
            player.score = 0
        for blk in self.blocks:
            self.players[blk.dominator].score += blk.status
        for i in self.players:
            Logger.info(i)


gameBroad = board(school_locations)