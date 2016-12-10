# -*- coding: utf-8 -*-
import random
from functools import partial

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
# from kivy.properties import ObjectProperty

from bot import MKDummy, COLORS


class BasicScreen(Screen):

    def __init__(self, **kwargs):
        description = kwargs.pop('description')
        self.options = kwargs.pop('options')

        super(BasicScreen, self).__init__(**kwargs)

        main_box = BoxLayout(orientation='vertical')
        self.screen_title = Label(text=self.name, font_size=30)
        self.screen_description = Label(text=description, font_size=30)
        main_box.add_widget(self.screen_title)
        main_box.add_widget(self.screen_description)

        options_box = BoxLayout()
        for opt in self.options:
            opt_button = Button(text=opt, font_size=30)

            # each button will bind on release to self.handle_button(opt)
            handle_btn_for_option = partial(self.handle_button, opt)
            opt_button.bind(on_release=handle_btn_for_option)
            options_box.add_widget(opt_button)

        main_box.add_widget(options_box)
        self.add_widget(main_box)

    def handle_button(self, option, button):
        self.screen_description.text = option
        # self.manager.current = option


class ChooseDummyScreen(BasicScreen):

    def handle_button(self, option, button):
        self.choose_dummy(option)

    def choose_dummy(self, option):
        if option == 'norowas':
            norowas = MKDummy(name=option, prime_color=COLORS[-1], sec_color=COLORS[1])  #2 white 1 green
            self.manager.dummy = norowas
        elif option == 'goldyx':
            goldyx = MKDummy(name=option, prime_color=COLORS[1], sec_color=COLORS[0])  #2 green 1 blue
            self.manager.dummy = goldyx
        elif option == 'arythea':
            arythea = MKDummy(name=option, prime_color=COLORS[2], sec_color=COLORS[-1])  #2 red 1 white
            self.manager.dummy = arythea
        elif option == 'tovak':
            tovak = MKDummy(name=option, prime_color=COLORS[0], sec_color=COLORS[2])  #2 blue 1 red
            self.manager.dummy = tovak
        elif option == 'random':
            return self.choose_dummy(random.choice(self.options[:-1]))
        self.manager.dummy.shuffle()
        self.manager.current = 'Dummy Options'


class DummyOptScreen(BasicScreen):
    def __init__(self, **kwargs):
        super(DummyOptScreen, self).__init__(**kwargs)

    def handle_button(self, option, button):
        if option == 'draw':
            self.draw()
        else:
            self.manager.current = 'New Round'

    def draw(self):
        self.manager.dummy.resolve_turn()
        self.update_description()
        if self.manager.dummy.end_of_round:
            self.manager.current = 'New Round'

    def update_title(self):
        if self.manager and self.manager.dummy:
            self.screen_title.text = self.manager.dummy.name

    def update_description(self):
        if self.manager and self.manager.dummy:
            self.screen_description.text = self.manager.dummy.get_status()

    def on_pre_enter(self):
        self.update_description()
        self.update_title()


class NewRoundScreen(BasicScreen):

    def __init__(self, **kwargs):
        super(NewRoundScreen, self).__init__(**kwargs)
        self.description_text = "Dummy is asking for the End of Round!"
        self.description_text += "\n\nNew Card: {0} \n New Crystal: {1}"

    def update_description(self):
        self.screen_description.text = self.description_text.format(
            self.manager.new_card,
            self.manager.new_crystal
        )

    def on_pre_enter(self):
        self.update_description()

    def handle_button(self, option, button):
        self.manager.current = option


class AddColorScreen(BasicScreen):

    def handle_button(self, option, button):
        self.add_card_or_crystal_state(option)

    def add_card_or_crystal_state(self, option):
        if 'card' in self.name.lower():
            self.manager.new_card = option
        else:
            self.manager.new_crystal = option
        if self.manager.new_card and self.manager.new_crystal:
            self.manager.dummy.new_round_setup(
                self.manager.new_card,
                self.manager.new_crystal
            )
            self.manager.new_card, self.manager.new_crystal = None, None
            self.manager.current = 'Dummy Options'
        else:
            self.manager.current = 'New Round'
