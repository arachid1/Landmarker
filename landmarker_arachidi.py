# Ali Rachidi - Contrast Security Internship Application: Project Submission - 10/24/2018

# The goal of this project is to provide an annotation tool to build image databases for computer vision research.
# In this example, we are landmarking critical points on images extracted from a recording of a chemical synthesis
# that produces a melting zone.

# Nonetheless, this tool can be generalized. The initial step is placing general points on all the images, approximatively
# where they should be located (i.e, all corners and extremities of the waist). this step that can be disregarded based
# on the type of annotations). Then, a GUI opens, and the user can drag the points where they should be. By pressing 'n',
# the user can move to the next image, while pressing 's' will save the landmarked image and pressing 'a' will print the
# coordinates. Each image is stored in a landmarkedimage object, which is appended to a list.

# The purpose is to observe how the coordinates of the critical points vary as a result of a change of parameter,
# which will then help understand how to make more successful syntheses using Machine Learning.

# This implementation has a flaw, because when a image is annotated then saved, stopping the program and reopening it again
# will show the previous landmarks on the image, without trace of them stored anywhere. That is because a real time database
# is required, and the issue could be solved by adding an boolean attribute to the landmarked image object, in order to
# know whether or not to refer to the dictionary that is stored (in which case you can read the dictionary and extract
# the coordinates).

import warnings

warnings.filterwarnings("ignore")
import numpy as np
import cv2

# Our landmarked image object.
# It stores the image in a numpy array, and the coordinates of the points in a dictionary that labels them via letters
# (i.e, 'a' -> (2, 3)). It also stores the image_path for references in case elements get misplaced.

class landmarkedimage:
    def __init__(self, img, points, image_path):
        self.frame = img
        self.points = points
        self.image_path = image_path

    image = np.zeros(248832)
    points = dict()

# This function is used for 2 purposes: if the updated_label parameter is an empty character, then the function
# is initializing an image by landmarking points around where critical points are assumed to be located.
# if the updated_label parameter is not empty, then the function updates the coordinate of the point labeled by the
# parameter updated_label on the given image.
# The reason I am not using a switch statement is because the update_label is not always going to be one of the labels.
# it might increase the time complexity but we don't have to write another helper function!

def set_points(image, image_path, updated_label):
    points = {}
    if updated_label != 'a' or updated_label == '':
        coordinates = [247, 125]
        points['a'] = coordinates
        cv2.circle(image, (coordinates[0], coordinates[1]), 5,(255,0,0),-1)
    if updated_label != 'c' or updated_label == '':
        coordinates = [255, 170]
        points['c'] = coordinates
        cv2.circle(image, (coordinates[0], coordinates[1]), 5,(255,0,0),-1)
    if updated_label != 'e' or updated_label == '':
        coordinates = [255, 212]
        points['e'] = coordinates
        cv2.circle(image, (coordinates[0], coordinates[1]), 5,(255,0,0),-1)
    if updated_label != 'b' or updated_label == '':
        coordinates = [370, 125]
        points['b'] = coordinates
        cv2.circle(image, (coordinates[0], coordinates[1]), 5,(255,0,0),-1)
    if updated_label != 'd' or updated_label == '':
        coordinates = [370, 170]
        points['d'] = coordinates
        cv2.circle(image, (coordinates[0], coordinates[1]), 5,(255,0,0),-1)
    if updated_label != 'f' or updated_label == '':
        coordinates = [377, 212]
        points['f'] = coordinates
        cv2.circle(image, (coordinates[0], coordinates[1]), 5,(255,0,0),-1)
    landmarked_image = landmarkedimage(image, points, image_path)
    return landmarked_image

# this function creates a new image & copies all the landmarked points, except the one that is being dragged elsewhere.
# That is why we reuse the set_points function and pass it an updated_label parameter so that the point being
# replace is not reinitialized. We use a global dictionary 'changes_count' to keep track of changed images.

def update_points(landmarkedimage, x, y, label):
    global changes_count
    if changes_count[landmarkedimage.image_path] == 0: # no changes
        new_frame = cv2.imread(landmarkedimage.image_path, 0)
        set_points(new_frame, landmarkedimage.image_path, label)
        landmarkedimage.points[label][0] = x
        landmarkedimage.points[label][1] = y
        cv2.circle(new_frame, (x, y), 5, (255, 0, 0), -1)
        landmarkedimage.frame = new_frame
        changes_count[landmarkedimage.image_path] += 1
    else: # previous changes
        new_frame = cv2.imread(landmarkedimage.image_path, 0)
        temporary_label = '`'
        for i in range(len(landmarkedimage.points)):
            temporary_label = chr(ord(temporary_label) + 1)
            if temporary_label == label:
                continue
            cv2.circle(new_frame, (landmarkedimage.points[temporary_label][0],
                                   landmarkedimage.points[temporary_label][1]), 5, (255, 0, 0), -1)
        landmarkedimage.points[label][0] = x
        landmarkedimage.points[label][1] = y
        cv2.circle(new_frame, (x, y), 5, (255, 0, 0), -1)
        landmarkedimage.frame = new_frame

# this function is the function that allows to move around various points. It does so by detecting the closest point to
# where the mouse is being pressed down, and moves it to the new coordinates of the mouse when it's being pressed up.

def draw_circle(event,x,y,flags,param):
    global chosenLabel
    index = param
    landmarkedimage = landmarked_images[index]
    label = 'a'
    if event == cv2.EVENT_LBUTTONDOWN:
        for i in range(len(landmarkedimage.points)):
            if (landmarkedimage.points[label][0] - 10) <= x <= landmarkedimage.points[label][0] + 10 and \
                    landmarkedimage.points[label][1] - 10 <= y <= landmarkedimage.points[label][1] + 10:
                chosenLabel = label
                break
            elif label == 'f':
                print("you didn't click a point. ")
                break
            else:
                label = chr(ord(label) + 1)
    elif event == cv2.EVENT_LBUTTONUP:
        mouseX = x
        mouseY = y
        update_points(landmarkedimage, mouseX, mouseY, chosenLabel)

def main():
    i = 1
    global changes_count
    global landmarked_images
    global mouseX, mouseY
    global chosenLabel
    changes_count = dict()
    landmarked_images = list()
    coordinates = list()
    image_path = 'data_frames/frame0.jpg'
    while (True):
        img = cv2.imread(image_path, 0)
        #todo: add condition and load image with points if needed
        landmarked_image = set_points(img, image_path, '')
        if (img is not  None): # we know the index of the path will be incremented until the last image is reached.
            landmarked_images.append(landmarked_image)
            changes_count[image_path] = 0
        else:
            break;
        i = i + 1
        image_path = 'data_frames/frame' + str(i) + '.jpg'
    cv2.namedWindow('image')
    i = 1
    while(True):
        cv2.setMouseCallback('image',draw_circle, i)
        cv2.imshow('image',landmarked_images[i].frame)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break
        elif k == ord('a'): #
            print(mouseX,mouseY)
        elif k == ord('n'):
            i = i + 1
            cv2.setMouseCallback('image',draw_circle, i)
            cv2.imshow('image', i)
        elif k == ord('s'):
            for i in range(len(landmarked_images)):
                if (changes_count[landmarked_images[i].image_path] != 0):
                    cv2.imwrite(landmarked_images[i].image_path, landmarked_images[i].frame)
        
if __name__== "__main__":
    main()
