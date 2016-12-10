# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.core.window import Window

from kivy.uix.screenmanager import ScreenManager

from screens import DummyOptScreen, ChooseDummyScreen, NewRoundScreen, AddColorScreen
from bot import COLORS


Window.clearcolor = (1, 1, 1, 1)


class MKScreenManager(ScreenManager):

    def __init__(self, *args, **kwargs):
        super(MKScreenManager, self).__init__()
        self.dummy = None
        self.new_card = None
        self.new_crystal = None


class MKDummyApp(App):

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def build(self):
        sm = MKScreenManager()

        choose_dummy_screen = ChooseDummyScreen(
            name='Choose Dummy',
            options=[
                'norowas',
                'goldyx',
                'arythea',
                'tovak',
                'random',
            ],
            description='Pick any of these:'
        )
        sm.add_widget(choose_dummy_screen)

        dummy_screen = DummyOptScreen(
            name='Dummy Options',
            options=[
                'draw',
                'new round',
            ],
            description='description'
        )
        sm.add_widget(dummy_screen)

        new_round_Screen = NewRoundScreen(
            name='New Round',
            options=[
                'Add Card',
                'Add Crystal',
            ],
            description='description'
        )
        sm.add_widget(new_round_Screen)

        add_card = AddColorScreen(
            name='Add Card',
            options=list(COLORS),
            description='Choose the new Advanced Action card color:'
        )
        sm.add_widget(add_card)

        add_crystal = AddColorScreen(
            name='Add Crystal',
            options=list(COLORS),
            description='Choose the new Crystal color:'
        )
        sm.add_widget(add_crystal)

        return sm


MKDummyApp().run()
