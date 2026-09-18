#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Candidatas a foto sacadas de las CATEGORÍAS de Commons (no de la búsqueda por
texto, que devuelve cualquier cosa). Reanudable: solo pide lo que falta."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from buscafotos import de_categoria
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SALIDA = 'generador/datos-fuente/fotos3.json'

# los nombres exactos salen de list=search en srnamespace=14: inventárselos
# devuelve categorías vacías sin decir que no existen
CATS = {
 'hero':        'Views of Lyon',
 'vieux':       'Vieux Lyon',
 'fourviere':   'Views of Basilique Notre-Dame de Fourvière',
 'fourviere2':  'Basilique Notre-Dame de Fourvière',
 'romanos':     'Théâtre romain de Fourvière',
 'terreaux':    'Place des Terreaux (Lyon)',
 'bellecour':   'Place Bellecour (Lyon)',
 'croix':       'Mur des Canuts',
 'croix2':      'Boulevard de la Croix-Rousse (Lyon)',
 'croix3':      'Place de la Croix-Rousse (Lyon)',
 'confluence':  'Musée des Confluences',
 'halles':      'Halles de Lyon-Paul Bocuse',
 'lumiere':     'Institut Lumière',
 'teteor':      "Parc de la Tête d'Or",
 'traboules':   'Traboules',
 'mercadosa':   'Quai Saint-Antoine (Lyon)',
}

res = json.load(open(SALIDA)) if os.path.exists(SALIDA) else {}
for k, cat in CATS.items():
    if res.get(k):
        print('  %-11s ya estaba (%d)' % (k, len(res[k]))); continue
    r = de_categoria(cat, 14)
    res[k] = r
    print('  %-11s %2d candidatas, %d apaisadas · %s' %
          (k, len(r), sum(1 for x in r if x['apaisada']), r[0]['t'][5:60] if r else '— vacía'))
    json.dump(res, open(SALIDA, 'w'), ensure_ascii=False)
    time.sleep(5)
print('\nAhora: python3 generador/hoja-contacto.py generador/datos-fuente/fotos3.json <carpeta>')
