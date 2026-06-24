# ===================== ЧАСТЬ 1 — IMPORTS + DATA =====================

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
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader
from kivy.core.window import Window


# ---------------- ЛОКАЛИЗАЦИЯ ---------------- #

LANGS = {
    "RU": {
        "shop": "Магазин",
        "profile": "Профиль",
        "back": "Назад",
        "settings": "Настройки",
        "quests": "Квесты",
        "achievements": "Достижения",
        "start": "Начать",
        "name_q": "Введите имя",
        "name_inp": "Ваше имя",
        "click": "Клик",
        "level": "Уровень",
        "exp": "Опыт",
        "cost": "Цена",
        "on": "ВКЛ",
        "off": "ВЫКЛ",
        "sound": "Звук",
        "lang": "Язык",
        "sake": "Саке",
        "clicks": "Клики",
        "player": "Игрок",
        "date": "Дата"
    },
    "EN": {
        "shop": "Shop",
        "profile": "Profile",
        "back": "Back",
        "settings": "Settings",
        "quests": "Quests",
        "achievements": "Achievements",
        "start": "Start",
        "name_q": "Enter name",
        "name_inp": "Your name",
        "click": "Click",
        "level": "Level",
        "exp": "EXP",
        "cost": "Cost",
        "on": "ON",
        "off": "OFF",
        "sound": "Sound",
        "lang": "Language",
        "sake": "Sake",
        "clicks": "Clicks",
        "player": "Player",
        "date": "Date"
    }
}


# ---------------- LEVEL SYSTEM ---------------- #

def get_level_title(level, lang):
    titles = {
        "RU": ["Новичок", "Ученик", "Опытный", "Мастер", "Легенда"],
        "EN": ["Novice", "Apprentice", "Experienced", "Master", "Legend"]
    }
    t = titles[lang]

    if level < 5:
        return t[0]
    elif level < 10:
        return t[1]
    elif level < 20:
        return t[2]
    elif level < 40:
        return t[3]
    return t[4]


# ---------------- ANIMATION ---------------- #

def animate_button(btn):
    Animation.cancel_all(btn)

    w, h = btn.size
    anim = Animation(size=(w * 0.9, h * 0.9), duration=0.05) + Animation(size=(w, h), duration=0.05)
    anim.start(btn)
    # ===================== ЧАСТЬ 2 — BASE WIDGETS + SCREENS =====================

class BackgroundWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.bg = Rectangle(pos=self.pos, size=Window.size)
        self.bind(pos=self.update, size=self.update)

    def update(self, *args):
        self.bg.pos = self.pos
        self.bg.size = Window.size


class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Loading...", font_size=40))

    def on_enter(self):
        app = App.get_running_app()
        Clock.schedule_once(lambda dt: setattr(self.manager, "current", "name"), 2)


class NameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical")

        self.lbl = Label(text="")
        self.input = TextInput(multiline=False)

        self.btn = Button(text="OK")
        self.btn.bind(on_press=self.save)

        layout.add_widget(self.lbl)
        layout.add_widget(self.input)
        layout.add_widget(self.btn)

        self.add_widget(layout)

    def on_enter(self):
        self.lbl.text = LANGS["RU"]["name_q"]

    def save(self, *args):
        app = App.get_running_app()
        app.player_name = self.input.text
        app.reg_date = str(datetime.now())
        app.save_game()
        self.manager.current = "game"


class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation="vertical")

        self.lbl = Label(text="")
        self.back = Button(text="Back")
        self.back.bind(on_press=lambda x: setattr(self.manager, "current", "game"))

        self.layout.add_widget(self.lbl)
        self.layout.add_widget(self.back)

        self.add_widget(self.layout)

    def on_enter(self):
        app = App.get_running_app()
        t = LANGS[app.lang]

        self.lbl.text = f"{t['player']}: {app.player_name}\n{t['clicks']}: {app.clicks}"
        # ===================== ЧАСТЬ 3 — SHOP =====================

class ShopScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation="vertical")

        self.lbl = Label(text="Shop")
        self.buy = Button(text="Buy +1")
        self.buy.bind(on_press=self.buy_item)

        self.back = Button(text="Back")
        self.back.bind(on_press=lambda x: setattr(self.manager, "current", "game"))

        self.layout.add_widget(self.lbl)
        self.layout.add_widget(self.buy)
        self.layout.add_widget(self.back)

        self.add_widget(self.layout)

    def buy_item(self, *args):
        app = App.get_running_app()
        if app.clicks >= app.price:
            app.clicks -= app.price
            app.power += 1
            app.price = int(app.price * 1.5)
            app.save_game()


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation="vertical")

        self.lbl = Label(text="Settings")

        self.sound_btn = Button(text="Sound")
        self.sound_btn.bind(on_press=self.toggle_sound)

        self.lang_btn = Button(text="Lang")
        self.lang_btn.bind(on_press=self.toggle_lang)

        self.back = Button(text="Back")
        self.back.bind(on_press=lambda x: setattr(self.manager, "current", "game"))

        self.layout.add_widget(self.lbl)
        self.layout.add_widget(self.sound_btn)
        self.layout.add_widget(self.lang_btn)
        self.layout.add_widget(self.back)

        self.add_widget(self.layout)

    def toggle_sound(self, *args):
        app = App.get_running_app()
        app.sound = not app.sound
        app.save_game()

    def toggle_lang(self, *args):
        app = App.get_running_app()
        app.lang = "EN" if app.lang == "RU" else "RU"
        app.save_game()


class QuestsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation="vertical")

        self.lbl = Label(text="Quests")

        self.back = Button(text="Back")
        self.back.bind(on_press=lambda x: setattr(self.manager, "current", "game"))

        self.layout.add_widget(self.lbl)
        self.layout.add_widget(self.back)

        self.add_widget(self.layout)
        # ===================== ЧАСТЬ 4 — GAME =====================

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()

        self.layout = BoxLayout(orientation="vertical")

        self.info = Label(text="")
        self.click_btn = Button(text="CLICK", font_size=40)

        self.click_btn.bind(on_press=self.click)

        self.shop = Button(text="Shop")
        self.shop.bind(on_press=lambda x: setattr(self.manager, "current", "shop"))

        self.settings = Button(text="Settings")
        self.settings.bind(on_press=lambda x: setattr(self.manager, "current", "settings"))

        self.profile = Button(text="Profile")
        self.profile.bind(on_press=lambda x: setattr(self.manager, "current", "profile"))

        self.layout.add_widget(self.info)
        self.layout.add_widget(self.click_btn)
        self.layout.add_widget(self.shop)
        self.layout.add_widget(self.settings)
        self.layout.add_widget(self.profile)

        self.add_widget(self.layout)

    def click(self, *args):
        app = App.get_running_app()
        animate_button(self.click_btn)

        app.clicks += app.power
        app.total_clicks += 1
        app.add_exp(5)

    def on_enter(self):
        self.update()

    def update(self):
        app = App.get_running_app()
        self.info.text = f"Clicks: {app.clicks} | Level: {app.level}"
        # ===================== ЧАСТЬ 5 — APP + RUN =====================

class ClickerApp(App):

    def build(self):
        self.clicks = 0
        self.power = 1
        self.price = 100
        self.total_clicks = 0

        self.level = 1
        self.exp = 0

        self.player_name = ""
        self.reg_date = ""

        self.lang = "RU"
        self.sound = True

        self.sm = ScreenManager()

        self.sm.add_widget(LoadingScreen(name="load"))
        self.sm.add_widget(NameScreen(name="name"))
        self.sm.add_widget(GameScreen(name="game"))
        self.sm.add_widget(ShopScreen(name="shop"))
        self.sm.add_widget(ProfileScreen(name="profile"))
        self.sm.add_widget(SettingsScreen(name="settings"))
        self.sm.add_widget(QuestsScreen(name="quests"))

        self.sm.current = "load"
        return self.sm

    def add_exp(self, val):
        self.exp += val
        if self.exp >= 100:
            self.level += 1
            self.exp = 0

    def save_game(self):
        data = {
            "clicks": self.clicks,
            "power": self.power,
            "price": self.price,
            "total_clicks": self.total_clicks,
            "level": self.level,
            "exp": self.exp,
            "player_name": self.player_name,
            "reg_date": self.reg_date,
            "lang": self.lang,
            "sound": self.sound
        }

        with open("save.json", "w") as f:
            json.dump(data, f)

    def load_game(self):
        if os.path.exists("save.json"):
            with open("save.json", "r") as f:
                d = json.load(f)
                self.clicks = d.get("clicks", 0)
                self.power = d.get("power", 1)
                self.price = d.get("price", 100)
                self.total_clicks = d.get("total_clicks", 0)
                self.level = d.get("level", 1)
                self.exp = d.get("exp", 0)
                self.player_name = d.get("player_name", "")
                self.reg_date = d.get("reg_date", "")
                self.lang = d.get("lang", "RU")
                self.sound = d.get("sound", True)


if __name__ == "__main__":
    ClickerApp().run()
