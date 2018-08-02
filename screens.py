# -*- coding: utf-8 -*-
from utils import *
from question_screen import QuestionScreen
from dual_screen import DualScreen
from map_screen import MapScreen
from chance_screen import ChanceScreen
from location_screen import LocationScreen
from chance_choose_team_screen import ChanceChooseTeamScreen

class CorrectAnswerScreen(Screen):
    description = StringProperty()
    def __init__(self, **kwargs):
        super(CorrectAnswerScreen, self).__init__(**kwargs)
    
    def callback(self):
        Logger.info(self.description)
        self.manager.current = 'result'

class WrongAnswerScreen(Screen):
    show_result = False
    correct_answer = StringProperty()
    description = StringProperty()
    def __init__(self, **kwargs):
        super(WrongAnswerScreen, self).__init__(**kwargs)
    
    def callback(self):
        if self.show_result:
            Logger.info(self.description)
            self.show_result = False
            self.manager.current = 'result'
        else:
            Logger.info(self.description)
            self.manager.get_screen('map').enter()
            self.manager.current = 'map'

class TitleScreen(Screen):
    def __init__(self, **kwargs):
        super(TitleScreen, self).__init__(**kwargs)
    
    def gotoInfo(self):
        self.manager.current = 'info'
    
    def startGame(self):
        self.manager.current = 'map'
        self.manager.get_screen('map').enter()

class InfoScreen(Screen):
    def __init__(self, **kwargs):
        super(InfoScreen, self).__init__(**kwargs)

    def goback(self):
        self.manager.current = 'title'
    
    def startGame(self):
        self.manager.current = 'map'
        self.manager.get_screen('map').enter()

class ResultScreen(Screen):
    player = NumericProperty()
    action = StringProperty()
    location = StringProperty()
    score = NumericProperty()
    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
    
    def update(self, result):
        # result: [player, status, locationId]
        gameboard.updateScore()
        if result[1] == 1:
            self.action = '佔領'
        elif result[1] == 2:
            self.action = '衛冕'
        elif result[1] == 3:
            self.action = '永久佔領'
        self.player = result[0]
        self.location = school_locations[result[2]]
        self.score = gameboard.players[self.player].score
    
    def callback(self):
        self.manager.get_screen('map').enter()
        self.manager.current = 'map'

class EndScreen(Screen):
    background_color = ObjectProperty()
    background_color = colors
    score1 = NumericProperty()
    score2 = NumericProperty()
    score3 = NumericProperty()
    score4 = NumericProperty()
    score5 = NumericProperty()
    score6 = NumericProperty()
    def __init__(self, **kwargs):
        super(EndScreen, self).__init__(**kwargs)
    
    def on_enter(self):
        gameboard.updateScore()
        self.score1 = gameboard.players[0].score
        self.score2 = gameboard.players[1].score
        self.score3 = gameboard.players[2].score
        self.score4 = gameboard.players[3].score
        self.score5 = gameboard.players[4].score
        self.score6 = gameboard.players[5].score
    
    def callback(self):
        self.manager.current = 'map'