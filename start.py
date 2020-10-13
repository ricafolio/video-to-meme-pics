import cv2
import sys
import os
import math

dir_path = os.path.dirname(os.path.realpath(__file__))

meme_id = input('Meme Project Folder Name: ')

# create directory 
directory1 = dir_path + '/output_frames/' + meme_id
directory2 = dir_path + '/output_memes/' + meme_id

if not os.path.exists(directory1) and not os.path.exists(directory2):
    os.makedirs(directory1)
    os.makedirs(directory2)

video_id = input('Video file in videos (ex. clip.mp4): ')
videoFile = dir_path + '/videos/' + video_id

# extract image frames from video
cap = cv2.VideoCapture(videoFile)
frameRate = cap.get(5)
x=1
while(cap.isOpened()):
    frameId = cap.get(1) 
    ret, frame = cap.read()
    if (ret != True):
        break
    if (frameId % math.floor(frameRate) == 0):
        filename = dir_path + '/output_frames/' + meme_id + '/' +  str(int(x)) + '.jpg';x+=1
        cv2.imwrite(filename, frame)
        print('[INFO] Video frame extracted #'+str(int(x))+'...')
cap.release()
print ('[FINISHED] Step 1. Video Frames Extracting')

# capture faces aka create meme
directory = dir_path + '/output_frames/' + meme_id

for filename in os.listdir(directory):
    if filename.endswith('.jpg'): 
        imagePath = os.path.join(directory, filename)
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3, minSize=(40, 40))
        print('[INFO] Found {0} Faces.'.format(len(faces)))
        for (x, y, w, h) in faces:\
            # adjust the target frame size
            h2 = h + 70
            y2 = y - 10
            w2 = w + 60
            x2 = x - 30
            roi_color = image[y2:y2 + h2, x2:x2 + w2]
            print('[INFO] Object found. Saving locally.')
            cv2.imwrite(dir_path + '/output_memes/' + meme_id + '/' + str(w) + str(h) + '_meme.jpg', roi_color)
        continue
    else:
        continue

print('[FINISHED] Job finished!')