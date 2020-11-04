 # -*- coding: euc-kr -*- 
import os, glob, numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
import matplotlib.pyplot as plt
import keras.backend.tensorflow_backend as K
import pandas as pd

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)

X_train, X_test, y_train, y_test = np.load('landmark_data_final.npy')
print(X_train.shape)
print(X_train.shape[0])
csv=pd.read_csv('out.csv',names=['id_value'],encoding='CP949')
cate=csv['id_value']
caltech_dir  = '/data/projectData/seoul/'
cate=cate.values

categories=[]
for d in cate:
   categories.append(d)
#csv=pd.read_csv('category.csv',names=['landmark_id','landmark_name'],encoding='CP949')
#cate=csv['landmark_name']
#cate=cate.values
categories=[]

#for d in cate:
#    tmp=d.replace(" ","")
#    categories.append(tmp)

gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.333)
sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))

nb_classes = len(categories)

X_train = X_train.astype(float) / 255
X_test = X_test.astype(float) / 255

with K.tf.device('/device:GPU:0'):
    model = Sequential()
    model.add(Conv2D(32, (3,3), padding="same", input_shape=X_train.shape[1:], activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))
    
    model.add(Conv2D(64, (3,3), padding="same", activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))
    
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model_dir = './model1'
    
    if not os.path.exists(model_dir):
        os.mkdir(model_dir)
    
    model_path = model_dir + '/landmark_img_classification.model'
    checkpoint = ModelCheckpoint(filepath=model_path , monitor='val_loss', verbose=1, save_best_only=True)
    early_stopping = EarlyStopping(monitor='val_loss', patience=6)
    
model.summary()

#,steps_per_epoch=15
history = model.fit(X_train, y_train, batch_size=128,epochs=100, validation_data=(X_test, y_test), callbacks=[checkpoint, early_stopping])
print("ACC : %.4f" % (model.evaluate(X_test, y_test)[1]))

model.save('landmark_img_classification_final.model')
