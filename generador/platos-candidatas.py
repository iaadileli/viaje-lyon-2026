#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Candidatas a foto para cada plato de «Qué hay que probar» (sep-2026, lo pidió Adil).
Por categoría de Commons, como categorias.py; donde no hay categoría, ficheros sueltos
encontrados con list=search. Reanudable. Luego: hoja-contacto.py y elegir-platos.py"""
import json, os, sys, time, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from buscafotos import de_categoria, UA
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SALIDA = 'generador/datos-fuente/fotos-platos.json'

CATS = {
 'quenelle':   'Quenelles sauce Nantua',
 'quenelle2':  'Quenelles',
 'brioche':    'Saucisson brioché',
 'salade':     'Salade lyonnaise',
 'tablier':    'Tablier de sapeur',
 'andouillette':'Andouillette',
 'cervelle':   'Cervelle de canut',
 'marcellin':  'Saint-marcellin (cheese)',
 'tarte':      'Tarte aux pralines',
 'pralines':   'Pralines roses',
 'pot':        'Pot lyonnais',
}
SUELTAS = {
 'cardons': ['File:Gratin de cardons à la moelle.jpg', 'File:Cardoon Gratin (4202801518).jpg',
             'File:Cardoon Gratin (4202801676).jpg'],
 'bugnes':  ['File:Bugnes in Dauphiné region France.jpg'],
}

def ficheros(titulos):
    cmd = ['curl','-s','--max-time','30','-G','https://commons.wikimedia.org/w/api.php','-A',UA,
      '--data-urlencode','action=query','--data-urlencode','titles=' + '|'.join(titulos),
      '--data-urlencode','prop=imageinfo','--data-urlencode','iiprop=url|size|extmetadata',
      '--data-urlencode','iiurlwidth=1100','--data-urlencode','format=json']
    d = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)
    out = []
    for p in d['query']['pages'].values():
        if 'imageinfo' not in p: print('    ✗ no existe:', p['title']); continue
        im = p['imageinfo'][0]; m = im.get('extmetadata', {})
        out.append({'t': p['title'], 'url': im.get('thumburl') or im['url'],
                    'lic': m.get('LicenseShortName', {}).get('value','?'),
                    'w': im['width'], 'h': im['height'], 'apaisada': im['width'] > im['height']*1.15})
    return out

res = json.load(open(SALIDA)) if os.path.exists(SALIDA) else {}
for k, cat in CATS.items():
    if res.get(k): print('  %-12s ya estaba (%d)' % (k, len(res[k]))); continue
    res[k] = de_categoria(cat, 20)
    print('  %-12s %2d candidatas' % (k, len(res[k])))
    json.dump(res, open(SALIDA, 'w'), ensure_ascii=False); time.sleep(3)
for k, tits in SUELTAS.items():
    if res.get(k): continue
    res[k] = ficheros(tits)
    print('  %-12s %2d sueltas' % (k, len(res[k])))
    json.dump(res, open(SALIDA, 'w'), ensure_ascii=False); time.sleep(3)
