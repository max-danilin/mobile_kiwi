from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from hoverable import HoverBehavior
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json
from datetime import datetime
import random

Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"
        
    def login(self, uname, pword):
        with open("users.json", 'r') as file:
            users = json.load(file)
        if uname in users.keys():
            if uname == users[uname].get('username') and pword == users[uname].get('password'):
                self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong username or password"
            
    def get_password(self):
        self.manager.current = "forgot_password_screen"

class ForgotPasswordScreen(Screen):
    def restore_password(self, user, year, month, date):
        full_year = year + '-' + month + '-' + date
        with open("users.json", 'r') as file:
            users = json.load(file)
        if user in users.keys():
            dt = datetime.strptime(users[user].get('created'), "%Y-%m-%d %H:%M:%S")
            dt = dt.strftime("%Y-%m-%d")
            if user == users[user].get('username') and full_year == dt:
                self.ids.restored.text = users[user].get('password')
            else:
                self.ids.restored.text = "Such combination not found."
        else:
            self.ids.restored.text = "Such combination not found."

    def back_to_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("users.json", 'r') as file:
            users = json.load(file)
        users[uname] = {'username': uname, 'password': pword, 'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        with open("users.json", 'w') as file:
            json.dump(users, file)
        self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

    def get_quote(self, feel):
        feelings = ['sad', 'happy', 'unloved']
        if feel.lower() in feelings:
            with open("quotes/{}.txt".format(feel.lower()), encoding="utf-8") as fin:
                f = fin.readlines()
                self.ids.quote.text = random.choice(f)
        else:
            self.ids.quote.text = "You cannot feel that to the Emperor! Call the spacemarines."

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()