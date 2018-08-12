from utils import *

class ChanceChooseTeamScreen(Screen):
    description = StringProperty('')
    currentPlayer = NumericProperty(-1)
    drawed_card = StringProperty('')
    def __init__(self, **kwargs):
        super(ChanceChooseTeamScreen, self).__init__(**kwargs)
    
    def choose_team(self, id):
        if self.drawed_card == 'thunder':
            label_text = gameboard.thunder(id)
            pop = Popup(title = 'HAHAHA!', size_hint = (.6,.3), 
                        content = Label(text = label_text,
                        font_name = default_font, font_size = 32))
            pop.on_dismiss = self.goto_map_screen
            pop.open()
        else:
            gameboard.players[id].card[self.drawed_card] = True
            self.goto_map_screen()
    
    def goto_map_screen(self):
        self.manager.get_screen('map').enter()
        self.manager.current = 'map'
    