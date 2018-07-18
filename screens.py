# -*- coding: utf-8 -*-
from utils import *

school_locations = ['起點', '校門口', 'N號館', '傅鐘', '校史館', '行政大樓', '文學院', '機會', 
'溫州街', '社科院', '小福', '工綜', '農業陳列館', '醉月湖', '水源校區', '機會', '法學院', '活大', 
'118巷', '機會', '土木系館', '總圖', '機會', '教學館', '城中校區', '體育館', '公館商圈', 
'實驗林場', '臺大農場', '舟山路', '小小福', '二活', '機會', '椰林小舖', '宿舍區', '桃花心木道']
questions={}
gameBroad = board(school_locations)

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
    limit = NumericProperty(10)
    loc = StringProperty()
    Qs = StringProperty()
    c1 = StringProperty()
    c2 = StringProperty()
    c3 = StringProperty()
    c4 = StringProperty()
    cd = ObjectProperty()
    description = StringProperty()
    def __init__(self, **kwargs):
        super(QuestionScreen, self).__init__(**kwargs)

    def tic(self, dt):
        if self.limit > 0.1:
            self.limit -= 0.1
        else:
            self.cd.cancel()

    def update(self):
        tmp = questions[self.loc]
        if len(tmp) == 0:
            self.limit = 10
            if self.cd:
                self.cd.cancel()
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
            self.limit = 10
            if self.cd:
                self.cd.cancel()
            self.cd = Clock.schedule_interval(self.tic, 0.1)

    def callback(self, id):
        if id == self.correct_id:
            self.manager.get_screen('map').update(correct=True)
            self.manager.get_screen('correctAnswer').description = self.description
            self.manager.transition.direction = 'up'
            self.manager.current = 'correctAnswer'
        else:
            correct_answer = self.current_ques[self.correct_id]
            self.manager.get_screen('map').update(correct=False)
            self.manager.get_screen('wrongAnswer').correct_answer = correct_answer
            self.manager.get_screen('wrongAnswer').description = self.description
            self.manager.transition.direction = 'down'
            self.manager.current = 'wrongAnswer'

class CorrectAnswerScreen(Screen):
    description = StringProperty()
    def __init__(self, **kwargs):
        super(CorrectAnswerScreen, self).__init__(**kwargs)
    
    def callback(self):
        Logger.info(self.description)
        self.manager.get_screen('map').enter()
        self.manager.current = 'map'

class WrongAnswerScreen(Screen):
    correct_answer = StringProperty()
    description = StringProperty()
    def __init__(self, **kwargs):
        super(WrongAnswerScreen, self).__init__(**kwargs)
    
    def callback(self):
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

class MapScreen(Screen):
    currentPlayer = NumericProperty()
    dice1 = NumericProperty()
    dice2 = NumericProperty()
    diceSum = StringProperty()
    def __init__(self, **kwargs):
        super(MapScreen, self).__init__(**kwargs)
        self.currentPlayer = -1
    
    def enter(self):
        self.currentPlayer += 1
        self.currentPlayer %= 6
        turnPop = Popup(title = 'Next!',
                        content = Label(text = '第{}組的回合!'.format(self.currentPlayer+1),
                        font_name = 'data/DroidSansFallback.ttf', 
                        font_size = 32),
                        size_hint = (.6,.3))
        Clock.schedule_once(turnPop.dismiss, 1)
        turnPop.open()
    
    def rollDice(self):
        self.dice1 = randint(1, 6)
        self.dice2 = randint(1, 6)
        self.diceSum = str(self.dice1 + self.dice2)
        Logger.info(self.diceSum)
        # move chess
        self.moveChess(self.currentPlayer, self.dice1+self.dice2)
        next_loc = school_locations[gameBroad.players[self.currentPlayer].current_location]
        rulePop = Popup(title = self.diceSum,
                        content = Label(text = '第{}組前進{}格,到{}'.format(self.currentPlayer+1, self.diceSum, next_loc),
                        font_name = 'data/DroidSansFallback.ttf', 
                        font_size = 32),                   
                        size_hint = (.6, .3))
        Clock.schedule_once(rulePop.dismiss, 1)
        if next_loc in questions.keys():
            rulePop.bind(on_dismiss = lambda x: self.startQuestion(self.currentPlayer, next_loc))
        else:
            self.enter()
        rulePop.open()

    def update(self, correct):
        pass

    def moveChess(self, player_id, moves):
        gameBroad.move_chess(player_id, moves)

    def startQuestion(self, player_id, loc):
        self.manager.get_screen('question').loc = loc
        self.manager.get_screen('question').update()
        self.manager.transition.direction = 'right'
        self.manager.current = 'question'

    
