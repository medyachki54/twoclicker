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
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.core.audio import SoundLoader

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
    if lang == 'RU':
        if level < 5: return "Новичок"
        elif level < 12: return "Ученик"
        elif level < 20: return "Адепт"
        elif level < 30: return "Опытный"
        elif level < 40: return "Воин"
        elif level < 50: return "Мастер"
        elif level < 60: return "Ронин"
        elif level < 72: return "Самурай"
        elif level < 85: return "Сёгун"
        elif level < 95: return "Лорд"
        else: return "Император"
    else:
        if level < 5: return "Novice"
        elif level < 12: return "Apprentice"
        elif level < 20: return "Adept"
        elif level < 30: return "Experienced"
        elif level < 40: return "Warrior"
        elif level < 50: return "Master"
        elif level < 60: return "Ronin"
        elif level < 72: return "Samurai"
        elif level < 85: return "Shogun"
        elif level < 95: return "Lord"
        else: return "Emperor"

def animate_button(widget):
    w, h = widget.width, widget.height
    anim = Animation(size=(w * 0.9, h * 0.9), duration=0.05) + Animation(size=(w, h), duration=0.05)
    anim.start(widget)

class BackgroundWidget(Widget):
    def __init__(self, source, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        with self.canvas.before:
            self.bg_rect = Rectangle(source=source, pos=self.pos, size=self.size)
            self.dark_color = Color(0, 0, 0, 0.5)
            self.dark_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.dark_rect.pos = self.pos
        self.dark_rect.size = self.size

class RoundedIconButton(ButtonBehavior, FloatLayout):
    def __init__(self, text='', icon='', **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (300, 300)
        self.img = Image(source=icon, allow_stretch=True, keep_ratio=True, size_hint=(1, 0.7), pos_hint={'center_x': 0.5, 'top': 1})
        self.add_widget(self.img)
        self.lbl = Label(text=text, font_size=24, size_hint=(1, 0.3), pos_hint={'center_x': 0.5, 'y': 0})
        self.add_widget(self.lbl)
    def on_press(self): animate_button(self)

class AchievementScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg = BackgroundWidget(source='space.jpg')
        self.add_widget(self.bg)
        layout = BoxLayout(orientation='vertical', padding=20)
        scroll = ScrollView()
        self.container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.container.bind(minimum_height=self.container.setter('height'))
        scroll.add_widget(self.container)
        layout.add_widget(scroll)
        btn_back = Button(text="Назад", size_hint=(1, 0.08))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'profile'))
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def on_pre_enter(self):
        self.bg.size = self.size

    def on_enter(self):
        self.container.clear_widgets()
        app = App.get_running_app()
        app.check_achievements()
        for ach in app.achievements:
            is_done = app.ach_status.get(ach['name'], False)
            bg_color = (0, 0.6, 0, 1) if is_done else (0.4, 0.4, 0.4, 1)
            btn = Button(text=f"{ach['name']}", size_hint_y=None, height=100, background_normal='', background_color=bg_color)
            self.container.add_widget(btn)

