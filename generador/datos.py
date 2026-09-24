#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fuente única de los sitios de comer de Lyon.
Genera generador/plantilla/comer/<zona>.html y sitios.js (el «qué tengo cerca»).
Las direcciones se han comprobado una a una en Nominatim (generador/direcciones.py);
donde OpenStreetMap no da el número de portal, va solo la calle: no se inventan.

sellos: bouchon (bouchon de cocina tradicional; el cartel va en «label»), leyenda (lleva
        décadas abierto), barato (se come por menos de 20 €), local (donde come la
        gente de aquí), cena (la comida buena del viaje), amigo (te lo recomienda
        alguien que ha estado), mere (casa de una de las mères lyonnaises)
r:      nota de 1 a 3 estrellas (3 = imprescindible, 2 = muy bueno, 1 = correcto / plan B);
        solo en restaurantes, no en tiendas ni mercados. Sale de lo que dicen Michelin,
        Gault&Millau, Le Fooding y el label, comprobado en sep-2026 (ver README).
label:  True si está en la lista del label «Les Bouchons Lyonnais» (lesbouchonslyonnais.org,
        descargada entera en sep-2026). El sello bouchon ya NO significa «tiene el cartel»:
        significa bouchon de cocina tradicional; el cartel lo dice este campo.
Revisión de sep-2026: Substrat cerró el 6-jul-2024 (fuera); Le Bœuf d'Argent ya no es
bouchon (gastronómico, menús 60-205 €); La Mère Brazier cierra sábado y domingo.
"""

ZONAS = {
 'vieux':     ('Qué y dónde comer en el Vieux Lyon',
               ['Quenelle de lucio', 'Cochonailles', 'Cervelle de canut', 'Helado de 150 sabores']),
 'presquile': ('Qué y dónde comer en la Presqu’île',
               ['Bouchon de verdad', 'Saucisson brioché', 'Tablier de sapeur',
                'Praline rosa', 'Cervecería de 1836']),
 'croix':     ('Qué y dónde comer en la Croix-Rousse',
               ['Mercado de la mañana', 'Bistró de producto', 'Pastelería', 'Vino natural']),
 'brotteaux': ('Qué y dónde comer en las Halles, Brotteaux y la Tête d’Or',
               ['Las Halles de Bocuse', 'Saint-Marcellin', 'Andouillette AAAAA', 'Chocolate']),
}

SITIOS = [
# ------------------------------------------------------------------ VIEUX LYON
 dict(z='vieux', n='Daniel et Denise Saint-Jean', s=['bouchon','cena'], r=3, label=True,
   dir='36 rue Tramassac, 69005 · Vieux Lyon',
   geo='Daniel et Denise Saint-Jean, rue Tramassac, Lyon',
   t='El bouchon de <b>Joseph Viola</b>, Meilleur Ouvrier de France, y el sitio donde se come el '
     '<b>pâté en croûte</b> que ganó el campeonato del mundo en 2009: hojaldre, foie y mollejas, servido '
     'en una rodaja que parece un mosaico. Manteles de cuadros, paredes de madera y cocina seria '
     'detrás de la broma. Está en la Guía Michelin y en el label. Es el que yo elegiría para la cena buena del viaje.',
   p='El <b>pâté en croûte</b> de entrada, sí o sí, y luego la <b>quenelle de brochet</b> con salsa Nantua',
   d='🕐 <b>de martes a sábado</b>, mediodía y noche · cerrado domingo y lunes → <b>os cuadra el viernes o el sábado</b> · 💶 35–50 € · 📞 04 78 42 24 62 · <b>reservad con días</b>, no hay sitio de sobra'),
 dict(z='vieux', n='Le Bœuf d’Argent', s=['cena'], r=2,
   dir='29 rue du Bœuf, 69005 · Vieux Lyon',
   geo='Le Boeuf d Argent, rue du Boeuf, Lyon',
   t='<b>Ojo, que ya no es un bouchon.</b> Lo lleva desde 2023 <b>Viviana Pisacane</b> con sus '
     'hermanos, y en 2026 ganó <b>Top Chef</b> en Francia: cocina franco-italiana de menú '
     'degustación, en la calle más bonita del barrio renacentista. Es la opción «cena especial» '
     'si La Mère Brazier os pilla cerrada, pero desde el programa está muy solicitado.',
   p='Uno de los <b>menús</b>, el más corto si no queréis salir a las doce de la noche',
   d='🕐 según Gault&Millau, <b>de jueves a domingo</b>, mediodía y noche · 💶 <b>menús de 60 a 205 €</b> · reservad ya: desde Top Chef se llena'),
 dict(z='vieux', n='Les Adrets', s=['barato','local'], r=1,
   dir='30 rue du Bœuf, 69005 · Vieux Lyon',
   geo='Les Adrets, rue du Boeuf, Lyon',
   t='Justo enfrente del anterior, y el secreto es el <b>menú del mediodía</b>: entrada, plato y '
     'postre por poco más de veinte euros, con cocina de verdad y no de turista. Por la noche '
     'sube bastante de precio, así que el truco es ir a comer.',
   p='El <b>menú del mediodía</b>. Si está la <i>terrine</i> de la casa, empezad por ahí',
   d='🕐 <b>de lunes a viernes</b>, y ahí está el problema: el fin de semana cierra · 💶 22–28 € al mediodía · llegad a las 12:15 o no hay mesa'),
 dict(z='vieux', n='Notre Maison', s=['bouchon','local'], r=1,
   dir='2 rue de Gadagne, 69005 · Vieux Lyon, al lado del museo Gadagne',
   geo='Notre Maison, rue de Gadagne, Lyon',
   t='Bouchon pequeño y familiar en una calleja del Vieux Lyon, lejos del tumulto de la rue '
     'Saint-Jean. Es de los pocos de su clase que <b>sirve el domingo al mediodía</b>, que para '
     'vosotros es justo el día difícil.',
   p='Quenelle o tablier de sapeur, y de postre la <i>tarte aux pralines</i>, rosa fosforito',
   d='🕐 viernes <b>solo cena</b>, sábado mediodía y noche, <b>domingo al mediodía</b>, que aquí es rareza · 💶 menú 36 € · no sale en las guías, pero los clientes lo puntúan muy alto · sitio pequeño: llamad antes'),
 dict(z='vieux', n='Terre Adélice', s=['barato'],
   dir='1 place de la Baleine, 69005 · Vieux Lyon',
   geo='Terre Adelice, place de la Baleine, Lyon',
   t='Heladería artesana con <b>unos 150 sabores</b>, muchos ecológicos y unos cuantos que son '
     'una provocación: tomate-albahaca, queso azul, absenta. Está en una placita junto al río, '
     'a dos pasos de la catedral.',
   p='Una bola sensata y otra rara. El de <b>praline rosa</b> es el sabor de Lyon',
   d='🕐 todos los días hasta la noche · 💶 3–6 € · se coge y se pasea por el muelle'),

# ------------------------------------------------------------------ PRESQU’ÎLE
 dict(z='presquile', n='Café des Fédérations', s=['bouchon','leyenda'], r=2,
   dir='8-10 rue du Major Martin, 69001 · detrás de la place des Terreaux',
   geo='Cafe des Federations, rue du Major Martin, Lyon',
   t='El bouchon más conocido de Lyon y, aun así, de los que no defraudan: manteles de cuadros '
     'rojos, salchichones colgando del techo, camareros que llevan ahí media vida y una carta '
     'que no ha cambiado en décadas. Se empieza con una tabla de entradas que van dejando en la '
     'mesa —lentejas, morro, arenques, patata tibia— y ya con eso casi se llena uno.',
   p='El <b>menú completo</b> y un pot de Beaujolais. De plato, la <b>quenelle</b> o la <i>andouillette</i> si os atrevéis',
   d='🕐 <b>todos los días 12:00–14:00 y 19:30–22:00, domingo incluido</b> (lo han cambiado hace poco, antes cerraba el finde) · 💶 30–38 € · 📞 04 78 28 26 00 · <b>reservad</b>'),
 dict(z='presquile', n='Chez Hugon', s=['bouchon','leyenda','local'], r=1,
   dir='12 rue Pizay, 69001 · junto al Ópera',
   geo='Chez Hugon, rue Pizay, Lyon',
   t='Familia desde <b>1937</b>, doce mesas y la cocina a la vista desde la puerta. Es el bouchon '
     'que recomiendan los lyoneses cuando quieren zanjar la discusión. El <b>tablier de sapeur</b> '
     '—callos rebozados y fritos, mucho mejor de lo que suena— es el plato de la casa.',
   p='<b>Tablier de sapeur</b> con salsa gribiche, y de postre las <i>bugnes</i> si las tienen',
   d='🕐 <b>de lunes a viernes</b>, 12:00–14:00 y 19:30–22:00 · <b>cierra sábado y domingo</b>: si queréis venir, tiene que ser el viernes · 💶 30–38 € · 📞 04 78 28 10 94'),
 dict(z='presquile', n='Le Garet', s=['bouchon','leyenda','local'], r=3,
   dir='7 rue du Garet, 69001 · detrás del Ayuntamiento',
   geo='Le Garet, rue du Garet, Lyon',
   t='Otro clásico de los de toda la vida, a un minuto del Ópera. Famoso por el <b>saladier '
     'lyonnais</b>: una ronda de ensaladas de las de antes —morro, sesos, lentejas, arenque— que '
     'se comparten. Sala pequeña, ruido de platos y ni una concesión a la moda. Está en la Guía '
     'Michelin y <b>Le Fooding</b> lo eligió en 2024 como <b>el bouchon más auténtico</b> de Lyon.',
   p='<b>Saladier lyonnais</b> para los dos y luego un plato a compartir, que las raciones son grandes',
   d='🕐 <b>de lunes a viernes</b> · cierra sábado y domingo · 💶 28–36 € · 📞 04 78 28 16 94'),
 dict(z='presquile', n='Café Comptoir Abel', s=['bouchon','leyenda','mere'], r=3, label=True,
   dir='25 rue Guynemer, 69002 · barrio de Ainay',
   geo='Cafe Comptoir Abel, rue Guynemer, Lyon',
   t='La casa es de 1726 y el bouchon lo abrió la <b>Mère Abel en 1928</b>: suelos de baldosa, '
     'barra de zinc, vitrinas con la vajilla de la abuela. Es el más bonito de todos y, por '
     'suerte para vosotros, <b>abre el domingo</b>. El <i>saucisson brioché</i> y el pollo al '
     'vinagre son de manual.',
   p='<b>Saucisson brioché</b> de entrada y el <b>poulet au vinaigre</b>. Sentaos en la sala de abajo',
   d='🕐 <b>abre los siete días</b>; el domingo, 12:00–14:30 y 19:30–22:00 · 💶 menús de 32 a 49 € · 📞 04 78 37 46 18 · reservad'),
 dict(z='presquile', n='Le Poêlon d’Or', s=['bouchon','local'], r=2, label=True,
   dir='Rue des Remparts d’Ainay, 69002 · Ainay',
   geo='Le Poelon d Or, rue des Remparts d Ainay, Lyon',
   t='Menos turístico que los de Terreaux y muy querido en el barrio. Cocina de bouchon bien '
     'hecha, con quenelle soufflée y una carta corta que cambia. Ainay es además el trozo más '
     'tranquilo y elegante de la Presqu’île, con su iglesia románica del siglo XI.',
   p='La <b>quenelle soufflée</b>, que aquí la hacen inflada y ligera, nada que ver con la de lata',
   d='🕐 abre viernes y sábado; <b>cierra el domingo</b> · 💶 menús de 34 a 43 €'),
 dict(z='presquile', n='Café du Jura', s=['bouchon','leyenda'], r=2, label=True,
   dir='Rue Tupin, 69002 · Cordeliers',
   geo='Cafe du Jura, rue Tupin, Lyon',
   t='Abierto desde la <b>década de 1860</b>, con la decoración de los años treinta intacta y un cartel que '
     'parece de película. Es de los bouchons con más solera de la ciudad y de los que mejor '
     'clavan los clásicos: gratin de cardos con tuétano, cervelas trufado, ternera charolesa.',
   p='<b>Gratin de cardons à la moelle</b> si está en carta: es un plato que casi no se ve fuera de Lyon',
   d='🕐 abre viernes y sábado; <b>cierra el domingo</b> · 💶 28–36 € · a dos calles de la rue Mercière'),
 dict(z='presquile', n='Brasserie Georges', s=['leyenda'], r=1,
   dir='30 cours de Verdun, 69002 · junto a la estación de Perrache',
   geo='Brasserie Georges, cours de Verdun, Lyon',
   t='Una cervecería alsaciana de <b>1836</b>, enorme, con techos art déco de catorce metros, '
     'trescientas y pico plazas y camareros de chaleco. No es un bouchon: es una brasserie de las '
     'de verdad, con choucroute, marisco y su propia cerveza. <b>Abre todos los días y hasta '
     'tarde</b>, que en Lyon es oro en domingo.',
   p='La <b>choucroute</b> o un plateau de ostras, y la cerveza de la casa. De postre, el <i>vacherin</i> glacé',
   d='🕐 <b>todos los días</b>, hasta las 23:00 o más · 💶 25–40 € · cabe todo el mundo, no suele hacer falta reservar'),
 dict(z='presquile', n='Chez Paul', s=['bouchon','barato'], r=1,
   dir='11 rue du Major Martin, 69001 · al lado del Café des Fédérations',
   geo='Chez Paul, rue du Major Martin, Lyon',
   t='En la misma calle que el Fédés y bastante más barato. Bouchon sin pretensiones, raciones '
     'generosas y clientela de barrio. El plan B perfecto cuando el de al lado está lleno, que '
     'lo está casi siempre. Desde hace poco es del mismo dueño que el Fédés.',
   p='El <b>menú del día</b>. Y si hay <i>quenelle</i>, es buena y cuesta la mitad que en la puerta de enfrente',
   d='🕐 viernes y sábado; el <b>domingo solo al mediodía</b> · 💶 20–28 € · se come bien por poco dinero'),
 dict(z='presquile', n='La Mère Brazier', s=['cena','mere'], r=3,
   dir='12 rue Royale, 69001 · Terreaux',
   geo='La Mere Brazier, rue Royale, Lyon',
   t='La casa de <b>Eugénie Brazier</b>, la primera persona del mundo con seis estrellas Michelin, '
     'en 1933, y la maestra de Bocuse. En la cocina sigue Mathieu Viannay y conserva <b>dos '
     'estrellas</b>. Esto ya no es comer: es ir a ver de dónde sale la cocina lyonesa. Es la '
     'única alta cocina de la guía, y está porque es la casa de la mère más grande.',
   p='Si os lo dais: el <b>menú del mediodía</b>, el más corto. La <i>volaille de Bresse demi-deuil</i> —pollo con láminas de trufa bajo la piel— venía de la Mère Fillioux y Eugénie la hizo famosa',
   d='🕐 <b>de lunes a viernes</b>, 12:00–13:15 y 19:45–21:15 · <b>cierra sábado y domingo</b>: para vosotros, <b>solo el viernes</b> · 💶 el menú grande cuesta 195 €; mirad el del mediodía en su web · 📞 04 78 23 17 20 · reservar con semanas'),
 dict(z='presquile', n='Maison Léa', s=['bouchon','mere'], r=2, label=True,
   dir='11 quai des Célestins, 69002 · orilla del Saona, frente al Vieux Lyon',
   geo='Maison Lea, quai des Celestins, Lyon',
   t='La casa de la <b>Mère Léa</b> —Léa Bidaut—, que abrió aquí en 1943 y llegó a tener una '
     'estrella. Desde 2013 es de Christian Têtedoie, y hoy la llevan Lionel y Carole Sarre. '
     'Está en la Guía Michelin y en el label.',
   p='<b>Quenelle</b>, <i>tablier de sapeur</i> o las <b>ancas de rana</b>',
   d='🕐 <b>de martes a sábado</b>, 12:00–14:00 y 19:00–21:30 · cierra domingo y lunes · 💶 menús de 42 y 52 €, plato del día 24 € · 📞 04 78 42 01 33'),
 dict(z='presquile', n='Bouchon Léa', s=['bouchon','mere'], r=2, label=True,
   dir='11 place Antonin Gourju, 69002 · a la vuelta de Maison Léa',
   geo='Bouchon Lea, place Antonin Gourju, Lyon',
   t='La otra mitad de la casa de la Mère Léa, en la <b>bóveda original</b> —La Voûte, que se '
     'conocía como «chez Léa»—, con los mismos dueños. Más sencillo y más barato que Maison Léa, '
     'con la carta de bouchon de toda la vida.',
   p='<b>Quenelle de lucio con cangrejos</b> o <i>tête de veau</i> si os va la casquería',
   d='🕐 <b>de martes a sábado</b>, 12:00–14:00 y 19:00–21:30 · cierra domingo y lunes · 💶 menús de 26 a 36 € · 📞 04 78 42 03 13'),
 dict(z='presquile', n='La Mère Jean', s=['bouchon','mere','leyenda'], r=1,
   dir='Rue des Marronniers, 69002 · junto a Bellecour',
   geo='La Mere Jean, rue des Marronniers, Lyon',
   t='La fundó en <b>1923</b> Françoise Donnet, la «Mère Jean», y fue la cantina de los '
     'periodistas de <i>Le Progrès</i>. Ha tenido cinco dueños en cien años y sigue igual: sala '
     'diminuta, cocina de casa. No sale en ninguna guía, así que va por su historia, no por '
     'ser de lo mejor.',
   p='<b>Gâteau de foies de volaille</b> —un flan de hígados de pollo—, que ya casi no se ve, o la quenelle',
   d='🕐 <b>de lunes a sábado</b> · cierra el domingo · 💶 no he podido confirmar el precio actual · 📞 04 78 37 81 27'),
 dict(z='presquile', n='Sève', s=[],
   dir='Quai Saint-Antoine, 69002 · frente al mercado',
   geo='Seve chocolatier, quai Saint-Antoine, Lyon',
   t='Richard Sève es uno de los chocolateros de referencia de Francia. Aquí se compran las '
     '<b>pralines rosas</b> —almendras caramelizadas teñidas de rosa, la obsesión dulce de esta '
     'ciudad— y los bombones para llevar a casa.',
   p='Una bolsa de <b>pralines</b> y una porción de <i>tarte aux pralines</i> para el camino',
   d='🕐 de martes a sábado, y domingo por la mañana · 💶 desde 5 € · el escaparate ya merece la parada'),
 dict(z='presquile', n='Marché Saint-Antoine', s=['barato','local'],
   dir='Quai Saint-Antoine, 69002 · orilla del Saona',
   geo='Marche Saint-Antoine, quai Saint-Antoine, Lyon',
   t='El mercado de la Presqu’île, a lo largo del río: quesos, charcutería, fruta, pescado y '
     'puestos donde te preparan un plato para comértelo allí mismo. <b>El domingo por la mañana '
     'es el mejor plan de la ciudad</b>, con el puente de Bonaparte al fondo y el Vieux Lyon '
     'enfrente.',
   p='<b>Saint-Marcellin</b>, un trozo de <i>rosette</i> y pan. Se desayuna o se hace el picnic del día',
   d='🕐 de martes a domingo por la mañana, hasta las 13:00 · 💶 muy barato · el <b>domingo</b> es cuando está a tope'),

# ----------------------------------------------------------------- CROIX-ROUSSE
 dict(z='croix', n='Le Bouchon des Filles', s=['bouchon','local'], r=2,
   dir='Rue Sergent Blandan, 69001 · al pie de las pendientes',
   geo='Le Bouchon des Filles, rue Sergent Blandan, Lyon',
   t='Bouchon llevado por mujeres, en la tradición de las <b>mères lyonnaises</b> que inventaron '
     'esta cocina. Sirven un menú único con una ronda larga de entradas y el plato a elegir. Es '
     'más ligero y más fino que el bouchon de manual —menos grasa, más verdura— y <b>abre todas '
     'las noches</b>, fin de semana incluido.',
   p='El <b>menú único</b>. Dejad sitio para el carrito de postres',
   d='🕐 <b>todas las noches</b>, y de viernes a domingo también al mediodía (confirmadlo) · 💶 unos 32 € el menú · pequeño y muy solicitado: reservad'),
 dict(z='croix', n='Daniel et Denise Croix-Rousse', s=['bouchon','local'], r=2,
   dir='8 rue de Cuire, 69004 · Croix-Rousse, junto al mercado',
   geo='8 Rue de Cuire, 69004 Lyon',
   t='El tercer bouchon de Joseph Viola, en el barrio de los canuts y a dos minutos del mercado '
     'del bulevar. La misma cocina que en el Vieux Lyon, con terraza y ambiente de barrio. Está '
     'en la Guía Michelin. Va perfecto para comer el sábado después del mercado.',
   p='El <b>pâté en croûte</b> de la casa y el plato del día',
   d='🕐 según Michelin, <b>de martes a sábado al mediodía</b>; confirmad si hay cenas · cierra domingo y lunes · 💶 30–45 € · 📞 04 78 28 27 44'),
 dict(z='croix', n='Le Canut et les Gones', s=['local'], r=3,
   dir='Impasse Gigodot, 69004 · Croix-Rousse',
   geo='Le Canut et les Gones, impasse Gigodot, Lyon',
   t='Bistró con decoración de relojes viejos por todas partes y cocina de mercado que se sale de '
     'la ortodoxia del bouchon. Muy de barrio, muy de la Croix-Rousse, con carta corta y vinos '
     'naturales. Está en la Guía Michelin y tiene de las mejores notas de Gault&Millau de esta lista.',
   p='El menú del día y una copa de lo que os recomienden: aquí el vino lo eligen ellos bien',
   d='🕐 <b>de martes a sábado</b>; la cena, de 19:30 a 20:45, así que no lleguéis tarde · cierra el domingo · 💶 28–38 € · reservad'),
 dict(z='croix', n='Marché de la Croix-Rousse', s=['barato','local'],
   dir='Boulevard de la Croix-Rousse, 69004 · el bulevar entero',
   geo='Marche de la Croix-Rousse, boulevard de la Croix-Rousse, Lyon',
   t='El mercado de barrio más grande y más vivo de Lyon, a lo largo del bulevar, bajo los '
     'plátanos. Aquí no hay turistas: hay vecinos con el carro. Quesos de Saboya, charcutería, '
     'verdura de la región y puestos de comida caliente.',
   p='Un <b>bocadillo de rosette</b> o una porción de <i>tarte aux pralines</i> y café en una terraza del bulevar',
   d='🕐 de martes a domingo, de 6:00 a 13:30 · 💶 muy barato · <b>sábado y domingo por la mañana</b> es cuando está mejor'),
 dict(z='croix', n='Bouillet', s=[],
   dir='Place de la Croix-Rousse, 69004',
   geo='Sebastien Bouillet, place de la Croix-Rousse, Lyon',
   t='Sébastien Bouillet es el pastelero de la Croix-Rousse y su escaparate es una pequeña '
     'exposición. Macarons, tartas y los <b>bugnes</b> en su temporada. En la misma plaza está el '
     'mercado, así que cae de camino.',
   p='Una <b>tarte aux pralines</b> en porción y un macaron. El de praline rosa, otra vez',
   d='🕐 todos los días menos lunes · 💶 4–8 € · hay otra tienda suya en la Presqu’île'),

# ------------------------------------------- HALLES, BROTTEAUX Y LA TÊTE D’OR
 dict(z='brotteaux', n='Les Halles de Lyon Paul Bocuse', s=['leyenda','local'],
   dir='102 cours Lafayette, 69003 · metro Part-Dieu',
   geo='Halles de Lyon Paul Bocuse, cours Lafayette, Lyon',
   t='El mercado cubierto de Lyon, el que Bocuse llamaba «el vientre de la ciudad»: cincuenta y '
     'tantos puestos de los mejores productores de la región, con barras donde se come allí '
     'mismo. <b>Mère Richard</b> y sus Saint-Marcellin, la charcutería de <b>Colette Sibilia</b> '
     'con su <i>rosette</i> y su <i>jésus</i>, ostras con vino blanco a las once de la mañana. '
     'Es una visita y una comida a la vez.',
   p='Ostras y una copa de Mâcon en una barra, y luego queso de <b>Mère Richard</b> para llevar',
   d='🕐 martes a sábado 7:00–22:30 aprox. · <b>domingo solo hasta media tarde y lunes cerrado</b> · 💶 15–35 € según lo que piquéis'),
 dict(z='brotteaux', n='Daniel et Denise Créqui', s=['bouchon','cena'], r=2, label=True,
   dir='156 rue de Créqui, 69003 · esquina con rue Le Royer',
   geo='Daniel et Denise Crequi, rue de Crequi, Lyon',
   t='La casa madre de Joseph Viola, más de barrio que la del Vieux Lyon y con la misma cocina. '
     'Si el del Vieux Lyon está lleno —que lo estará—, este es el mismo pâté en croûte a veinte '
     'minutos andando.',
   p='<b>Pâté en croûte</b> campeón del mundo y el plato del día de la pizarra',
   d='🕐 de lunes a viernes · <b>cierra el fin de semana</b> · 💶 35–45 € · 📞 04 78 60 66 53'),
 dict(z='brotteaux', n='À Ma Vigne', s=['local','barato'], r=1,
   dir='23 rue Jean Larrivé, 69003 · cerca de Part-Dieu',
   geo='A Ma Vigne, rue Jean Larrive, Lyon',
   t='Sitio de barrio sin ninguna gracia decorativa y con fama de servir <b>la mejor andouillette '
     'de Lyon</b> —la AAAAA, la de la asociación que las certifica— y unas patatas fritas hechas '
     'a mano que la gente viene a buscar de lejos. Aquí no hay turistas. Ha cambiado de dueños hace poco.',
   p='<b>Andouillette AAAAA</b> con sus patatas. Aviso: la andouillette es fuerte, o encanta o espanta',
   d='🕐 viernes y sábado; <b>cierra el domingo</b> · 💶 18–25 € · efectivo mejor que tarjeta'),
 dict(z='brotteaux', n='Bernachon', s=['leyenda'],
   dir='42 cours Franklin Roosevelt, 69006 · Brotteaux',
   geo='Bernachon, cours Franklin Roosevelt, Lyon',
   t='Una de las poquísimas casas de Francia que hace el chocolate <b>desde el grano de cacao</b>, '
     'en el propio obrador, desde 1953. El <i>Président</i> —la tarta de chocolate que le hicieron '
     'a Giscard— y los palets d’or son de los mejores bombones que vais a comer.',
   p='Una caja pequeña de <b>palets d’or</b>. Y si hay sitio en el salón, una porción de tarta con café',
   d='🕐 de martes a sábado · 💶 desde 8 € · cerrado domingo y lunes'),
 dict(z='brotteaux', n='Le Sully', s=['bouchon'], r=2, label=True,
   dir='Rue Sully, 69006 · Brotteaux, cerca de la Tête d’Or',
   geo='Le Bouchon Sully, rue Sully, Lyon',
   t='Antes se llamaba Bouchon Sully. Bouchon en el barrio burgués del este, a un paseo del parque de la Tête d’Or. Sirve la '
     'carta clásica en un comedor tranquilo, sin la aglomeración de los de Terreaux, y va bien '
     'para el día que paséis por el parque. Está en la Guía Michelin y en el label.',
   p='<b>Quenelle</b> o <i>tête de veau</i> si os va la casquería. Menú corto y correcto',
   d='🕐 <b>cierra sábado y domingo</b>: solo el viernes · 💶 28–35 € · diez minutos andando desde la puerta del parque'),
 dict(z='brotteaux', n='Brasserie des Brotteaux', s=['leyenda'], r=1,
   dir='Place Jules Ferry, 69006 · en la antigua estación de los Brotteaux',
   geo='Brasserie des Brotteaux, place Jules Ferry, Lyon',
   t='Dentro de la <b>estación de los Brotteaux</b>, una joya art nouveau de 1908 que ya no tiene '
     'trenes: mosaicos, vidrieras y techos altos. La brasserie conserva la barra y los azulejos '
     'originales, y <b>abre el domingo por la noche</b>, cosa rara aquí.',
   p='Cocina de brasserie: <i>oeufs meurette</i>, pescado del día, tarta Tatin',
   d='🕐 <b>abre todos los días</b>; el domingo, de 12:00 a 21:30 · 💶 platos de 22 a 39 €, menú 43 € · la sala es el motivo para venir'),
 dict(z='brotteaux', n='Café du Peintre', s=['bouchon','local'], r=2,
   dir='Boulevard des Brotteaux, 69006 · Brotteaux',
   geo='Cafe du Peintre, boulevard des Brotteaux, Lyon',
   t='No es de una mère histórica, pero es su <b>heredero directo</b>: lo abrió en 2009 Florence '
     'Périer, cuya madre y abuela llevaban «Chez Périer» en Perrache, y hoy lo lleva su hijo. '
     'Cocina de bouchon de las de verdad y una bodega enorme.',
   p='Lo que haya en la pizarra y un vino que os recomienden: tienen unas 1.200 referencias',
   d='🕐 <b>cierra sábado y domingo</b>: solo el viernes (mediodía, y cena según el día) · 💶 30–40 €'),
]
