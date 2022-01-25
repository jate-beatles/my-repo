import zipfile
from PIL import Image, ImageOps, ImageDraw
from numpy.lib.function_base import disp
import pytesseract 
import cv2 as cv
import numpy as np
from IPython.display import display 
import math
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'
face_cascade = cv.CascadeClassifier('face_detect_haarcascade\haarcascade_frontalface_default.xml')


##texttest = pytesseract.image_to_string('Lv_0_PY_Practice\calmstack.png')
##print(texttest)
#display ('Lv_0_PY_Practice\calmstack.png')
zip_img = dict()
with zipfile.ZipFile('LV_1_PY_Practice\small_img.zip','r') as f:
    for fname in f.infolist():
        #display(fname)
        with f.open(fname) as file:
            img = Image.open(file).convert('RGB')
            #display(img)
            zip_img[fname.filename] = {'pil_img':img}
 
for png_name in zip_img.keys():
    text = pytesseract.image_to_string(zip_img[png_name]['pil_img'])
    zip_img[png_name]['text'] = text

####print(zip_img)
for png_name in zip_img.keys():
    zip_img[png_name]['faces'] = list()

    open_cv_image = np.array(zip_img[png_name]['pil_img'])
    img_gray = cv.cvtColor(open_cv_image,cv.COLOR_BGR2GRAY)
    faces_boxes = face_cascade.detectMultiScale(img_gray,1.3,5)

    ####print(faces_boxes)
    for x,y,w,h in faces_boxes:
        face = zip_img[png_name]['pil_img'].crop((x,y,x+w,y+h))
        ##display(face)
        zip_img[png_name]['faces'].append(face)
    
for png_name in zip_img:
    display(zip_img[png_name]['faces'])

def search(keyword):
    for png_name in zip_img:
        if (keyword in zip_img[png_name]['text']):
            if (len(zip_img[png_name]['faces']) != 0):
                print('Result found in file{}'.format(png_name))
                h = math.ceil(len(zip_img[png_name]['faces'])/5)
                contact_sheet = Image.new('RGB',(500,100*h))
                xc = 0
                yc = 0
                for face in zip_img[png_name]['faces']:
                    contact_sheet.paste(face,(xc,yc))
                    if xc + 100 == contact_sheet.width:
                        xc = 0
                        yc += 100
                    else:
                        xc += 100
                display(contact_sheet)
            else:
                print("Result found in file{}\n But there no faces in page\n".format(png_name))
    return

search("Christopher")



