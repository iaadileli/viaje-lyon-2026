#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Segunda tanda de platos para «Qué hay que probar» (oct-2026, Adil pidió una lista larga).
Mismo método que platos-candidatas.py: categorías de Commons (buscadas, no inventadas) y,
donde no hay categoría, búsqueda por texto. Reanudable. Luego: hoja-contacto.py y elegir-platos.py"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from buscafotos import de_categoria, buscar
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SALIDA = 'generador/datos-fuente/fotos-platos2.json'

CATS = {
 'croute':      'Pâté en croute',
 'tete':        'Tête de veau',
 'meurette':    'Œufs en meurette',
 'pommes':      'Pommes de terre à la lyonnaise',
 'rosette':     'Rosettes de Lyon',
 'jesus':       'Jésus (saucisson)',
 'chaud':       'Saucisson chaud',
 'grattons':    'Grattons',
 'bresse':      'Bresse chicken dishes',
 'coussin':     'Coussin de Lyon',
 'genix':       'Gâteau de Saint-Genix',
 'felicien':    'Saint-félicien (cheese)',
 'rigotte':     'Rigotte de Condrieu',
 'faisselle':   'Faisselle',
 'lentilles':   'Lentil salads',
 'machon':      'Mâchon',
 'flottante':   'Floating island (dessert)',
 'foie':        'Foie de veau à la lyonnaise',
 'beaujolais':  'Beaujolais nouveau',
 'lyonfood':    'Food in Lyon',
 'lyoncuisine': 'Cuisine of Lyon',
}
TEXTO = {
 'demideuil':  'poularde demi-deuil',
 'grasdouble': 'gras-double lyonnaise',
 'gateaufoie': 'gâteau de foie de volaille',
 'vinaigre':   'poulet au vinaigre',
 'boudin':     'boudin noir pommes',
 'harengs':    'harengs pommes à l\'huile',
}
res = json.load(open(SALIDA)) if os.path.exists(SALIDA) else {}
for k, cat in CATS.items():
    if res.get(k): print('  %-12s ya estaba (%d)' % (k, len(res[k]))); continue
    res[k] = de_categoria(cat, 40 if k.startswith('lyon') else 20)
    print('  %-12s %2d candidatas' % (k, len(res[k])))
    json.dump(res, open(SALIDA, 'w'), ensure_ascii=False); time.sleep(3)
for k, q in TEXTO.items():
    if res.get(k): print('  %-12s ya estaba (%d)' % (k, len(res[k]))); continue
    res[k] = buscar(q, 10)
    print('  %-12s %2d por texto' % (k, len(res[k])))
    json.dump(res, open(SALIDA, 'w'), ensure_ascii=False); time.sleep(4)
