from utils import *

class QuestionScreen(Screen):
    '''
        Question screen:
        Qs is the question, c1-c4 are possible choices
        cd is the countdown object, limit is the time limit
    '''
    current_ques = ObjectProperty()
    correct_id = NumericProperty()
    limit = NumericProperty(20)
    playerID = NumericProperty()
    blockID = NumericProperty()
    loc = StringProperty()
    Qs = StringProperty()
    c1 = StringProperty()
    c2 = StringProperty()
    c3 = StringProperty()
    c4 = StringProperty()
    __cd = ObjectProperty()
    description = StringProperty()
    popout_cnt = 0
    def __init__(self, **kwargs):
        super(QuestionScreen, self).__init__(**kwargs)

    def tic(self, dt):
        if self.popout_cnt == 0:
            if self.limit > 0.1:
                self.limit -= 0.1
            else:
                self.__cd.cancel()
                self.__timeout()
    
    def back_to_map(self, instance):    # instance is the instance binded with this callback func
        #Logger.info(instance)
        self.manager.get_screen('map').enter()
        self.manager.current = 'map'
    
    def decrease_popcnt(self):
        self.popout_cnt -= 1

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
        print(self.current_ques, self.playerID)
        self.limit = 20
        if self.__cd:
            self.__cd.cancel()

    def update(self):
        global questions    # question asked, delete it
        tmp, self.loc = pick_question_set(questions, self.loc)
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
            self.__reset_time()
            rm = self.card_effect()
            if rm == True:  # remove the question or not
                questions[self.loc].remove(questions[self.loc][idx])

    def callback(self, id):
        self.__reset_time()
        # chance card: allpass, answer is always correct this turn
        if gameboard.players[self.playerID].card['allpass'] == True:
            id = self.correct_id
            gameboard.players[self.playerID].card['allpass'] = False
        if id == self.correct_id:
            if gameboard.players[self.playerID].card['angry_prof'] == True:
                result = [self.playerID, 4, self.blockID]  # return [teamId, status, locId]
                gameboard.players[self.playerID].card['angry_prof'] = False
            else:
                result = self.manager.get_screen('map').update(self.playerID, self.blockID)    # return [teamId, status, locId]
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
    
    def start_time(self):
        if self.__cd:
            self.__reset_time()
        self.__cd = Clock.schedule_interval(self.tic, 0.1)

    def card_bonus_time(self, id):
        self.popout_cnt += 1
        bonusPop = Popup(title='bonus time!', size_hint = (.6,.3), 
                        content=Label(text='第{}組的機會卡"共筆助攻"發動:\n答題時間延長20秒!'.format(id+1),
                        font_name = default_font, font_size = 32))
        #bonusPop.on_dismiss = self.start_time
        bonusPop.on_dismiss = self.decrease_popcnt
        bonusPop.open()
        gameboard.players[self.playerID].card['bonus_time'] = False
        self.limit = 40
    
    def card_carry(self, id):
        self.popout_cnt += 1
        carryPop = Popup(title='carry!', size_hint = (.6,.3), 
                        content=Label(text='第{}組的機會卡"凱瑞組員"發動:\n可使任意隊友代為答題!'.format(id+1),
                        font_name = default_font, font_size = 32))
        gameboard.players[self.playerID].card['carry'] = False
        carryPop.on_dismiss = self.decrease_popcnt
        carryPop.open()
    
    def card_free_land(self, id):
        def goto_result(self):
            self.manager.current = 'result'
        freePop = Popup(title='free land!', size_hint = (.7, .3), 
                        content=Label(text='第{}組的機會卡"免修大一英文"發動:\n不用答題即可佔領!'.format(id+1),
                        font_name = default_font, font_size = 32))
        gameboard.players[id].card['free_land'] = False
        result = self.manager.get_screen('map').update(id, self.blockID)    # return [teamId, status, locId]
        self.manager.get_screen('result').update(result)
        freePop.on_dismiss = partial(goto_result, self)
        freePop.open()
    
    def card_TA_help(self, id):
        self.popout_cnt += 1
        TAPop = Popup(title='TA helps me!', size_hint = (.6,.3), 
                    content=Label(text='第{}組的狀態"助教幫幫忙"發動:\n請被指定者負責答題!'.format(id+1),
                    font_name = default_font, font_size = 32))
        gameboard.players[id].card['TA_help'] = False
        TAPop.on_dismiss = self.decrease_popcnt
        TAPop.open()

    def card_allpass(self, id):
        self.popout_cnt += 1
        allpassPop = Popup(title='allpass!', size_hint = (.6,.3), 
                        content=Label(text='第{}組的機會卡"歐趴糖"發動:\n點任意選項無條件答對!'.format(id+1),
                        font_name = default_font, font_size = 32))
        allpassPop.on_dismiss = self.decrease_popcnt
        allpassPop.open()
    
    def card_angry_prof(self, id):
        self.popout_cnt += 1
        angryPop = Popup(title='angry prof!', size_hint = (.6,.3), 
                        content=Label(text='第{}組的機會卡"得罪教授"發動:\n答題正確也無法佔領QQ!'.format(id+1),
                        font_name = default_font, font_size = 32))
        angryPop.on_dismiss = self.decrease_popcnt
        angryPop.open()

    def card_effect(self):
        if gameboard.players[self.playerID].card['free_land']==True:
            self.card_free_land(self.playerID)
            # no need to start timer
            return False    # remove the question or not
        else:
            if gameboard.players[self.playerID].card['bonus_time']==True:
                self.card_bonus_time(self.playerID)  # get bonus time
            if gameboard.players[self.playerID].card['carry']==True:
                self.card_carry(self.playerID)
            if gameboard.players[self.playerID].card['TA_help']==True:
                self.card_TA_help(self.playerID)
            if gameboard.players[self.playerID].card['allpass']==True:
                self.card_allpass(self.playerID)
            elif gameboard.players[self.playerID].card['angry_prof']==True:
                self.card_angry_prof(self.playerID)
            self.start_time()
            return True # remove the question or not