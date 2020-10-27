## Webmap

# we need a third party library: folium 
import folium
import pandas as pd
# print(dir(folium))

# ******** create map object (basemap) *********
# zoom_start - adds zoom (optional). add tiles - display layer (optional. Default is from open street map)
map = folium.Map(location = [41.336606, -100.413935], zoom_start = 5, tiles = "Stamen Terrain")

# ******** between object and save, you can add features *******
# With feature groups, you can add multiple children and add more control layers later. Also good for readability

# **** FEATURE GROUP 1 ****
fgv = folium.FeatureGroup(name = 'Volcanoes')

# ** add markers from files ** 
df = pd.read_csv('Volcanoes.txt')
lat = list(df['LAT'])  # create a list of latitudes
long = list(df['LON']) # create a list of longitudes
elev = list(df['ELEV']) # get elevations for popups. **popup gets strings, not numbers**
name = list(df["NAME"])

# add html links for pop ups
html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

# dynamic colors for the range of elevations
def color_producer(el):
    if el < 1000:
        return 'green'
    elif 1000 <= el < 3000:
        return 'orange'
    else:
        return 'red'

# add markers for volcanoes
# iterate through many lists - zip function
for lt, ln, el, na in zip(lat, long, elev, name):
    iframe = folium.IFrame(html=html % (na, na, el), width=200, height=80) #html 
    fgv.add_child(folium.CircleMarker(location = [lt, ln], popup = folium.Popup(iframe),
                                    icon = folium.Icon(color = color_producer(el)), 
                                    fill_color = color_producer(el), color = 'grey', fill_opacity = 0.7))

# **** FEATURE GROUP 2 ****
# add polygon layer for all countries
fgp = folium.FeatureGroup(name = 'Population')

fgp.add_child(folium.GeoJson(data = open('world.json', 'r', encoding='utf-8-sig').read(), 
                            style_function = lambda x: {
                                'fillColor': 'green' if x['properties']['POP2005'] < 25000000
                                else 'yellow' if 25000000 <= x['properties']['POP2005'] < 50000000 
                                else 'orange' if 50000000 <= x['properties']['POP2005'] <= 100000000 else 'red'
                            }))

# ******** add child which is comprised of feature groups to the map object ********
map.add_child(fgv)
map.add_child(fgp) # make sure to put population FG after volcanoes FG

map.add_child(folium.LayerControl())

# ******** point to map object and save map in html format ********
map.save('map1.html')