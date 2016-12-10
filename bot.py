#!/usr/bin/env python
import random

COLORS = ['BLUE', 'GREEN', 'RED', 'WHITE']


class EndOfDeckException(Exception):
    pass


class Crystal(object):
    """
    """
    def __init__(self, color=None):
        super(Crystal, self).__init__()
        if not color:
            color = random.choice(COLORS)
        self.color = color

    def __str__(self):
        return "Crystal({})".format(self.color)

    def __repr__(self):
        return self.__str__()


class Card(object):
    """
    """
    def __init__(self, color):
        super(Card, self).__init__()
        self.color = color

    def __str__(self):
        return "Card({})".format(self.color)

    def __repr__(self):
        return self.__str__()

    def __mul__(self, n):
        return [self for i in xrange(n)]


class MKDummy(object):
    """
    creates a dummy player based on a given
    the character primary and secondary colors (card and crystals)
    """

    def __init__(self, name="", prime_color=None, sec_color=None):
        super(MKDummy, self).__init__()
        self.name = name
        if not prime_color or not sec_color:
            prime_color, sec_color = random.sample(COLORS, 2)
        self._init_crystals(prime_color, sec_color)
        self._init_deck()
        self.end_of_round = False

    def _init_crystals(self, prime_color, sec_color):
        crystals = {color: 0 for color in COLORS}
        crystals[prime_color] += 2
        crystals[sec_color] += 1
        self.crystals = crystals

    def _init_deck(self):
        self.deck = []
        self.discard = []
        for color in COLORS:
            self.deck.extend(Card(color) * 4)

    def shuffle(self):
        random.shuffle(self.deck)
        return self.deck

    def draw(self):
        if len(self.deck) == 0:
            raise EndOfDeckException()
        self.discard.append(self.deck.pop())
        return self.discard[-1]

    def new_round_setup(self, card_color, crystal_color):
        new_deck = [Card(card_color)]
        new_deck.extend(self.deck)
        new_deck.extend(self.discard)
        self.deck = new_deck
        self.discard = []
        self.crystals[crystal_color] += 1
        self.end_of_round = False

    def last_discarded_card(self):
        return self.discard[-1] if self.discard else None

    def resolve_turn(self):
        last_card = None
        try:
            for i in xrange(3):
                last_card = self.draw()
            extra_cards_n = self.crystals[last_card.color]
            for j in xrange(extra_cards_n):
                last_card = self.draw()
        except EndOfDeckException:
            self.end_of_round = True
        return last_card

    def __str__(self):
        return "deck: {0} \n crystals: {1}".format(self.deck, self.crystals)

    def get_status(self):
        status = "Deck Cards: {0}/{1}".format(len(self.deck), self.get_total_cards())
        status += "\n"
        status += "Crystals: {}".format(self.crystals)
        return status

    def print_status(self):
        # print "Last Discarded Card: {}".format(self.last_discarded_card())
        print self.get_status()

    def get_total_cards(self):
        return len(self.deck) + len(self.discard)


