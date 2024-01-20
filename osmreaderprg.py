import osmread
import tkinter as tk
from tkinter.dialog import askopenfilename
import folium





tk.Tk().withdraw()
def parse_osm_file(osm_file):
    # This function will parse the OSM file and return a list of nodes (latitude, longitude)
    nodes = []
    for entity in osmread.parse_file(osm_file):
        if isinstance(entity, osmread.Node):
            nodes.append((entity.lat, entity.lon))
    return nodes

# Parse the OSM file
osm_file_path = askopenfilename(title='Select osm', filetypes=[("openstreets", "*.osm")])
nodes = parse_osm_file(osm_file_path)

# Create a map using Folium
m = folium.Map(location=[nodes[0][0], nodes[0][1]], zoom_start=15)

# Add nodes to the map
for node in nodes:
    folium.CircleMarker(location=node, radius=1, color='blue').add_to(m)

# Save to an HTML file
m.save('osm_map.html')
