from utils import *

class MapScreen(Screen):
    currentPlayer = NumericProperty()
    dice1 = NumericProperty()
    dice2 = NumericProperty()
    diceSum = StringProperty()
    def __init__(self, **kwargs):
        super(MapScreen, self).__init__(**kwargs)
        self.currentPlayer = -1
        for i in range(6):
            self.ids['player_chess_{}'.format(i)].color = colors[i]
            self.ids['player_chess_{}'.format(i)].rel_pos = get_player_loc(i, gameboard.players[i].current_location)
            self.ids['player_chess_{}'.format(i)].source = 'data/images/chess_icon{}.png'.format(i)
        for i in domination_status_map:
            self.add_widget(i)

    def update_chess_on_map(self, player_id, loc_id):
        self.ids['player_chess_{}'.format(player_id)].rel_pos = get_player_loc(player_id, loc_id)

    def enter(self):
        update_domination_status_on_map()
        self.currentPlayer += 1
        self.currentPlayer %= 6
        # chance card: skip the turn
        if gameboard.players[self.currentPlayer].card['skip'] == True:
            label_text = '"停修死線到"\n第{}組暫停一回合!'.format(self.currentPlayer+1)
        elif gameboard.players[self.currentPlayer].card['sanbao'] == True:
            label_text = '"三寶出沒"\n第{}組暫停一回合!'.format(self.currentPlayer+1)
        elif gameboard.players[self.currentPlayer].card['yellow_ribbon'] == True:
            label_text = '"黃絲帶運動"\n第{}組暫停一回合!'.format(self.currentPlayer+1)
        elif gameboard.players[self.currentPlayer].card['one_step'] == True:
            label_text = '"早八聯發"\n第{}組此回合只能前進一格!'.format(self.currentPlayer+1)
        else:
            label_text = '第{}組的回合!'.format(self.currentPlayer+1)
        turnPop = Popup(title = 'Next!', size_hint = (.6,.3), 
                        content = Label(text = label_text,
                        font_name = default_font, font_size = 32))
        Clock.schedule_once(turnPop.dismiss, 1)
        turnPop.open()
        if gameboard.players[self.currentPlayer].card['skip'] == True:
            gameboard.players[self.currentPlayer].card['skip'] = False
            turnPop.on_dismiss = self.enter
        elif gameboard.players[self.currentPlayer].card['sanbao'] == True:
            gameboard.players[self.currentPlayer].card['sanbao'] = False
            turnPop.on_dismiss = self.enter
        elif gameboard.players[self.currentPlayer].card['yellow_ribbon'] == True:
            gameboard.players[self.currentPlayer].card['yellow_ribbon'] = False
            turnPop.on_dismiss = self.enter
    
    def rollDice(self):
        self.dice1 = randint(1, 6)
        self.dice2 = randint(1, 6)
        if gameboard.players[self.currentPlayer].card['one_step'] == True:
            gameboard.players[self.currentPlayer].card['one_step'] = False
            self.dice1 = 0
            self.dice2 = 1
        self.diceSum = str(self.dice1 + self.dice2)
        print('player:{}, dice:{}'.format(self.currentPlayer, self.diceSum))
        self.moveChess(self.dice1 + self.dice2)
    
    def moveChess(self, steps, loc=-1):
        if loc == -1:   # move chess relatively
            if gameboard.players[self.currentPlayer].card['bike_stolen'] == True:
                gameboard.move_chess(self.currentPlayer, int(steps/2))
                self.diceSum = str(int(steps/2))
            elif gameboard.players[self.currentPlayer].card['early_grad'] == True:
                gameboard.move_chess(self.currentPlayer, steps*2)
                self.diceSum = str(steps*2)
            else:
                gameboard.move_chess(self.currentPlayer, steps)
        else:
            gameboard.move_chess_directly(self.currentPlayer, loc)
        self.next_loc_id = gameboard.players[self.currentPlayer].current_location
        next_loc = school_locations[self.next_loc_id]
        if loc == -1:
            if gameboard.players[self.currentPlayer].card['bike_stolen'] == True:
                label_text = '腳踏車被偷QQ,第{}組前進{}格,到{}'.format(self.currentPlayer+1, self.diceSum, next_loc)
                gameboard.players[self.currentPlayer].card['bike_stolen'] = False
            elif gameboard.players[self.currentPlayer].card['early_grad'] == True:
                label_text = '提早畢業,第{}組前進{}格,到{}'.format(self.currentPlayer+1, self.diceSum, next_loc)
                gameboard.players[self.currentPlayer].card['early_grad'] = False
            else:
                label_text = '第{}組前進{}格,到{}'.format(self.currentPlayer+1, self.diceSum, next_loc)
        else:
            label_text = '第{}組移動到{}'.format(self.currentPlayer+1, next_loc)
        rulePop = Popup(title = 'Go!', size_hint = (.6, .3), 
                        content = Label(text = label_text,
                        font_name = default_font, font_size = 32))
        Clock.schedule_once(rulePop.dismiss, 1)
        
        # update chesses on broad visually
        self.update_chess_on_map(self.currentPlayer, self.next_loc_id)

        if gameboard.blocks[self.next_loc_id].status >= 3:   # the location has been dominated
            dominatePop = Popup(title = '!', size_hint = (.6, .3), 
                        content = Label(text = '{}已經被第{}組永久佔領!'.format(next_loc, gameboard.blocks[self.next_loc_id].dominator+1),
                        font_name = default_font, font_size = 32))
            dominatePop.open()
            dominatePop.on_dismiss = self.enter
            #self.enter()
        elif next_loc in questions.keys():
            # other team is the dominator
            if gameboard.blocks[self.next_loc_id].status > 0 and gameboard.blocks[self.next_loc_id].dominator != self.currentPlayer:
                rulePop.bind(on_dismiss = lambda x: self.startDual(gameboard.blocks[self.next_loc_id].dominator, 
                                                                    self.currentPlayer, self.next_loc_id, next_loc))
            else:  # no one dominate the block
                rulePop.bind(on_dismiss = lambda x: self.startQuestion(self.currentPlayer, self.next_loc_id, next_loc))
        elif next_loc=='機會':
            self.manager.current = 'chanceBG'
        elif next_loc=='起點':
            self.step_on_start()
        else:
            self.enter()
        rulePop.open()

    def update(self, playerID, blockID):
        # the question is answered correctly, update gameboard
        # ret = [teamId, status, locId]
        ret = gameboard.blocks[blockID].update(playerID)
        # update domination status on broad visually
        update_domination_status_on_map()
        return ret

    def startQuestion(self, player_id, block_id, loc):
        self.manager.get_screen('question').loc = loc
        self.manager.get_screen('question').blockID = block_id
        self.manager.get_screen('question').playerID = player_id
        self.manager.get_screen('question').update()
        self.manager.transition.direction = 'right'
        self.manager.current = 'question'

    def startDual(self, dominator, challenger, block_id, loc):
        print('challenger:{}, dominator:{}'.format(challenger, dominator))
        self.manager.get_screen('dual').challenger = challenger
        self.manager.get_screen('dual').dominator = dominator
        self.manager.get_screen('dual').blockID = block_id
        self.manager.get_screen('dual').loc = loc
        self.manager.get_screen('dual').update()
        self.manager.transition.direction = 'right'
        self.manager.current = 'dual'

    def step_on_start(self):
        bonus_loc = randint(0, len(school_locations)-1)
        while gameboard.blocks[bonus_loc].status >= 3 or school_locations[bonus_loc] not in questions.keys():
            bonus_loc = randint(0, len(school_locations)-1)
        startPop = Popup(title = 'GO!', size_hint = (.6, .3), 
                        content = Label(text = '獲得隨機地點:{}答題機會'.format(school_locations[bonus_loc]), 
                        font_name = default_font, font_size = 32))
        #Clock.schedule_once(startPop.dismiss, 1)
        if gameboard.blocks[bonus_loc].status > 0 and gameboard.blocks[bonus_loc].dominator != self.currentPlayer:
            startPop.bind(on_dismiss = lambda x: self.startDual(gameboard.blocks[bonus_loc].dominator, 
                                                        self.currentPlayer, bonus_loc, school_locations[bonus_loc]))
        else:  # no one dominate the block
            startPop.bind(on_dismiss = lambda x: self.startQuestion(self.currentPlayer, bonus_loc, school_locations[bonus_loc]))
        startPop.open()
