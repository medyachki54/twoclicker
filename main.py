import json
import os
import time
from datetime import datetime
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.core.audio import SoundLoader
from kivy.core.window import Window

# --- ЛОКАЛИЗАЦИЯ ---
LANGS = {
    'RU': {
        'shop': 'Магазин', 'prof': 'Профиль', 'back': 'Назад', 
        'snd': 'Звук: ', 'lng': 'Язык: РУ', 'on': 'ВКЛ', 'off': 'ВЫКЛ', 
        'sake': 'Саке: ', 'load': 'Загрузка игры...',
        'name_q': 'Как вас зовут?', 'name_inp': 'Ваше имя...', 'start': 'Начать игру',
        'click': 'Кликай!', 'buy_pwr': 'Сила: ', 'buy_auto': 'Авто: ',
        'player': 'Игрок: ', 'date': 'Дата: ', 'power': 'Сила: ',
        'auto': 'Авто: ', 'sec': '/с', 'clicks': 'Кликов: ', 
        'time': 'Время: ', 'h': 'ч ', 'm': 'мин', 'quests': 'Квесты',
        'claim': 'Забрать', 'timer': 'До сброса: ', 'level': 'Уровень: ',
        'exp': 'EXP: ', 'q_time': '10 мин игры', 'q_save1': '1000 саке', 'q_save5': '5000 саке',
        'q_click250': '250 кликов', 'q_click500': '500 кликов',
        'q_login1': 'Зайти в игру', 'q_shop': 'Покупка в магазине',
        'gift': 'Подарок (+200)', 'achs': 'Достижения',
        'reset_btn': 'Сбросить прогресс', 'change_name': 'Изменить имя',
        'max_lvl': 'МАКС. УРОВЕНЬ'
    },
    'EN': {
        'shop': 'Shop', 'prof': 'Profile', 'back': 'Back', 
        'snd': 'Sound: ', 'lng': 'Lang: EN', 'on': 'ON', 'off': 'OFF', 
        'sake': 'Sake: ', 'load': 'Loading...',
        'name_q': 'What is your name?', 'name_inp': 'Your name...', 'start': 'Start Game',
        'click': 'Click!', 'buy_pwr': 'Power: ', 'buy_auto': 'Auto: ',
        'player': 'Player: ', 'date': 'Date: ', 'power': 'Power: ',
        'auto': 'Auto: ', 'sec': '/s', 'clicks': 'Clicks: ', 
        'time': 'Time: ', 'h': 'h ', 'm': 'm', 'quests': 'Quests',
        'claim': 'Claim', 'timer': 'Reset in: ', 'level': 'Level: ',
        'exp': 'EXP: ', 'q_time': '10 min play', 'q_save1': '1000 sake', 'q_save5': '5000 sake',
        'q_click250': '250 clicks', 'q_click500': '500 clicks',
        'q_login1': 'Login', 'q_shop': 'Shop purchase',
        'gift': 'Gift (+200)', 'achs': 'Achievements',
        'reset_btn': 'Reset Progress', 'change_name': 'Change Name',
        'max_lvl': 'MAX LEVEL'
    }
}

def get_level_title(level, lang):
    titles = {
        'RU': ["Новичок", "Ученик", "Адепт", "Опытный", "Воин", "Мастер", "Ронин", "Самурай", "Сёгун", "Лорд", "Император"],
        'EN': ["Novice", "Apprentice", "Adept", "Experienced", "Warrior", "Master", "Ronin", "Samurai", "Shogun", "Lord", "Emperor"]
    }
    t = titles[lang]
    if level < 5: return t[0]
    elif level < 12: return t[1]
    elif level < 20: return t[2]
    elif level < 30: return t[3]
    elif level < 40: return t[4]
    elif level < 50: return t[5]
    elif level < 60: return t[6]
    elif level < 72: return t[7]
    elif level < 85: return t[8]
    elif level < 95: return t[9]
    return t[10]

def animate_button(widget):
    anim = Animation(size=(widget.width * 0.9, widget.height * 0.9), duration=0.05) + Animation(size=(widget.width, widget.height), duration=0.05)
    anim.start(widget)

