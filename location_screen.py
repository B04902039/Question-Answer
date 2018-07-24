from utils import *

class LocationScreen(Screen):
    '''
        location screen (deprecated feature)
        select the location and switch the questions screen
    '''
    currentPlayer = NumericProperty(-1)
    def __init__(self, **kwargs):
        super(LocationScreen, self).__init__(**kwargs)
    # create button dynamically according to locations in csv
    def create_button(self):
        out_layout = RelativeLayout()
        layout = GridLayout(cols=3, spacing=1, size_hint=(.75, .7), pos_hint={'center_x':.5, 'center_y':.5})
        out_layout.add_widget(layout)
        for i in questions.keys():
            tmp = Button(text=i, font_name=default_font)
            tmp.bind(on_release=partial(self.select_loc, i))
            layout.add_widget(tmp)
        self.add_widget(out_layout)

    def select_loc(self, loc, instance):
        self.manager.get_screen('map').currentPlayer = self.currentPlayer
        id = 0
        for i in range(len(school_locations)):
            if school_locations[i] == loc:
                id = i
                break
        self.manager.get_screen('map').moveChess(0, id)


