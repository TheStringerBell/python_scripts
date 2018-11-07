import pyautogui
import time
from PIL import Image, ImageFilter
import cv2
import numpy as np
import sys


img = cv2.imread('cs.jpg', 0)
 

def volume(image):
    img = image
    print("Choose your preference(1-10 | \"d\" for default | \"q\" for quit )")
    x = input("x: ")
    if x != "q":
        try:
            x = int(x)
            convert_image(img, x)
        except ValueError:
            default(img)       
    else:
        print("Done")
        sys.exit()


def convert_image(image, ammount):
    
       
    dynamic_image = cv2.bilateralFilter(image, 1, 75, 75)   
    th, bw = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    edges = cv2.Canny(image, th/int(ammount) , th)
    dynamic_image = Image.fromarray(edges)
        
    timer(dynamic_image)
    

def default(image, sigma = 0.33):

    
    v = np.median(image)     
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edge = cv2.Canny(image, lower, upper)
    default_image = Image.fromarray(edge) 
    timer(default_image)

    

def timer(image):
    image.show()
    while True:
        yn = input("Do you want to draw it? (Y/N)").lower()

        if yn == "y":            
            for i in ("5", "4", "3", "2", "1"):                    
                print(i, end = "")
                time.sleep(1)
                print("\b" * len(i), end = "", flush = True)                           
                
            get_positions(image)
             
        if yn == "n":
            print("Not drawing.")
            volume(img)
        else:
            continue

def get_positions(img):

    xcord = []
    ycord = []
    
    for x in range(img.size[0]):
        for y in range(img.size[1]):      
            if img.getpixel((x,y)) == 255:
                xcord.append(x)
                ycord.append(y)
    draw(xcord, ycord)      

def draw(x, y):
    width, height = pyautogui.size()

    width = width / 2.4
    xcord = x
    ycord = y
    for i in range(len(xcord)-1):
            
        pyautogui.mouseDown(width +xcord[i], height+ycord[i], button='left')
        pyautogui.dragTo(width +xcord[i]+1, height+ycord[i]+1)
        pyautogui.mouseUp()
    

if __name__ == '__main__':
    volume(img)

    