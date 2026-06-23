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
        'exp': 'Опыт: ', 'q_time': '10 мин игры', 'q_save1': '1000 саке', 'q_save5': '5000 саке',
        'q_click250': '250 кликов', 'q_click500': '500 кликов',
        'q_login1': 'Зайти в игру', 'q_shop': 'Покупка в магазине',
        'gift': 'Подарок (+200)', 'achs': 'Достижения', 'settings': 'Настройки',
        'reset_btn': 'Сбросить прогресс', 'change_name': 'Изменить имя',
        'max_lvl': 'МАКС. УРОВЕНЬ', 'cost': 'Цена: '
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
        'gift': 'Gift (+200)', 'achs': 'Achievements', 'settings': 'Settings',
        'reset_btn': 'Reset Progress', 'change_name': 'Change Name',
        'max_lvl': 'MAX LEVEL', 'cost': 'Cost: '
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
    # Исправление бага с бесконечным уменьшением:
    # Запоминаем оригинальный размер кнопки
    if not hasattr(widget, 'orig_size'):
        widget.orig_size = widget.size
        
    # Отменяем предыдущую анимацию, чтобы не наслаивать их друг на друга
    Animation.cancel_all(widget)
    
    w, h = widget.orig_size
    anim = Animation(size=(w * 0.9, h * 0.9), duration=0.05) + Animation(size=(w, h), duration=0.05)
    anim.start(widget)

# --- ВИДЖЕТЫ ---