class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg = BackgroundWidget(source='space.jpg')
        self.add_widget(self.bg)
        self.lbl = Label(text="", font_size=40)
        self.add_widget(self.lbl)

    def on_pre_enter(self):
        self.bg.size = self.size

    def on_enter(self):
        app = App.get_running_app()
        self.lbl.text = LANGS[app.lang]['load']
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'name' if not app.player_name else 'game'), 2)

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.bg = BackgroundWidget(source='space.jpg')
        self.add_widget(self.bg)
        
        main_layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        self.name_input = TextInput(multiline=False, font_size=28, size_hint=(1, None), height=60, hint_text="")
        self.b_change_name = Button(size_hint=(1, None), height=60)
        self.b_change_name.bind(on_press=self.change_name)
        
        main_layout.add_widget(Widget())
        main_layout.add_widget(self.name_input)
        main_layout.add_widget(self.b_change_name)

        self.b_snd = Button(size_hint=(1, None), height=60)
        self.b_lng = Button(size_hint=(1, None), height=60)
        self.b_reset = Button(size_hint=(1, None), height=60, background_color=(0.8, 0, 0, 1))
        self.b_back = Button(size_hint=(1, None), height=60)
        
        self.b_snd.bind(on_press=self.toggle_sound)
        self.b_lng.bind(on_press=self.toggle_lang)
        self.b_reset.bind(on_press=self.reset_progress)
        self.b_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'game'))
        
        main_layout.add_widget(self.b_snd)
        main_layout.add_widget(self.b_lng)
        main_layout.add_widget(self.b_reset)
        main_layout.add_widget(self.b_back)
        
        self.add_widget(main_layout)

    def on_pre_enter(self):
        self.bg.size = self.size

    def change_name(self, instance):
        new_name = self.name_input.text.strip()
        if new_name:
            self.app.player_name = new_name
            self.name_input.text = ""
            self.app.save_game()

    def reset_progress(self, instance):
        self.app.clicks = 0
        self.app.power = 1
        self.app.auto = 0
        self.app.price_p = 350
        self.app.price_a = 450
        self.app.total_clicks = 0
        self.app.pwr_bought = 0
        self.app.auto_bought = 0
        self.app.level = 1
        self.app.current_exp = 0
        self.app.exp_goal = 250
        self.app.ach_status = {}
        self.app.last_gift_time = 0
        self.app.quests = {'c1':0, 'c2':0, 'c3':1, 'time':0, 'save':0, 'save5':0}
        self.app.save_game()
        self.manager.current = 'name'

    def toggle_sound(self, instance):
        self.app.sound = not self.app.sound
        if self.app.music:
            if self.app.sound: self.app.music.play()
            else: self.app.music.stop()
        self.app.save_game()
        self.update_ui()
        
    def toggle_lang(self, instance): 
        self.app.lang = 'EN' if self.app.lang == 'RU' else 'RU'
        self.app.save_game()
        self.update_ui()

    def update_ui(self):
        t = LANGS.get(self.app.lang, LANGS['RU'])
        self.b_snd.text = t['snd'] + (t['on'] if self.app.sound else t['off'])
        self.b_lng.text = t['lng']
        self.b_back.text = t['back']
        self.b_reset.text = t['reset_btn']
        self.b_change_name.text = t['change_name']
        self.name_input.hint_text = t['name_inp']

    def on_enter(self): 
        self.update_ui()

class NameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg = BackgroundWidget(source='space.jpg')
        self.add_widget(self.bg)

        layout = BoxLayout(orientation='vertical', padding=80, spacing=30)
        self.lbl = Label(text="", font_size=40, color=(1, 0, 0, 1))
        layout.add_widget(self.lbl)
        self.name_input = TextInput(multiline=False, font_size=30, size_hint=(1, None), height=80)
        layout.add_widget(self.name_input)
        self.btn = Button(size_hint=(1, 0.2), font_size=32, color=(1, 0, 0, 1))
        self.btn.bind(on_press=self.save_name)
        layout.add_widget(self.btn)
        self.add_widget(layout)

    def on_pre_enter(self):
        self.bg.size = self.size

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

class QuestScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.bg = BackgroundWidget(source='space.jpg')
        self.add_widget(self.bg)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.timer_lbl = Label(text="", size_hint_y=0.1)
        self.layout.add_widget(self.timer_lbl)
        scroll = ScrollView()
        self.container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.container.bind(minimum_height=self.container.setter('height'))
        scroll.add_widget(self.container)
        self.layout.add_widget(scroll)
        self.btn_back = Button(size_hint=(1, 0.15))
        self.btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'game'))
        self.layout.add_widget(self.btn_back)
        self.add_widget(self.layout)
        Clock.schedule_interval(self.update_timer, 1)

    def on_pre_enter(self):
        self.bg.size = self.size

    def update_timer(self, dt):
        if self.manager.current == 'quests':
            t = LANGS[self.app.lang]
            rem = max(0, 3600 - (time.time() - self.app.last_quest_reset))
            m, s = divmod(int(rem), 60)
            self.timer_lbl.text = f"{t['timer']} {m:02d}:{s:02d}"

    def on_enter(self):
        t = LANGS[self.app.lang]
        self.btn_back.text = t['back']
        self.container.clear_widgets()
        
        self.app.quests['time'] = self.app.play_time // 60
        self.app.quests['c1'] = int(self.app.total_clicks)
        self.app.quests['c2'] = int(self.app.total_clicks)
        self.app.quests['save'] = int(self.app.clicks)
        self.app.quests['save5'] = int(self.app.clicks)
        
        quests = [
            (t['q_click250'], 250, 'c1', 150),
            (t['q_click500'], 500, 'c2', 300),
            (t['q_time'], 10, 'time', 100),
            (t['q_save1'], 1000, 'save', 500),
            (t['q_save5'], 5000, 'save5', 2500),
            (t['q_login1'], 1, 'c3', 300),
        ]
        
        for name, goal, key, reward in quests:
            if key == 'c3' and self.app.quests.get('c3_done', False): continue
            box = BoxLayout(size_hint_y=None, height=100)
            progress = min(self.app.quests.get(key, 0), goal)
            box.add_widget(Label(text=f"{name}: {progress}/{goal}"))
            if not self.app.quests.get(f"{key}_done", False):
                is_done = progress >= goal
                btn = Button(text=t['claim'], size_hint_x=0.3, background_normal='', 
                             background_color=(0, 0.6, 0, 1) if is_done else (0.4, 0.4, 0.4, 1))
                if is_done:
                    btn.bind(on_press=lambda x, k=key, r=reward: self.claim(k, r))
                box.add_widget(btn)
            self.container.add_widget(box)

    def claim(self, key, reward):
        self.app.quests[f"{key}_done"] = True
        self.app.clicks += reward
        self.app.save_game()
        self.on_enter()

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.bg = BackgroundWidget(source='space.jpg')
        self.add_widget(self.bg)
        
        self.info_panel = BoxLayout(orientation='vertical', size_hint=(1, 0.2), pos_hint={'top': 0.98})
        self.info = Label(text='', font_size=40)
        self.lvl_lbl = Label(text='', font_size=34) 
        self.exp_lbl = Label(text='', font_size=34)
        self.info_panel.add_widget(self.info)
        self.info_panel.add_widget(self.lvl_lbl)
        self.info_panel.add_widget(self.exp_lbl)
        self.add_widget(self.info_panel)
        
        self.btn_quest = Button(background_normal='quest.png', size_hint=(None, None), size=(120, 120), pos_hint={'x': 0.05, 'top': 0.98})
        self.btn_quest.bind(on_press=lambda x: setattr(self.manager, 'current', 'quests'))
        self.add_widget(self.btn_quest)
        self.btn_set = Button(background_normal='settings.png', size_hint=(None, None), size=(120, 120), pos_hint={'right': 0.95, 'top': 0.98})
        self.btn_set.bind(on_press=lambda x: setattr(self.manager, 'current', 'settings'))
        self.add_widget(self.btn_set)

        self.lbl_click = Label(text="", font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.75})
        self.add_widget(self.lbl_click)
        self.btn = Button(background_normal='ship.png', size_hint=(None, None), size=(450, 450), pos_hint={'center_x': 0.5, 'center_y': 0.45})
        self.btn.bind(on_press=self.on_click)
        self.add_widget(self.btn)
        
        nav = BoxLayout(size_hint=(1, None), height=150, pos_hint={'bottom': 0}, padding=20, spacing=20)
        self.btn_shop = Button(background_normal='shop.png', size_hint=(0.5, 1))
        self.btn_shop.bind(on_press=lambda x: setattr(self.manager, 'current', 'shop'))
        self.btn_prof = Button(background_normal='profile.png', size_hint=(0.5, 1))
        self.btn_prof.bind(on_press=lambda x: setattr(self.manager, 'current', 'profile'))
        nav.add_widget(self.btn_shop)
        nav.add_widget(self.btn_prof)
        self.add_widget(nav)

    def on_pre_enter(self):
        self.bg.size = self.size

    def on_click(self, instance):
        if self.app.sound and self.app.sound_click:
            self.app.sound_click.stop()
            self.app.sound_click.play()
        self.app.clicks += self.app.power
        self.app.total_clicks += 1
        self.app.quests['c1'] = self.app.total_clicks
        self.app.quests['c2'] = self.app.total_clicks
        self.app.quests['save'] = self.app.clicks
        self.app.quests['save5'] = self.app.clicks
        if self.app.level < 100:
            self.app.current_exp += 1 
            if self.app.current_exp >= self.app.exp_goal:
                self.app.level = min(100, self.app.level + 1)
                self.app.current_exp = 0
                self.app.exp_goal *= 2 
                self.app.clicks += 500
        self.app.check_achievements() 
        self.app.save_game()
        self.update_ui()

    def update_ui(self):
        t = LANGS[self.app.lang]
        title = get_level_title(self.app.level, self.app.lang)
        self.info.text = f"{t['sake']}{int(self.app.clicks)}"
        self.lvl_lbl.text = f"{t['level']}{self.app.level} / 100 [{title}]"
        if self.app.level >= 100:
            self.exp_lbl.text = t['max_lvl']
        else:
            self.exp_lbl.text = f"{t['exp']}{self.app.current_exp}/{self.app.exp_goal}"
        self.lbl_click.text = t['click']
        self.btn_shop.text = t['shop']
        self.btn_prof.text = t['prof']

    def on_enter(self): 
        self.update_ui()

