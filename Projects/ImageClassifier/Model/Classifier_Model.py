import numpy as np
import cv2
import matplotlib
from matplotlib import pyplot as plt
import os
import shutil
import pywt
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
import pandas as pd
from sklearn.metrics import confusion_matrix
import seaborn as sns
import joblib
import json


face_casecade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_casecade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def get_cropped_image_if_2_eyes(image_path):
    img = cv2.imread(image_path)
    
    if img is None:
        return None
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_casecade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_casecade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            return roi_color
        
path_to_data = "./dataset/"
path_to_cr_data = "./dataset/cropped/"
img_dirs = []

for entry in os.scandir(path_to_data):
    if entry.is_dir():
        img_dirs.append(entry.path)

"""
if os.path.exists(path_to_cr_data):
    shutil.rmtree(path_to_cr_data)
os.mkdir(path_to_cr_data)
"""



for img_dir in img_dirs:
    celeb_name = img_dir.split('/')[-1]
    count = 1
    
    if celeb_name == "cropped":
        continue
        
    for entry in os.scandir(img_dir):
        roi_color = get_cropped_image_if_2_eyes(entry.path)
        if roi_color is not None:
            cropped_folder = path_to_cr_data + celeb_name 
            if not os.path.exists(cropped_folder):
                os.makedirs(cropped_folder)
                
                print("Generating cropped images in folder: ",cropped_folder)
            
            cropped_file_name = celeb_name + str(count) + ".png"
            cropped_file_path = cropped_folder + "/" + cropped_file_name
            
            cv2.imwrite(cropped_file_path, roi_color)
            count += 1

player_dict = {}

for img_dir in os.scandir(path_to_cr_data):
    player_name = img_dir.name
    player_dict[player_name] = []
    
    for entry in os.scandir(img_dir.path):
        player_dict[player_name].append(entry.path)
    
            
def w2d(img, mode='haar', level=1):
    imArray = img
    imArray = cv2.cvtColor(imArray,cv2.COLOR_RGB2GRAY)
    imArray = np.float32(imArray)
    imArray /= 255
    
    coeffs=pywt.wavedec2(imArray, mode, level=level)
    
    coeffs_H=list(coeffs)
    coeffs_H[0] *= 0
    
    imArray_H=pywt.waverec2(coeffs_H, mode)
    imArray_H *= 255
    imArray_H = np.uint8(imArray_H)
    
    return imArray_H

"""
for key, item in player_dict.items():
    print(f"{key}:")
    for file_path in item:
        print(f"s{file_path}")
"""

class_dict = {
    'kareem abdul-jabbar - Google Search': 0,
    'kobe bryant - Google Search': 1,
    'larry bird - Google Search': 2,
    'magic johnson - Google Search': 3,
    'michael jordan - Google Search': 4,
}

x, y = [], []
for key, item in player_dict.items():
    for file_path in item:
        img = cv2.imread(file_path)
        scalled_raw_img = cv2.resize(img, (32, 32))
        img_har = w2d(img, 'db1', 5)
        scalled_img_har = cv2.resize(img_har, (32, 32))
        combined_img = np.vstack((scalled_raw_img.reshape(32*32*3, 1),scalled_img_har.reshape(32*32, 1)))
        x.append(combined_img)
        y.append(class_dict[key])
        
x = np.array(x).reshape(len(x),4096).astype(float)
        
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=42)

pipe = Pipeline([('scaler', StandardScaler()), ('svc', SVC(kernel='rbf', C=10, gamma='auto'))])
pipe.fit(x_train, y_train)

model_params = {
    'svm': {
        'model': svm.SVC(gamma='auto',probability=True),
        'params' : {
            'svc__C': [1,10,100,1000],
            'svc__kernel': ['rbf','linear']
        }  
    },
    'random_forest': {
        'model': RandomForestClassifier(),
        'params' : {
            'randomforestclassifier__n_estimators': [1,5,10]
        }
    },
    'logistic_regression' : {
        'model': LogisticRegression(solver='liblinear'),
        'params': {
            'logisticregression__C': [1,5,10]
        }
    }
}

scores = []
best_estimators = {}
for algo, mp in model_params.items():
    pipe = make_pipeline(StandardScaler(), mp['model'])
    clf = GridSearchCV(pipe, mp['params'], cv=5, return_train_score=False)
    clf.fit(x_train, y_train)
    scores.append({
        'model': algo,
        'best_score': clf.best_score_,
        'best_params': clf.best_params_
    })
    best_estimators[algo] = clf.best_estimator_
    
df = pd.DataFrame(scores,columns=['model','best_score','best_params'])

for algo in best_estimators:
    print(f'{algo}: {best_estimators[algo].score(x_test, y_test)}')
    
best_clf = best_estimators['svm']

cm = confusion_matrix(y_test, best_clf.predict(x_test))

plt.figure(figsize=(10,7))
sns.heatmap(cm, annot=True)
plt.xlabel('Predicted')
plt.ylabel('Truth')
plt.show()

joblib.dump(best_clf, 'saved_model.pkl')
with open('class_dictionary.json','w') as f:
    f.write(json.dumps(class_dict))