class BackgroundWidget(Widget):
    def __init__(self, source='space.jpg', **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.bg_rect = Rectangle(source=source, pos=self.pos, size=Window.size)
            Color(0, 0, 0, 0.5) # Затемнение фона для читаемости
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

# --- ЭКРАНЫ ---

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
        self.lbl = Label(text="", font_size=40, color=(1, 1, 1, 1))
        layout.add_widget(self.lbl)
        self.name_input = TextInput(multiline=False, font_size=30, size_hint=(1, None), height=80)
        layout.add_widget(self.name_input)
        self.btn = Button(size_hint=(1, 0.2), font_size=32)
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
            app.player_name = self.name_input.text.strip()
            app.reg_date = datetime.now().strftime("%d.%m.%Y %H:%M")
            app.save_game()
            self.manager.current = 'game'

class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(BackgroundWidget(source='space.jpg'))
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        self.title_lbl = Label(text="Profile", font_size=40, size_hint=(1, 0.1))
        layout.add_widget(self.title_lbl)
        
        self.frame = RoundedFrame(orientation='vertical', padding=20, spacing=10, size_hint=(0.9, 0.6), pos_hint={'center_x': 0.5})
        self.label = Label(text="", font_size=24, markup=True, color=(1, 1, 1, 1), halign="center")
        self.frame.add_widget(self.label)
        layout.add_widget(self.frame)
        
        btn_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, 0.3))
        self.btn_achs = Button(text="", size_hint=(1, 0.5), font_size=24)
        self.btn_achs.bind(on_press=lambda x: setattr(self.manager, 'current', 'achievements'))
        self.btn_back = Button(text="", size_hint=(1, 0.5), font_size=24)
        self.btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'game'))
        btn_layout.add_widget(self.btn_achs)
        btn_layout.add_widget(self.btn_back)
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)

    def on_enter(self):
        app = App.get_running_app()
        t = LANGS[app.lang]
        self.title_lbl.text = t['prof']
        h, m = divmod(app.play_time // 60, 60)
        title = get_level_title(app.level, app.lang)
        stats = f"[b]{t['player']}[/b] {app.player_name}\n\n[b]{t['level']}[/b] {app.level} ({title})\n[b]{t['exp']}[/b] {int(app.current_exp)}/{app.exp_goal}\n[b]{t['date']}[/b] {app.reg_date}\n[b]{t['power']}[/b] {app.power}\n[b]{t['auto']}[/b] {app.auto}{t['sec']}\n[b]{t['clicks']}[/b] {app.total_clicks}\n[b]{t['time']}[/b] {h}{t['h']} {m}{t['m']}"
        self.label.text = stats
        self.btn_back.text = t['back']
        self.btn_achs.text = t['achs']

class ShopScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(BackgroundWidget(source='space.jpg'))
        self.app = App.get_running_app()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        self.title_lbl = Label(text="Shop", font_size=40, size_hint=(1, 0.1))
        layout.add_widget(self.title_lbl)
        
        self.sake_lbl = Label(text="Sake: 0", font_size=30, size_hint=(1, 0.1), color=(1, 0.8, 0, 1))
        layout.add_widget(self.sake_lbl)
        
        # Покупка Силы
        pwr_box = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.2))
        self.lbl_pwr = Label(text="Power: +1", font_size=20)
        self.btn_pwr = Button(text="Buy", font_size=20)
        self.btn_pwr.bind(on_press=self.buy_power)
        pwr_box.add_widget(self.lbl_pwr)
        pwr_box.add_widget(self.btn_pwr)
        layout.add_widget(pwr_box)
        
        # Покупка Авто
        auto_box = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.2))
        self.lbl_auto = Label(text="Auto: +1/s", font_size=20)
        self.btn_auto = Button(text="Buy", font_size=20)
        self.btn_auto.bind(on_press=self.buy_auto)
        auto_box.add_widget(self.lbl_auto)
        auto_box.add_widget(self.btn_auto)
        layout.add_widget(auto_box)
        
        self.btn_back = Button(text="Back", size_hint=(1, 0.2), font_size=24)
        self.btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'game'))
        layout.add_widget(self.btn_back)
        
        self.add_widget(layout)

    def on_enter(self):
        self.update_ui()

    def update_ui(self):
        t = LANGS[self.app.lang]
        self.title_lbl.text = t['shop']
        self.sake_lbl.text = f"{t['sake']} {int(self.app.clicks)}"
        self.lbl_pwr.text = f"{t['buy_pwr']} +1\n{t['cost']} {int(self.app.price_p)}"
        self.btn_pwr.text = t['shop']
        self.lbl_auto.text = f"{t['buy_auto']} +1/s\n{t['cost']} {int(self.app.price_a)}"
        self.btn_auto.text = t['shop']
        self.btn_back.text = t['back']

    def buy_power(self, instance):
        if self.app.clicks >= self.app.price_p:
            if self.app.sound and self.app.sound_buy: self.app.sound_buy.play()
            self.app.clicks -= self.app.price_p
            self.app.power += 1
            self.app.pwr_bought += 1
            self.app.price_p = int(self.app.price_p * 1.5)
            self.app.quests['q_shop'] = 1
            self.app.save_game()
            self.update_ui()

    def buy_auto(self, instance):
        if self.app.clicks >= self.app.price_a:
            if self.app.sound and self.app.sound_buy: self.app.sound_buy.play()
            self.app.clicks -= self.app.price_a
            self.app.auto += 1
            self.app.auto_bought += 1
            self.app.price_a = int(self.app.price_a * 1.5)
            self.app.quests['q_shop'] = 1
            self.app.save_game()
            self.update_ui()

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(BackgroundWidget(source='space.jpg'))
        self.app = App.get_running_app()
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        self.title_lbl = Label(text="Settings", font_size=40, size_hint=(1, 0.2))
        layout.add_widget(self.title_lbl)
        
        self.btn_snd = Button(size_hint=(1, 0.15), font_size=24)
        self.btn_snd.bind(on_press=self.toggle_sound)
        layout.add_widget(self.btn_snd)
        
        self.btn_lng = Button(size_hint=(1, 0.15), font_size=24)
        self.btn_lng.bind(on_press=self.toggle_lang)
        layout.add_widget(self.btn_lng)

        self.btn_name = Button(size_hint=(1, 0.15), font_size=24)
        self.btn_name.bind(on_press=self.change_name)
        layout.add_widget(self.btn_name)

        self.btn_reset = Button(size_hint=(1, 0.15), font_size=24, color=(1,0,0,1))
        self.btn_reset.bind(on_press=self.reset_game)
        layout.add_widget(self.btn_reset)
        
        self.btn_back = Button(size_hint=(1, 0.2), font_size=24)
        self.btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'game'))
        layout.add_widget(self.btn_back)
        
        self.add_widget(layout)

    def on_enter(self):
        self.update_ui()

    def update_ui(self):
        t = LANGS[self.app.lang]
        self.title_lbl.text = t['settings']
        snd_state = t['on'] if self.app.sound else t['off']
        self.btn_snd.text = f"{t['snd']} {snd_state}"
        self.btn_lng.text = t['lng']
        self.btn_name.text = t['change_name']
        self.btn_reset.text = t['reset_btn']
        self.btn_back.text = t['back']

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

    def change_name(self, instance):
        self.manager.current = 'name'

    def reset_game(self, instance):
        # Жесткий сброс прогресса
        self.app.clicks = 0
        self.app.power = 1
        self.app.auto = 0
        self.app.level = 1
        self.app.current_exp = 0
        self.app.total_clicks = 0
        self.app.price_p = 350
        self.app.price_a = 450
        self.app.save_game()
        self.manager.current = 'game'

class QuestsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(BackgroundWidget(source='space.jpg'))
        self.app = App.get_running_app()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        self.title_lbl = Label(text="Quests", font_size=40, size_hint=(1, 0.1))
        layout.add_widget(self.title_lbl)
        
        # Уменьшен шрифт, чтобы все квесты помещались на экране
        self.quest_lbl = Label(text="In Progress...", font_size=20, size_hint=(1, 0.6), halign="center", markup=True)
        layout.add_widget(self.quest_lbl)

        self.btn_claim = Button(text="Claim Gift", size_hint=(1, 0.15), font_size=24)
        self.btn_claim.bind(on_press=self.claim_gift)
        layout.add_widget(self.btn_claim)
        
        self.btn_back = Button(text="Back", size_hint=(1, 0.15), font_size=24)
        self.btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'game'))
        layout.add_widget(self.btn_back)
        
        self.add_widget(layout)

    def on_enter(self):
        self.update_ui()

    def update_ui(self):
        t = LANGS[self.app.lang]
        self.title_lbl.text = t['quests']
        self.btn_back.text = t['back']
        self.btn_claim.text = t['gift']
        
        # Обновление текста: теперь отображаются ВСЕ квесты
        quests_text = f"[b]{t['q_login1']}[/b]: 1/1\n"
        quests_text += f"[b]{t['q_time']}[/b]: {min(self.app.play_time//60, 10)}/10\n"
        quests_text += f"[b]{t['q_click250']}[/b]: {min(self.app.total_clicks, 250)}/250\n"
        quests_text += f"[b]{t['q_click500']}[/b]: {min(self.app.total_clicks, 500)}/500\n"
        quests_text += f"[b]{t['q_save1']}[/b]: {min(int(self.app.clicks), 1000)}/1000\n"
        quests_text += f"[b]{t['q_save5']}[/b]: {min(int(self.app.clicks), 5000)}/5000\n"
        quests_text += f"[b]{t['q_shop']}[/b]: {min(self.app.pwr_bought + self.app.auto_bought, 1)}/1\n"
        self.quest_lbl.text = quests_text

    def claim_gift(self, instance):
        now = time.time()
        if now - self.app.last_gift_time > 300: # 5 минут кулдаун
            self.app.clicks += 200
            self.app.last_gift_time = now
            self.app.save_game()
            self.btn_claim.text = "Claimed!"
            self.btn_claim.disabled = True
            Clock.schedule_once(self.enable_claim, 5)

    def enable_claim(self, dt):
        self.btn_claim.disabled = False
        t = LANGS[self.app.lang]
        self.btn_claim.text = t['gift']

class AchievementScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(BackgroundWidget(source='space.jpg'))
        self.app = App.get_running_app()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        self.title_lbl = Label(text="Achievements", font_size=40, size_hint=(1, 0.1))
        layout.add_widget(self.title_lbl)
        
        self.scroll = ScrollView(size_hint=(1, 0.7))
        self.ach_list = Label(text="", font_size=20, size_hint_y=None, markup=True, halign="left")
        self.ach_list.bind(texture_size=self.ach_list.setter('size'))
        self.scroll.add_widget(self.ach_list)
        layout.add_widget(self.scroll)
        
        self.btn_back = Button(text="Back", size_hint=(1, 0.2), font_size=24)
        self.btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'profile'))
        layout.add_widget(self.btn_back)
        
        self.add_widget(layout)

    def on_enter(self):
        t = LANGS[self.app.lang]
        self.title_lbl.text = t['achs']
        self.btn_back.text = t['back']
        
        # Расширенный список всех достижений
        achievements = [
            ("Click Novice", "10 Clicks", self.app.total_clicks >= 10),
            ("Click Amateur", "250 Clicks", self.app.total_clicks >= 250),
            ("Click Pro", "1000 Clicks", self.app.total_clicks >= 1000),
            ("Click Master", "5000 Clicks", self.app.total_clicks >= 5000),
            ("Click God", "10000 Clicks", self.app.total_clicks >= 10000),
            ("Level 5!", "Reach Level 5", self.app.level >= 5),
            ("Level 10!", "Reach Level 10", self.app.level >= 10),
            ("Level 25!", "Reach Level 25", self.app.level >= 25),
            ("Level 50!", "Reach Level 50", self.app.level >= 50),
            ("Auto Novice", "Buy 1 Auto", self.app.auto_bought >= 1),
            ("Auto Master", "Buy 5 Auto", self.app.auto_bought >= 5),
            ("Auto Tycoon", "Buy 20 Auto", self.app.auto_bought >= 20),
            ("Power Novice", "Buy 1 Power", self.app.pwr_bought >= 1),
            ("Power Master", "Buy 5 Power", self.app.pwr_bought >= 5),
            ("Power God", "Buy 20 Power", self.app.pwr_bought >= 20)
        ]
        
        text = ""
        for name, desc, unlocked in achievements:
            color = "[color=00FF00]" if unlocked else "[color=FF0000]"
            status = "UNLOCKED" if unlocked else "LOCKED"
            text += f"{color}[b]{name}[/b] - {desc} ({status})[/color]\n\n"
            
        self.ach_list.text = text

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.add_widget(BackgroundWidget(source='space.jpg'))
        
        self.info_panel = BoxLayout(orientation='vertical', size_hint=(1, 0.2), pos_hint={'top': 0.98})
        self.info = Label(text='', font_size=30, color=(1,0.8,0,1), bold=True)
        self.lvl_lbl = Label(text='', font_size=24) 
        self.info_panel.add_widget(self.info)
        self.info_panel.add_widget(self.lvl_lbl)
        self.add_widget(self.info_panel)
        
        # Кнопки навигации верхние (Обе имеют одинаковый размер 80x80)
        self.btn_quest = Button(background_normal='quest.png', size_hint=(None, None), size=(80, 80), pos_hint={'x': 0.05, 'top': 0.98})
        self.btn_quest.bind(on_press=lambda x: setattr(self.manager, 'current', 'quests'))
        self.add_widget(self.btn_quest)
        
        self.btn_set = Button(background_normal='settings.png', size_hint=(None, None), size=(80, 80), pos_hint={'right': 0.95, 'top': 0.98})
        self.btn_set.bind(on_press=lambda x: setattr(self.manager, 'current', 'settings'))
        self.add_widget(self.btn_set)

        # Главная кнопка (Корабль)
        self.btn = Button(background_normal='ship.png', size_hint=(None, None), size=(300, 300), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.btn.bind(on_press=self.on_click)
        self.add_widget(self.btn)
        
        # Нижняя панель (Исправлены растянутые кнопки)
        nav = BoxLayout(size_hint=(1, None), height=100, pos_hint={'bottom': 0}, spacing=20, padding=10)
        nav.add_widget(Widget()) # Центрирующий отступ слева
        
        # Жесткий размер 250х80 чтобы кнопки не растягивались
        self.btn_shop = Button(background_normal='shop.png', text='Shop', size_hint=(None, None), size=(250, 80), pos_hint={'center_y': 0.5})
        self.btn_shop.bind(on_press=lambda x: setattr(self.manager, 'current', 'shop'))
        
        self.btn_prof = Button(background_normal='profile.png', text='Profile', size_hint=(None, None), size=(250, 80), pos_hint={'center_y': 0.5})
        self.btn_prof.bind(on_press=lambda x: setattr(self.manager, 'current', 'profile'))
        
        nav.add_widget(self.btn_shop)
        nav.add_widget(self.btn_prof)
        nav.add_widget(Widget()) # Центрирующий отступ справа
        self.add_widget(nav)

    def on_click(self, instance):
        animate_button(self.btn)
        if self.app.sound and self.app.sound_click:
            self.app.sound_click.play()
        self.app.clicks += self.app.power
        self.app.total_clicks += 1
        self.app.add_exp(5) # Опыт за клик
        self.update_ui()

    def update_ui(self):
        t = LANGS[self.app.lang]
        self.info.text = f"{t['sake']} {int(self.app.clicks)}"
        self.lvl_lbl.text = f"{t['level']} {self.app.level} | {t['exp']} {int(self.app.current_exp)}/{self.app.exp_goal}"
        self.btn_shop.text = t['shop']
        self.btn_prof.text = t['prof']

    def on_enter(self):
        self.update_ui()

# --- ОСНОВНОЙ КЛАСС APP ---

class ClickerApp(App):
    def build(self):
        # Загрузка звуков
        self.sound_click = SoundLoader.load('click.mp3')
        self.sound_buy = SoundLoader.load('buy.mp3')
        self.music = SoundLoader.load('background.mp3')
        
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
        self.quests = {'c1':0, 'c2':0, 'c3':1, 'time':0, 'save':0, 'save5':0, 'q_shop':0} 
        
        self.load_game()
        
        # Запуск фоновой музыки
        if self.music and self.sound:
            self.music.loop = True
            self.music.volume = 0.3
            self.music.play()

        # Инициализация экранов
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
        # Таймер для автоклика и времени в игре (вызывается каждую секунду)
        Clock.schedule_interval(self.game_tick, 1.0)
        # Таймер для автосохранения (каждые 10 секунд)
        Clock.schedule_interval(self.auto_save, 10.0)

    def game_tick(self, dt):
        self.play_time += 1
        if self.auto > 0:
            self.clicks += self.auto
            self.add_exp(self.auto * 0.5) # Немного опыта за автоклики
            # Обновляем UI если мы на главном экране
            if self.sm.current == 'game':
                self.sm.get_screen('game').update_ui()

    def add_exp(self, amount):
        self.current_exp += amount
        if self.current_exp >= self.exp_goal:
            self.level += 1
            self.current_exp = 0
            self.exp_goal = int(self.exp_goal * 1.5) # Увеличиваем порог следующего уровня
        
    def auto_save(self, dt):
        self.save_game()

    def save_game(self):
        save_data = {
            'clicks': self.clicks, 
            'power': self.power, 
            'auto': self.auto,
            'price_p': self.price_p,
            'price_a': self.price_a,
            'total_clicks': self.total_clicks, 
            'name': self.player_name, 
            'reg_date': self.reg_date,
            'play_time': self.play_time,
            'level': self.level, 
            'current_exp': self.current_exp,
            'exp_goal': self.exp_goal,
            'lang': self.lang,
            'sound': self.sound,
            'pwr_bought': self.pwr_bought,
            'auto_bought': self.auto_bought
        }
        with open('save.json', 'w', encoding='utf-8') as f: 
            json.dump(save_data, f, ensure_ascii=False)

    def load_game(self):
        if os.path.exists('save.json'):
            try:
                with open('save.json', 'r', encoding='utf-8') as f:
                    d = json.load(f)
                    self.clicks = d.get('clicks', 0)
                    self.power = d.get('power', 1)
                    self.auto = d.get('auto', 0)
                    self.price_p = d.get('price_p', 350)
                    self.price_a = d.get('price_a', 450)
                    self.total_clicks = d.get('total_clicks', 0)
                    self.player_name = d.get('name', '')
                    self.reg_date = d.get('reg_date', '')
                    self.play_time = d.get('play_time', 0)
                    self.level = d.get('level', 1)
                    self.current_exp = d.get('current_exp', 0)
                    self.exp_goal = d.get('exp_goal', 250)
                    self.lang = d.get('lang', 'RU')
                    self.sound = d.get('sound', True)
                    self.pwr_bought = d.get('pwr_bought', 0)
                    self.auto_bought = d.get('auto_bought', 0)
            except Exception as e:
                print("Ошибка при загрузке сохранения:", e)

if __name__ == '__main__':
    ClickerApp().run()
