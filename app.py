from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenue sur ma page d'accueil !"

@app.route('/about')
def about():
    return "À propos de moi : Je suis en train d'apprendre à développer des applications web avec Flask !"

if __name__ == '__main__':
    app.run(debug=True)

    import folium
from geopy.distance import geodesic
import random  # Pour simuler des trajets différents

# Coordonnées
coordGareCalaisVille = (50.9536, 1.8509)
coordUniversite = (50.9532, 1.8804)

# Création de la carte
m = folium.Map(location=(50.95, 1.87), zoom_start=14, tiles="cartodb positron")  # Ajustement du zoom pour mieux voir les détails

# Ajout des marqueurs principaux
folium.Marker(
    location=[coordUniversite[0], coordUniversite[1]],
    tooltip="ULCO Calais",
    popup="Université du Littoral Côte d'Opale",
    icon=folium.Icon(icon='graduation-cap', prefix='fa', color='red'),
).add_to(m)

folium.Marker(
    location=[coordGareCalaisVille[0], coordGareCalaisVille[1]],
    tooltip="Gare Calais-Ville",
    popup="Gare de Calais-Ville",
    icon=folium.Icon(icon='train', prefix='fa', color='blue'),
).add_to(m)

# Calcul de la distance directe
distance = geodesic(coordUniversite, coordGareCalaisVille).kilometers

# Simuler différents trajets

# 1. Trajet piéton (plus sinueux, suivant les rues)
# Simulation de points intermédiaires pour un trajet piéton
pieton_points = [
    coordGareCalaisVille,
    (50.9540, 1.8540),  # Points intermédiaires pour simuler un trajet piéton
    (50.9545, 1.8580),
    (50.9542, 1.8630),
    (50.9538, 1.8680),
    (50.9535, 1.8730),
    (50.9533, 1.8760),
    coordUniversite
]

# 2. Trajet en bus (quelques arrêts, trajet différent)
bus_points = [
    coordGareCalaisVille,
    (50.9550, 1.8550),  # Points pour simuler arrêts de bus
    (50.9558, 1.8620),  # Arrêt bus 1
    (50.9552, 1.8700),  # Arrêt bus 2
    (50.9540, 1.8750),  # Arrêt bus 3
    coordUniversite
]

# 3. Trajet en voiture (plus direct)
voiture_points = [
    coordGareCalaisVille,
    (50.9545, 1.8550),
    (50.9550, 1.8650),
    (50.9545, 1.8730),
    coordUniversite
]

# Ajout des trajets à la carte
# Trajet piéton en orange
pieton_line = folium.PolyLine(
    locations=pieton_points,
    color='orange',
    weight=4,
    opacity=0.8,
    tooltip="Trajet piéton"
).add_to(m)

# Distance pour le trajet piéton
pieton_distance = sum(geodesic(pieton_points[i], pieton_points[i+1]).kilometers for i in range(len(pieton_points)-1))
folium.Marker(
    location=[(coordGareCalaisVille[0] + coordUniversite[0]) / 2 - 0.002, (coordGareCalaisVille[1] + coordUniversite[1]) / 2],
    icon=folium.DivIcon(html=f'<div style="font-size: 12pt; color: orange;">🚶 {pieton_distance:.2f} km (~{int(pieton_distance/0.07)} min)</div>')
).add_to(m)

# Trajet bus en vert
bus_line = folium.PolyLine(
    locations=bus_points,
    color='green',
    weight=4,
    opacity=0.8,
    tooltip="Trajet bus"
).add_to(m)

# Distance pour le trajet en bus
bus_distance = sum(geodesic(bus_points[i], bus_points[i+1]).kilometers for i in range(len(bus_points)-1))
folium.Marker(
    location=[(coordGareCalaisVille[0] + coordUniversite[0]) / 2, (coordGareCalaisVille[1] + coordUniversite[1]) / 2 - 0.005],
    icon=folium.DivIcon(html=f'<div style="font-size: 12pt; color: green;">🚌 {bus_distance:.2f} km (~{int(bus_distance/0.4)} min)</div>')
).add_to(m)

# Trajet voiture en bleu
voiture_line = folium.PolyLine(
    locations=voiture_points,
    color='blue',
    weight=4,
    opacity=0.8,
    tooltip="Trajet voiture"
).add_to(m)

# Distance pour le trajet en voiture
voiture_distance = sum(geodesic(voiture_points[i], voiture_points[i+1]).kilometers for i in range(len(voiture_points)-1))
folium.Marker(
    location=[(coordGareCalaisVille[0] + coordUniversite[0]) / 2 + 0.002, (coordGareCalaisVille[1] + coordUniversite[1]) / 2],
    icon=folium.DivIcon(html=f'<div style="font-size: 12pt; color: blue;">🚗 {voiture_distance:.2f} km (~{int(voiture_distance/0.5)} min)</div>')
).add_to(m)

# Ajout d'une légende
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 180px; height: 120px; 
            border:2px solid grey; z-index:9999; font-size:14px;
            background-color:white;
            padding: 10px">
    <b>Légende</b><br>
    <i style="background:orange;width:10px;height:10px;display:inline-block"></i> Trajet piéton<br>
    <i style="background:green;width:10px;height:10px;display:inline-block"></i> Trajet bus<br>
    <i style="background:blue;width:10px;height:10px;display:inline-block"></i> Trajet voiture<br>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Sauvegarde de la carte
m.save("carte_trajets.html")
