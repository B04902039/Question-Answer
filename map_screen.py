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
        #self.loc_demo = [0, 0, 0, 0, 0, 0]
    
    def update_chess_on_map(self, dt):
        for i in range(6):
            self.loc_demo[i] = (self.loc_demo[i] + randint(0, 2)) % 36
            self.ids['player_chess_{}'.format(i)].color = colors[i]
            self.ids['player_chess_{}'.format(i)].rel_pos = get_player_loc(i, self.loc_demo[i])

    def enter(self):
        self.currentPlayer += 1
        self.currentPlayer %= 6
        turnPop = Popup(title = 'Next!',
                        content = Label(text = '第{}組的回合!'.format(self.currentPlayer+1),
                        font_name = default_font, font_size = 32),
                        size_hint = (.6,.3))
        Clock.schedule_once(turnPop.dismiss, 1)
        turnPop.open()
    
    def rollDice(self):
        self.dice1 = randint(1, 6)
        self.dice2 = randint(1, 6)
        self.diceSum = str(self.dice1 + self.dice2)
        Logger.info(self.diceSum)
        # move chess
        self.moveChess(self.currentPlayer, self.dice1+self.dice2)
        self.next_loc_id = gameboard.players[self.currentPlayer].current_location
        next_loc = school_locations[self.next_loc_id]
        rulePop = Popup(title = self.diceSum,
                        content = Label(text = '第{}組前進{}格,到{}'.format(self.currentPlayer+1, self.diceSum, next_loc),
                        font_name = default_font, font_size = 32),                   
                        size_hint = (.6, .3))
        Clock.schedule_once(rulePop.dismiss, 1)
        
        # update chesses on broad visually
        self.ids['player_chess_{}'.format(self.currentPlayer)].rel_pos = get_player_loc(self.currentPlayer, self.next_loc_id)

        if gameboard.blocks[self.next_loc_id].status >= 3:   # the location has been dominated
            dominatePop = Popup(title = '!', 
                        content = Label(text = '{}已經被第{}組永久佔領!'.format(next_loc, gameboard.blocks[self.next_loc_id].dominator+1),
                        font_name = default_font, font_size = 32),
                        size_hint = (.6, .3))
            dominatePop.open()
            dominatePop.on_dismiss = self.enter
            #self.enter()
        elif next_loc in questions.keys():
            # other team is the dominator
            if gameboard.blocks[self.next_loc_id].status > 0 and gameboard.blocks[self.next_loc_id].dominator != self.currentPlayer:
                rulePop.bind(on_dismiss = lambda x: self.startDual(gameboard.blocks[self.next_loc_id].dominator, 
                                                                    self.currentPlayer, next_loc))
            else:  # no one dominate the block
                rulePop.bind(on_dismiss = lambda x: self.startQuestion(self.currentPlayer, next_loc))
        else:
            self.enter()
        rulePop.open()

    def update(self, playerID):
        # the question is answered correctly, update gameboard
        # return [teamId, status, locId]
        return gameboard.blocks[self.next_loc_id].update(playerID)

    def moveChess(self, player_id, moves):
        gameboard.move_chess(player_id, moves)

    def startQuestion(self, player_id, loc):
        self.manager.get_screen('question').loc = loc
        self.manager.get_screen('question').playerID = player_id
        self.manager.get_screen('question').update()
        self.manager.transition.direction = 'right'
        self.manager.current = 'question'

    def startDual(self, dominator, challenger, loc):
        Logger.info('challenger:{}, dominator:{}'.format(challenger, dominator))
        self.manager.get_screen('dual').challenger = challenger
        self.manager.get_screen('dual').dominator = dominator
        self.manager.get_screen('dual').loc = loc
        self.manager.get_screen('dual').update()
        self.manager.transition.direction = 'right'
        self.manager.current = 'dual'
