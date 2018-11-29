import cv2
import numpy as np
import kivy
from grade_paper import ProcessPage
kivy.require('1.8.0')

from os import getcwd, getenv
from os.path import exists, dirname, join, expanduser
from os.path import splitext

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

        if path == droid :
            DATA_FOLDER = getenv('EXTERNAL_STORAGE')
        else:
            expanduser("~")
        
        if path == Mac :
            DATA_FOLDER = getcwd()

        if(exists(DATA_FOLDER)):
            self.cwd = DATA_FOLDER
            self.ids.path_label.text = self.cwd
        else:
            self.cwd = getcwd()
            self.ids.path_label.text = self.cwd

    def do_capture(self):
        filepath = join(self.cwd,self.ids.filename_text.text)
        ext = splitext(self.ids.filename_text.text)[-1].lower()

        if(exists(filepath)):
            popup = MsgPopup("Picture with this name already exists!")
            popup.open()
            return False

        try:
            camera.take_picture(filename=filepath,
                                on_complete=self.camera_callback)
        except NotImplementedError:
            popup = MsgPopup("This feature has not yet been implemented for this platform.")
            popup.open()
        

    def camera_callback(self, filepath):
        if(exists(filepath)):
            popup = MsgPopup("Picture saved!")
            popup.open()
        else:
            popup = MsgPopup("Could not save your picture in " + filepath)
            popup.open()

    def do_scanner(self):
        
        if platform == 'android' :
            # get any files into images directory
            curdir = '/sdcard/images/*'
    
        if platform == 'macosx' :
            curdir = join(getcwd(),'images/test1.jpg')

        if platform == 'ios' :
            curdir == "/private/var/mobile/Media/DCIM/"

        #load the image
        image = cv2.imread(curdir)
        ratio = len(image[0]) / 500.0 #used for resizing the image
        original_image = image #make a copy of the original image

        #find contours on the smaller image because it's faster
        image = cv2.resize(image, (0,0), fx=1/ratio, fy=1/ratio)
        print("past resize1")

        #gray and filter the image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #bilateral filtering removes noise and preserves edges
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        #find the edges
        edged = cv2.Canny(gray, 150, 150)

        #find the contours
        temp_img, contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #sort the contours
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        #find the biggest contour
        biggestContour = None

        print("starting loop over contour")

        x=0
        # loop over our contours
        for contour in contours:
            # approximate the contour
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            x += 1

            #return the biggest 4 sided approximated contour
            if len(approx) == 4:
                biggestContour = approx
                break

        #used for the perspective transform
        points = []
        desired_points = [[0,0], [425, 0], [425, 550], [0, 550]] #8.5in by 11in. paper

        #convert to np.float32
        desired_points = np.float32(desired_points)

        #extract points from contour
        if biggestContour is not None:
            for i in range(0, 4):
                points.append(biggestContour[i][0])

        #find midpoint of all the contour points for sorting algorithm
        mx = sum(point[0] for point in points) / 4
        my = sum(point[1] for point in points) / 4
        
        #calculation to rotate
        r = [100,100]
        rotate = (np.arctan2(r[0] - mx, r[1] - my) + 0.5 * np.pi) % (2 * np.pi)
        print("past arctan2")
        
        #sorts point
        #points.sort(key=rotate, reverse=True)

        #convert points to np.float32
        points = np.float32(points)

        #resize points so we can take the persepctive transform from the
        #original image giving us the maximum resolution
        paper = []
        points *= ratio
        answers = 1

        try:
            #send scanned image to grade the answer
            if biggestContour is not None:
                #create perspective matrix
                M = cv2.getPerspectiveTransform(points, desired_points)
                #warp persepctive
                paper = cv2.warpPerspective(original_image, M, (425, 550))
                answers, paper2, codes = ProcessPage(paper)
                cv2.imshow("graded paper", paper2)

            #draw the contour
            if biggestContour is not None:
                if answers != -1:
                    cv2.drawContours(image, [biggestContour], -1, (0, 255, 0), 3)
                    print(answers)
                    if codes is not None:
                        print(codes)
            else:
                cv2.drawContours(image, [biggestContour], -1, (0, 0, 255), 3)
        except NotImplementedError:
            popuplast = MsgPopup("there is an error while looking for contour")
            cv2.imshow('paper',paper)
            


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