class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg = BackgroundWidget(source='space.jpg')
        self.add_widget(self.bg)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Widget(size_hint_y=0.2))
        self.label = Label(text="", font_size=30, markup=True, color=(1, 0, 0, 1), size_hint=(1, 0.4))
        layout.add_widget(self.label)
        self.btn_achs = Button(text="", size_hint=(1, 0.08))
        self.btn_achs.bind(on_press=lambda x: setattr(self.manager, 'current', 'achievements'))
        layout.add_widget(self.btn_achs)
        self.btn_back = Button(size_hint=(1, 0.08))
        self.btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'game'))
        layout.add_widget(self.btn_back)
        self.add_widget(layout)
        
    def on_pre_enter(self):
        self.bg.size = self.size
        if os.path.exists('profile.jpg'):
            self.bg.bg_rect.source = 'profile.jpg'
        else:
            self.bg.bg_rect.source = 'space.jpg'

    def on_enter(self):
        app = App.get_running_app()
        t = LANGS[app.lang]
        h, m = divmod(app.play_time // 60, 60)
        title = get_level_title(app.level, app.lang)
        stats = f"{t['player']}{app.player_name}\n{t['level']}{app.level}/100 ({title})\n{t['date']}{app.reg_date}\n{t['power']}{app.power}\n{t['auto']}{app.auto}{t['sec']}\n{t['clicks']}{app.total_clicks}\n{t['time']}{h}{t['h']} {m}{t['m']}"
        self.label.text = stats
        self.btn_back.text = t['back']
        self.btn_achs.text = t['achs']

class ShopScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.bg = BackgroundWidget(source='space.jpg')
        self.add_widget(self.bg)
        center_box = BoxLayout(orientation='vertical', size_hint=(0.8, 0.3), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        self.lbl_bal = Label(text='', font_size=60, color=(1, 0, 0, 1))
        self.timer_lbl = Label(text="", font_size=30)
        center_box.add_widget(self.lbl_bal)
        center_box.add_widget(self.timer_lbl)
        self.add_widget(center_box)
        btn_layout = BoxLayout(orientation='vertical', size_hint=(0.9, 0.4), pos_hint={'center_x': 0.5, 'bottom': 0.05}, spacing=15)
        self.b_gift = Button(size_hint_y=None, height=120)
        self.b_gift.bind(on_press=self.claim_gift)
        self.b1 = Button(size_hint_y=None, height=120)
        self.b1.bind(on_press=lambda x: self.buy(True))
        self.b2 = Button(size_hint_y=None, height=120)
        self.b2.bind(on_press=lambda x: self.buy(False))
        self.btn_back = Button(size_hint_y=None, height=120)
        self.btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'game'))
        btn_layout.add_widget(self.b_gift)
        btn_layout.add_widget(self.b1)
        btn_layout.add_widget(self.b2)
        btn_layout.add_widget(self.btn_back)
        self.add_widget(btn_layout)
        Clock.schedule_interval(self.update_timer, 1)

    def on_pre_enter(self):
        self.bg.size = self.size

    def update_timer(self, dt):
        t = LANGS[self.app.lang]
        rem = max(0, 86400 - (time.time() - self.app.last_gift_time))
        h, rem = divmod(int(rem), 3600)
        m, s = divmod(rem, 60)
        self.timer_lbl.text = f"{t['timer']} {h:02d}:{m:02d}:{s:02d}" if self.app.last_gift_time != 0 else ""

    def claim_gift(self, instance):
        if time.time() - self.app.last_gift_time >= 86400 or self.app.last_gift_time == 0:
            self.app.clicks += 200
            self.app.last_gift_time = time.time()
            self.app.save_game()
            self.update_ui()

    def buy(self, is_power):
        price = self.app.price_p if is_power else self.app.price_a
        if self.app.clicks >= price:
            if self.app.sound and self.app.sound_buy: self.app.sound_buy.play()
            self.app.clicks -= price
            if is_power: 
                self.app.power += 1
                self.app.pwr_bought += 1
                self.app.price_p *= 2
            else: 
                self.app.auto += 1
                self.app.auto_bought += 1
                self.app.price_a *= 2
            self.app.save_game()
            self.update_ui()

    def update_ui(self):
        t = LANGS[self.app.lang]
        self.lbl_bal.text = f"{t['sake']}{int(self.app.clicks)}"
        self.b_gift.text = t['gift']
        self.b1.text = f"{t['buy_pwr']}{int(self.app.price_p)}"
        self.b2.text = f"{t['buy_auto']}{int(self.app.price_a)}"
        self.btn_back.text = t['back']

    def on_enter(self): 
        self.update_ui()

