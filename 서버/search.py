# -*- coding: euc-kr -*-
import json
with open('crawling_ex.json', 'r',encoding='cp949') as f:
    locations = json.load(f)
def search_name(landmark_name):
    data=locations
    id_number=data['DATA']

    for id_num in id_number:
        if id_num['spot_name']==landmark_name:
            print(id_num['lat'])
            return id_num['lat'],id_num['lng']

    return -1

