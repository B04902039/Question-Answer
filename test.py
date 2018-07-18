import kivy
kivy.require('1.0.6') # replace with your current kivy version !

import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

class MyApp(App):
    def build(self):
        self.modes = (
            '%I:%m:%S',
            '%H:%m:%S %P',
            '%S:',
        )
        self.mode = 0
        self.main_box = BoxLayout(orientation='vertical')
        
        self.button = Button(text='label', font_size=100, font_name='comic.ttf')
        self.main_box.add_widget(self.button)
    
        self.button.bind(on_press=self.tap)
        Clock.schedule_interval(self.timer, 0.01)
        
        return self.main_box
    
    def tap(self, button):
        if self.mode +1 == len(self.modes):
            self.mode = 0
        else:
            self.mode +=1
    
    def timer(self, dt):
        now = datetime.datetime.now()
        self.button.text = now.strftime(self.modes[self.mode])
        if self.mode == 2:
            self.button.text += str(now.microsecond)[:3]
            
if __name__ == '__main__':
    MyApp().run()