#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Candidatas para la portada (28-sep-2026): Adil quiere algo con más luz que la
foto nocturna de Saint-Georges. Referencia: Place des Terreaux de día, con la
fuente Bartholdi en primer plano y el Hôtel de Ville detrás. Reanudable."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from buscafotos import de_categoria
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SALIDA = 'generador/datos-fuente/fotos6.json'

CATS = {
 'terreaux':   'Place des Terreaux',
 'bartholdi':  'Fontaine Bartholdi (Lyon)',
 'hotelville': 'Hôtel de ville de Lyon',
 'hvexterior': 'Exterior of Hôtel de ville de Lyon',
 'hvfacade':   'Façade of Hôtel de ville de Lyon (place des Terreaux)',
}

res = json.load(open(SALIDA)) if os.path.exists(SALIDA) else {}
for k, cat in CATS.items():
    if res.get(k):
        print('  %-11s ya estaba (%d)' % (k, len(res[k]))); continue
    try:
        r = de_categoria(cat, 40)
    except RuntimeError as e:
        print('  %-11s ✗ %s' % (k, e)); res[k] = []; continue
    r = [x for x in r if x['apaisada'] and x['w'] >= 2000]   # para portada: apaisada y grande
    res[k] = r
    print('  %-11s %2d apaisadas grandes' % (k, len(r)))
    json.dump(res, open(SALIDA, 'w'), ensure_ascii=False)
    time.sleep(3)
