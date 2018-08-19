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

special_locations = {'起點', '機會'}
school_locations = ['起點', '校門口', 'N號館', '傅鐘', '校史館', '行政大樓', '文學院', '機會', 
'溫州街', '社科院', '小福', '工綜', '農業陳列館', '醉月湖', '水源校區', '機會', '法學院', '活大', 
'118巷', '機會', '土木系館', '總圖', '機會', '教學館', '城中校區', '體育館', '公館商圈', 
'桃花心木道', '學生宿舍', '椰林小舖', '機會', '二活', '小小福', '舟山路', '臺大農場', '實驗林場']
default_font = 'data/HuaKangTiFan-CuTi-1.otf'
colors = [(0.474, 0.874, 0.803, 1), (1, 0.752, 0.752, 1), (1, 0.921, 0.686, 1), 
        (0.862, 0.772, 0.933, 1), (1, 0.733, 0.552 ,1), (0.6, 0.756, 0.886, 1)]
questions = {}
domination_status_map = []
domination_status_loc = []

def shuffleChoice(choice):
    # shuffle the list in place and return the index of the true answer
    correct = choice[0]
    shuffle(choice)
    for i, c in enumerate(choice):
        if c == correct:
            print('{}, {}'.format(i, c))
            return i

def auto_close(my_callback, sec):
    Clock.schedule_once(my_callback, sec)

def get_player_loc(player_id, block_id):
    x = grid_constants.grid_loc[block_id]['x'] + grid_constants.player_offset[player_id]['x']
    y = grid_constants.grid_loc[block_id]['y'] + grid_constants.player_offset[player_id]['y']
    return {'x': x, 'y': y}

def get_block_loc(block_id):
    x = grid_constants.grid_loc[block_id]['x']
    y = grid_constants.grid_loc[block_id]['y']
    return {'x': x, 'y': y}

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
            print('{} is dominated by team {}'.format(self.location_name, self.dominator))
        return [self.dominator, self.status, self.id]

class PlayerChess(Widget):
    color = ListProperty()
    rel_pos = ObjectProperty({'x': 0, 'y': 0})
    source = StringProperty()
    def move(self):
        pass

class BlockStatus(Widget):
    color = ListProperty([1, 1, 1, 0])
    rel_pos = ObjectProperty({'x': 0, 'y': 0})
    source_img = StringProperty('')
    def update(self):
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
            #'carry': False,
            'free_land': False,
            'TA_help': False, 
            'permanent_domination': False,
            'bike': False,
            'bike_stolen': False,
            'skip': False,
            'allpass': False,
            'one_step': False,
            'sanbao': False,
            'go_to_start': False,
            'thunder': False,
            'retake': False,
            'early_grad': False,
            'angry_prof': False,
            'yellow_ribbon': False
        }
    def __str__(self):
        return str((self.id, self.current_location, self.score))
    def __repr__(self):
        return str((self.id, self.current_location, self.score))

class Board(object):
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
        print(self.players)

    def move_chess_directly(self, player_id, loc):
        # player on old block leave
        self.blocks[self.players[player_id].current_location].current_player.remove(player_id)
        self.players[player_id].current_location = loc
        # player arrive on new block
        self.blocks[self.players[player_id].current_location].current_player.add(player_id)
        print(self.players)
    
    def updateScore(self):
        for player in self.players:
            player.score = 0
        for blk in self.blocks:
            self.players[blk.dominator].score += blk.status
        for i in self.players:
            print(i)
        
    def thunder(self, id):
        # remove one of non-perment domination location from team id
        possible_locs = [x for x in self.blocks if x.dominator==id and x.status<3]
        if len(possible_locs)==0:
            return '第{}隊沒有可以被雷的地點QQ'.format(id+1)
        else:
            loc = choice(possible_locs)
            loc.dominator = -1
            loc.status = 0
            return '第{}隊失去佔領{}'.format(id+1, loc.location_name)

def pick_question_set(questions, location):
    '''
        questions are dic of location:[question sets]
        return a question set of that location
    '''
    ret = questions[location]
    print(location+' remain '+str(len(ret)))
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
        #'carry': '凱瑞組員:\n遇到菩薩下凡普渡了！，獲得答題pass卡，下次答題時可交給任一同隊隊友答題，下次作答時使用。',
        'free_land': '免修大一英文:\n不用修大一英文還能拿學分A_A，下次到地點時不用答題即可佔領該地',
        'TA_help': '助教幫幫忙:\n助教才是成績的關鍵！請隊輔答題。指定任意隊輔幫任意隊伍下次抵達景點或是對決時答題，被指定隊伍及隊輔不得拒絕。',
        'permanent_domination': '免修:\n永久佔領隨機一塊已被隊伍佔領的土地',
        'bike': '腳踏車:\n腳踏車在手，天下任我走，此回合任意移動到喜歡的土地上(然後進行答題或是對決，依抵達的景點而異)',
        'bike_stolen': '腳踏車被偷:\n身為台大人，腳踏車被偷已經見怪不怪ˊ_>ˋ，下一回合移動格數為骰子點數的一半，採無條件捨去法，擲到1不前進',
        'skip': '停修死線到，期中考太差，不停修會被當QQ\n暫停移動一回合',
        'allpass': '歐趴糖:\n下次答題無條件答對，也會在對決時發動',
        'one_step': '早八聯發:\n因為太早起床精神不濟血壓過低沒有力氣，下一回合只能移動一格',
        'sanbao': '三寶出沒，生人迴避!:\n在椰林大道上被九十度轉彎又不看後方來車的三寶撞QQ，指定一個隊伍暫停一回合',
        'go_to_start': '重考:\n明年指考等你喔~直接回到起點',
        'thunder': '雷組員:\n雷隊友雷到我一個外焦內嫩、心力交瘁、生無可戀......指定一個隊伍失去一個隨機非永久佔領地點(直接指定並使用)',
        'retake': '重修:\n下次會更好，再抽一張機會命運',
        'early_grad': '提早畢業:\n學霸如我早早就修完畢業學分了，下回合前進骰子次數*2',
        'angry_prof': '得罪教授！\n說教授壞話被教授聽到，必修直接被當，下一回合就算答題正確，也無法占領該地點',
        'yellow_ribbon': '黃絲帶運動:\n黃絲帶運動怎樣我不知道啦，我只知道我趕課被堵住了！暫停移動一回合'
    }
    if card in description.keys():
        return description[card]
    else:
        return 'card description not exist!'

def init_domination_status():
    print('init domination status')
    for idx in range(len(school_locations)):
        ds_tmp = BlockStatus(id='ds_{}'.format(idx))
        ds_tmp.rel_pos = get_block_loc(idx)
        ds_tmp2 = BlockStatus(id='ds_{}'.format(idx))
        ds_tmp2.rel_pos = get_block_loc(idx)
        domination_status_map.append(ds_tmp)
        domination_status_loc.append(ds_tmp2)
    
def update_domination_status_on_map():
    for id, blk in enumerate(gameboard.blocks):
        dominator = blk.dominator
        status = blk.status
        if dominator != -1:
            domination_status_map[id].color = colors[dominator]
            domination_status_map[id].source_img = ('data/images/domination_status{}_{}.png'.format(dominator, status))
            domination_status_loc[id].color = colors[dominator]
            domination_status_loc[id].source_img = ('data/images/domination_status{}_{}.png'.format(dominator, status))
        else:
            domination_status_map[id].color = (1, 1, 1, 0)
            domination_status_map[id].source_img = ('')
            domination_status_loc[id].color = (1, 1, 1, 0)
            domination_status_loc[id].source_img = ('')

gameboard = Board(school_locations)
