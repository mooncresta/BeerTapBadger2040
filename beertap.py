# For Badger 2040 e-Ink Display
# Images must be 144x128 pixel with 1bit colour depth to fit side by side

# You can use examples/badger2040/image_converter/convert.py to convert them:
# python3 convert.py --binary --resize image_file_1.png image_file_2.png image_file_3.png
# Create a new "images" directory via Thonny, and upload the .bin files there.
# Don't use --resize as image is half width
# %Run convert.py --binary images/b1/Jupiler.png

import os
import sys
import time
import badger2040
from badger2040 import HEIGHT
import badger_os

OVERLAY_BORDER = 40
OVERLAY_SPACING = 20
OVERLAY_TEXT_SIZE = 0.5
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT
IMAGE_WIDTH=144
TOTAL_IMAGES1 = 0
TOTAL_IMAGES2 = 0

# Turn the act LED on as soon as possible
display = badger2040.Badger2040()
#display.led(128)

# Load images
try:
    IMAGES1 = [f for f in os.listdir("/images/b1") if f.endswith(".bin")]
    TOTAL_IMAGES1 = len(IMAGES1)
    IMAGES2 = [f for f in os.listdir("/images/b2") if f.endswith(".bin")]
    TOTAL_IMAGES2 = len(IMAGES2)
except OSError:
    pass

image1 = bytearray(int(148 * 128 / 8))
image2 = bytearray(int(148 * 128 / 8))

state = {
    "current_image1": 0,
    "current_image2": 0,
    "side": 1,
    "show_info": False
}

def show_image1(n):
    file = IMAGES1[n]
    name = file.split(".")[0]
    open("/images/b1/{}".format(file), "r").readinto(image1)
    display.image(image1, int(144), HEIGHT, 0,0)
    display.update()

def show_image2(n):
    file = IMAGES2[n]
    name = file.split(".")[0]
    open("/images/b2/{}".format(file), "r").readinto(image2)
    display.image(image2, int(144), HEIGHT, 148 ,0)
    display.update()
    
# from example
if TOTAL_IMAGES1 == 0 and TOTAL_IMAGES2 == 0:
    display.pen(15)
    display.clear()
    badger_os.warning(display, "Create images directory on your device and upload some 1bit 296x128 pixel images.")
    time.sleep(4.0)
    sys.exit()


badger_os.state_load("image", state)
#print("Image 1 is", state["current_image1"])
#print("Image 2 is", state["current_image2"])

#changed = not badger2040.woken_by_button()
show_image1(state["current_image1"])
show_image2(state["current_image2"])
changed = False

while True:
    
    if display.pressed(badger2040.BUTTON_A):
        # LHS
#        print("BUTT A")
        state["side"] = 1
        badger_os.state_save("image", state)
       
    if display.pressed(badger2040.BUTTON_C):
        # RHS
#        print("BUTT C")
        state["side"] = 2
        badger_os.state_save("image", state)
        
    if display.pressed(badger2040.BUTTON_UP):
        if state["side"] == 1:     
            if state["current_image1"] > 0:
                state["current_image1"] -= 1
                changed = True
#                print("Image 1 is", state["current_image1"])
        if state["side"] == 2:
             if state["current_image2"] > 0:
                state["current_image2"] -= 1
                changed = True
#                print("Image 2 is", state["current_image2"])               
    if display.pressed(badger2040.BUTTON_DOWN):
        if state["side"] == 1:     
            if state["current_image1"] < TOTAL_IMAGES1 - 1:
                state["current_image1"] += 1
                changed = True
#                print("Image 1 is", state["current_image1"])
        if state["side"] == 2:
             if state["current_image2"] < TOTAL_IMAGES2 - 1:
                state["current_image2"] += 1
                changed = True                
#                print("Image 2 is", state["current_image2"])               
                
    if changed:
        badger_os.state_save("image", state)
        changed = False
        if state["side"] == 1:     
            show_image1(state["current_image1"])
        if state["side"] == 2:     
            show_image2(state["current_image2"])                      

    # Halt the Badger to save power, it will wake up if any of the front buttons are pressed
    display.halt()

