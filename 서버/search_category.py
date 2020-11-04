# -*- coding: euc-kr -*-
import json
with open('seoul_culture_data_processed.json', 'r',encoding='CP949') as f:
    data = json.load(f)

def search_cate(hansik):
    id_number=data['DATA']
    res=[]
    for id_num in id_number:
        if id_num['category_name']==hansik:
            if id_num['name_kor']!=None and id_num['add_kor_road']!=None and id_num['lat'] and id_num['lng']!=None:
                name,add,lat,lng=id_num['name_kor'],id_num['add_kor_road'],id_num['lat'],id_num['lng']
                res.append([name,add,lat,lng])

    return res