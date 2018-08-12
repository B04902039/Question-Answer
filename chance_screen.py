from utils import *

no_flag_cards = {'TA_help', 'permanent_domination', 'bike', 'sanbao', 'thunder', 'retake'}
choice_team_cards = {'sanbao', 'TA_help', 'thunder'}

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
        # activate immediate effect if drawn
        self.immediate_effect()

    def callback(self):
        if self.drawed_card == 'bike':
            self.manager.current = 'location'
        elif self.drawed_card == 'retake':
            self.manager.current = 'chance'
            self.on_enter()
        elif self.drawed_card in choice_team_cards:
            self.manager.current = 'chance_choose_team'
        else:
            self.manager.get_screen('map').enter()
            self.manager.current = 'map'
    
    def immediate_effect(self):
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
        elif self.drawed_card in choice_team_cards:
            self.manager.get_screen('chance_choose_team').description = self.description
            self.manager.get_screen('chance_choose_team').drawed_card = self.drawed_card
            self.manager.get_screen('chance_choose_team').currentPlayer = self.currentPlayer
            self.btn_text = '選擇隊伍'
        elif self.drawed_card == 'go_to_start':
            gameboard.move_chess_directly(self.currentPlayer, 0)
            self.manager.get_screen('map').update_chess_on_map(self.currentPlayer, 0)
        elif self.drawed_card == 'retake':
            self.btn_text = '再...再抽一次'

