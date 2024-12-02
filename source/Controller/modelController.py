import os
import cv2

class ModelController:
    def __init__(self):
        pass

    def getImages(self):
        ''' Get the images '''
        
        # get the path to the folder containing the images
        image_folder = 'Model/images'
        # print(os.getcwd()) # debug
        image_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith('.jpg')]

        # Load and return the images
        images = []
        for path in image_paths:
            image = cv2.imread(path)
            images.append(image)
        return images