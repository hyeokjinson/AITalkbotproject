# -*- coding: euc-kr -*-
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from PIL import Image
import os, glob, numpy as np
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import pandas as pd

data_datagen = ImageDataGenerator(rescale=1. / 255)
csv=pd.read_csv('out.csv',names=['id_value'],encoding='CP949')
cate=csv['id_value']
caltech_dir  = '/data/projectData/seoul/'
cate=cate.values

categories=[]
for d in cate:
   categories.append(d)
nb_classes=len(categories)

datagen = ImageDataGenerator(rescale=1. / 255,
                                  rotation_range=15,
                                  shear_range=0.5,
                                  # width_shift_range=0.1,
                                  # height_shift_range=0.1,
                                  horizontal_flip=True,
                                  vertical_flip=True,
                                  fill_mode='nearest')
for idx, cat in enumerate(categories):
    label = [0 for i in range(nb_classes)]
    label[idx] = 1

    image_dir = caltech_dir + "/" + cat
    files = glob.glob(image_dir+"/*.*")
    for i, f in enumerate(files):
        img = load_img(f)  # PIL �̹���
        x = img_to_array(img)  # (3, 150, 150) ũ���� NumPy �迭
        x = x.reshape((1,) + x.shape)  # (1, 3, 150, 150) ũ���� NumPy �迭

# �Ʒ� .flow() �Լ��� ���� ��ȯ�� �̹����� ��ġ ������ �����ؼ�
# ������ `preview/` ������ �����մϴ�.
        i = 0
        for batch in datagen.flow(x, batch_size=1,
                            save_to_dir=image_dir, save_prefix='1', save_format='JPG'):
            i += 1
            if i > 2:
                break  # �̹��� 20���� �����ϰ� ��Ĩ�ϴ�
        print("finish")