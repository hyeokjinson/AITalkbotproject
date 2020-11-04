# -*- coding: euc-kr -*-
import folium
import json
from search import search_name
import  webbrowser
import sys
# MapView(����, �浵, zoom����)�� �⺻���� ���� ȣ��.
# MapView(���帶ũ ����, ���帶ũ �浵, zoom����, ���帶ũ�̸�, ���帶ũ ����)���� �ش� ��ġ�� ���帶ũ ��Ŀ�� �����ִ� ������ ���� ȣ��.
# MapView.add_extra_data(json ���)�� ��Ŀ ������ �߰��Ͽ� ���� ����. **������ �߰� ���ҽ� �� ������ �� �� ����!**

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

            # ī�װ� �з�
            if category not in categories:
                categories.append(category)
            if category in ['�ѽ�', '�߽�', '�Ͻ�', '���', '����/ǻ��/��Ÿ', '���/ī��/��/����']:
                icon_name = 'cutlery'
                icon_color = 'red'
            elif category in ['�鼼��', '��ȭ��', '����Ÿ��', '�������']:
                icon_name = 'gift'
                icon_color = 'orange'
            elif category in ['����/��Ϲ�ȭ��', '����', '��ȭ����/����', '����/����', '��买/�μӹ�ȭ��', '�ڹ���', '����']:
                icon_name = 'university'
                icon_color = 'blue'
            elif category in ['������', '������', '������', '��ȭ��']:
                icon_name = 'book'
                icon_color = 'green'
            elif category in ['ȣ��']:
                icon_name = 'hotel'
                icon_color = 'purple'
            else:
                icon_name = 'thumbtack'
                icon_color = 'black'

            # ��Ŀ ����
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

