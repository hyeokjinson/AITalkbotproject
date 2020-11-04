
 # -*- coding: euc-kr -*- 
from PIL import Image
import os, glob, numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd

csv=pd.read_csv('out.csv',names=['id_value'],encoding='CP949')
cate=csv['id_value']
caltech_dir  = '/data/projectData/seoul/'
cate=cate.values

categories=[]
for d in cate:
   categories.append(d)

nb_classes   = len(categories)

image_w = 128
image_h = 128

pixel = image_h * image_w * 3

X = []
y = []
print(len(categories))
for idx, cat in enumerate(categories):
    label = [0 for i in range(nb_classes)]
    label[idx] = 1

    image_dir = caltech_dir + "/" + cat
    files = glob.glob(image_dir+"/*.jpeg")
    print(cat, " file length : ", len(files))
    for i, f in enumerate(files):
        img = Image.open(f)
        img = img.convert("RGB")
        img = img.resize((image_w, image_h))
        data = np.asarray(img)

        X.append(data)
        y.append(label)

        if i % 700 == 0:
            print(cat, " : ", f)

X = np.array(X)
y = np.array(y)



X_train, X_test, y_train, y_test = train_test_split(X, y)
xy = (X_train, X_test, y_train, y_test)
np.save("landmark_data_final.npy", xy)

print("ok", len(y))


