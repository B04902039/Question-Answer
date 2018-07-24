from utils import *

no_flag_cards = {'TA_help', 'permanent_domination', 'bike'}

class ChanceScreen(Screen):
    btn_text = StringProperty('')
    description = StringProperty('')
    currentPlayer = NumericProperty(-1)
    drawed_card = StringProperty('')
    def __init__(self, **kwargs):
        super(ChanceScreen, self).__init__(**kwargs)
    
    def on_enter(self):
        self.btn_text = '回地圖'
        self.currentPlayer = self.manager.get_screen('map').currentPlayer
        player_card = gameboard.players[self.currentPlayer].card    #shallow copy
        possible_card = []
        for i in player_card.items():
            if i[1] == False:
                possible_card.append(i[0])
        if len(possible_card) > 0:
            self.drawed_card = choice(possible_card)
            if self.drawed_card not in no_flag_cards:
                player_card[self.drawed_card] = True # add to player's card set
            self.description = chance_card_description(self.drawed_card)
        else:
            self.description = '你已經有所有機會卡囉!'

        if self.drawed_card == 'permanent_domination':
            candidate_land = []
            for blk in gameboard.blocks:
                if blk.dominator==self.currentPlayer and blk.status<3:
                    candidate_land.append(blk.location_name)
            if len(candidate_land) == 0:
                self.description += '\n...但是你的隊伍沒有占領任何一塊土地QAQ'
                self.btn_text = '嗚嗚嗚嗚嗚'
            else:
                land = choice(candidate_land)
                for blk in gameboard.blocks:
                    if blk.location_name == land:
                        blk.update(self.currentPlayer)
                        blk.update(self.currentPlayer)
                        blk.update(self.currentPlayer)
                        break
                self.description += '\n恭喜永久佔領{}'.format(land)
                self.btn_text = '太爽啦!'
        elif self.drawed_card == 'bike':
            self.manager.get_screen('location').currentPlayer = self.currentPlayer
            self.btn_text = '太爽啦!'

    def callback(self):
        if self.drawed_card == 'bike':
            self.manager.current = 'location'    
        else:
            self.manager.get_screen('map').enter()
            self.manager.current = 'map'
