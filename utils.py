import kivy
kivy.require('1.10.0')
import math, time
from random import randint, shuffle, choice
from functools import partial
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.logger import Logger
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.clock import Clock
import kivy.resources
import grid_constants
kivy.resources.resource_add_path('.')

school_locations = ['起點', '校門口', 'N號館', '傅鐘', '校史館', '行政大樓', '文學院', '機會', 
'溫州街', '社科院', '小福', '工綜', '農業陳列館', '醉月湖', '水源校區', '機會', '法學院', '活大', 
'118巷', '機會', '土木系館', '總圖', '機會', '教學館', '城中校區', '體育館', '公館商圈', 
'桃花心木道', '學生宿舍', '椰林小舖', '機會', '二活', '小小福', '舟山路', '臺大農場', '實驗林場']
default_font = 'data/DroidSansFallback.ttf'
colors = [(0.474, 0.874, 0.803, 1), (1, 0.752, 0.752, 1), (1, 0.921, 0.686, 1), 
        (0.862, 0.772, 0.933, 1), (1, 0.733, 0.552 ,1), (0.6, 0.756, 0.886, 1)]
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

class PlayerChess(Widget):
    color = ListProperty()
    rel_pos = ObjectProperty({'x': 0, 'y': 0})

    def move(self):
        pass

class player(object):
    id = -1
    current_location = -1
    score = 0
    def __init__(self, i):
        self.id = i
        self.color = colors[self.id]
        self.current_location = 0
        self.card = {
            'bonus_time': False,
            'prior': False,
            'carry': False,
            'free_land': False,
            'TA_help': False, 
            'permanent_domination': False,
            'bike': False
        }
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

    def move_chess_directly(self, player_id, loc):
        # player on old block leave
        self.blocks[self.players[player_id].current_location].current_player.remove(player_id)
        self.players[player_id].current_location = loc
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

def get_player_loc(player_id, block_id):
    x = grid_constants.grid_loc[block_id]['x'] + grid_constants.player_offset[player_id]['x']
    y = grid_constants.grid_loc[block_id]['y'] + grid_constants.player_offset[player_id]['y']
    return {'x': x, 'y': y}

def pick_question_set(questions, location):
    '''
        questions are dic of location:[question sets]
        return a question set of that location
    '''
    ret = questions[location]
    Logger.info(location+' remain '+str(len(ret)))
    if len(ret) > 0:
        return ret, location
    else:
        q_cnt = 0
        for i in questions.keys():
            q_cnt += len(questions[i])
        if q_cnt == 0:
            return ret, location
        new_loc = choice(list(questions.keys()))
        while len(questions[new_loc]) == 0:
            new_loc = choice(list(questions.keys()))
        ret = questions[new_loc]
        return ret, new_loc

def chance_card_description(card):
    description = {
        'bonus_time': '共筆助攻:\n有了共編，期中期末考就有希望！下次答題免費延長20秒答題',
        'prior': '對面的sorry:\n下次對決時，獲得優先答題的機會',
        'carry': '凱瑞組員\n遇到菩薩下凡普渡了！，獲得答題pass卡，下次答題時可交給任一同隊隊友答題，下次作答時使用。',
        'free_land': '免修大一英文\n不用修大一英文還能拿學分A_A，下次到地點時不用答題即可佔領該地',
        'TA_help': '助教幫幫忙\n助教才是成績的關鍵！請隊輔答題。指定任意隊輔幫任意隊伍下次抵達景點或是對決時答題，被指定隊伍不得拒絕。',
        'permanent_domination': '免修\n永久佔領隨機一塊已被隊伍佔領的土地',
        'bike': '腳踏車\n腳踏車在手，天下任我走，此回合任意移動到喜歡的土地上(然後進行答題或是對決，依抵達的景點而異)'
    }
    if card in description.keys():
        return description[card]
    else:
        return 'card description not exist!'

gameboard = board(school_locations)