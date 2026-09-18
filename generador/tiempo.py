#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""El tiempo de los tres días del viaje, para Lyon.

A tres semanas vista NO existe predicción: Open-Meteo llega a 16 días. Así que
mientras tanto esto escribe la CLIMATOLOGÍA de esos mismos días en los últimos
diez años (API de archivo, también de Open-Meteo) y lo dice claramente. Las filas
llevan su data-t con la fecha, así que en cuanto la predicción exista, el JS de la
página la repinta solo al abrir la web, sin tocar nada.

Uso:  python3 generador/tiempo.py   (y luego montar.py)"""
import json, os, statistics, sys, urllib.request, datetime

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRIMER, ULTIMO = '2026-10-09', '2026-10-11'
LAT, LON, TZ = 45.7640, 4.8357, 'Europe%2FParis'
UA = {'User-Agent': 'guia-lyon/1.0 (uso personal)'}
ANOS_ATRAS = 10

CIELO = {0:('☀️','despejado'), 1:('🌤️','casi despejado'), 2:('⛅','nubes y claros'), 3:('☁️','nublado'),
         45:('🌫️','niebla'), 48:('🌫️','niebla helada'),
         51:('🌦️','llovizna'), 53:('🌦️','llovizna'), 55:('🌧️','llovizna fuerte'),
         56:('🌧️','llovizna helada'), 57:('🌧️','llovizna helada'),
         61:('🌦️','lluvia floja'), 63:('🌧️','lluvia'), 65:('🌧️','lluvia fuerte'),
         66:('🌧️','lluvia helada'), 67:('🌧️','lluvia helada'),
         71:('🌨️','nieve'), 73:('🌨️','nieve'), 75:('🌨️','nieve fuerte'), 77:('🌨️','granizo menudo'),
         80:('🌦️','chubascos'), 81:('🌧️','chubascos'), 82:('🌧️','chubascos fuertes'),
         85:('🌨️','chubascos de nieve'), 86:('🌨️','chubascos de nieve'),
         95:('⛈️','tormenta'), 96:('⛈️','tormenta con granizo'), 99:('⛈️','tormenta con granizo')}
SEMANA = ['lunes','martes','miércoles','jueves','viernes','sábado','domingo']
MESES = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto',
         'septiembre','octubre','noviembre','diciembre']

def pide(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))

# ---------------------------------------------------------------- predicción
API = ('https://api.open-meteo.com/v1/forecast?latitude=%s&longitude=%s'
       '&daily=weather_code,temperature_2m_max,temperature_2m_min,'
       'precipitation_probability_max,precipitation_sum,wind_speed_10m_max,sunrise,sunset'
       '&timezone=%s&forecast_days=16' % (LAT, LON, TZ))
d = pide(API)['daily']
dias, es_prediccion = [], True
for i, fecha in enumerate(d['time']):
    if not (PRIMER <= fecha <= ULTIMO):
        continue
    f = datetime.date.fromisoformat(fecha)
    emoji, texto = CIELO.get(d['weather_code'][i], ('🌡️', 'variable'))
    dias.append({'f': fecha, 'dia': '%s %d' % (SEMANA[f.weekday()], f.day), 'mes': MESES[f.month-1],
                 'e': emoji, 't': texto,
                 'max': round(d['temperature_2m_max'][i]), 'min': round(d['temperature_2m_min'][i]),
                 'lluvia': d['precipitation_probability_max'][i] or 0,
                 'viento': round(d['wind_speed_10m_max'][i]),
                 'sale': d['sunrise'][i][11:16], 'pone': d['sunset'][i][11:16]})

# ------------------------------------------------- si aún no hay, el histórico
if not dias:
    es_prediccion = False
    print('Todavía no hay predicción para esos días (faltan más de 16): uso el histórico.')
    hoy = datetime.date.today()
    for fecha in (PRIMER, ULTIMO):
        pass
    objetivo = [datetime.date.fromisoformat(PRIMER) + datetime.timedelta(days=n)
                for n in range((datetime.date.fromisoformat(ULTIMO) -
                                datetime.date.fromisoformat(PRIMER)).days + 1)]
    for f in objetivo:
        maxs, mins, lluvias, vientos, sale, pone = [], [], [], [], '', ''
        for año in range(hoy.year - ANOS_ATRAS, hoy.year):
            dia = f.replace(year=año).isoformat()
            h = pide('https://archive-api.open-meteo.com/v1/archive?latitude=%s&longitude=%s'
                     '&start_date=%s&end_date=%s&daily=temperature_2m_max,temperature_2m_min,'
                     'precipitation_sum,wind_speed_10m_max,sunrise,sunset&timezone=%s'
                     % (LAT, LON, dia, dia, TZ))['daily']
            if h['temperature_2m_max'][0] is None:
                continue
            maxs.append(h['temperature_2m_max'][0]); mins.append(h['temperature_2m_min'][0])
            lluvias.append((h['precipitation_sum'][0] or 0) >= 1)
            vientos.append(h['wind_speed_10m_max'][0] or 0)
            sale, pone = h['sunrise'][0][11:16], h['sunset'][0][11:16]
        prob = round(100 * sum(lluvias) / len(lluvias)) if lluvias else 0
        emoji, texto = ('🌧️','con lluvia más años que no') if prob >= 50 else \
                       (('🌦️','algún chubasco') if prob >= 30 else ('⛅','nubes y claros'))
        dias.append({'f': f.isoformat(), 'dia': '%s %d' % (SEMANA[f.weekday()], f.day),
                     'mes': MESES[f.month-1], 'e': emoji, 't': texto,
                     'max': round(statistics.mean(maxs)), 'min': round(statistics.mean(mins)),
                     'lluvia': prob, 'viento': round(statistics.mean(vientos)),
                     'sale': sale, 'pone': pone})
        print('  %s · media %d°/%d° · llovió %d de cada 10 años' %
              (f, dias[-1]['max'], dias[-1]['min'], prob // 10))

if not dias:
    sys.exit('Ni predicción ni histórico: revisa la conexión')

hoy = datetime.date.today()
actualizado = '%d de %s' % (hoy.day, MESES[hoy.month - 1])
mojados = [x for x in dias if x['lluvia'] >= 50]
maxima = max(x['max'] for x in dias)
minima = min(x['min'] for x in dias)

if es_prediccion:
    if not mojados:
        resumen = ('Ningún día con la lluvia por encima del 50 %. Aun así, octubre en Lyon es '
                   'traicionero: un paraguas plegable en la mochila y listo.')
    else:
        resumen = ('Lluvia probable %s. Ese día es el bueno para meterse en '
                   '<a href="#presquile">el museo de Bellas Artes</a> o en '
                   '<a href="#brotteaux">las Halles</a>, que son todo techo.'
                   % (' y el '.join(x['dia'] for x in mojados)))
else:
    resumen = ('<b>Todavía no hay predicción para esos días</b> —los modelos llegan a dos semanas— '
               'así que esto es <b>lo que ha hecho de verdad esos mismos días en los últimos %d '
               'años</b>: temperaturas medias y cuántos de esos años llovió. Cuando falte menos de '
               'una semana, <b>esta tabla se convertirá sola en la predicción real</b> la próxima '
               'vez que abráis la web.' % ANOS_ATRAS)

filas = []
for x in dias:
    clase = ' mojado' if x['lluvia'] >= 50 else ''
    filas.append(
'''      <div class="t-dia%s" data-t="%s">
        <div class="t-cuando"><b>%s</b><span>de %s</span></div>
        <div class="t-icono" aria-hidden="true">%s</div>
        <div class="t-cielo">%s</div>
        <div class="t-grados"><b>%d°</b><span>%d°</span></div>
        <div class="t-lluvia">💧 %d%%</div>
        <div class="t-viento">💨 %d km/h</div>
      </div>''' % (clase, x['f'], x['dia'], x['mes'], x['e'], x['t'], x['max'], x['min'],
                   x['lluvia'], x['viento']))

sello = ('Predicción del %s · se actualiza sola al abrir la web' % actualizado) if es_prediccion else \
        ('Media de los últimos %d años · en cuanto haya predicción, esto se actualiza solo' % ANOS_ATRAS)

html = '''
<section id="tiempo" class="etapa-sec">
  <div class="kicker">Qué meter en la maleta</div>
  <h2>El tiempo, día a día</h2>
  <p class="intro">%s</p>

  <div class="tiempo-rejilla" id="tiempoRejilla">
%s
  </div>

  <div class="t-pie sans">
    <span id="tiempoSello">%s</span>
    <span>🌅 amanece a las %s · 🌇 anochece a las %s</span>
    <span>Máximas de %d° a %d° · mínimas de hasta %d°</span>
  </div>

  <div class="tip"><b>Con esos números:</b> jersey y <b>una chaqueta cortavientos</b>, porque en
  octubre Lyon amanece a nueve grados y a mediodía va por dieciocho. <b>Calzado cerrado y cómodo</b>:
  los adoquines del Vieux Lyon y las cuestas de la Croix-Rousse no perdonan. Y un paraguas
  plegable, que el valle del Ródano se moja sin avisar. <b>Anochece antes de las siete y media</b>:
  contad con que la tarde se hace corta.</div>
</section>
''' % (resumen, '\n'.join(filas), sello, dias[0]['sale'], dias[0]['pone'], minima, maxima, minima)

open('generador/plantilla/d0-tiempo.html', 'w').write(html)
print('d0-tiempo.html · %d días (%s a %s) · %s · máx %d° · mín %d°'
      % (len(dias), dias[0]['dia'], dias[-1]['dia'],
         'predicción' if es_prediccion else 'histórico', maxima, minima))
