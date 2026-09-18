#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compone el mapa de la guía: un MAPA DE VERDAD de fondo (teselas de
OpenStreetMap) con las zonas encima, cada una en su coordenada real.
Genera img/mapa-lyon.jpg y generador/plantilla/c3-mapa.html.
OSM es ODbL: la atribución «© OpenStreetMap» va en el pie del mapa."""
import math, os, time, urllib.request
from PIL import Image, ImageEnhance

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA = 'guia-viaje-lyon/1.0 (uso personal, una sola composicion)'
ZOOM = 15
# el recorte: entra Confluence por abajo, el Institut Lumière por la derecha,
# Fourvière por la izquierda y la Croix-Rousse y la Tête d'Or por arriba
OESTE, ESTE = 4.806, 4.884
SUR, NORTE  = 45.727, 45.786

# zona -> (lat, lon, sección, título, subtítulo, destacada, dónde va la etiqueta)
ZONAS = [
 (45.7630, 4.8272, '#vieux',      'Vieux Lyon',       'traboules y catedral',      True,  'arriba'),
 (45.7622, 4.8225, '#fourviere',  'Fourvière',        'basílica y romanos',        True,  'izquierda'),
 (45.7675, 4.8337, '#presquile',  'Terreaux',         'museos y bouchons',         True,  'arriba'),
 (45.7578, 4.8320, '#presquile',  'Bellecour',        'el centro de todo',         False, 'abajo'),
 (45.7745, 4.8323, '#croix',      'Croix-Rousse',     'el barrio de los canuts',   True,  'arriba'),
 (45.7330, 4.8180, '#confluence', 'Confluence',       'el museo y los dos ríos',   True,  'abajo'),
 (45.7770, 4.8520, '#brotteaux',  'Tête d’Or',        'el parque grande',          True,  'arriba'),
 (45.7628, 4.8506, '#brotteaux',  'Les Halles',       'el mercado de Bocuse',      True,  'derecha'),
 (45.7452, 4.8710, '#lumiere',    'Institut Lumière', 'donde nació el cine',       True,  'izquierda'),
 (45.7605, 4.8590, '#transporte', 'Part-Dieu',        'el tren del aeropuerto',    False, 'derecha'),
 (45.7490, 4.8265, '#transporte', 'Perrache',         'la otra estación',          False, 'izquierda'),
]

def x_tile(lon, z): return (lon + 180.0) / 360.0 * 2**z
def y_tile(lat, z):
    r = math.radians(lat)
    return (1.0 - math.log(math.tan(r) + 1/math.cos(r)) / math.pi) / 2.0 * 2**z

x0f, x1f = x_tile(OESTE, ZOOM), x_tile(ESTE, ZOOM)
y0f, y1f = y_tile(NORTE, ZOOM), y_tile(SUR, ZOOM)
x0, x1 = math.floor(x0f), math.ceil(x1f)
y0, y1 = math.floor(y0f), math.ceil(y1f)
ancho_t, alto_t = x1 - x0, y1 - y0
print('teselas: %d x %d = %d (zoom %d)' % (ancho_t, alto_t, ancho_t * alto_t, ZOOM))

cache = 'generador/datos-fuente/teselas'
os.makedirs(cache, exist_ok=True)
lienzo = Image.new('RGB', (ancho_t * 256, alto_t * 256), '#e8eef6')
bajadas = 0
for tx in range(x0, x1):
    for ty in range(y0, y1):
        ruta = '%s/%d-%d-%d.png' % (cache, ZOOM, tx, ty)
        if not os.path.exists(ruta):
            url = 'https://tile.openstreetmap.org/%d/%d/%d.png' % (ZOOM, tx, ty)
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=30) as r, open(ruta, 'wb') as f:
                f.write(r.read())
            bajadas += 1
            time.sleep(0.4)
        lienzo.paste(Image.open(ruta).convert('RGB'), ((tx - x0) * 256, (ty - y0) * 256))
print('teselas descargadas ahora:', bajadas, '· el resto, de la caché')

# recorte exacto al trozo que interesa
izq   = round((x0f - x0) * 256)
arr   = round((y0f - y0) * 256)
der   = round((x1f - x0) * 256)
abajo = round((y1f - y0) * 256)
mapa = lienzo.crop((izq, arr, der, abajo))
W, H = mapa.size
print('mapa recortado: %dx%d px' % (W, H))

# se aclara y desatura para que las etiquetas se lean por encima
mapa = ImageEnhance.Color(mapa).enhance(0.55)
mapa = Image.blend(mapa, Image.new('RGB', mapa.size, 'white'), 0.28)
# el SVG escala la imagen al viewBox, así que se puede guardar más pequeña que el recorte:
# 1007 KB en el móvil de alguien que va andando por la calle no tienen sentido
ANCHO_FINAL = 1250
if mapa.width > ANCHO_FINAL:
    mapa = mapa.resize((ANCHO_FINAL, round(H * ANCHO_FINAL / W)), Image.LANCZOS)
mapa.save('img/mapa-lyon.jpg', 'JPEG', quality=80, optimize=True, progressive=True)
print('img/mapa-lyon.jpg · %d KB' % (os.path.getsize('img/mapa-lyon.jpg') // 1024))

# ---- coordenadas de cada zona dentro de la imagen
def a_pixel(lat, lon):
    return ((x_tile(lon, ZOOM) - x0f) * 256, (y_tile(lat, ZOOM) - y0f) * 256)

puntos = []
for lat, lon, dest, titulo, sub, destaca, donde in ZONAS:
    px, py = a_pixel(lat, lon)
    assert 0 <= px <= W and 0 <= py <= H, 'fuera del mapa: %s' % titulo
    puntos.append((px, py, dest, titulo, sub, destaca, donde))
    print('  %-24s %6.0f, %6.0f  (%s)' % (titulo, px, py, donde))

# ---------------------------------------------------------------- el SVG
def escapa(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

filas = []
for px, py, dest, titulo, sub, destaca, donde in puntos:
    r = 13 if destaca else 10
    if donde == 'arriba':
        tx, ty, sy, anclaje = px, py - 28, py - 8, 'middle'
    elif donde == 'abajo':
        tx, ty, sy, anclaje = px, py + 36, py + 56, 'middle'
    elif donde == 'izquierda':
        tx, ty, sy, anclaje = px - 21, py + 2, py + 22, 'end'
    else:                                     # derecha
        tx, ty, sy, anclaje = px + 21, py + 2, py + 22, 'start'
    ancho = 22 + 12.5 * len(titulo)
    if anclaje == 'middle':   rx = tx - ancho / 2
    elif anclaje == 'end':    rx = tx - ancho
    else:                     rx = tx
    ry = min(ty, py) - 20
    rh = max(sy, py) - ry + 12
    clase = ' destaca' if destaca else ''
    filas.append(
      '''    <a class="m-punto%s" href="%s" aria-label="Ir a %s">
      <rect class="m-toca" x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="10"/>
      <circle cx="%.0f" cy="%.0f" r="%d"/>
      <text class="m-tit" x="%.0f" y="%.0f" text-anchor="%s">%s</text>
      <text class="m-sub" x="%.0f" y="%.0f" text-anchor="%s">%s</text>
    </a>''' % (clase, dest, escapa(titulo.replace('·', 'y')),
                min(rx, px - r - 5), ry, max(ancho, 2 * r + 10), rh,
                px, py, r, tx, ty, anclaje, escapa(titulo), tx, sy, anclaje, escapa(sub)))

html = '''
<section id="mapa" class="etapa-sec">
  <div class="kicker">Para hacerse el mapa mental</div>
  <h2>Dónde está cada cosa</h2>
  <p class="intro">Lyon se entiende con <strong>dos ríos y una colina</strong>. El Saona pasa por
  el oeste, pegado al casco viejo; el Ródano, más ancho, por el este; en medio queda la
  <strong>Presqu’île</strong>, la lengua de tierra donde está el centro. Sobre el Saona se levanta
  <strong>Fourvière</strong>, y al norte la meseta de la <strong>Croix-Rousse</strong>. Todo lo que
  vais a ver está dentro de este cuadrado: <strong>de Terreaux al Vieux Lyon se cruza andando en
  diez minutos</strong>. Cada chincheta está en su sitio de verdad y
  <strong>pulsándola se va a su apartado</strong>.</p>

  <div class="mapa-wrap">
  <svg viewBox="0 0 %d %d" class="mapa-svg" role="img"
       aria-label="Mapa de Lyon con las zonas de la guía señaladas; cada una es un enlace a su apartado">
    <image class="m-base" href="img/mapa-lyon.jpg" xlink:href="img/mapa-lyon.jpg"
           x="0" y="0" width="%d" height="%d" preserveAspectRatio="xMidYMid slice"/>
%s
  </svg>
  </div>

  <div class="mapa-pie sans">
    <span><i class="m-ll destaca"></i>las zonas de la guía</span>
    <span><i class="m-ll"></i>otros sitios que se nombran</span>
    <span class="mapa-pinchar"><b>👆 Pulsad en una zona</b> y os lleva a ella</span>
    <span class="mapa-credito">Mapa: <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">© OpenStreetMap</a></span>
  </div>

  <div class="tip"><b>La regla que os ahorra tiempo:</b> el centro de Lyon es pequeño y casi todo
  se hace andando, pero <b>las cuestas se pagan</b>. A Fourvière se sube en funicular y a la
  Croix-Rousse en metro, y luego se baja andando. Subir a pie las pendientes de la Croix-Rousse
  después de comer en un bouchon es una mala idea con forma de escalera.</div>

  <div class="cerca-invita sans">
    <b>📍 ¿Y qué tengo cerca ahora mismo?</b> Abajo del todo hay un botón que usa el GPS del móvil
    y os ordena por distancia los <span data-total-sitios>27</span> sitios de comer de esta guía.
    Sirve para el momento «son las dos, tenemos hambre y estamos aquí».
  </div>
</section>
''' % (W, H, W, H, chr(10).join(filas))

open('generador/plantilla/c3-mapa.html', 'w').write(html)
print('generador/plantilla/c3-mapa.html · %d zonas sobre el mapa' % len(puntos))
