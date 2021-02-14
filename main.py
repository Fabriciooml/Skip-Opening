import pyscreenshot as ImageGrab
from skimage.metrics import structural_similarity as ssim
from skimage import exposure, feature
import cv2
from pyautogui import click, size, sleep

global X1
global X2
global Y1
global Y2
Y2 = 930
X1 = 1630
Y1 = 860
X2 = 1870

WIDTH, HEIGHT = size()

def getHog(img):
	(H, hogImage) = feature.hog(img, orientations=8, pixels_per_cell=(16, 16),
		cells_per_block=(1, 1), visualize=True, multichannel=True)
	hogImage = exposure.rescale_intensity(hogImage, out_range=(0, 255))
	hogImage = hogImage.astype("uint8")
	return hogImage

def setNewBox():
  global X1
  global X2
  global Y1
  global Y2
  X1 = int(X1*WIDTH/1920)
  X2 = int(X2*WIDTH/1920)
  Y1 = int(Y1*HEIGHT/1080)
  Y2 = int(Y2*HEIGHT/1080)
  
def screenshot():
  img = ImageGrab.grab(bbox=(X1, Y1, X2, Y2))
  img = getHog(img)
  cv2.imwrite("temp.jpg", img)

def compareImages():
  imageA = cv2.imread("./templates/netflixHOG.jpg")
  imageB = cv2.imread("temp.jpg")
  
  s = ssim(imageA, imageB, multichannel=True)
  
  print(s)
  if s>0.8:
    return True
  return False

def positionToClick():
  x = (X1 + X2)/2
  y = (Y1 + Y2)/2
  return x, y
  
setNewBox()
click_x, click_y = positionToClick()

while True:
  screenshot()
  if compareImages():
    click(x = click_x, y = click_y)
    sleep(2)
  else:
    pass