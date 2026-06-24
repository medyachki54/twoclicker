from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window
from kivy.animation import Animation
import time

# ======================
# 🎨 BRAWL STYLE UI
# ======================
Window.clearcolor = (0.04, 0.05, 0.08, 1)

store = JsonStore("save.json")

def load():
    if store.exists("player"):
        return store.get("player")
    return {
        "name": "Player",
        "cake": 0,
        "click_power": 1,
        "autoclick": 0,
        "level": 1,
        "xp": 0,
        "last_daily": 0
    }

data = load()

def save():
    store.put("player", **data)

def daily_reward():
    now = int(time.time())
    if now - data["last_daily"] > 86400:
        data["cake"] += 500
        data["last_daily"] = now
        save()

# ======================
# UI BUTTON (BRAWL STYLE)
# ======================
class GameButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_color = (0.2, 0.6, 1, 1)
        self.font_size = 18
        self.size_hint = (1, None)
        self.height = 70

    def on_press(self):
        Animation(scale=0.95, d=0.05) + Animation(scale=1, d=0.05)


# ======================
# LOADING
# ======================
class Loading(Screen):
    def on_enter(self):
        box = BoxLayout()
        box.add_widget(Label(text="Loading BRAWL...", font_size=40))
        self.add_widget(box)
        Clock.schedule_once(lambda dt: setattr(self.manager, "current", "name"), 1.5)


# ======================
# NAME SCREEN
# ======================
class NameScreen(Screen):
    def on_enter(self):
        self.clear_widgets()

        from kivy.uix.textinput import TextInput

        box = BoxLayout(orientation="vertical", padding=30, spacing=15)

        box.add_widget(Label(text="ENTER NAME", font_size=28))

        self.input = TextInput(multiline=False, font_size=22)
        box.add_widget(self.input)

        btn = GameButton(text="START")
        btn.bind(on_press=self.start)
        box.add_widget(btn)

        self.add_widget(box)

    def start(self, instance):
        if self.input.text.strip():
            data["name"] = self.input.text
            save()
        self.manager.current = "game"


# ======================
# GAME SCREEN (BRAWL HUD)
# ======================
class GameScreen(Screen):

    def on_enter(self):
        self.clear_widgets()
        daily_reward()

        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # ======================
        # 🟦 TOP HUD (BRAWL STYLE)
        # ======================
        hud = BoxLayout(size_hint=(1, 0.15))

        left = Label(text="🅱 BRAWL", font_size=22, bold=True)
        center = Label(text=self.text(), font_size=18)
        right = Label(text="⚡", font_size=22)

        hud.add_widget(left)
        hud.add_widget(center)
        hud.add_widget(right)

        root.add_widget(hud)

        # ======================
        # 🔥 BIG TAP BUTTON
        # ======================
        self.tap = Button(
            text="🔥 TAP!",
            font_size=65,
            background_normal="",
            background_color=(1, 0.35, 0.2, 1)
        )
        self.tap.bind(on_press=self.click)
        root.add_widget(self.tap)

        # ======================
        # NAV BAR
        # ======================
        nav = BoxLayout(size_hint=(1, 0.18), spacing=5)

        for icon, scr in [
            ("🛒", "shop"),
            ("👤", "profile"),
            ("🎯", "quests"),
            ("🏆", "ach"),
            ("⚙️", "settings")
        ]:
            b = GameButton(text=icon)
            b.bind(on_press=lambda x, s=scr: self.go(s))
            nav.add_widget(b)

        root.add_widget(nav)
        self.add_widget(root)

        self.auto()

    def text(self):
        return f"{data['name']} | 💰 {data['cake']} | ⭐ {data['level']}"

    def click(self, instance):
        data["cake"] += data["click_power"]
        data["xp"] += 1

        if data["xp"] >= 10:
            data["level"] += 1
            data["xp"] = 0

        save()
        self.on_enter()

    def auto(self):
        Clock.schedule_interval(self.autoclick, 1)

    def autoclick(self, dt):
        if data["autoclick"] > 0:
            data["cake"] += data["autoclick"]
            save()

    def go(self, s):
        self.manager.current = s


