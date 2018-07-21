# -*- coding: utf-8 -*-
from utils import *

default_font = 'data/DroidSansFallback.ttf'
school_locations = ['起點', '校門口', 'N號館', '傅鐘', '校史館', '行政大樓', '文學院', '機會', 
'溫州街', '社科院', '小福', '工綜', '農業陳列館', '醉月湖', '水源校區', '機會', '法學院', '活大', 
'118巷', '機會', '土木系館', '總圖', '機會', '教學館', '城中校區', '體育館', '公館商圈', 
'實驗林場', '臺大農場', '舟山路', '小小福', '二活', '機會', '椰林小舖', '宿舍區', '桃花心木道']
questions={}
gameBroad = board(school_locations)
colors = [(1, 0, 0, .5), (1, 1, 0, .5), (0, 1, 0, .5), (0, 1, 1, .5), (0, 0, 1 , .5), (1, 0, 1, .5)]

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

class QuestionScreen(Screen):
    '''
        Question screen:
        Qs is the question, c1-c4 are possible choices
        cd is the countdown object, limit is the time limit
    '''
    current_ques = ObjectProperty()
    correct_id = NumericProperty()
    limit = NumericProperty(10)
    playerID = NumericProperty()
    loc = StringProperty()
    Qs = StringProperty()
    c1 = StringProperty()
    c2 = StringProperty()
    c3 = StringProperty()
    c4 = StringProperty()
    __cd = ObjectProperty()
    description = StringProperty()
    def __init__(self, **kwargs):
        super(QuestionScreen, self).__init__(**kwargs)

    def tic(self, dt):
        #Logger.info(str(self.limit))
        if self.limit > 0.1:
            self.limit -= 0.1
        else:
            self.__cd.cancel()
            self.__timeout()
    
    def back_to_map(self, instance):    # instance is the instance binded with this callback func
        #Logger.info(instance)
        self.manager.get_screen('map').enter()
        self.manager.current = 'map'

    def __timeout(self):
        poplayout = BoxLayout(orientation='vertical')
        lb = Label(text = '時間到!', font_name = default_font, font_size = 32, size_hint=(1, 0.7))
        bt = Button(text = '回地圖', font_name = default_font, font_size = 20, size_hint=(1, 0.3))
        poplayout.add_widget(lb)
        poplayout.add_widget(bt)
        timeoutPop = Popup(title='Time out!', content=poplayout, size_hint = (.6,.5), auto_dismiss=False)
        bt.bind(on_release = timeoutPop.dismiss)
        timeoutPop.bind(on_dismiss = self.back_to_map)
        timeoutPop.open()
    
    def __reset_time(self):
        self.limit = 10
        if self.__cd:
            self.__cd.cancel()

    def update(self):
        global questions    # question asked, delete it
        tmp = questions[self.loc]
        if len(tmp) == 0:
            self.__reset_time()
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
            questions[self.loc].remove(questions[self.loc][idx])
            self.__reset_time()
            self.__cd = Clock.schedule_interval(self.tic, 0.1)

    def callback(self, id, ):
        self.__reset_time()
        if id == self.correct_id:
            result = self.manager.get_screen('map').update(self.playerID)    # return [teamId, status, locId]
            self.manager.get_screen('result').update(result)
            self.manager.get_screen('correctAnswer').description = self.description
            self.manager.transition.direction = 'up'
            self.manager.current = 'correctAnswer'
        else:
            correct_answer = self.current_ques[self.correct_id]
            self.manager.get_screen('wrongAnswer').correct_answer = correct_answer
            self.manager.get_screen('wrongAnswer').description = self.description
            self.manager.transition.direction = 'down'
            self.manager.current = 'wrongAnswer'

class DualScreen(QuestionScreen):
    challenger = NumericProperty(-1)
    dominator = NumericProperty(-1)
    playerID = NumericProperty()    # the answerer
    def __init__(self, **kwargs):
        super(DualScreen, self).__init__(**kwargs)
        self.ids.leftLayout.remove_widget(self.ids.timer)
        buttons_layout = BoxLayout(orientation = 'vertical', spacing = 10, padding = 10, size_hint = (1, .2))
        self.button_dominator = Button(font_size = 32)
        self.button_challenger = Button(font_size = 32)
        buttons_layout.add_widget(self.button_dominator)
        buttons_layout.add_widget(self.button_challenger)
        self.ids.leftLayout.add_widget(buttons_layout)

    def update(self):
        global questions    # question asked, delete it
        self.button_challenger.text = str(self.challenger+1)
        self.button_dominator.text = str(self.dominator+1)
        self.button_challenger.on_release = partial(self.set_answerer, self.challenger)
        self.button_dominator.on_release = partial(self.set_answerer, self.dominator)
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
            questions[self.loc].remove(questions[self.loc][idx])
            # no timer
    
    def set_answerer(self, player):
        self.playerID = player

class CorrectAnswerScreen(Screen):
    description = StringProperty()
    def __init__(self, **kwargs):
        super(CorrectAnswerScreen, self).__init__(**kwargs)
    
    def callback(self):
        Logger.info(self.description)
        self.manager.current = 'result'

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
                        font_name = default_font, font_size = 32),
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
        self.next_loc_id = gameBroad.players[self.currentPlayer].current_location
        next_loc = school_locations[self.next_loc_id]
        rulePop = Popup(title = self.diceSum,
                        content = Label(text = '第{}組前進{}格,到{}'.format(self.currentPlayer+1, self.diceSum, next_loc),
                        font_name = default_font, font_size = 32),                   
                        size_hint = (.6, .3))
        Clock.schedule_once(rulePop.dismiss, 1)

        if gameBroad.blocks[self.next_loc_id].status >= 3:   # the location has been dominated
            dominatePop = Popup(title = '!', 
                        content = Label(text = '{}已經被第{}組永久佔領!'.format(next_loc, gameBroad.blocks[self.next_loc_id].dominator),
                        font_name = default_font, font_size = 32),
                        size_hint = (.6, .3))
            #Clock.schedule_once(dominatePop.dismiss, 1)
            dominatePop.open()
            self.enter()
        elif next_loc in questions.keys():
            if gameBroad.blocks[self.next_loc_id].status == 0:  # no one dominate the block
                rulePop.bind(on_dismiss = lambda x: self.startQuestion(self.currentPlayer, next_loc))
            else:
                rulePop.bind(on_dismiss = lambda x: self.startDual(gameBroad.blocks[self.next_loc_id].dominator, 
                                                                    self.currentPlayer, next_loc))
        else:
            self.enter()
        rulePop.open()

    def update(self, playerID):
        # the question is answered correctly, update gamebroad
        # return [teamId, status, locId]
        return gameBroad.blocks[self.next_loc_id].update(playerID)

    def moveChess(self, player_id, moves):
        gameBroad.move_chess(player_id, moves)

    def startQuestion(self, player_id, loc):
        self.manager.get_screen('question').loc = loc
        self.manager.get_screen('question').playerID = player_id
        self.manager.get_screen('question').update()
        self.manager.transition.direction = 'right'
        self.manager.current = 'question'

    def startDual(self, dominator, challenger, loc):
        Logger.info('challenger:{}, dominator:{}'.format(challenger, dominator))
        self.manager.get_screen('dual').challenger = challenger
        self.manager.get_screen('dual').dominator = dominator
        self.manager.get_screen('dual').loc = loc
        self.manager.get_screen('dual').update()
        self.manager.transition.direction = 'right'
        self.manager.current = 'dual'

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