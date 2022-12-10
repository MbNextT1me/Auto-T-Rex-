import mss.tools
import numpy as np
import cv2
import pyautogui as pg
import time

top = 350
left = 271
width = 30
height = 38

close_diff = 111

checkBox = {"top": top, "left": left, "width": width, "height": height}
checkBox_close = {"top": top, "left": left-close_diff, "width": width+25, "height": height}

def process_image(original_image):
    processed_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_image = cv2.Canny(processed_image, threshold1=200, threshold2=300)
    return processed_image

def play():
     global left
     global close_diff
     global checkBox
     global checkBox_close
     sct = mss.mss()
     start_time = time.time()
     current_time = 0
     change_flag = 0
     while True:
        img = process_image(np.array(sct.grab(checkBox)))
        img_near = process_image(np.array(sct.grab(checkBox_close)))
        mean = np.mean(img)
        mean_close = np.mean(img_near)
        if current_time > 21 and change_flag!=1 and current_time  % 10  == 0 :
            left += 5 + int(current_time/10)*2
            close_diff += 5 + int(current_time/10)*2
            change_flag = 1
            checkBox = {"top": top, "left": left, "width": width, "height": height}
            checkBox_close = {"top": top, "left": left-close_diff, "width": width+25   , "height": height}
            print(checkBox)
            print(f"Game time: {current_time} sec")
        if mean != 0.0 or mean_close != 0.0:
            pg.press('space')
        if (current_time != int(time.time()-start_time)):
            change_flag = 0
            current_time = int(time.time()-start_time)

if __name__ == '__main__':
    play()
    # test screen
    image = pg.screenshot(region=(0,0, 1920, 1080))
    image = np.array(image)
    cv2.rectangle(image, (left-close_diff, top), (left+width-close_diff+20, top+height), (255, 0, 0), 2)
    cv2.rectangle(image, (left, top), (left+width, top+height), (255, 0, 0), 2)
    cv2.imwrite('pic.png', image)