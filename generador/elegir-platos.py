#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baja a img/platos/ la foto elegida de cada plato de «Qué hay que probar» (sep-2026),
tras mirar las hojas de contacto de fotos-platos.json. Reutiliza thumb/baja/encoge de
elegir.py sin ejecutarlo. Créditos en datos-fuente/creditos-platos.json (montar.py los
pone en el pie, junto a los de las demás fotos)."""
import json, os, re, sys, time, urllib.parse
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
# funciones de elegir.py, sin disparar su bucle de descargas
fuente = open('generador/elegir.py').read().split('creditos = {}')[0].split('# con argumentos')[0]
exec(fuente)

# plato -> (clave en fotos-platos.json, índice elegido)
PLATOS = {
 'quenelle':     ('quenelle', 5),      # gratinada en su cazuela, la de bouchon
 'brioche':      ('brioche', 1),
 'salade':       ('salade', 6),
 'tablier':      ('tablier', 5),       # con su gribiche y patatas
 'andouillette': ('andouillette', 7),
 'cervelle':     ('cervelle', 0),      # la de la Brasserie Georges, que está en la guía
 'cardons':      ('cardons', 2),       # con el tuétano a la vista
 'marcellin':    ('marcellin', 13),    # abierto y cremoso, como se come aquí
 'tarte':        ('tarte', 7),
 'bugnes':       ('bugnes', 0),
 'pot':          ('pot', 1),
}
cand = json.load(open('generador/datos-fuente/fotos-platos.json'))
os.makedirs('img/platos', exist_ok=True)
RUTA = 'generador/datos-fuente/creditos-platos.json'
cred = json.load(open(RUTA)) if os.path.exists(RUTA) else {}
for plato, (clave, idx) in PLATOS.items():
    ruta = 'img/platos/%s.jpg' % plato
    c = cand[clave][idx]
    if os.path.exists(ruta) and cred.get(plato, {}).get('titulo') == c['t'][5:]:
        continue
    url, _, lic, autor = thumb(c['t'], 800)
    baja(url, ruta)
    w, h = encoge(ruta, 800)
    cred[plato] = {'titulo': c['t'][5:], 'licencia': lic,
                   'autor': re.sub(r'<[^>]+>', '', autor).strip()[:60],
                   'pagina': 'https://commons.wikimedia.org/wiki/' + urllib.parse.quote(c['t'].replace(' ', '_'))}
    print('  %-13s %4d KB  %dx%d  [%s]' % (plato, os.path.getsize(ruta)//1024, w, h, lic))
    json.dump(cred, open(RUTA, 'w'), ensure_ascii=False, indent=1)
    time.sleep(3)
