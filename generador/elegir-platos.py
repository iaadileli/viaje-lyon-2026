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

# plato -> (clave en fotos-platos.json, índice elegido); si la clave empieza por «2:»,
# viene de fotos-platos2.json (segunda tanda, oct-2026, platos2-candidatas.py)
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
 # --- segunda tanda (oct-2026): Adil pidió una lista larga
 'croute':       ('2:croute', 6),      # el de Daniel et Denise, que está en la guía
 'tete':         ('2:tete', 1),        # Brasserie Georges, con su ravigote
 'meurette':     ('2:meurette', 3),    # en una brasserie de la Croix-Rousse
 'chaud':        ('2:chaud', 9),       # pistachos y patatas salteadas
 'sabodet':      ('2:chaud', 3),       # el sabodet de Daniel et Denise
 'rosette':      ('2:rosette', 4),
 'jesus':        ('2:jesus', 1),
 'grattons':     ('2:grattons', 0),    # sobre rosette y mantel de cuadros
 'gateaufoie':   ('2:lyoncuisine', 12),
 'moelle':       ('2:lyoncuisine', 18),
 'bresse':       ('2:bresse', 0),      # entera, con morillas
 'demideuil':    ('2:demideuil', 0),   # la propia Mère Fillioux (Françoise Fayolle), dominio público
 'vinaigre':     ('2:vinaigre', 3),
 'boudin':       ('2:boudin', 3),      # Chez Paul, que está en la guía
 'pommes':       ('2:pommes2', 2),
 'lentilles':    ('2:lentilles', 6),   # Bouillon de Lyon
 'foie':         ('2:foie', 0),
 'flottante':    ('pralines', 0),      # Brasserie Georges, pralines rosas
 'genix':        ('2:genix', 1),
 'coussin':      ('2:coussin', 3),
 'rigotte':      ('2:rigotte', 2),     # abierta
 'faisselle':    ('2:faisselle', 0),
 'machon':       ('2:lyonfood', 29),   # tabla de embutido del Café du Gros Caillou (Croix-Rousse); la placa de los Francs-Mâchons no gustó
}
cand = json.load(open('generador/datos-fuente/fotos-platos.json'))
cand.update({'2:' + k: v for k, v in json.load(open('generador/datos-fuente/fotos-platos2.json')).items()})
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
