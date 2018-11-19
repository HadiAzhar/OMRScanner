import cv2
import numpy as np
#from matplotlib import pyplot as plt

multiple_img = ['template.jpg'] #'tmp2.pg','tmp3.jpg','tmp4.jpg']

for mat in multiple_img:
    img = cv2.imread(mat, 1) 
    #img = cv2.imread('template.jpg',1)
    img2 = img.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("template", img)

    # All the 6 methods for comparison in a list
    #methods = 'cv2.TM_CCOEFF' 
            #'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            #'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    #img = img2.copy()
    method = eval('cv2.TM_SQDIFF')
    for im in ['image1.jpg','image2.jpg','image3.jpg','image4.jpg']: 
        #,'image2.jpg','image3.jpg','image4.jpg','image5.jpg','image6.jpg','image7.jpg','image8.jpg','image9.jpg','image10.jpg','image11.jpg'};
        macht = cv2.imread(im,0)
        print(macht)
        w, h = macht.shape[::-1]

        # Apply template Matching
        res = cv2.matchTemplate(img,macht,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
            print('max_loc = ', top_left)
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(img2,top_left, bottom_right, (0,255,0), 2)
            
    #img = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
    img = cv2.resize(img, (800,600))
    cv2.imshow("matched", img2)
cv2.waitKey(0)
cv2.destroyWindow("matched")        



#img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
#cv2.rectangle(img,top_left, bottom_right, (0,255,0), 2)


#plt.subplot(121),plt.imshow(res,cmap = 'gray')
#plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
#plt.subplot(122),plt.imshow(img,cmap = 'gray')
#plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
#plt.suptitle(meth)

#plt.show()
