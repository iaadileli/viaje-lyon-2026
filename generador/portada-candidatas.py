#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Candidatas para cambiar la portada (sep-2026): la vista desde Fourvière era
un mar de tejados sin nada que mirar. Se buscan vistas del Saona con el Vieux Lyon
y Fourvière, que es la postal de Lyon. Reanudable, como categorias.py."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from buscafotos import de_categoria
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SALIDA = 'generador/datos-fuente/fotos5.json'

CATS = {
 'pecherie':   'Quai de la Pêcherie (Lyon)',
 'stvincent':  'Quai Saint-Vincent (Lyon)',
 'bonaparte':  'Pont Bonaparte (Lyon)',
 'couturier':  'Passerelle Paul Couturier (Lyon)',
 'feuillee':   'Pont la Feuillée (Lyon)',
 'stjeannoche':'Cathédrale Saint-Jean de Lyon at night',
 'viewsfour':  'Views of Basilique Notre-Dame de Fourvière',
}

res = json.load(open(SALIDA)) if os.path.exists(SALIDA) else {}
for k, cat in CATS.items():
    if res.get(k):
        print('  %-11s ya estaba (%d)' % (k, len(res[k]))); continue
    r = de_categoria(cat, 30)
    r = [x for x in r if x['apaisada'] and x['w'] >= 2000]   # para portada: apaisada y grande
    res[k] = r
    print('  %-11s %2d apaisadas grandes' % (k, len(r)))
    json.dump(res, open(SALIDA, 'w'), ensure_ascii=False)
    time.sleep(3)
