import easyocr
import cv2

#To use GPU you need to have CUDA configured for the pytorch library.
reader = easyocr.Reader(['en'], gpu=False)  

img = cv2.imread('OCR/road signs.png')

results = reader.readtext(img, detail=1, paragraph=False) 
#Paragraph=True will combine all results making it easy to capture it in a dataframe. 

#print(results)

for (bbox, text, prob) in results:
    
    #Define bounding boxes
    (tl, tr, br, bl) = bbox
    tl = (int(tl[0]), int(tl[1]))
    tr = (int(tr[0]), int(tr[1]))
    br = (int(br[0]), int(br[1]))
    bl = (int(bl[0]), int(bl[1]))
        
    #Remove non-ASCII characters to display clean text on the image (using opencv)
    text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
         
    #Put rectangles and text on the image
    cv2.rectangle(img, tl, br, (0, 255, 0), 2)
    cv2.putText(img, text, (tl[0], tl[1] - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
# show the output image
cv2.imshow("Result", img)
cv2.waitKey(0)

#####################################################################

#Read multiple images in a directory, extract text using OCR and capture 
# it in a pandas dataframe. 
import cv2
import glob
import pandas as pd

#select the path
path = "OCR/*.*"
img_number = 1 
reader = easyocr.Reader(['en'])  #English

df=pd.DataFrame()
for file in glob.glob(path):
    print(file)     #just stop here to see all file names printed
    img= cv2.imread(file, 0)  #now, we can read each file since we have the full path
    results = reader.readtext(img, detail=0, paragraph=True) #Set detail to 0 for simple text output
    df = df.append(pd.DataFrame({'image': file, 'detected_text': results[0]}, index=[0]), ignore_index=True)
    img_number +=1   
    
print(df)

df.to_excel('OCR.xlsx')
