# -*- coding: euc-kr -*-
import folium
import json
import time

# MapView(?�도, 경도, zoom배율)�?기본?�인 지???�출.
# MapView(?�드마크 ?�도, ?�드마크 경도, zoom배율, ?�드마크?�름, ?�드마크 ?�명)?�로 ?�당 ?�치???�드마크 마커가 찍�??�는 ?�태??지???�출.
# MapView.add_extra_data(json 경로)�?마커 ?�이??추�??�여 지???�?? **?�이??추�? ?�할??�?지?�만 �????�음!**
# MapView.add_extra_data(json 경로, 카테고리 ?�정(배열))�??�하??카테고리??마커?�만 추�??�여 지???�??가??
# MapView.add_extra_data(json 경로, 범위(km,?�수))�??�하??범위??마커?�만 추�??�여 지???�??가??
# MapView.add_extra_data(json 경로, 카테고리 ?�정(배열), 범위(km,?�수))�??�하??카테고리???�하??범위??마커?�만 추�??�여 지???�??가??
# MapView.marker_reset()?�로 맵의 마커�??��? 지?�고, MapView.add_data_to_map(카테고리 ?�정(배열), 범위(km,?�수))?�으�??�하??조건??맵을 ?�시 ?�성?�수 ?�다.

lat500m = 0.0090943410364699
lng500m = 0.0056344376831192


class Spot_type:
    cutlery = ['?�식', '중식', '?�식', '?�식', '뷔페/?�전/기�?', '?�식/카페/�?주점']
    gift = ['면세??, '백화??, '?�핑?�??, '?�통?�장']
    university = ['?�형/?�록문화??, '기념관', '문화?�적/?�상', '�?��/?�적', '기념�?민속문화??, '박물관', '공원']
    book = ['?�시??, '?�서관', '공연??, '?�화관']
    hotel = ['?�텔']


class MapView2:

    def __init__(self, lat, lng, zoom, landmark_name=None, landmark_description=None):
        self.locations = {}
        self.lat = lat
        self.lng = lng
        self.zoom = zoom
        self.landmark_name = landmark_name
        self.landmark_description = landmark_description
        self.map_osm = folium.Map(location=[lat, lng], zoom_start=zoom)
        self.marker_list = []
        if landmark_name is not None:
            if landmark_description is None:
                landmark_description = ""
            popup = folium.Popup(landmark_name + "<br><br>" + landmark_description, max_width=450)
            icon = folium.Icon(icon='star', color='red')
            target_marker = folium.Marker([lat, lng], popup=popup, icon=icon, language='kor')
            self.marker_list.append(target_marker)
            target_marker.add_to(self.map_osm)

    def add_extra_data(self, data_dir, selected_category=None, range=None):
        with open(data_dir, 'r') as f:
            self.locations = json.load(f)

        self.add_data_to_map(selected_category, range)

    def add_data_to_map(self, selected_category=None, range=None):

        categories = Spot_type.cutlery + Spot_type.gift + Spot_type.hotel + Spot_type.book + Spot_type.university

        selected_list = []
        marker_json = {}

        if selected_category is not None:
            for selected in selected_category:
                selected_list.append(selected)
        else:
            for selected in categories:
                selected_list.append(selected)

        if self.lat is not None and self.lng is not None and range is not None:
            latRangeMin = self.lat - lat500m * range  # lat좌표??+-0.5km * range범위
            lngRangeMin = self.lng - lng500m * range  # lng좌표??+-0.5km * range범위
            latRangeMax = self.lat + lat500m * range  # lat좌표??+-0.5km * range범위
            lngRangeMax = self.lng + lng500m * range  # lng좌표??+-0.5km * range범위
        else:
            latRangeMin = None
            lngRangeMin = None
            latRangeMax = None
            lngRangeMax = None

        for selected in selected_list:
            marker_json[selected] = []
            for data in self.locations[selected]:
                name = data['name_kor']
                category = data['category_name']
                add_kor_road = data['add_kor_road']
                lat = data['lat']
                lng = data['lng']

                if lat is not None and lng is not None:
                    if latRangeMax is not None and lngRangeMax is not None:
                        if lat < latRangeMin or lat > latRangeMax or lng < lngRangeMin or lng > lngRangeMax:
                            continue

                    marker_json[selected].append(data)

                    # 카테고리 분류
                    if category in Spot_type.cutlery:
                        icon_name = 'cutlery'
                        icon_color = 'red'
                    elif category in Spot_type.gift:
                        icon_name = 'gift'
                        icon_color = 'orange'
                    elif category in Spot_type.university:
                        icon_name = 'university'
                        icon_color = 'blue'
                    elif category in Spot_type.book:
                        icon_name = 'book'
                        icon_color = 'green'
                    elif category in Spot_type.hotel:
                        icon_name = 'hotel'
                        icon_color = 'purple'
                    else:
                        icon_name = 'thumbtack'
                        icon_color = 'black'

                    # 마커 ?�성

                    popup = folium.Popup(name + ' : ' + category + '<br><br>' + add_kor_road, max_width=450)
                    marker = folium.Marker([lat, lng], popup=popup,
                                           icon=folium.Icon(icon=icon_name, color=icon_color, prefix='fa'),
                                           language='kor')
                    marker.add_to(self.map_osm)

        self.save_map()
        self.save_json(selected_category, marker_json)

    def save_map(self, filename='recommand_total'):
        self.map_osm.save(filename + '.html')

    def save_json(self, selected_category, marker_json):
        with open("location_classify_by_category.json", 'w') as fw:
            json.dump(marker_json, fw, indent=4, ensure_ascii=False)
        return marker_json

    def marker_reset(self):
        self.map_osm = folium.Map([self.lat, self.lng], zoom_start=self.zoom)
        self.marker_list = []
        if self.landmark_name is not None:
            if self.landmark_description is None:
                self.landmark_description = ""
            popup = folium.Popup(self.landmark_name + "<br><br>" + self.landmark_description, max_width=450)
            icon = folium.Icon(icon='star', color='red')
            target_marker = folium.Marker([self.lat, self.lng], popup=popup, icon=icon, language='kor')
            self.marker_list.append(target_marker)
            target_marker.add_to(self.map_osm)


if __name__ == '__main__':
    start = time.time()
    mapview = MapView(lat=37.5710015, lng=126.9747479, zoom=16, landmark_name="?�순?�장군동??)
    # mapview.add_extra_data('seoul_culture_data_processed.json')
    mapview.add_extra_data('location_classify_by_category.json', ['면세??], range=4)  # ?�을 ?�이?? 출력??카테고리, km범위
    mapview.marker_reset()
    mapview.add_data_to_map(['?�식'], range=2)
    print("time :", time.time() - start)  # ?�재?�각 - ?�작?�간 = ?�행 ?�간
