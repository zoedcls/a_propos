from flask import Flask, render_template
import folium
from geopy.distance import geodesic

app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenue sur ma page d'accueil !"

@app.route('/about')
def about():
    return "À propos de moi : Je suis en train d'apprendre à développer des applications web avec Flask !"

@app.route('/carte')
def carte():
    # Créer la carte
    coordGareFrethun = (50.901235, 1.811054)
    coordGareCalaisVille = (50.9536, 1.8509)
    coordUniversite = (50.9532, 1.8804)
    
    m = folium.Map(location=(50.95, 1.88), zoom_start=12, tiles="cartodb positron")
    
    # Ajouter les marqueurs
    folium.Marker(
        location=[coordUniversite[0], coordUniversite[1]],
        tooltip="Click me!",
        popup="Université",
        icon=folium.Icon(icon='1', prefix='fa', color='red'),
    ).add_to(m)
    
    folium.Marker(
        location=[coordGareCalaisVille[0], coordGareCalaisVille[1]],
        tooltip="Click me!",
        popup="Gare Calais ville",
        icon=folium.Icon(icon='2', prefix='fa', color='blue'),
    ).add_to(m)
    
    folium.Marker(
        location=[coordGareFrethun[0], coordGareFrethun[1]],
        tooltip="Click me!",
        popup="Gare Calais Frethun",
        icon=folium.Icon(icon='3', prefix='fa', color='green'),
    ).add_to(m)
    
    # Ajouter les lignes et distances
    distance = geodesic(coordUniversite, coordGareFrethun).kilometers
    folium.PolyLine(locations=[coordUniversite, coordGareFrethun], color='blue').add_to(m)
    folium.Marker(
        location=[(coordUniversite[0] + coordGareFrethun[0]) / 2, (coordUniversite[1] + coordGareFrethun[1]) / 2],
        icon=folium.DivIcon(html=f'<div style="font-size: 12pt; color: blue;">{distance:.2f} km</div>')
    ).add_to(m)
    
    distance = geodesic(coordUniversite, coordGareCalaisVille).kilometers
    folium.PolyLine(locations=[coordUniversite, coordGareCalaisVille], color='blue').add_to(m)
    folium.Marker(
        location=[(coordUniversite[0] + coordGareCalaisVille[0]) / 2, (coordUniversite[1] + coordGareCalaisVille[1]) / 2],
        icon=folium.DivIcon(html=f'<div style="font-size: 12pt; color: blue;">{distance:.2f} km</div>')
    ).add_to(m)
    
    # Sauvegarder la carte dans un fichier HTML temporaire
    carte_html = m._repr_html_()
    
    # Retourner la carte directement dans le navigateur
    return carte_html

if __name__ == '__main__':
    app.run(debug=True)
