import cv2
import numpy as np
import math
import pyautogui

(dw, dh) = pyautogui.size()  # gives us the screen size of our machine.
print(dw, dh)
(camx, camy) = (640, 480)  # camera image capturing resolution.
# frameR = 100
cap = cv2.VideoCapture(0)
cap.set(3, camx)
cap.set(4, camy)
flag = 0
upper = np.array([180, 255, 255])
lower = np.array([165, 155, 84])
kernal = np.ones((5, 5))
kernalc = np.ones((15, 15))

flag = 0

while True:
    success, img_inv = cap.read()
    img = cv2.flip(img_inv, 1)
    # converting normal image to HSV format.
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # filtering out only red color from the image
    mask = cv2.inRange(hsv_img, lower, upper)

    # noise removal, morphological operations
    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernal)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernalc)

    contours, h = cv2.findContours(maskClose.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(img, contours, -1,(0,0,255),2)
    # for i in range(len(contours)):
    # x, y, w, h = cv2.boundingRect(contours[i])
    # cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)

    if len(contours) == 2:

        x1, y1, w1, h1 = cv2.boundingRect(contours[0])
        x2, y2, w2, h2 = cv2.boundingRect(contours[1])
        cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), (255, 255, 0), 2)
        cv2.rectangle(img, (x2, y2), (x2 + w2, y2 + h2), (255, 255, 0), 2)
        a1 = w1 * h1
        a2 = w2 * h2
        cx1 = x1 + w1 // 2
        cx2 = x2 + w2 // 2
        cy1 = y1 + w1 // 2
        cy2 = y2 + w2 // 2
        cx = (cx1 + cx2) // 2
        cy = (cy1 + cy2) // 2
        cv2.circle(img, (cx, cy), 3, (255, 255, 0), 3)
        LANE = cv2.line(img, (cx1, cy1), (cx2, cy2), (0, 0, 0), 3)
        length = math.hypot(cx2 - cx1, cy2 - cy1)
        print(length)
        # mouse movements:
        if length > 90:
            if flag == 0 or flag == 2:
                flag = 1
                pyautogui.click(button='right')
            # cv2.rectangle(img, (frameR, frameR), (camx - frameR, camy - frameR), (255, 0, 255), 2)
            pyautogui.moveTo((cx * dw / camx), (cy * dh / camy))  # screen conversions.
        if length < 90 and length > 60:
            if flag == 1 or flag == 0:
                flag = 2
                pyautogui.click()
            pyautogui.moveTo((cx * dw / camx), (cy * dh / camy))  # screen conversions.

    if len(contours) == 1:
        if flag == 1 or flag == 2:
            flag = 0
        x, y, w, h = cv2.boundingRect(contours[0])
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
        cx = x + w // 2
        cy = y + h // 2
        cv2.circle(img, (cx, cy), (w + h) // 4, (0, 0, 255), 2)  # review it.
        # mouse movements:

        # cv2.rectangle(img,(frameR,frameR),(camx-frameR, camy-frameR), (255, 0, 255), 2)
        pyautogui.moveTo((cx * dw / camx), (cy * dh / camy))  # screen conversions.

    cv2.imshow('image', img)
    # cv2.imshow('image2', mask)
    # cv2.imshow('image3', hsv_img)
    # cv2.imshow('image5', maskClose)
    cv2.waitKey(1)
