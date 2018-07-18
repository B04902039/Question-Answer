# -*- coding: utf-8 -*-
from utils import *

school_locations = ['校門口', '行政大', '校史館', '文學院', '土木系館', '活大', '農業陳列館', '小福', 
'教學館', '小小福', '椰林小舖', '醉月湖', '臺大農場', '社科院', '總圖', '法學院', '工綜', '二活', 
'桃花心木道', '體育館', '118巷', '溫州街', '公館商圈', '水源校區', '城中校區', '舟山路', '學生宿舍', 
'N號館', '實驗林場']
questions={}

class LocationScreen(Screen):
    def __init__(self, **kwargs):
        super(LocationScreen, self).__init__(**kwargs)
    
    def create_button(self):
        layout = GridLayout(cols=2, padding=50, spacing=1)
        for i in questions.keys():
            tmp = Button(text=i, font_name='data/DroidSansFallback.ttf')
            tmp.bind(on_release=partial(self.select_loc, i))
            layout.add_widget(tmp)
        self.add_widget(layout)

    def select_loc(self, loc, instance):
        self.manager.get_screen('question').loc = loc
        self.manager.get_screen('question').update()
        self.manager.transition.direction = 'right'
        self.manager.current = 'question'

class QuestionScreen(Screen):
    current_ques = ObjectProperty()
    correct_id = NumericProperty()
    loc = StringProperty()
    Qs = StringProperty()
    c1 = StringProperty()
    c2 = StringProperty()
    c3 = StringProperty()
    c4 = StringProperty()
    description = StringProperty()
    def __init__(self, **kwargs):
        super(QuestionScreen, self).__init__(**kwargs)

    def update(self):
        tmp = questions[self.loc]
        if len(tmp) == 0:
            self.Qs = self.c1 = self.c2 = self.c3 = self.c4 = 'Out of questions'
        else:
            #Logger.info(tmp)
            idx = randint(0, len(tmp)-1)
            self.Qs = tmp[idx][0]
            self.current_ques = tmp[idx][1:5]
            self.description = tmp[idx][-1]
            self.manager.get_screen('correctAnswer').description = self.description
            self.manager.get_screen('wrongAnswer').description = self.description
            self.correct_id = shuffleChoice(self.current_ques)
            self.c1 = self.current_ques[0]
            self.c2 = self.current_ques[1]
            self.c3 = self.current_ques[2]
            self.c4 = self.current_ques[3]
            global questions    # question asked, delete it
            questions[self.loc].remove(questions[self.loc][idx])

    def callback(self, id):
        if id == self.correct_id:
            self.manager.get_screen('correctAnswer').description = self.description
            self.manager.transition.direction = 'up'
            self.manager.current = 'correctAnswer'
        else:
            self.manager.get_screen('wrongAnswer').description = self.description
            self.manager.transition.direction = 'down'
            self.manager.current = 'wrongAnswer'

class CorrectAnswerScreen(Screen):
    description = StringProperty()
    def __init__(self, **kwargs):
        super(CorrectAnswerScreen, self).__init__(**kwargs)
    
    def callback(self):
        Logger.info(self.description)
        self.manager.current = 'location'

class WrongAnswerScreen(Screen):
    description = StringProperty()
    def __init__(self, **kwargs):
        super(WrongAnswerScreen, self).__init__(**kwargs)
    
    def callback(self):
        Logger.info(self.description)
        self.manager.current = 'location'

class TitleScreen(Screen):
    def __init__(self, **kwargs):
        super(TitleScreen, self).__init__(**kwargs)
    
    def gotoInfo(self):
        self.manager.current = 'info'
    
    def startGame(self):
        self.manager.current = 'map'
        self.manager.get_screen('map').enter(1)

class InfoScreen(Screen):
    def __init__(self, **kwargs):
        super(InfoScreen, self).__init__(**kwargs)

    def goback(self):
        self.manager.current = 'map'
        self.manager.get_screen('map').enter(2)
    
    def startGame(self):
        self.manager.current = 'location'

class MapScreen(Screen):
    currentPlayer = NumericProperty()
    dice1 = NumericProperty()
    dice2 = NumericProperty()
    diceSum = StringProperty()
    def __init__(self, **kwargs):
        super(MapScreen, self).__init__(**kwargs)
    
    def enter(self, n):
        self.currentPlayer = n
        turnPop = Popup(title = 'Next!',
                        content = Label(text = '第{}組的回合!'.format(n), 
                        font_name = 'data/DroidSansFallback.ttf', 
                        font_size = 32),
                        size_hint = (1,.3))
        turnPop.open()
    
    def rollDice(self):
        self.dice1 = randint(1, 6)
        self.dice2 = randint(1, 6)
        self.diceSum = str(self.dice1 + self.dice2)
        Logger.info(self.diceSum)
