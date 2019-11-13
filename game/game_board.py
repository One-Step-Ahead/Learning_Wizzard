from game.cards import Card, create_all_cards
from game.player import *
from game.score_board import ScoreBoard
from random import choice


class GameBoardMeta(type):
    _instance = None

    def __call__(cls, player_total):
        if cls._instance is None:
            cls._instance = super().__call__(player_total)
        return cls._instance


class GameBoard(metaclass=GameBoardMeta):

    def __init__(self, player_total: int):
        self.card_deck = list()
        self.players = create_players(player_total)
        self.cards_in_play = list()
        self.round = 0
        self.atut = Card
        self.rounds_total = get_rounds_total(player_total)
        self.score_board = ScoreBoard(self.round)
        self.current_player = Player

    def new_round(self):
        # Reihenfolge ist wichtig!
        self.round += 1
        self.reset_card_deck()
        self.prepare_players()
        self.set_new_atut()
        print('New Round! [', self.round, ']', sep='')

    def new_stich(self):
        self.cards_in_play.clear()

    def prepare_players(self):
        for i in self.players:
            i.hand.clear()
            i.stich_score = 0
            i.draw_card(self.card_deck, self.round)

    def reset_card_deck(self):
        self.card_deck.clear()
        create_all_cards(self.card_deck)

    def set_new_atut(self):
        if self.round != self.rounds_total:
            self.atut = choice(self.card_deck)
        else:
            self.atut = None

    def game_loop(self):
        self.new_round()
        self.score_board.make_prediction(self.current_player, 1)


def create_players(total_player_number):
    players = []
    for i in range(0, total_player_number):
        players.append(Player(i))
    return players


def get_rounds_total(total_player_number: int):
    if total_player_number == 3:
        return 20
    if total_player_number == 4:
        return 15
    if total_player_number == 5:
        return 12
    if total_player_number == 6:
        return 10
    else:
        raise ValueError("PlayerCount needs to be between 3-6!")