class Main(object):
    STATES = {
        'init': [
            'choose dummy',
            'exit',
        ],
        'choose dummy': [
            'norowas',
            'goldyx',
            'arythea',
            'tovak',
            'random',
        ],
        'dummy options': [
            'draw',
            'new round',
            'exit',
        ],
        'new round': [
            'add card',
            'add crystal',
        ],
        'add card': list(COLORS),
        'add crystal': list(COLORS)
    }

    def __init__(self):
        self.dummy = None
        self.new_crystal = None
        self.new_card = None
        self.last_input = None
        self.state = 'init'

    def run(self):
        self.clear_console()
        while not self.state == 'exit':
            self.present_status()
            self.present_options()
            self.get_input()
            self.process_input()
            self.clear_console()

    def present_status(self):
        print "STATE: {}".format(self.state.upper())

        if self.dummy:
            self.dummy.print_status()
            # print "Deck Cards: {0}/{1}".format(len(self.dummy.deck), self.dummy.get_total_cards())
            # print "Last Discarded Card: {}".format(self.dummy.last_discarded_card())
            # print "Crystals: {}".format(self.dummy.crystals)

    def present_options(self):

        print "Options:"
        print "========"
        for i, option in enumerate(self.STATES[self.state]):
            print "[{0}] {1}".format(i + 1, option)
        print "========"

    def get_input(self):
        r_input = raw_input()
        if len(r_input) == 0:
            r_input = 1
        self.last_input = int(r_input) - 1

    def init_state(self):
        self.state = self.STATES[self.state][self.last_input]

    def choose_dummy_state(self):
        if self.last_input == 0:
            norowas = MKDummy(prime_color=COLORS[-1], sec_color=COLORS[1])  #2 white 1 green
            self.dummy = norowas
        elif self.last_input == 1:
            goldyx = MKDummy(prime_color=COLORS[1], sec_color=COLORS[0])  #2 green 1 blue
            self.dummy = goldyx
        elif self.last_input == 2:
            arythea = MKDummy(prime_color=COLORS[2], sec_color=COLORS[-1])  #2 red 1 white
            self.dummy = arythea
        elif self.last_input == 3:
            tovak = MKDummy(prime_color=COLORS[0], sec_color=COLORS[2])  #2 blue 1 red
            self.dummy = tovak
        elif self.last_input == 4:
            self.last_input = random.randint(0, 3)
            return self.process_input()
        self.dummy.shuffle()
        self.state = 'dummy options'

    def dummy_options_state(self):
        if self.last_input == 0:
            self.dummy.resolve_turn()
            if self.dummy.end_of_round:
                self.state = 'new round'
        elif self.last_input == 1:
            self.state = 'new round'
        else:
            self.state = 'exit'

    def new_round_state(self):
        self.state = self.STATES[self.state][self.last_input]

    def add_card_or_crystal_state(self):
        if 'card' in self.state:
            self.new_card = COLORS[self.last_input]
        else:
            self.new_crystal = COLORS[self.last_input]
        if self.new_card and self.new_crystal:
            self.dummy.new_round_setup(self.new_card, self.new_crystal)
            self.new_card, self.new_crystal = None, None
            self.state = 'dummy options'
        else:
            self.state = 'new round'

    def process_input(self):
        if self.state == 'init':
            self.init_state()
            # self.state = self.STATES[self.state][self.last_input]
        elif self.state == 'choose dummy':
            self.choose_dummy_state()
            # if self.last_input == 0:
            #     norowas = MKDummy(prime_color=COLORS[-1], sec_color=COLORS[1])  #2 white 1 green
            #     self.dummy = norowas
            # elif self.last_input == 1:
            #     goldyx = MKDummy(prime_color=COLORS[1], sec_color=COLORS[0])  #2 green 1 blue
            #     self.dummy = goldyx
            # elif self.last_input == 2:
            #     arythea = MKDummy(prime_color=COLORS[2], sec_color=COLORS[-1])  #2 red 1 white
            #     self.dummy = arythea
            # elif self.last_input == 3:
            #     tovak = MKDummy(prime_color=COLORS[0], sec_color=COLORS[2])  #2 blue 1 red
            #     self.dummy = tovak
            # elif self.last_input == 4:
            #     self.last_input = random.randint(0, 3)
            #     return self.process_input()
            # self.dummy.shuffle()
            # self.state = 'dummy options'
        elif self.state == 'dummy options':
            self.dummy_options_state()
            # if self.last_input == 0:
            #     self.dummy.resolve_turn()
            #     if self.dummy.end_of_round:
            #         self.state = 'new round'
            # if self.last_input == 1:
            #     self.state = 'new round'
        elif self.state == 'new round':
            self.new_round_state()
            # self.state = self.STATES[self.state][self.last_input]
        elif self.state in ['add card', 'add crystal']:
            self.add_card_or_crystal_state()
            # if 'card' in self.state:
            #     self.new_card = COLORS[self.last_input]
            # else:
            #     self.new_crystal = COLORS[self.last_input]
            # if self.new_card and self.new_crystal:
            #     self.dummy.new_round_setup(self.new_card, self.new_crystal)
            #     self.new_card, self.new_crystal = None, None
            #     self.state = 'dummy options'
            # else:
            #     self.state = 'new round'

    def clear_console(self):
        print ("\n" * 100)


if __name__ == '__main__':
    app = Main()
    app.run()
