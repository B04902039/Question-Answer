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
            questions[self.loc].remove(questions[self.loc][idx])
            self.__reset_time()
            self.__cd = Clock.schedule_interval(self.tic, 0.1)

    def callback(self, id):
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
