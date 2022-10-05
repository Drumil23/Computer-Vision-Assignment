from PIL import Image
import os
from os import listdir
import cv2
import numpy as np
  

def cutThreatImage():
  folder = "./sample_data/threat_images/"
  cropped_image = "./sample_data/cropped_images/"
  for fileName in os.listdir(folder):
    print(fileName)
    img = cv2.imread(folder+fileName)
    img = cv2.blur(img,(2,2))
    gray_seg = cv2.Canny(img, 50, 200)

    ## find the non-zero min-max coords of canny
    pts = np.argwhere(gray_seg>0)
    y1,x1 = pts.min(axis=0)
    y2,x2 = pts.max(axis=0)

    ## crop the region
    cropped = img[y1:y2, x1:x2]
    cv2.imwrite(cropped_image+fileName.split(".")[0]+".png", cropped)
#    print(fileName.split("."))

cutThreatImage()

folder1 = "./sample_data/background_images/"
folder2 = "./sample_data/cropped_images/"

# Read background file list
for fileN1 in os.listdir(folder1):

  img1 = Image.open(folder1+fileN1)
#Read Cropped image files
  for fileN2 in os.listdir(folder2):

    img2 = Image.open(folder2+fileN2)
    img1copy = img1.copy().resize((500,500))
    bg_w, bg_h = img1copy.size

    img2 = img2.convert("RGBA")
    pixdata = img2.load()

# transperent image 
    width, height = img2.size
    for y in range(height):
      for x in range(width):
        if pixdata[x, y] == (255, 255, 255, 255):
            pixdata[x, y] = (255, 255, 255, 0)

    img2 = img2.rotate(45)
    img2copy=img2.copy()

    img2copy = img2copy.resize((100,175))

    img_w, img_h = img2copy.size

#offset to paste in between bg image
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)

    img1copy.paste(img2copy,offset,img2copy)
    img1copy.save("./sample_data/merged_images/"+fileN1.split(".")[0]+fileN2.split(".")[0]+".png", "PNG")

print("Successful")