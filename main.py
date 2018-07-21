# -*- coding: utf-8 -*-
from screens import *

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
        ls.create_button()
        sm.add_widget(CorrectAnswerScreen(name='correctAnswer'))
        sm.add_widget(WrongAnswerScreen(name='wrongAnswer'))
        sm.add_widget(ResultScreen(name='result'))
        sm.add_widget(EndScreen(name='end'))
        return sm

if __name__ == '__main__':
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

    TestApp().run()