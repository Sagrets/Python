import cv2
import joblib
import json
import numpy as np
import base64
from wavelet import w2d

def classify_image(image_data, file_path=None):
    imgs = get_cropped_image_if_2_eyes(file_path, image_data)
    
    for img in imgs:
        img = cv2.imread(file_path)
        scalled_raw_img = cv2.resize(img, (32, 32))
        img_har = w2d(img, 'db1', 5)
        scalled_img_har = cv2.resize(img_har, (32, 32))
        combined_img = np.vstack((scalled_raw_img.reshape(32*32*3, 1),scalled_img_har.reshape(32*32, 1)))

        len_image_array = 32*32*3 + 32*32
        
        final = combined_img.reshape(1, len_image_array).astype(float)

def load_saved_artifacts():
    print("Loading saved artifacts...start")
    global class_name_to_number
    global class_number_to_name

def get_cv2_image_from_base64_string(b64str):
    encoded_data = b64str.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def get_cropped_image_if_2_eyes(image_path, image_base64_data):
    face_casecade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_frontalface_default.xml')
    eye_casecade = cv2.CascadeClassifier('./opencv/haarcascade/haarcascade_eye.xml')
    
    if image_path:
        img = cv2.imread(image_path)
    else:
        img = get_cv2_image_from_base64_string(image_base64_data)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_casecade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_casecade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            return roi_color

def get_bs64_test():
    with open('base64_img.txt', 'r') as f:
        return f.read()

if __name__ == "__main__":
    print(classify_image(get_bs64_test(), None))