class BackgroundWidget(Widget):
    def __init__(self, source='space.jpg', **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.bg_rect = Rectangle(source=source, pos=self.pos, size=Window.size)
            Color(0, 0, 0, 0.5)
            self.dark_rect = Rectangle(pos=self.pos, size=Window.size)
        self.bind(pos=self.update, size=self.update)

    def update(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = Window.size
        self.dark_rect.pos = self.pos
        self.dark_rect.size = Window.size

class RoundedFrame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 0.8)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20,])
        self.bind(pos=self.update, size=self.update)
    def update(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(BackgroundWidget(source='space.jpg'))
        self.lbl = Label(text="", font_size=40)
        self.add_widget(self.lbl)
    
    def on_enter(self):
        app = App.get_running_app()
        self.lbl.text = LANGS[app.lang]['load']
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'name' if not app.player_name else 'game'), 2)

class NameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(BackgroundWidget(source='space.jpg'))
        layout = BoxLayout(orientation='vertical', padding=80, spacing=30)
        self.lbl = Label(text="", font_size=40, color=(1, 0, 0, 1))
        layout.add_widget(self.lbl)
        self.name_input = TextInput(multiline=False, font_size=30, size_hint=(1, None), height=80)
        layout.add_widget(self.name_input)
        self.btn = Button(size_hint=(1, 0.2), font_size=32, color=(1, 0, 0, 1))
        self.btn.bind(on_press=self.save_name)
        layout.add_widget(self.btn)
        self.add_widget(layout)

    def on_enter(self):
        t = LANGS[App.get_running_app().lang]
        self.lbl.text = t['name_q']
        self.name_input.hint_text = t['name_inp']
        self.btn.text = t['start']

    def save_name(self, instance):
        app = App.get_running_app()
        if self.name_input.text.strip():
            app.player_name = self.name_input.text
            app.reg_date = datetime.now().strftime("%d.%m.%Y %H:%M")
            app.save_game()
            self.manager.current = 'game'