# ======================
# SHOP
# ======================
class Shop(Screen):
    def on_enter(self):
        self.clear_widgets()

        box = BoxLayout(orientation="vertical", padding=20, spacing=10)

        box.add_widget(Label(text="🛒 SHOP", font_size=30))

        b1 = GameButton(text="⚡ CLICK +1 (350)")
        b2 = GameButton(text="🤖 AUTO +1 (450)")

        b1.bind(on_press=self.buy1)
        b2.bind(on_press=self.buy2)

        back = GameButton(text="⬅ BACK")
        back.bind(on_press=lambda x: self.back())

        box.add_widget(b1)
        box.add_widget(b2)
        box.add_widget(back)

        self.add_widget(box)

    def buy1(self, x):
        if data["cake"] >= 350:
            data["cake"] -= 350
            data["click_power"] += 1
            save()
            self.on_enter()

    def buy2(self, x):
        if data["cake"] >= 450:
            data["cake"] -= 450
            data["autoclick"] += 1
            save()
            self.on_enter()

    def back(self):
        self.manager.current = "game"


# ======================
# PROFILE
# ======================
class Profile(Screen):
    def on_enter(self):
        self.clear_widgets()

        box = BoxLayout(orientation="vertical", padding=20)

        box.add_widget(Label(text="👤 PROFILE", font_size=30))
        box.add_widget(Label(text=f"Name: {data['name']}"))
        box.add_widget(Label(text=f"Cake: {data['cake']}"))
        box.add_widget(Label(text=f"Level: {data['level']}"))
        box.add_widget(Label(text=f"Power: {data['click_power']}"))
        box.add_widget(Label(text=f"Auto: {data['autoclick']}"))

        b = GameButton(text="BACK")
        b.bind(on_press=lambda x: self.back())
        box.add_widget(b)

        self.add_widget(box)

    def back(self):
        self.manager.current = "game"


# ======================
# SETTINGS
# ======================
class Settings(Screen):
    def on_enter(self):
        self.clear_widgets()

        box = BoxLayout(orientation="vertical", padding=20)

        box.add_widget(Label(text="⚙ SETTINGS", font_size=30))
        box.add_widget(Label(text="Sound: ON"))
        box.add_widget(Label(text="Language: EN"))

        b = GameButton(text="BACK")
        b.bind(on_press=lambda x: self.back())
        box.add_widget(b)

        self.add_widget(box)

    def back(self):
        self.manager.current = "game"


# ======================
# QUESTS
# ======================
class Quests(Screen):
    def on_enter(self):
        self.clear_widgets()

        box = BoxLayout(orientation="vertical", padding=20)

        box.add_widget(Label(text="🎯 QUESTS", font_size=30))
        box.add_widget(Label(text="Tap 50 times"))
        box.add_widget(Label(text="Get 1000 cake"))
        box.add_widget(Label(text="Buy auto click"))

        b = GameButton(text="BACK")
        b.bind(on_press=lambda x: self.back())
        box.add_widget(b)

        self.add_widget(box)

    def back(self):
        self.manager.current = "game"


# ======================
# ACHIEVEMENTS
# ======================
class Ach(Screen):
    def on_enter(self):
        self.clear_widgets()

        box = BoxLayout(orientation="vertical", padding=20)

        box.add_widget(Label(text="🏆 ACHIEVEMENTS", font_size=30))

        box.add_widget(Label(text="✔ First click" if data["cake"] > 0 else "✖ First click"))
        box.add_widget(Label(text="✔ 100 cake" if data["cake"] >= 100 else "✖ 100 cake"))
        box.add_widget(Label(text="✔ 1000 cake" if data["cake"] >= 1000 else "✖ 1000 cake"))

        b = GameButton(text="BACK")
        b.bind(on_press=lambda x: self.back())
        box.add_widget(b)

        self.add_widget(box)

    def back(self):
        self.manager.current = "game"


# ======================
# APP
# ======================
class ClickerApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(Loading(name="loading"))
        sm.add_widget(NameScreen(name="name"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(Shop(name="shop"))
        sm.add_widget(Profile(name="profile"))
        sm.add_widget(Settings(name="settings"))
        sm.add_widget(Quests(name="quests"))
        sm.add_widget(Ach(name="ach"))

        sm.current = "loading"
        return sm


if __name__ == "__main__":
    ClickerApp().run()
