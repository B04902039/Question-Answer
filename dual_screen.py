from utils import *
from question_screen import QuestionScreen

class DualScreen(QuestionScreen):
    challenger = NumericProperty(-1)
    dominator = NumericProperty(-1)
    playerID = NumericProperty()    # the answerer
    blockID = NumericProperty()
    flag = False    # whether player is choisen
    def __init__(self, **kwargs):
        super(DualScreen, self).__init__(**kwargs)
        self.ids.leftLayout.remove_widget(self.ids.timer)
        buttons_layout = BoxLayout(orientation = 'vertical', spacing = 10, padding = 10, size_hint = (1, .2))
        self.button_dominator = Button(font_size = 32, background_color=(0.392, 0.850, 0.776, 1), 
                                        color=(1,1,1,1), background_normal='data/images/white.png', 
                                        font_name=default_font)
        self.button_challenger = Button(font_size = 32, background_color=(0.392, 0.850, 0.776, 1), 
                                        color=(1,1,1,1), background_normal='data/images/white.png', 
                                        font_name=default_font)
        buttons_layout.add_widget(self.button_dominator)
        buttons_layout.add_widget(self.button_challenger)
        self.ids.leftLayout.add_widget(buttons_layout)

    def update(self):
        global questions    # question asked, delete it
        self.flag = False
        self.button_challenger.text = '挑戰者:' + str(self.challenger+1)
        self.button_dominator.text = '占領者:' + str(self.dominator+1)
        self.button_challenger.on_release = partial(self.set_answerer, self.challenger)
        self.button_dominator.on_release = partial(self.set_answerer, self.dominator)
        tmp, self.loc = pick_question_set(questions, self.loc)
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
            rm = self.card_effect()
            if rm == True:
                questions[self.loc].remove(questions[self.loc][idx])
            # no timer
    
    def callback(self, id):
        if self.flag:
            # chance card: allpass, answer is always correct this turn
            if gameboard.players[self.playerID].card['allpass'] == True:
                id = self.correct_id
                gameboard.players[self.playerID].card['allpass'] = False
            if id == self.correct_id:   # correct answer
                if gameboard.players[self.playerID].card['angry_prof'] == True:
                    result = [self.playerID, 4, self.blockID]  # return [teamId, status, locId]
                    gameboard.players[self.playerID].card['angry_prof'] = False
                else:
                    result = self.manager.get_screen('map').update(self.playerID, self.blockID)    # return [teamId, status, locId]
                self.manager.get_screen('result').update(result)
                self.manager.get_screen('correctAnswer').description = self.description
                self.manager.transition.direction = 'up'
                self.manager.current = 'correctAnswer'
            elif self.playerID == self.dominator:   # dominator answer wrong => challenger win
                self.set_answerer(self.challenger)
                result = self.manager.get_screen('map').update(self.playerID, self.blockID)
                correct_answer = self.current_ques[self.correct_id]
                self.manager.get_screen('result').update(result)
                self.manager.get_screen('wrongAnswer').show_result = True
                self.manager.get_screen('wrongAnswer').correct_answer = correct_answer
                self.manager.get_screen('wrongAnswer').description = self.description
                self.manager.transition.direction = 'down'
                self.manager.current = 'wrongAnswer'
            else:   # challenger answer wrong => dominator win
                self.set_answerer(self.dominator)
                result = self.manager.get_screen('map').update(self.playerID, self.blockID)
                correct_answer = self.current_ques[self.correct_id]
                self.manager.get_screen('result').update(result)
                self.manager.get_screen('wrongAnswer').show_result = True
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
    
    def card_prior(self):
        def make_popup(text_on_label):
            pop = Popup(title='Me first!', size_hint = (.8, .3))
            lab = Label(text=text_on_label, font_name=default_font, font_size=32)
            pop.content = lab
            return pop
        if gameboard.players[self.challenger].card['prior'] == True:
            pop1 = make_popup('第{}組的機會卡"對面的Sorry"發動:\n獲得優先答題權!'.format(self.challenger+1))
            gameboard.players[self.challenger].card['prior'] = False
            pop1.open()
        if gameboard.players[self.dominator].card['prior'] == True:
            pop2 = make_popup('第{}組的機會卡"對面的Sorry"發動:\n獲得優先答題權!'.format(self.dominator+1))
            gameboard.players[self.dominator].card['prior'] = False
            pop2.open()
    
    def card_effect(self):
        if gameboard.players[self.challenger].card['free_land']:
            self.card_free_land(self.challenger)
            return False    # remove the question or not
        else: 
            self.card_prior()
            if gameboard.players[self.dominator].card['carry']:
                self.card_carry(self.dominator)
            if gameboard.players[self.challenger].card['carry']:
                self.card_carry(self.challenger)
            if gameboard.players[self.challenger].card['allpass']:
                self.card_allpass(self.challenger)
            elif gameboard.players[self.challenger].card['angry_prof']:
                self.card_angry_prof(self.challenger)
            if gameboard.players[self.dominator].card['allpass']:
                self.card_allpass(self.dominator)
            elif gameboard.players[self.dominator].card['angry_prof']:
                self.card_angry_prof(self.dominator)
            if gameboard.players[self.challenger].card['TA_help']:
                self.card_TA_help(self.challenger)
            if gameboard.players[self.dominator].card['TA_help']:
                self.card_TA_help(self.dominator)
            return True