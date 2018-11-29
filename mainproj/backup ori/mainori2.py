'''
Basic camera example
Default picture is saved as
/sdcard/org.test.cameraexample/enter_file_name_here.jpg
'''
import kivy
kivy.require('1.8.0')

from os import getcwd, getenv
from os.path import exists, dirname, join, expanduser
from os.path import splitext
from os import makedirs

from kivy.utils import platform
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.logger import Logger
from plyer import camera

class CameraDemo(FloatLayout):
    def __init__(self):
        super(CameraDemo, self).__init__()
        path = platform
        droid = "android"
        Mac = "macosx"
        path1 = "/OMRpaper/"


        if path == droid :
            DATA_FOLDER = getenv('INTERNAL_STORAGE')
        else:
            expanduser("~")
        
        if path == Mac :
            DATA_FOLDER = getcwd()

        if(exists(DATA_FOLDER)):
            #path_name = join(rootfolder,storagetype,folder)
            self.cwd = DATA_FOLDER + path1
            self.ids.path_label.text = self.cwd
        else:
            self.cwd = getcwd()
            self.ids.path_label.text = self.cwd

    def do_capture(self):
        filepath = self.cwd + self.ids.filename_text.text
        ext = splitext(self.ids.filename_text.text)[-1].lower()

        if(exists(filepath)):
            popup = MsgPopup("Picture with this name already exists!")
            popup.open()
            return False

        try:
            camera.take_picture(filename=filepath,
                                on_complete=self.camera_callback)
        except NotImplementedError:
            popup = MsgPopup(
                "This feature has not yet been implemented for this platform.")
            popup.open()

    def camera_callback(self, filepath):
        if(exists(filepath)):
            popup = MsgPopup("Picture saved!")
            popup.open()
        else:
            popup = MsgPopup("Could not save your picture in " + filepath)
            popup.open()


class CameraDemoApp(App):
    def __init__(self):
        super(CameraDemoApp, self).__init__()
        self.demo = None

    def build(self):
        self.demo = CameraDemo()
        return self.demo

    def on_pause(self):
        return True

    def on_resume(self):
        pass


class MsgPopup(Popup):
    def __init__(self, msg):
        super(MsgPopup, self).__init__()
        self.ids.message_label.text = msg


if __name__ == '__main__':
    CameraDemoApp().run()
