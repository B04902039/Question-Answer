# -*- coding: utf-8 -*-
from utils import *
from question_screen import QuestionScreen
from dual_screen import DualScreen
from map_screen import MapScreen

class LocationScreen(Screen):
    '''
        location screen (deprecated feature)
        select the location and switch the questions screen
    '''
    def __init__(self, **kwargs):
        super(LocationScreen, self).__init__(**kwargs)
    # create button dynamically according to locations in csv
    def create_button(self):
        layout = GridLayout(cols=2, padding=50, spacing=1)
        for i in questions.keys():
            tmp = Button(text=i, font_name=default_font)
            tmp.bind(on_release=partial(self.select_loc, i))
            layout.add_widget(tmp)
        self.add_widget(layout)

    def select_loc(self, loc, instance):
        self.manager.get_screen('question').loc = loc
        self.manager.get_screen('question').update()
        self.manager.transition.direction = 'right'
        self.manager.current = 'question'

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
        gameBroad.updateScore()
        if result[1] == 1:
            self.action = '佔領'
        elif result[1] == 2:
            self.action = '衛冕'
        elif result[1] == 3:
            self.action = '永久佔領'
        self.player = result[0]
        self.location = school_locations[result[2]]
        self.score = gameBroad.players[self.player].score
    
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
        self.score1 = gameBroad.players[0].score
        self.score2 = gameBroad.players[1].score
        self.score3 = gameBroad.players[2].score
        self.score4 = gameBroad.players[3].score
        self.score5 = gameBroad.players[4].score
        self.score6 = gameBroad.players[5].score
    
    def callback(self):
        self.manager.current = 'map'