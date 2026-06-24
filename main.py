import json
import os
import time
from datetime import datetime

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.core.audio import SoundLoader
from kivy.core.window import Window


# 🔥 УВЕЛИЧИЛИ ОБЩИЙ МАСШТАБ КНОПОК
UI_SCALE = 1.4


def scale(v):
    return int(v * UI_SCALE)


def animate_button(widget):
    if not hasattr(widget, "orig_size"):
        widget.orig_size = widget.size

    Animation.cancel_all(widget)
    w, h = widget.orig_size
    anim = Animation(size=(w * 0.92, h * 0.92), duration=0.05) + Animation(size=(w, h), duration=0.05)
    anim.start(widget)
    class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

        self.add_widget(BackgroundWidget(source='space.jpg'))

        # 📊 верхняя панель (увеличена)
        self.info_panel = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.25)
        )

        self.info = Label(font_size=scale(28), color=(1, 0.8, 0, 1))
        self.lvl_lbl = Label(font_size=scale(22))

        self.info_panel.add_widget(self.info)
        self.info_panel.add_widget(self.lvl_lbl)
        self.add_widget(self.info_panel)

        # 🎯 КНОПКИ (УВЕЛИЧЕНЫ)
        self.btn_quest = Button(
            background_normal='quest.png',
            size_hint=(None, None),
            size=(scale(110), scale(110)),
            pos_hint={'x': 0.03, 'top': 0.98}
        )
        self.btn_quest.bind(on_press=lambda x: setattr(self.manager, 'current', 'quests'))
        self.add_widget(self.btn_quest)

        self.btn_set = Button(
            background_normal='settings.png',
            size_hint=(None, None),
            size=(scale(110), scale(110)),
            pos_hint={'right': 0.97, 'top': 0.98}
        )
        self.btn_set.bind(on_press=lambda x: setattr(self.manager, 'current', 'settings'))
        self.add_widget(self.btn_set)

        # 🚀 КНОПКА КЛИКА (УВЕЛИЧЕНА)
        self.btn = Button(
            background_normal='ship.png',
            size_hint=(None, None),
            size=(scale(380), scale(380)),
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )
        self.btn.bind(on_press=self.on_click)
        self.add_widget(self.btn)

        # 🏪 магазин
        self.btn_shop = Button(
            background_normal='shop.png',
            size_hint=(None, None),
            size=(scale(110), scale(110)),
            pos_hint={'x': 0.03, 'y': 0.03}
        )
        self.btn_shop.bind(on_press=lambda x: setattr(self.manager, 'current', 'shop'))
        self.add_widget(self.btn_shop)

        # 👤 профиль
        self.btn_prof = Button(
            background_normal='profile.png',
            size_hint=(None, None),
            size=(scale(110), scale(110)),
            pos_hint={'right': 0.97, 'y': 0.03}
        )
        self.btn_prof.bind(on_press=lambda x: setattr(self.manager, 'current', 'profile'))
        self.add_widget(self.btn_prof)
        class ClickerApp(App):
    def build(self):
        # 🎵 ЗВУКИ
        self.sound_click = SoundLoader.load('click.mp3')
        self.sound_buy = SoundLoader.load('buy.mp3')
        self.music = SoundLoader.load('background.mp3')

        # 🔊 громкость
        if self.music:
            self.music.volume = 0.4

        # 📊 данные
        self.clicks = 0
        self.power = 1
        self.auto = 0

        self.sm = ScreenManager()
        self.sm.add_widget(LoadingScreen(name='load'))
        self.sm.add_widget(NameScreen(name='name'))
        self.sm.add_widget(GameScreen(name='game'))
        self.sm.add_widget(ShopScreen(name='shop'))
        self.sm.add_widget(ProfileScreen(name='profile'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        self.sm.add_widget(QuestsScreen(name='quests'))
        self.sm.add_widget(AchievementScreen(name='achievements'))

        self.sm.current = 'load'
        return self.sm

    def on_start(self):
        # 🎵 фоновая музыка
        if self.music:
            self.music.loop = True
            self.music.play()
            class GameScreen(Screen):
    def on_click(self, instance):
        animate_button(self.btn)

        # 🔊 звук клика
        app = App.get_running_app()
        if app.sound_click:
            app.sound_click.play()

        app.clicks += app.power
        self.update_ui()

    def update_ui(self):
        app = App.get_running_app()
        self.info.text = f"Coins: {app.clicks}"
        self.lvl_lbl.text = f"Level system"

# 🚀 запуск
if __name__ == "__main__":
    ClickerApp().run()
