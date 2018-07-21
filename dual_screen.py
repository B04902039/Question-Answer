from utils import *
from question_screen import QuestionScreen

class DualScreen(QuestionScreen):
    challenger = NumericProperty(-1)
    dominator = NumericProperty(-1)
    playerID = NumericProperty()    # the answerer
    flag = False    # whether player is choisen
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
        self.flag = False
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
    
    def callback(self, id):
        if self.flag:
            if id == self.correct_id:   # correct answer
                result = self.manager.get_screen('map').update(self.playerID)    # return [teamId, status, locId]
                self.manager.get_screen('result').update(result)
                self.manager.get_screen('correctAnswer').description = self.description
                self.manager.transition.direction = 'up'
                self.manager.current = 'correctAnswer'
            elif self.playerID == self.dominator:   # dominator answer wrong => challenger win
                self.set_answerer(self.challenger)
                result = self.manager.get_screen('map').update(self.playerID)
                self.manager.get_screen('wrongAnswer').show_result = True
                self.manager.get_screen('result').update(result)
                self.manager.get_screen('wrongAnswer').description = self.description
                self.manager.transition.direction = 'down'
                self.manager.current = 'wrongAnswer'
            else:   # challenger answer wrong
                correct_answer = self.current_ques[self.correct_id]
                self.manager.get_screen('wrongAnswer').correct_answer = correct_answer
                self.manager.get_screen('wrongAnswer').description = self.description
                self.manager.transition.direction = 'down'
                self.manager.current = 'wrongAnswer'
        else:
            warnPop = Popup(title='warning', size_hint = (.6,.3))
            poplayout = BoxLayout(orientation='vertical')
            buttonLayout = BoxLayout(orientation='horizontal', padding=5, spacing=20)
            buttonLayout.add_widget(Button(font_size=32, text=str(self.dominator+1), 
                                            on_press=partial(self.set_answerer, self.dominator), 
                                            on_release=warnPop.dismiss))
            buttonLayout.add_widget(Button(font_size=32, text=str(self.challenger+1), 
                                            on_press=partial(self.set_answerer, self.challenger), 
                                            on_release=warnPop.dismiss))
            poplayout.add_widget(Label(text = '請選擇組別!', font_name = default_font, font_size = 32, size_hint = (1, .6)))
            poplayout.add_widget(buttonLayout)
            warnPop.content = poplayout
            warnPop.open()
    
    def set_answerer(self, player, *args):
        self.flag = True
        self.playerID = player
