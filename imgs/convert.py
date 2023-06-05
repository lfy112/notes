'''
Author: LFY
Date: 2023-06-05 15:38:53
LastEditors: LFY
LastEditTime: 2023-06-05 15:41:04
FilePath: \notes\imgs\convert.py
Description: 

'''
import cv2

img = cv2.imread('imgs/img.jfif')

cv2.imwrite('imgs/img.png', img)
