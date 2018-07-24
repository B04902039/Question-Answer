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
        ls.create_button()
        sm.add_widget(CorrectAnswerScreen(name='correctAnswer'))
        sm.add_widget(WrongAnswerScreen(name='wrongAnswer'))
        sm.add_widget(ResultScreen(name='result'))
        sm.add_widget(EndScreen(name='end'))

        #Clock.schedule_interval(sm.get_screen('map').update_chess_demo, 0.25)

        return sm

if __name__ == '__main__':
    # disable the left click red dot
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

    with open ('kv/test.kv', 'r', encoding='utf-8') as f:
        Builder.load_string(f.read())
    f = open('data/questions_v2.csv', 'r', encoding='big5')
    data = f.readlines()
    for row in data:
        tmp = row.split(',')
        tmp_ls = []
        if tmp[0] != '':
            for i in range(100):
                if tmp[i*6+1] == '':
                    break
                tmp_ls.append(tmp[i*6+1:i*6+7])
            global questions
            questions[tmp[0]] = tmp_ls
    for i in questions.keys():
        if i not in school_locations:
            print('Location missed: s', i)
    TestApp().run()