class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(BackgroundWidget(source='space.jpg'))
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        layout.add_widget(Widget(size_hint_y=0.2))
        
        # Красивая рама
        self.frame = RoundedFrame(orientation='vertical', padding=20, spacing=10, size_hint=(0.9, 0.5), pos_hint={'center_x': 0.5})
        self.label = Label(text="", font_size=24, markup=True, color=(1, 1, 1, 1))
        self.frame.add_widget(self.label)
        layout.add_widget(self.frame)
        
        btn_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, 0.2))
        self.btn_achs = Button(text="", size_hint=(1, 0.4))
        self.btn_achs.bind(on_press=lambda x: setattr(self.manager, 'current', 'achievements'))
        self.btn_back = Button(text="", size_hint=(1, 0.4))
        self.btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'game'))
        btn_layout.add_widget(self.btn_achs)
        btn_layout.add_widget(self.btn_back)
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)

    def on_enter(self):
        app = App.get_running_app()
        t = LANGS[app.lang]
        h, m = divmod(app.play_time // 60, 60)
        title = get_level_title(app.level, app.lang)
        stats = f"[b]{t['player']}[/b]{app.player_name}\n\n[b]{t['level']}[/b]{app.level}/100 ({title})\n[b]{t['date']}[/b]{app.reg_date}\n[b]{t['power']}[/b]{app.power}\n[b]{t['auto']}[/b]{app.auto}{t['sec']}\n[b]{t['clicks']}[/b]{app.total_clicks}\n[b]{t['time']}[/b]{h}{t['h']} {m}{t['m']}"
        self.label.text = stats
        self.btn_back.text = t['back']
        self.btn_achs.text = t['achs']

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.add_widget(BackgroundWidget(source='space.jpg'))
        
        self.info_panel = BoxLayout(orientation='vertical', size_hint=(1, 0.2), pos_hint={'top': 0.98})
        self.info = Label(text='', font_size=30)
        self.lvl_lbl = Label(text='', font_size=24) 
        self.info_panel.add_widget(self.info)
        self.info_panel.add_widget(self.lvl_lbl)
        self.add_widget(self.info_panel)
        
        # Кнопки навигации (картинки)
        self.btn_quest = Button(background_normal='quest.png', size_hint=(None, None), size=(100, 100), pos_hint={'x': 0.05, 'top': 0.98})
        self.btn_quest.bind(on_press=lambda x: setattr(self.manager, 'current', 'quests'))
        self.add_widget(self.btn_quest)
        
        self.btn_set = Button(background_normal='settings.png', size_hint=(None, None), size=(100, 100), pos_hint={'right': 0.95, 'top': 0.98})
        self.btn_set.bind(on_press=lambda x: setattr(self.manager, 'current', 'settings'))
        self.add_widget(self.btn_set)

        self.btn = Button(background_normal='ship.png', size_hint=(None, None), size=(350, 350), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.btn.bind(on_press=self.on_click)
        self.add_widget(self.btn)
        
        nav = BoxLayout(size_hint=(1, None), height=120, pos_hint={'bottom': 0}, spacing=10)
        self.btn_shop = Button(background_normal='shop.png', text='Shop', size_hint=(0.5, 1))
        self.btn_shop.bind(on_press=lambda x: setattr(self.manager, 'current', 'shop'))
        self.btn_prof = Button(background_normal='profile.png', text='Profile', size_hint=(0.5, 1))
        self.btn_prof.bind(on_press=lambda x: setattr(self.manager, 'current', 'profile'))
        nav.add_widget(self.btn_shop)
        nav.add_widget(self.btn_prof)
        self.add_widget(nav)

    def on_click(self, instance):
        if self.app.sound and self.app.sound_click:
            self.app.sound_click.play()
        self.app.clicks += self.app.power
        self.app.total_clicks += 1
        self.app.save_game()
        self.update_ui()

    def update_ui(self):
        t = LANGS[self.app.lang]
        self.info.text = f"{t['sake']}{int(self.app.clicks)}"
        self.lvl_lbl.text = f"{t['level']}{self.app.level}"

    def on_enter(self): self.update_ui()

class ClickerApp(App):
    def build(self):
        # Загрузка звуков
        self.sound_click = SoundLoader.load('click.mp3')
        self.sound_buy = SoundLoader.load('buy.mp3')
        self.music = SoundLoader.load('background.mp3')
        if self.music:
            self.music.loop = True
            self.music.volume = 0.3
            self.music.play()

        # Параметры (начальные)
        self.clicks = 0
        self.power = 1
        self.auto = 0
        self.price_p = 350
        self.price_a = 450
        self.player_name = ''
        self.reg_date = ''
        self.play_time = 0
        self.total_clicks = 0
        self.pwr_bought = 0
        self.auto_bought = 0
        self.level = 1
        self.current_exp = 0
        self.exp_goal = 250
        self.ach_status = {}
        self.lang = 'RU'
        self.sound = True
        self.last_quest_reset = time.time()
        self.last_gift_time = 0
        self.quests = {'c1':0, 'c2':0, 'c3':1, 'time':0, 'save':0, 'save5':0} 
        
        self.load_game()
        
        sm = ScreenManager()
        sm.add_widget(LoadingScreen(name='load'))
        sm.add_widget(NameScreen(name='name'))
        sm.add_widget(GameScreen(name='game'))
        # Добавьте остальные экраны (ShopScreen, AchievementScreen и т.д.) аналогично
        sm.current = 'load'
        return sm
    
    def save_game(self):
        save_data = {
            'clicks': self.clicks, 'power': self.power, 'auto': self.auto,
            'total_clicks': self.total_clicks, 'name': self.player_name, 
            'level': self.level, 'lang': self.lang
        }
        with open('save.json', 'w', encoding='utf-8') as f: 
            json.dump(save_data, f, ensure_ascii=False)

    def load_game(self):
        if os.path.exists('save.json'):
            with open('save.json', 'r', encoding='utf-8') as f:
                d = json.load(f)
                self.clicks = d.get('clicks', 0)
                self.player_name = d.get('name', '')

if __name__ == '__main__':
    ClickerApp().run()
