#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pregunta a Nominatim la dirección real de cada sitio candidato, para no
escribir direcciones de memoria. Deja el resultado en datos-fuente/direcciones.json."""
import json, os, sys, time, urllib.request, urllib.parse

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SALIDA = 'datos-fuente/direcciones.json'
UA = 'guia-viaje-lyon/1.0 (uso personal)'

CANDIDATOS = [
 # Vieux Lyon
 "Daniel et Denise Saint-Jean, Lyon", "Le Boeuf d'Argent, Lyon", "Les Adrets, rue du Boeuf, Lyon",
 "Notre Maison, Lyon", "Terre Adelice, Lyon", "Le Musee bouchon, Lyon",
 # Presqu'île
 "Cafe des Federations, Lyon", "Chez Hugon, Lyon", "Le Garet, Lyon",
 "Cafe Comptoir Abel, Lyon", "Le Poelon d'Or, Lyon", "Cafe du Jura, Lyon",
 "Brasserie Georges, Lyon", "La Mere Brazier, Lyon", "Prairial, Lyon", "Chez Paul, rue Major Martin, Lyon",
 "Halles de la Martiniere, Lyon", "Bistrot du Potager, rue de la Martiniere, Lyon",
 "Maison Pralus, Lyon", "Seve chocolatier, Lyon", "Marche Saint-Antoine, Lyon",
 # Croix-Rousse
 "Le Bouchon des Filles, Lyon", "Substrat restaurant, Lyon", "Le Canut et les Gones, Lyon",
 "Marche de la Croix-Rousse, Lyon", "Sebastien Bouillet, place de la Croix-Rousse, Lyon",
 "Mokxa, rue de l'Abbe Rozier, Lyon", "L'Ourson qui boit, Lyon",
 # Confluence
 "Le Selcius, Lyon", "La Sucriere, Lyon", "Musee des Confluences, Lyon",
 # Halles / Brotteaux / Tête d'Or
 # sep-2026: las mères y el sustituto de Substrat (cerró el 6-jul-2024)
 "Maison Lea, quai des Celestins, Lyon", "Bouchon Lea, place Antonin Gourju, Lyon",
 "La Mere Jean, rue des Marronniers, Lyon", "Cafe du Peintre, boulevard des Brotteaux, Lyon",
 "Daniel et Denise Croix-Rousse, rue de Cuire, Lyon",
 "Halles de Lyon Paul Bocuse", "Daniel et Denise Crequi, Lyon", "A Ma Vigne, Lyon",
 "Bernachon, Lyon", "Le Bouchon Sully, Lyon", "Brasserie des Brotteaux, Lyon",
 "Les Apothicaires, rue de Seze, Lyon", "L'Est Paul Bocuse, Lyon",
 # visitas
 "Basilique Notre-Dame de Fourviere, Lyon", "Theatres romains de Fourviere, Lyon",
 "Cathedrale Saint-Jean, Lyon", "Musee des Beaux-Arts de Lyon", "Mur des Canuts, Lyon",
 "Maison des Canuts, Lyon", "Institut Lumiere, Lyon", "Parc de la Tete d'Or, Lyon",
 "Place Bellecour, Lyon", "Place des Terreaux, Lyon", "Cour des Voraces, Lyon",
 "Musee Cinema et Miniature, Lyon", "Musee Gadagne, Lyon", "Fresque des Lyonnais, Lyon",
 "Passage Thiaffait, Lyon", "Halle Tony Garnier, Lyon", "Jardin Rosa Mir, Lyon",
]

datos = json.load(open(SALIDA)) if os.path.exists(SALIDA) else {}
for q in CANDIDATOS:
    if q in datos:
        continue
    url = 'https://nominatim.openstreetmap.org/search?' + urllib.parse.urlencode(
        {'q': q, 'format': 'jsonv2', 'limit': 1, 'addressdetails': 1})
    try:
        r = json.load(urllib.request.urlopen(
            urllib.request.Request(url, headers={'User-Agent': UA}), timeout=25))
    except Exception as e:
        print('  error %s: %s' % (q, e)); r = []
    if r:
        a = r[0].get('address', {})
        datos[q] = {
            'nombre': r[0].get('name', ''),
            'calle': ' '.join(x for x in [a.get('house_number', ''), a.get('road', '')] if x),
            'cp': a.get('postcode', ''),
            'barrio': a.get('suburb') or a.get('city_district') or '',
            'lat': round(float(r[0]['lat']), 6), 'lon': round(float(r[0]['lon']), 6),
            'tipo': r[0].get('type', ''),
        }
    else:
        datos[q] = None
    time.sleep(1.1)

json.dump(datos, open(SALIDA, 'w'), ensure_ascii=False, indent=1)
for q, d in datos.items():
    print('%-52s %s' % (q, ('%s | %s %s | %s' % (d['nombre'], d['calle'], d['cp'], d['barrio'])) if d else '✗ NO ENCONTRADO'))
