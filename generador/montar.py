#!/usr/bin/env python3
"""Monta index.html juntando las piezas de generador/plantilla/ e inyectando:
 - los bloques de comida DENTRO de la sección de su zona (el «qué tengo cerca» y
   los contadores buscan los .sitios dentro de la sección, no en una sección aparte)
 - los créditos de las fotos en el pie, leídos de datos-fuente/creditos.json, para
   que no se quede nunca la lista de otra guía."""
import json, re, os
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
P = 'generador/plantilla/'

PIEZAS = ['head-nuevo.html', 'css-base.html', 'css-lyon.html',
          'c1-cabecera.html', 'c2-lumiere.html', 'd0-tiempo.html', 'c3-mapa.html',
          'c4-vieux.html', 'c5-fourviere.html', 'c6-presquile.html', 'c7-croix.html',
          'c8-confluence.html', 'c9-brotteaux.html',
          'd3-comer.html', 'd1-hoteles.html', 'd2-paseos.html', 'd4-entradas.html',
          'd5-transporte.html', 'd6-practico.html', 'd7-offline.html', 'd8-footer.html',
          'js-tiempo.html', '3-scripts.html']
# id de la sección de la web -> fichero de comida
COMIDA = {'vieux': 'vieux', 'presquile': 'presquile', 'croix': 'croix', 'brotteaux': 'brotteaux'}

leyenda = open(P + 'comer/leyenda.html').read()
puesta = False
partes = []
for pieza in PIEZAS:
    s = open(P + pieza).read()
    for sec, fich in COMIDA.items():
        marca = '<section id="%s" class="etapa-sec">' % sec
        if marca not in s:
            continue
        bloque = open(P + 'comer/%s.html' % fich).read()
        pon = ('' if puesta else leyenda) + bloque
        puesta = True
        pat = re.compile(r'(<section id="%s" class="etapa-sec">.*?)(</section>)' % sec, re.S)
        s, n = pat.subn(lambda m: m.group(1) + '\n' + pon + m.group(2), s, count=1)
        assert n == 1, 'no se pudo inyectar la comida en #' + sec
    partes.append(s)

html = ''.join(partes)

# --- créditos de las fotos, desde el json que deja elegir.py
cred = 'generador/datos-fuente/creditos.json'
if os.path.exists(cred):
    c = json.load(open(cred))
    # y las de los platos de «qué hay que probar» (elegir-platos.py)
    if os.path.exists('generador/datos-fuente/creditos-platos.json'):
        c.update({'plato-' + k: v for k, v in json.load(open('generador/datos-fuente/creditos-platos.json')).items()})
    lis = '\n'.join(
        '    <li><a href="%s" target="_blank" rel="noopener">%s</a> · %s%s</li>'
        % (v['pagina'], v['titulo'], v['licencia'], (' · ' + v['autor']) if v.get('autor') else '')
        for v in c.values())
    html, n = re.subn(r'(<ul id="creditos-fotos">)\s*(</ul>)', r'\1\n%s\n    \2' % lis, html, count=1)
    assert n == 1, 'no encontré dónde poner los créditos de las fotos'
    print('créditos de %d fotos puestos en el pie' % len(c))
else:
    print('¡OJO! no hay creditos.json: el pie se queda sin créditos (ejecuta elegir.py)')

html = html.replace('</style>\n<body>', '</style>\n</head>\n<body>', 1)
if not html.rstrip().endswith('</html>'):
    html = html.rstrip() + '\n</html>\n'
open('index.html', 'w').write(html)
print('index.html montado: %d KB · %d sitios de comer · %d hoteles'
      % (len(html) // 1024, html.count('<li><span class="nombre">'), html.count('class="hotel"')))
