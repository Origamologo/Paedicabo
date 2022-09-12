#!/usr/bin/env python3

import geocoder
import folium

ip_adress = input("What ip do you want to locate?\n")
ip = geocoder.ip(ip_adress)
print(ip.city)
print(ip.latlng)

location = ip.latlng

map = folium.Map(location=location, zoom_start=10)
folium.CircleMarker(location=location, radius=50, color="red").add_to(map)
folium.Marker(location).add_to(map)

map
map.save("map.html")
