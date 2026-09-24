#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera plantilla/comer/<zona>.html y sitios.js a partir de datos.py.
Las coordenadas se piden a Nominatim y se cachean; ejecutar tras tocar datos.py."""
import json, os, sys, time, urllib.request, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datos import SITIOS, ZONAS

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
CACHE = 'generador/datos-fuente/coordenadas.json'
os.makedirs('generador/datos-fuente', exist_ok=True)
os.makedirs('generador/plantilla/comer', exist_ok=True)

SVG = {
 'amigo':  '<path d="M12 21s-7.5-4.7-9.4-9.1C1.2 8.5 3.1 5 6.5 5c2 0 3.5 1.1 4.4 2.4l1.1 1.5 1.1-1.5C14 6.1 15.5 5 17.5 5c3.4 0 5.3 3.5 3.9 6.9C19.5 16.3 12 21 12 21z"/>',
 'leyenda':'<path d="M12 2.6l2.9 5.9 6.5.9-4.7 4.6 1.1 6.5-5.8-3-5.8 3 1.1-6.5L2.6 9.4l6.5-.9z"/>',
 'local':  '<circle cx="12" cy="12" r="6"/>',
 'cena':   '<path d="M7 3v8a3 3 0 0 0 6 0V3M10 11v10M17 3c-1.5 2-2 4-2 6.5 0 1.5.7 2.5 2 2.5v9"/>',
 # el pot lyonnais: la botella gruesa de 46 cl con la que se bebe en los bouchons
 'bouchon':'<path d="M10 2h4v3.2l1.9 3.4c.4.7.6 1.5.6 2.3V20a2 2 0 0 1-2 2H9.5a2 2 0 0 1-2-2v-9.1c0-.8.2-1.6.6-2.3L10 5.2z"/>',
 # la toca de cocinera: las mères lyonnaises (sep-2026)
 'mere':   '<path d="M7 20h10v-5.2a4 4 0 0 0 1.2-7.6A4.5 4.5 0 0 0 12 4.4a4.5 4.5 0 0 0-6.2 2.8A4 4 0 0 0 7 14.8z"/>',
}
TITULO = {'amigo':'te lo recomienda alguien que ha estado', 'leyenda':'lleva décadas abierto',
          'barato':'se come por menos de 20 €', 'local':'donde come la gente de aquí',
          'cena':'la comida buena del viaje', 'bouchon':'bouchon de cocina tradicional',
          'mere':'casa de una mère lyonnaise'}
# la nota: se ve en la ficha, en «¿qué tengo cerca?» y en el cuadro de los mejores
NOTA = {3: 'imprescindible', 2: 'muy bueno', 1: 'correcto, o plan B'}
def estrellas(r):
    if not r: return ''
    return ('<span class="nota n%d" title="%d de 3: %s" aria-label="%d de 3 estrellas: %s">%s'
            '<i>%s</i></span>' % (r, r, NOTA[r], r, NOTA[r], '★' * r, '☆' * (3 - r)))
LABEL = ('<b class="label-bl" title="está en la lista oficial de la asociación, la del cartel de Gnafron">'
         '🏷️ label Les Bouchons Lyonnais</b> · ')
# el de «barato» es la etiqueta de precio, con trazo en vez de relleno
BARATO = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round">'
          '<path d="M11.5 2.5H20a1.5 1.5 0 0 1 1.5 1.5v8.5L12 21.5 2.5 12z"/>'
          '<circle cx="17" cy="7" r="1.6" fill="currentColor" stroke="none"/></svg>')

def cuerpo_sello(k):
    if k == 'barato':
        return BARATO
    if k == 'cena':
        return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                'stroke-linecap="round">%s</svg>' % SVG[k])
    return '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">%s</svg>' % SVG[k]

def sello(k):
    return '<span class="sello %s" title="%s">%s</span>' % (k, TITULO[k], cuerpo_sello(k))

def maps(consulta):
    return 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote(consulta)

# ---------------------------------------------------------------- coordenadas
# Nominatim no tiene estos tres locales; van a mano, a pie de portal (error < 50 m)
# Nominatim no devuelve estos tres con la consulta de la ficha: sus coordenadas
# vienen de generador/direcciones.py, que sí los encuentra por su nombre.
MANUAL = {
 'Brasserie Georges, cours de Verdun, Lyon':          [45.748322, 4.828343, 0],
 'Halles de Lyon Paul Bocuse, cours Lafayette, Lyon': [45.762832, 4.850551, 0],
 'Daniel et Denise Crequi, rue de Crequi, Lyon':      [45.762232, 4.847199, 0],
}
coords = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
coords.update({k: v for k, v in MANUAL.items() if not coords.get(k)})
def geo(consulta):
    if consulta in coords:
        return coords[consulta]
    url = ('https://nominatim.openstreetmap.org/search?' +
           urllib.parse.urlencode({'q': consulta, 'format': 'json', 'limit': 1}))
    req = urllib.request.Request(url, headers={'User-Agent': 'guia-lyon/1.0 (uso personal)'})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=20))
        if r:
            coords[consulta] = [round(float(r[0]['lat']), 6), round(float(r[0]['lon']), 6), 0]
            print('  ✓ %s' % consulta)
        else:
            coords[consulta] = None
            print('  ✗ SIN COORDENADAS: %s' % consulta)
    except Exception as e:
        coords[consulta] = None
        print('  ✗ error (%s): %s' % (e, consulta))
    time.sleep(1.1)   # Nominatim pide máximo una petición por segundo
    return coords[consulta]

print('Geocodificando %d sitios…' % len(SITIOS))
for s in SITIOS:
    geo(s['geo'])
json.dump(coords, open(CACHE, 'w'), ensure_ascii=False, indent=1)

# ------------------------------------------------------------- bloques comer
LEYENDA = ('  <div class="leyenda-sellos">' +
  ''.join('<span><i style="background:%s">%s</i>%s</span>' % (color, cuerpo, TITULO[k])
          for k, color, cuerpo in [
            ('bouchon', '#8d2033', cuerpo_sello('bouchon')),
            ('mere',    '#b4552d', cuerpo_sello('mere')),
            ('leyenda', '#8a6a1f', cuerpo_sello('leyenda')),
            ('barato',  '#2f6f8f', BARATO),
            ('local',   '#3d7a4a', cuerpo_sello('local')),
            ('cena',    '#7a4a86', cuerpo_sello('cena')),
          ]) +
  '<span><b class="nota n3">★★★</b> imprescindible · <b class="nota n2">★★<i>☆</i></b> muy bueno · '
  '<b class="nota n1">★<i>☆☆</i></b> correcto o plan B</span></div>\n')

for zona, (titulo, platos) in ZONAS.items():
    de_zona = [s for s in SITIOS if s['z'] == zona]
    h = ['  <div class="comer">', '    <h3>%s</h3>' % titulo, '    <div class="platos">']
    h.append('      ' + ''.join('<span class="plato">%s</span>' % p for p in platos))
    h += ['    </div>', '    <ul class="sitios">']
    for s in de_zona:
        h.append('      <li><span class="nombre">%s</span>%s%s — <span class="dir">%s</span> · %s'
                 % (s['n'], estrellas(s.get('r')), ''.join(sello(k) for k in s['s']), s['dir'], s['t']))
        h.append('        <span class="pedir"><b>Pedid</b> %s</span>' % s['p'])
        h.append('        <span class="datos">%s%s</span>' % (LABEL if s.get('label') else '', s['d']))
        h.append('        <a href="%s" target="_blank" rel="noopener">📍 Maps</a></li>' % maps(s['geo']))
    h += ['    </ul>', '  </div>']
    open('generador/plantilla/comer/%s.html' % zona, 'w').write('\n'.join(h) + '\n')
    print('comer/%s.html · %d sitios' % (zona, len(de_zona)))

open('generador/plantilla/comer/leyenda.html', 'w').write(LEYENDA)

# ----------------------------------------------------------------- sitios.js
ETIQUETA = {'vieux':'el Vieux Lyon', 'presquile':'la Presqu’île', 'croix':'la Croix-Rousse',
            'brotteaux':'las Halles y los Brotteaux'}
js = []
faltan = []
for s in SITIOS:
    c = coords.get(s['geo'])
    if not c:
        faltan.append(s['n']); continue
    principal = ([k for k in s['s'] if k != 'amigo'] + [k for k in s['s'] if k == 'amigo'] + [''])[0]
    js.append({'n': s['n'], 'z': s['dir'].split(' · ')[0], 'e': ETIQUETA[s['z']],
               's': principal, 'r': s.get('r', 0), 'la': c[0], 'lo': c[1], 'ap': c[2],
               'q': urllib.parse.quote(s['geo'])})
open('sitios.js', 'w').write('const SITIOS=' + json.dumps(js, ensure_ascii=False, separators=(',', ':')) + ';\n')
print('sitios.js · %d sitios situados%s' % (len(js), (', SIN COORDENADAS: ' + ', '.join(faltan)) if faltan else ''))
