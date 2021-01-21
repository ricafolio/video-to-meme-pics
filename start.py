import cv2
import sys
import os
import math
from datetime import datetime

# extract image frames from video
def start_extracting():
    cap = cv2.VideoCapture(video_file)
    frameRate = cap.get(5)
    x = 1
    while(cap.isOpened()):
        frameId = cap.get(1)
        ret, frame = cap.read()
        if (ret != True):
            break
        if (frameId % math.floor(frameRate) == 0):
            filename = dir_path + '/output_frames/' + meme_id + '/' +  str(int(x)) + '.jpg';x+=1
            cv2.imwrite(filename, frame)
            print(' [INFO] Video frame extracted #'+str(int(x))+'...')
    cap.release()
    print (' [FINISHED] Step 1. Video Frames Extracting')

    # capture faces aka create meme
    directory = dir_path + '/output_frames/' + meme_id
    for filename in os.listdir(directory):
        if filename.endswith('.jpg'):
            imagePath = os.path.join(directory, filename)
            image = cv2.imread(imagePath)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3, minSize=(40, 40))
            print(' [INFO] Found {0} Faces.'.format(len(faces)))
            for (x, y, w, h) in faces:\
                # adjust the target frame size
                h2 = h + 70
                y2 = y - 10
                w2 = w + 60
                x2 = x - 30
                roi_color = image[y2:y2 + h2, x2:x2 + w2]
                print(' [INFO] Object found. Saving locally.')
                try:
                    cv2.imwrite(dir_path + '/output_memes/' + meme_id + '/' + str(w) + str(h) + '_meme.jpg', roi_color)
                except Exception as e:
                    print(" [ERROR] Something didnt work hmmm")
            continue
        else:
            continue

    print(' [FINISHED] Job finished! See results at /output_memes/'+meme_id+'/')

print('\n Welcome to video-to-meme-pics!\n')

# set directory
dir_path = os.path.dirname(os.path.realpath(__file__))
meme_id = input(' Set the Project Folder Name: ')
if not meme_id:
    meme_id = datetime.now().strftime('%Y%m%d%H%M%S')
    print(" [INFO] Didn't set a name, folder " + meme_id + " was created instead\n")
else:
    print(" [INFO] Folder "+ meme_id +" created.\n")

# create directory for project
directory1 = dir_path + '/output_frames/' + meme_id
directory2 = dir_path + '/output_memes/' + meme_id

if not os.path.exists(directory1) and not os.path.exists(directory2):
    os.makedirs(directory1)
    os.makedirs(directory2)

# target video file location
video_id = input(' Target Video File Name (ex. clip.mp4): ')
if not video_id:
    print(" [ERROR] Please try again and input the file name.\n")
    exit(1)

video_file = dir_path + '/videos/' + video_id

if not os.path.isfile(video_file):
    print(" [ERROR] Video not found. Please try again!")
    exit(1)
else:
    start_extracting()