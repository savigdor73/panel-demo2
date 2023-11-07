from Dashboard import Dashboard
import panel as pn
import re
import folium
from folium.plugins import FastMarkerCluster
from time import time
from functools import wraps
from time import perf_counter

def memoize(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args)+str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    return wrapper


def init(self):
        start = time()
        m = folium.Map(location=[47.420664984, -120.321832046], zoom_start=7) ## map of Washington 
        num_rows = self.df.shape[0]
        cluster_size = num_rows
        count = int(num_rows / cluster_size) + 1
        marker_cluster = list([None] * count)
        #marker_cluster = MarkerCluster().add_to(m)
        folium_pane = pn.pane.plot.Folium(m, height=600)
        col_name = "Vehicle Location"

        i = 0
        cluster = 0
        locations = list()
        for row in self.df.iterrows():
            i += 1
            if i == 1:
               pass
               #marker_cluster[cluster] = FastMarkerCluster().add_to(m)
            elif i > cluster_size:
                 cluster += 1
                 print("Cluster=",cluster)
                 i = 0
            try:
                string = re.sub(r"POINT\s*\(|\)", "",row[1]['Vehicle Location'])
            except TypeError:
            # Split the string into two float numbers.
                if not isinstance(string, str):
                    print ("this is not a string!")
                    continue
            try:
                s_longitude, s_latitude  = string.split(" ")
                longitude = float(s_longitude)
                latitude = float(s_latitude)
                locations.append((latitude,longitude))
                #folium.Marker(list((latitude, longitude))).add_to(marker_cluster[cluster])
            except Exception:
                continue
            num_rows -= 1
        
        #latitude = float(47.575195000000065)
        #longitude = float(-122.61136499999998)
        #latitude1 = float(47.53730000000007)
        #longitude1 = float(-122.63926499999997)
        #try:
        #    m1 = folium.Marker((latitude, longitude))
        #    m2 = folium.Marker(list((latitude1,longitude1)))
        #    markers = [m1,m2]
        #    for marker in markers:
        #        marker.add_to(m)
        #except Exception as e:
        #    print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee=",e)
        
        marker_cluster[cluster] = FastMarkerCluster(locations).add_to(m)
        folium_pane.object = m
        
        row = pn.Column(folium_pane)
        self.content = row
        print(f'finished after {round(time() - start,2)} seconds')


class CountyInfoDashboard(Dashboard):
    pn.extension(sizing_mode="stretch_width")
    def __init__(self):
        init(self)

    def view(self):
        return self.content