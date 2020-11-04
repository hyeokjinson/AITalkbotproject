# -*- coding: euc-kr -*-
import folium
import json
from search import search_name
import  webbrowser
import sys
# MapView(위도, 경도, zoom배율)로 기본적인 지도 호출.
# MapView(랜드마크 위도, 랜드마크 경도, zoom배율, 랜드마크이름, 랜드마크 설명)으로 해당 위치에 랜드마크 마커가 찍혀있는 상태의 지도 호출.
# MapView.add_extra_data(json 경로)로 마커 데이터 추가하여 지도 저장. **데이터 추가 안할시 빈 지도만 볼 수 있음!**

class MapView1:

    def __init__(self, lat, lng, zoom, landmark_name=None, landmark_description=None):
        self.locations = {}
        self.map_osm = folium.Map(location=[lat, lng], zoom_start=zoom)
        self.marker_list = []
        if landmark_name is not None:
            popup = folium.Popup(landmark_name + "<br><br>" + landmark_description, max_width=450)
            icon = folium.Icon(icon='star', color='red')
            target_marker = folium.Marker([lat, lng], popup=popup, icon=icon, language='kor')
            self.marker_list.append(target_marker)
            target_marker.add_to(self.map_osm)

    def add_extra_data(self, data_dir):
        with open(data_dir, 'r',encoding='cp949') as f:
            self.locations = json.load(f)

        self.add_data_to_map()

    def add_data_to_map(self):
        categories = []
        for data in self.locations['DATA']:
            name = data['name_kor']
            category = data['category_name']
            lat = data['lat']
            lng = data['lng']

            # 카테고리 분류
            if category not in categories:
                categories.append(category)
            if category in ['한식', '중식', '일식', '양식', '뷔페/퓨전/기타', '양식/카페/바/주점']:
                icon_name = 'cutlery'
                icon_color = 'red'
            elif category in ['면세점', '백화점', '쇼핑타운', '전통시장']:
                icon_name = 'gift'
                icon_color = 'orange'
            elif category in ['유형/등록문화재', '기념관', '문화유적/동상', '국보/사적', '기념물/민속문화재', '박물관', '공원']:
                icon_name = 'university'
                icon_color = 'blue'
            elif category in ['전시장', '도서관', '공연장', '영화관']:
                icon_name = 'book'
                icon_color = 'green'
            elif category in ['호텔']:
                icon_name = 'hotel'
                icon_color = 'purple'
            else:
                icon_name = 'thumbtack'
                icon_color = 'black'

            # 마커 생성
            if lat is not None and lng is not None:
                popup = folium.Popup(name + ' : ' + category, max_width=450)
                marker = folium.Marker([lat, lng], popup=popup,
                                       icon=folium.Icon(icon=icon_name, color=icon_color, prefix='fa'), language='kor')
                if marker not in self.marker_list:
                    self.marker_list.append(marker)
                    marker.add_to(self.map_osm)

        self.save_map()
        return

    def save_map(self, filename='recommand_total'):
        self.map_osm.save('./templates/'+filename + '.html')

        filepath='./templates'
        webbrowser.open_new_tab(filepath)
        return

