from playsound import playsound
from PIL import Image
import cv2
import sys
import pyocr
import pyocr.builders

cam = cv2.VideoCapture(1)
img_name = 'opencv_frame.png'

#Take a photo
def photo(cam, img_name):
    while True:
        ret, frame = cam.read()
        if not ret:
            print('cannot activate your web cam')
            break
        #Draw rectangle on each frame
        cv2.rectangle(frame, (600, 50), (1250, 950), (0, 255, 0), 10)
        cv2.imshow('test', frame)

        k = cv2.waitKey(1)
        
        #If Escape is pressed, kill the program
        if k%256 == 27:
            print('[Escape], closing ... ')
            break
        #If Space is pressed, take a photo
        elif k%256 == 32:
            #sound for camera
            playsound('camera-shutter-click-03.wav')
            cv2.imwrite(img_name, frame)
            im = Image.open(img_name)
            #Crop image
            im_crop = im.crop((610, 60, 1240, 940))
            im_crop.save(img_name, quality=100)
            print('{} written'.format(img_name))
    cam.release()
    cv2.destroyAllWindows()

def image_to_text(img_name):
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print('No OCR tool found')
        sys.exit(1)
    tool = tools[0]
    #print('Use tool {}'.format(tool.get_name()))

    langs = tool.get_available_languages()
    #print('Available languages are {}'.format(langs))

    txt = tool.image_to_string(
            Image.open(img_name),
            #If you want japanese version, change 'eng' to 'jpn'
            lang='eng',
            builder=pyocr.builders.TextBuilder()
            )

    return txt

photo(cam, img_name)
text = image_to_text(img_name)
print(text)
