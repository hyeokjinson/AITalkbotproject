# -*- coding: euc-kr -*-
import flask
from flask import Flask, request, render_template
from PIL import Image
import joblib
import numpy as np
from search import search_name
from mapview import MapView1
import os, glob, numpy as np
from tensorflow.keras.models import load_model
import pandas as pd
from search_category import search_cate
from prediction_img import prediction

# from prediction_img import prediction
app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return flask.render_template('index.html')


@app.route("/recommand_total")
def recommand_total():
    return flask.render_template('recommand_total.html')


@app.route('/test1', methods=['GET'])
def make_prediction():
    if request.method == 'GET':
        # 업로드 파일 처리 분기
        global before_lat, before_lng
        # 이미지 픽셀 정보 읽기
        # 알파 채널 값 제거 후 1차원 Reshape
        res = prediction()
        lat, lng = search_name(str(res))
        before_lng = float(lng)
        before_lat = float(lat)
        mapview = MapView1(lat, lng, 16)

        mapview.add_extra_data('seoul_culture_data_processed.json')
        mapview.add_data_to_map()
        # 결과 리턴
        res = str(res)
        return res


@app.route('/hansik', methods=['GET'])
def find_hansik():
    if request.method == 'GET':
        mat_list = []
        mat={'맛집추천':''}
        
        res = search_cate("한식")
        
        for name,add,lat,lng in res:
            print(name,add,lat,lng)
            if before_lat - 0.004 <= float(lat) <= before_lat + 0.004 and before_lng - 0.004 <= float(lng) <= before_lng + 0.004:
                mat['맛집추천']+='맛집: '+name+"<br>"+'주소:'+add+"<br>"+"<br>"
        
          
    return mat['맛집추천'] 

@app.route('/china_food', methods=['GET'])
def find_china_food():
    if request.method == 'GET':
        mat_list = []
        mat={'맛집추천':''}
        
        res = search_cate("중식")
        
        for name,add,lat,lng in res:
            
            if before_lat - 0.008 <= float(lat) <= before_lat + 0.008 and before_lng - 0.008 <= float(lng) <= before_lng + 0.008:
                mat['맛집추천']+='맛집: '+name+"<br>"+'주소:'+add+"<br>"+"<br>"
        print(mat['맛집추천'])
    return mat['맛집추천'] 

@app.route('/japan_food', methods=['GET'])
def find_japan_food():
    if request.method == 'GET':
        mat_list = []
        mat={'맛집추천':''}
        
        res = search_cate("일식")
        
        for name,add,lat,lng in res:
            print(name,add,lat,lng)
            if before_lat - 0.004 <= float(lat) <= before_lat + 0.004 and before_lng - 0.004 <= float(lng) <= before_lng + 0.004:
                mat['맛집추천']+='맛집: '+name+"<br>"+'주소:'+add+"<br>"+"<br>"
        
          
    return mat['맛집추천']
@app.route('/culture', methods=['GET'])
def find_culture():
    if request.method == 'GET':
        mat_list = []
        mat={'문화유적':''}
        
        res = search_cate("문화유적/동상")
        
        for name,add,lat,lng in res:
            print(name,add,lat,lng)
            if before_lat - 0.004 <= float(lat) <= before_lat + 0.004 and before_lng - 0.004 <= float(lng) <= before_lng + 0.004:
                mat['문화유적']+='문화유적 및 동상: '+name+"<br>"+'주소:'+add+"<br>"+"<br>"
        
          
    return  mat['문화유적']

@app.route('/hotel', methods=['GET'])
def find_hotel():
    if request.method == 'GET':
        mat_list = []
        mat={'호텔추천':''}
        
        res = search_cate("호텔")
        
        for name,add,lat,lng in res:
            print(name,add,lat,lng)
            if before_lat - 0.004 <= float(lat) <= before_lat + 0.004 and before_lng - 0.004 <= float(lng) <= before_lng + 0.004:
                mat['호텔추천']+='호텔추천: '+name+"<br>"+'주소:'+add+"<br>"+"<br>"
        
          
    return  mat['호텔추천']   

if __name__ == '__main__':
    before_lat = 0
    before_lng = 0
    model=load_model('./model1/landmark_img_classification.model')
    app.run(host='0.0.0.0', port=5000)