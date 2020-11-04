 # -*- coding: euc-kr -*- 
from PIL import Image
import os, glob, numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

#csv=pd.read_csv('category.csv',names=['landmark_id','landmark_name'],encoding='CP949')
#cate=csv['landmark_name']
#cate=cate.values
categories=['N����Ÿ��','63��Ƽ','��걸û','�����ȭ��_��������','�湫���̼��ŵ���','â�ǹ�','�Ե�����Ÿ��','�ø��ȴ뱳','������б�','���������']

#for d in cate:
#    tmp=d.replace(" ","")
#    categories.append(tmp)

caltech_dir = "./test_data/imgs_others_test"
image_w = 128
image_h = 128

pixels = image_h * image_w * 3

X = []
filenames = []
files = glob.glob(caltech_dir+"/*.*")
for i, f in enumerate(files):
    img = Image.open(f)
    img = img.convert("RGB")
    img = img.resize((image_w, image_h))
    data = np.asarray(img)
    filenames.append(f)
    X.append(data)

X = np.array(X)
model = load_model('./model1/landmark_img_classification.model')

prediction = model.predict(X)

np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
cnt = 0

for i in prediction:
    pre_ans = i.argmax()
    print(len(i))
    print(cnt)
    print(i)
    print(pre_ans)
    pre_ans_str = ''
    for j in range(len(categories)):
        if pre_ans == j: pre_ans_str = categories[j]
        
        if pre_ans_str!='':
            if i[j] >= 0.8:
             print("the "+filenames[cnt].split("/")[3]+"imageis"+pre_ans_str+"acc")
             break
            
    cnt += 1