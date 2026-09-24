# Lyon 2026 — guía de un fin de semana

Web estática de una sola página, para **Edu y Sara**, que van a Lyon del **viernes 9 al domingo 11
de octubre de 2026**. No lleva día a día: va por zonas, y cada zona trae lo que ver y **dónde comer
allí mismo**. Hecha con la plantilla de `viaje-londres`.

Publicada en → https://iaadileli.github.io/viaje-lyon-2026/

## Lo que tiene de propio esta guía

- **La tabla de quién abre el fin de semana** (en `#comer`). Es el dato que decide el viaje: los
  bouchons históricos cerraban tradicionalmente sábado y domingo y varios lo siguen haciendo.
  Los horarios marcados con ✔ están comprobados en la web del propio sitio; el resto, no.
- **El Festival Lumière**, del 10 al 18 de octubre, les coincide con el sábado y el domingo.
  Sección propia con precios y qué hacer.
- **Tabla de hoteles de 100 a 200 €** con Booking precargado (9 → 11 oct, 2 adultos).
- **Sello nuevo `bouchon`** en las fichas de comer, para los del cartel de Gnafron.

## Cómo se monta

El `index.html` **no se edita a mano**: se monta juntando las piezas de `generador/plantilla/`.

```bash
python3 generador/direcciones.py   # comprueba en Nominatim la dirección real de cada sitio
python3 generador/comer.py         # datos.py -> plantilla/comer/*.html y sitios.js
python3 generador/tiempo.py        # d0-tiempo.html (predicción, o histórico si aún no la hay)
python3 generador/mapa.py          # teselas de OSM -> img/mapa-lyon.jpg + c3-mapa.html
python3 generador/montar.py        # junta las piezas -> index.html (y pone los créditos de las fotos)
node generador/revisar.mjs         # revisa la página EN MARCHA (obligatorio antes de dar nada por bueno)
node generador/capturas.mjs        # capturas para mirarla de verdad
python3 hacer-copia.py             # lyon-sin-conexion.html, un solo fichero
```

- **`generador/datos.py`** es la fuente única de los 31 sitios de comer.
- **`generador/direcciones.py`** es nuevo: pregunta a Nominatim la dirección real de cada sitio
  **antes** de escribirla en `datos.py`. Así salieron dos cosas que yo daba por otras: **Prairial**
  se ha mudado a la rue Casimir Périer y **Le Canut et les Gones**, a la impasse Gigodot.
  Donde OpenStreetMap no da el número de portal, en la guía va solo la calle: no se inventa.

## El tiempo: histórico hasta que haya predicción

Open-Meteo solo predice a 16 días y la guía se hizo a tres semanas vista. Mientras tanto,
`tiempo.py` escribe **la media real de esos mismos días en los últimos diez años** (API de archivo)
y lo dice en la página. Las filas llevan su `data-t` con la fecha, así que **en cuanto exista la
predicción, el JS la repinta solo** al abrir la web. No hay que volver a ejecutar nada.

## Tres cosas que se arreglaron aquí y conviene portar a las otras guías

1. **`buscafotos.py` se comía los errores de Wikimedia.** Cuando la API corta por exceso de
   peticiones devuelve texto plano o una página HTML de 2 KB, y el script lo contaba como
   «0 resultados»: hojas de contacto medio vacías sin explicación. Ahora distingue «no hay fotos»
   de «la API ha cortado», reintenta con espera y guarda sobre la marcha para poder reanudar.
2. **`elegir.py` guardaba páginas de error como si fueran fotos.** `img/lumiere.jpg` acabó siendo
   un HTML de 2 KB y el script murió después, con un `UnidentifiedImageError` que no explicaba
   nada. Ahora comprueba los bytes de cabecera JPEG, reintenta y **encoge las fotos**: la portada
   pesaba 1,9 MB.
3. **Las candidatas salen de las CATEGORÍAS de Commons**, no de la búsqueda por texto
   (`generador/categorias.py`). Buscando «Mur des Canuts» por texto salía una boca de incendios.
   Los nombres de categoría hay que **buscarlos** (`list=search`, `srnamespace=14`): inventarlos
   devuelve categorías vacías sin avisar de que no existen.

Y una comprobación nueva en `revisar.mjs`: **contraste en modo oscuro** medido sobre la página en
marcha, tamaño real de los sellos, filas completas en la tabla de horarios y accesos rápidos que
lleven a alguna parte.

## Revisión del 24 de septiembre de 2026 (en el Mac)

- **Portada nueva**: Saint-Georges y Fourvière de noche desde el Saona (`portada-candidatas.py`
  → `fotos5.json`; `elegir.py portada-hero` baja solo esa y conserva los demás créditos).
  La anterior era un mar de tejados.
- **Datos de comer comprobados otra vez**, y había errores gordos:
  **Substrat cerró** el 6-jul-2024 (lo sustituye Daniel et Denise Croix-Rousse);
  **Le Bœuf d’Argent ya no es bouchon** (gastronómico de la ganadora de Top Chef 2026, 60-205 €);
  **La Mère Brazier cierra sábado y domingo**; Bouchon Sully ahora es **Le Sully**; horarios
  corregidos en media lista. La tabla del fin de semana está rehecha.
- **Las mères**: sello nuevo `mere` (la toca) y tres casas más: Maison Léa, Bouchon Léa y
  La Mère Jean, más el Café du Peintre. Bloque propio en `#comer`.
- **Nota de 1 a 3 estrellas** en cada restaurante (`r` en `datos.py`) y bloque «los mejores».
  Sale de Michelin, Gault&Millau, Le Fooding y el label; ninguno tiene Bib Gourmand.
- **El label** ya no se deduce del sello 🍷: va en el campo `label` de cada sitio.
- **«Qué hay que probar» con foto de cada plato** (`platos-candidatas.py` → hojas de contacto →
  `elegir-platos.py` → `img/platos/`). El mâchon va sin foto: es una costumbre, no un plato.
- En el Mac: Pillow en `.venv/`, Playwright en `node_modules/`. Si no baja el «headless shell»,
  `revisar.mjs` usa el Chromium completo. `MOTOR=webkit` existe, pero el WebKit de Playwright
  se colgó al arrancar en este Mac (macOS 14): la revisión se hizo en Chromium.
