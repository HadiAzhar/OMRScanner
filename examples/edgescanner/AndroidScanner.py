import numpy as np
import cv2
from grade_paper import ProcessPage

import kivy
kivy.require('1.8.0')

from os import getcwd
from os.path import exists, dirname, join, abspath
from os.path import splitext
from os import makedirs

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.logger import Logger

from plyer import camera

class CameraDemo(FloatLayout):
    def __init__(self):
        super(CameraDemo, self).__init__()
        self.cwd = getcwd()
        rootfolder = 'Local'
        storagetype = 'internal'
        folder = 'screenshot'

        if(exists(self.cwd)):
            path_name = join(rootfolder,storagetype,folder)
            self.ids.path_label.text = path_name
        else:
            
            self.ids.path_label.text = self.cwd

    def do_capture(self):
        filepath = self.cwd + self.ids.filename_text.text
        ext = splitext(self.filepath)[-1].lower()

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
            popup = MsgPopup("Could not save your picture!")
            popup.open()

class MsgPopup(Popup):
    def __init__(self, msg):
        super(MsgPopup, self).__init__()
        self.ids.message_label.text = msg


#alogrithm for sorting points clockwise
def clockwise_sort(x):
	return (np.arctan2(x[0] - mx, x[1] - my) + 0.5 * np.pi) % (2*np.pi)

def scanner_main():
	cv2.namedWindow('Scanned Paper')#transformed perspective

	#ret, image = cap.read()
	image = cv2.imread("test.jpg")
	ratio = len(image[0]) / 500.0 #used for resizing the image
	original_image = image.copy() #make a copy of the original image


	#find contours on the smaller image because it's faster
	image = cv2.resize(image, (0,0), fx=1/ratio, fy=1/ratio)

	#gray and filter the image
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#bilateral filtering removes noise and preserves edges
	gray = cv2.bilateralFilter(gray, 11, 17, 17)
	#find the edges
	edged = cv2.Canny(gray, 150, 150)

	#find the contours
	temp_img, contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	#sort the contours
	contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

	#find the biggest contour
	biggestContour = None

	x=0
	# loop over our contours
	for contour in contours:
		# approximate the contour
		peri = cv2.arcLength(contour, True)
		approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
		x += 1
		print('loop over contour =',x)

		#return the biggest 4 sided approximated contour
		if len(approx) == 4:
			biggestContour = approx
			print('biggest contour',biggestContour)
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
			print('pointsAppended = ',biggestContour)

	#find midpoint of all the contour points for sorting algorithm
	mx = sum(point[0] for point in points) / 4
	my = sum(point[1] for point in points) / 4
	print('midpoint mx = ', mx)
	print('midpoint my = ', my)

	#sort points
	points.sort(key=clockwise_sort, reverse=True)

	#convert points to np.float32
	points = np.float32(points)

	#resize points so we can take the persepctive transform from the
	#original image giving us the maximum resolution
	paper = []
	points *= ratio
	answers = 1

	#send scanned image to grade the answer
	if biggestContour is not None:
		#create perspective matrix
		M = cv2.getPerspectiveTransform(points, desired_points)
		#warp persepctive
		paper = cv2.warpPerspective(original_image, M, (425, 550))
		cv2.imshow("Scanned Paper", paper)
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

	cv2.imshow("Canny edge", cv2.resize(edged, (0, 0), fx=0.7, fy=0.7))
	cv2.waitkey(0)

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
		
if __name__ == '__main__':
    CameraDemoApp().run()