class ClickerApp(App):
    def build(self):
        self.sound_click = SoundLoader.load('click.mp3')
        self.sound_buy = SoundLoader.load('buy.mp3')
        self.music = SoundLoader.load('background.mp3')
        if self.music:
            self.music.loop = True
            self.music.volume = 0.5
            self.music.play()

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
        
        self.achievements = [
            {'name': '1 клик', 'check': lambda a: a.total_clicks >= 1},
            {'name': '100 кликов', 'check': lambda a: a.total_clicks >= 100},
            {'name': '500 кликов', 'check': lambda a: a.total_clicks >= 500},
            {'name': '1000 кликов', 'check': lambda a: a.total_clicks >= 1000},
            {'name': '5000 кликов', 'check': lambda a: a.total_clicks >= 5000},
            {'name': '10000 кликов', 'check': lambda a: a.total_clicks >= 10000},
            {'name': '20000 кликов', 'check': lambda a: a.total_clicks >= 20000},
            {'name': '50000 кликов', 'check': lambda a: a.total_clicks >= 50000},
            {'name': '1000000 кликов', 'check': lambda a: a.total_clicks >= 1000000},
            {'name': '5 раз силу клика', 'check': lambda a: a.pwr_bought >= 5},
            {'name': '10 раз силу клика', 'check': lambda a: a.pwr_bought >= 10},
            {'name': '30 раз силу клика', 'check': lambda a: a.pwr_bought >= 30},
            {'name': '50 раз силу клика', 'check': lambda a: a.pwr_bought >= 50},
            {'name': '5 раз Автоклик', 'check': lambda a: a.auto_bought >= 5},
            {'name': '10 раз автоклик', 'check': lambda a: a.auto_bought >= 10},
            {'name': '30 раз автоклик', 'check': lambda a: a.auto_bought >= 30},
            {'name': '50 раз автоклик', 'check': lambda a: a.auto_bought >= 50}
        ]
        
        self.load_game()
        Clock.schedule_interval(self.tick, 1.0)
        sm = ScreenManager()
        sm.add_widget(LoadingScreen(name='load'))
        sm.add_widget(NameScreen(name='name'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(ShopScreen(name='shop'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(AchievementScreen(name='achievements'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(QuestScreen(name='quests'))
        sm.current = 'load'
        return sm
    
    def check_achievements(self):
        for ach in self.achievements:
            if not self.ach_status.get(ach['name'], False):
                if ach['check'](self):
                    self.ach_status[ach['name']] = True
                    self.clicks += 500
                    if self.level < 100:
                        self.current_exp += 100
                    self.save_game()

    def tick(self, dt):
        self.play_time += 1
        self.quests['time'] = self.play_time // 60
        self.quests['c1'] = self.total_clicks
        self.quests['c2'] = self.total_clicks
        self.quests['save'] = self.clicks
        self.quests['save5'] = self.clicks
        if time.time() - self.last_quest_reset >= 3600:
            self.quests = {
                'c1': 0, 'c2': 0, 'c3': 1, 'time': 0, 'save': 0, 'save5': 0,
                'c1_done': False, 'c2_done': False, 'c3_done': False,
                'time_done': False, 'save_done': False, 'save5_done': False
            }
            self.last_quest_reset = time.time()
            self.save_game()
        if self.auto > 0: 
            self.clicks += self.auto
            self.quests['save'] = self.clicks
            self.quests['save5'] = self.clicks
            
    def load_game(self):
        if os.path.exists('save.json'):
            with open('save.json', 'r') as f:
                d = json.load(f)
                self.clicks = d.get('clicks', 0)
                self.power = d.get('power', 1)
                self.auto = d.get('auto', 0)
                self.total_clicks = d.get('total_clicks', 0)
                self.pwr_bought = d.get('pwr_bought', 0)
                self.auto_bought = d.get('auto_bought', 0)
                self.level = d.get('level', 1)
                self.current_exp = d.get('current_exp', 0)
                self.exp_goal = d.get('exp_goal', 250)
                self.player_name = d.get('name', '')
                self.play_time = d.get('play_time', 0)
                self.ach_status = d.get('ach_status', {})
                self.lang = d.get('lang', 'RU')
                self.sound = d.get('sound', True)
                self.last_gift_time = d.get('last_gift_time', 0)
                self.last_quest_reset = d.get('last_quest_reset', time.time())
                self.quests = d.get('quests', self.quests)
                self.price_p = d.get('price_p', 350)
                self.price_a = d.get('price_a', 450)
                self.reg_date = d.get('reg_date', '')

    def save_game(self):
        save_data = {
            'clicks': self.clicks, 'power': self.power, 'auto': self.auto,
            'total_clicks': self.total_clicks, 'pwr_bought': self.pwr_bought,
            'auto_bought': self.auto_bought, 'level': self.level, 'name': self.player_name, 
            'play_time': self.play_time, 'current_exp': self.current_exp, 'exp_goal': self.exp_goal,
            'ach_status': self.ach_status, 'lang': self.lang, 'sound': self.sound,
            'last_gift_time': self.last_gift_time, 'last_quest_reset': self.last_quest_reset,
            'quests': self.quests, 'price_p': self.price_p, 'price_a': self.price_a,
            'reg_date': self.reg_date
        }
        with open('save.json', 'w') as f: json.dump(save_data, f)

if __name__ == '__main__':
    ClickerApp().run()
