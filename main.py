import kivy
kivy.require('1.10.0')
import math
from random import randint
from functools import partial
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.logger import Logger
import kivy.resources
kivy.resources.resource_add_path('.')

current_loc = ''
questions={}

class LocationScreen(Screen):

    def __init__(self, **kwargs):
        super(LocationScreen, self).__init__(**kwargs)
    
    def create_button(self):
        layout = GridLayout(cols=2, padding=10)
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
    loc = StringProperty()
    Qs = StringProperty()
    c1 = StringProperty()
    c2 = StringProperty()
    c3 = StringProperty()
    c4 = StringProperty()
    def __init__(self, **kwargs):
        super(QuestionScreen, self).__init__(**kwargs)

    def update(self):
        tmp = questions[self.loc]
        idx = randint(0, len(tmp)-1)
        self.current_ques = tmp[idx]
        self.Qs = self.current_ques[0]
        self.c1 = self.current_ques[1]
        self.c2 = self.current_ques[2]
        self.c3 = self.current_ques[3]
        self.c4 = self.current_ques[4]


class TestApp(App):
    def build(self):
        sm = ScreenManager()
        ls = LocationScreen(name='location')
        sm.add_widget(ls)
        sm.add_widget(QuestionScreen(name='question'))
        ls.create_button()
        return sm

Builder.load_file('data/test.kv')

if __name__ == '__main__':
    f = open('data/questions.csv', 'r', encoding='big5')
    data = f.readlines()
    for row in data:
        tmp = row.split(',')
        tmp_ls = []
        if tmp[0] != '':
            for i in range(6):
                tmp_ls.append(tmp[i*6+1:i*6+7])
            questions[tmp[0]] = tmp_ls

    TestApp().run()