'''An attempt with the kivy framework to create a chess clock
'''
__author__ = "Ahmed Kessemtini"

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class Button1(Button):
    def __init__(self, minutes, **kwargs):
        super().__init__(**kwargs)
        self.seconds = 60
        self.minutes = minutes
        self.text = "{:02d} : {:02d}".format(self.minutes + 1, 0)
        self.font_size = 45
        self.color = 0, 0, 0, 1
        self.background_normal = ""


class Button2(Button):
    def __init__(self, minutes, **kwargs):
        super().__init__(**kwargs)
        self.seconds = 60
        self.minutes = minutes
        self.text = "{:02d} : {:02d}".format(self.minutes+1, 0)
        self.font_size = 45
        self.color = 1, 1, 1, 1
        self.background_color = 0, 0, 0, 1


class MyBoxLayout(BoxLayout):
    def __init__(self, minutes, increment, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.minutes = minutes
        self.increment = increment
        self.Player1 = Button1(minutes)
        self.add_widget(self.Player1)
        self.Player2 = Button2(minutes)
        self.add_widget(self.Player2)
        self.check_not_finished = True
        self.Player1_not_pressed_last = True
        self.Player2_not_pressed_last = True
        self.Player2.bind(on_press=self.start_player1)
        self.Player1.bind(on_press=self.start_player2)
        content = FloatLayout()
        self.Button_res = Button(text="Restart", pos_hint={"x": 0.25, "y": 0.1}, size_hint=(0.5, 0.2))
        content.add_widget(self.Button_res)
        self.Button_return = Button(text="Return to menu screen", pos_hint={"x": 0.25, "y": 0.4}, size_hint=(0.5, 0.2))
        content.add_widget(self.Button_return)
        self.Button_exit = Button(text="Exit", pos_hint={"x": 0.25, "y": 0.7}, size_hint=(0.5, 0.2))
        content.add_widget(self.Button_exit)
        self.popup = Popup(title='Decide what to do', size_hint=(0.8, 0.8), content=content)
        self.bind(on_touch_down=self.create_clock, on_touch_up=self.delete_clock)

    def clock_on_player1(self, time_step):
        if self.check_not_finished:
            self.Player1.seconds = self.Player1.seconds - time_step
            if self.Player1.seconds > 0:
                self.Player1.text = "{:02d} : {:02d}".format(self.Player1.minutes, round(
                        self.Player1.seconds))  # str(self.MyButton.minutes)+":"+str(round(self.MyButton.seconds))
            elif round(self.Player1.seconds) == 0:
                self.Player1.text = "{:02d} : {:02d}".format(self.Player1.minutes, 0)
            else:
                if self.Player1.minutes >= 1:
                    self.Player1.seconds = self.Player1.seconds + 60
                    self.Player1.minutes = self.Player1.minutes - 1
                    self.Player1.text = "{:02d} : {:02d}".format(self.Player1.minutes, round(self.Player1.seconds))
                else:
                    self.Player1.text = "Game lost on time !"
        else:
            pass

    def clock_on_player2(self, time_step):
        if self.check_not_finished:
            self.Player2.seconds = self.Player2.seconds - time_step
            if self.Player2.seconds > 0:
                self.Player2.text = "{:02d} : {:02d}".format(self.Player2.minutes, round(
                    self.Player2.seconds))  # str(self.MyButton.minutes)+":"+str(round(self.MyButton.seconds))
            elif round(self.Player2.seconds) == 0:
                self.Player2.text = "{:02d} : {:02d}".format(self.Player2.minutes, 0)
            else:
                if self.Player2.minutes >= 1:
                    self.Player2.seconds = self.Player2.seconds + 60
                    self.Player2.minutes = self.Player2.minutes - 1
                    self.Player2.text = "{:02d} : {:02d}".format(self.Player2.minutes, round(self.Player2.seconds))
                else:
                    self.Player2.text = "Game lost on time !"
        else:
            pass

    def start_player1(self, instance):
        self.check_not_finished = True
        if self.Player2_not_pressed_last:
            Clock.schedule_interval(self.clock_on_player1, 1.)
            Clock.unschedule(self.clock_on_player2)
            if self.Player1_not_pressed_last:
                self.Player2.text = "{:02d} : {:02d}".format(self.Player2.minutes + 1, 0)
            else:
                if round(self.Player2.seconds) <= 59 - self.increment:
                    self.Player2.seconds = self.Player2.seconds+self.increment
                else:
                    self.Player2.minutes = self.Player2.minutes+1
                    self.Player2.seconds = self.increment - 60 + self.Player2.seconds
                self.Player2.text = "{:02d} : {:02d}".format(self.Player2.minutes, round(self.Player2.seconds))
            self.Player1_not_pressed_last = True
            self.Player2_not_pressed_last = False

    def start_player2(self, instance):
        self.check_not_finished = True
        if self.Player1_not_pressed_last:
            Clock.schedule_interval(self.clock_on_player2, 1.)
            Clock.unschedule(self.clock_on_player1)
            if self.Player2_not_pressed_last:
                self.Player1.text = "{:02d} : {:02d}".format(self.Player2.minutes + 1, 0)
            else:
                if round(self.Player1.seconds) <= 59 - self.increment:
                    self.Player1.seconds = self.Player1.seconds + self.increment
                else:
                    self.Player1.minutes = self.Player1.minutes + 1
                    self.Player1.seconds = self.increment - 60 + self.Player1.seconds
                self.Player1.text = "{:02d} : {:02d}".format(self.Player1.minutes, round(self.Player1.seconds))
            self.Player2_not_pressed_last = True
            self.Player1_not_pressed_last = False

    def on_touch_down(self, touch):
        if self.Player1.text == "Game lost on time !" or self.Player2.text == "Game lost on time !":
            self.popup.open()
            self.Button_res.bind(on_press=self.restart)
            self.Button_return.bind(on_press=self.parent.switch_screen_home)
            self.Button_exit.bind(on_press=self.exit)
            return True
        else:
            return super(MyBoxLayout, self).on_touch_down(touch)

    def callback(self, delta):
        self.popup.open()
        self.Button_res.bind(on_press=self.restart)
        self.Button_return.bind(on_press=self.parent.switch_screen_home)
        self.Button_exit.bind(on_press=self.exit)

    def create_clock(self, widget, touch, *args):
        Clock.schedule_once(self.callback, 2)

    def delete_clock(self, widget, touch, *args):
        Clock.unschedule(self.callback)

    def restart(self, instance):
        self.popup.dismiss()
        Clock.unschedule(self.clock_on_player1)
        Clock.unschedule(self.clock_on_player2)
        self.Player1.seconds = 60
        self.Player1.minutes = self.minutes
        self.Player2.seconds = 60
        self.Player2.minutes = self.minutes
        self.Player1.text = "{:02d} : {:02d}".format(self.Player1.minutes + 1, 0)
        self.Player2.text = "{:02d} : {:02d}".format(self.Player2.minutes + 1, 0)
        self.check_not_finished = False
        self.Player1_not_pressed_last = True
        self.Player2_not_pressed_last = True

    def exit(self, instance):
        App.get_running_app().stop()
        Window.close()


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(60/256, 60/256, 60/256)
            Rectangle(pos=(self.x, self.y), size=(5000, 5000))
        layout = BoxLayout(orientation="vertical")
        layout.padding = 50
        button_texts = ["Rapid chess 15|10 ",
                        "Rapid chess 25|10 ",
                        "Blitz chess 3|2 ",
                        "Blitz chess 5|0 ",
                        ]
        buttons = [Button()]*len(button_texts)
        for i in range(4):
            buttons[i] = Button(text=button_texts[i], font_size=30, background_normal="",
                                background_color=[i % 2, i % 2, i % 2, 1],
                                color=[(i+1) % 2, (i+1) % 2, (i+1) % 2, 1])
            layout.add_widget(buttons[i])
        buttons[0].bind(on_press=self.switch_screen_rapid1)
        buttons[1].bind(on_press=self.switch_screen_rapid2)
        buttons[2].bind(on_press=self.switch_screen_blitz1)
        buttons[3].bind(on_press=self.switch_screen_blitz2)
        self.add_widget(layout)

    def switch_screen_rapid1(self, instance):
        self.manager.current = "rapid_15|10"

    def switch_screen_rapid2(self, instance):
        self.manager.current = "rapid_25|10"

    def switch_screen_blitz1(self, instance):
        self.manager.current = "blitz_3|2"

    def switch_screen_blitz2(self, instance):
        self.manager.current = "blitz_5|0"


class Rapid1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MyBoxLayout(14, 10))

    def switch_screen_home(self, instance):
        self.children[0].popup.dismiss()
        self.manager.current = "home"
        self.remove_widget(self.children[0])
        self.add_widget(MyBoxLayout(14, 10))


