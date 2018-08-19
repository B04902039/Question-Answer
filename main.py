# -*- coding: utf-8 -*-
from screens import *
from kivy.config import Config

class TestApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TitleScreen(name='title'))
        sm.add_widget(InfoScreen(name='info'))
        sm.add_widget(MapScreen(name='map'))
        ls = LocationScreen(name='location')
        sm.add_widget(ls)
        sm.add_widget(QuestionScreen(name='question'))
        sm.add_widget(DualScreen(name='dual'))
        sm.add_widget(ChanceScreen(name='chance'))
        sm.add_widget(ChanceCardBG(name='chanceBG'))
        sm.add_widget(ChanceChooseTeamScreen(name='chance_choose_team'))
        ls.create_button()
        sm.add_widget(CorrectAnswerScreen(name='correctAnswer'))
        sm.add_widget(WrongAnswerScreen(name='wrongAnswer'))
        sm.add_widget(ResultScreen(name='result'))
        sm.add_widget(EndScreen(name='end'))

        return sm

if __name__ == '__main__':
    # disable the left click red dot
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    Config.set('graphics', 'width', '1024')
    Config.set('graphics', 'height', '768')

    with open ('kv/test.kv', 'r', encoding='utf-8') as f:
        Builder.load_string(f.read())
    f = open('data/questions_v3.csv', 'r', encoding='utf8')
    data = f.readlines()
    for row in data:
        tmp = row.split(',')
        tmp_ls = []
        if tmp[0] != '':
            #print(tmp[0])
            for i in range(100):
                tmp_ques =  tmp[i*6+1:i*6+7]
                all_empty = True
                for j in tmp_ques:
                    if j!='' and j!='\n':
                        all_empty = False
                if not all_empty and len(tmp_ques)==6:
                    tmp_ls.append(tmp_ques)
            global questions
            questions[tmp[0]] = tmp_ls
            print('{} has {} questions.'.format(tmp[0], len(tmp_ls)))
    for i in questions.keys():
        if i not in school_locations:
            print('Location missed: ', i)
    init_domination_status()
    TestApp().run()