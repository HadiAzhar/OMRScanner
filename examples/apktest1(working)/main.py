from kivy.app import App
#kivy.required("1.10.1")

from kivy.uix.scatter import Scatter
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

class mainApp(App):
    def build(self):
        f = FloatLayout()
        s = Scatter()
        l = Label(text="Hello World", font_size=50, pos=(100,100))
        b = Button(text="Sample Button", pos=(0,0), color=(0,0,1,1), font_size=30, size_hint=(0.3,0.1))
        
        f.add_widget(s)
        s.add_widget(l)
        f.add_widget(b)
        return f

if __name__ == "__main__":
    mainApp().run()