class Rapid2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MyBoxLayout(24, 10))

    def switch_screen_home(self, instance):
        self.children[0].popup.dismiss()
        self.manager.current = "home"
        self.remove_widget(self.children[0])
        self.add_widget(MyBoxLayout(24, 10))


class Blitz1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MyBoxLayout(2, 2))

    def switch_screen_home(self, instance):
        self.children[0].popup.dismiss()
        self.manager.current = "home"
        self.remove_widget(self.children[0])
        self.add_widget(MyBoxLayout(2, 2))


class Blitz2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MyBoxLayout(4, 0))

    def switch_screen_home(self, instance):
        self.children[0].popup.dismiss()
        self.manager.current = "home"
        self.remove_widget(self.children[0])
        self.add_widget(MyBoxLayout(4, 0))


screen_manager = ScreenManager()
h = HomeScreen(name="home")
rm1 = Rapid1(name="rapid_15|10")
rm2 = Rapid2(name="rapid_25|10")
bm1 = Blitz1(name="blitz_3|2")
bm2 = Blitz2(name="blitz_5|0")
screen_manager.add_widget(h)
screen_manager.add_widget(rm1)
screen_manager.add_widget(rm2)
screen_manager.add_widget(bm1)
screen_manager.add_widget(bm2)


class ChessClockApp(App):
    def build(self):
        return screen_manager


if __name__ == "__main__":
    ChessClockApp().run()
