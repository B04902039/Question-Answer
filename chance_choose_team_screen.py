from utils import *


class ChanceChooseTeamScreen(Screen):
    description = StringProperty('')
    currentPlayer = NumericProperty(-1)
    drawed_card = StringProperty('')
    def __init__(self, **kwargs):
        super(ChanceChooseTeamScreen, self).__init__(**kwargs)
    
    def choose_team(self, id):
        gameboard.players[id].card[self.drawed_card] = True
        self.manager.get_screen('map').enter()
        self.manager.current = 'map'
    