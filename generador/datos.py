#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fuente única de los sitios de comer de Lyon.
Genera generador/plantilla/comer/<zona>.html y sitios.js (el «qué tengo cerca»).
Las direcciones se han comprobado una a una en Nominatim (generador/direcciones.py);
donde OpenStreetMap no da el número de portal, va solo la calle: no se inventan.

sellos: bouchon (bouchon auténtico, de los del cartel de Gnafron), leyenda (lleva
        décadas abierto), barato (se come por menos de 20 €), local (donde come la
        gente de aquí), cena (la comida buena del viaje), amigo (te lo recomienda
        alguien que ha estado)
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
 dict(z='vieux', n='Daniel et Denise Saint-Jean', s=['bouchon','cena'],
   dir='36 rue Tramassac, 69005 · Vieux Lyon',
   geo='Daniel et Denise Saint-Jean, rue Tramassac, Lyon',
   t='El bouchon de <b>Joseph Viola</b>, Meilleur Ouvrier de France, y el sitio donde se come el '
     '<b>pâté en croûte</b> que ganó el campeonato del mundo: hojaldre, foie y mollejas, servido '
     'en una rodaja que parece un mosaico. Manteles de cuadros, paredes de madera y cocina seria '
     'detrás de la broma. Es el que yo elegiría para la cena buena del viaje.',
   p='El <b>pâté en croûte</b> de entrada, sí o sí, y luego la <b>quenelle de brochet</b> con salsa Nantua',
   d='🕐 <b>de martes a sábado</b>, mediodía y noche · cerrado domingo y lunes → <b>os cuadra el viernes o el sábado</b> · 💶 35–50 € · 📞 04 78 42 24 62 · <b>reservad con días</b>, no hay sitio de sobra'),
 dict(z='vieux', n='Le Bœuf d’Argent', s=['bouchon'],
   dir='29 rue du Bœuf, 69005 · Vieux Lyon',
   geo='Le Boeuf d Argent, rue du Boeuf, Lyon',
   t='En la calle del Bœuf, la más bonita del barrio renacentista. Bouchon con el cartel de '
     'Gnafron en la puerta —el sello de los auténticos— y la carta de siempre sin florituras: '
     'cochonailles, quenelle y una <b>cervelle de canut</b> que no es sesos de nada, sino queso '
     'fresco batido con hierbas, ajo y chalota.',
   p='El menú del bouchon completo y un <i>pot</i> de 46 cl de Côtes du Rhône, que es como se bebe aquí',
   d='🕐 todos los días en temporada, mediodía y noche · 💶 25–35 € · en plena zona turística, pero este es de los buenos'),
 dict(z='vieux', n='Les Adrets', s=['barato','local'],
   dir='30 rue du Bœuf, 69005 · Vieux Lyon',
   geo='Les Adrets, rue du Boeuf, Lyon',
   t='Justo enfrente del anterior, y el secreto es el <b>menú del mediodía</b>: entrada, plato y '
     'postre por poco más de veinte euros, con cocina de verdad y no de turista. Por la noche '
     'sube bastante de precio, así que el truco es ir a comer.',
   p='El <b>menú del mediodía</b>. Si está la <i>terrine</i> de la casa, empezad por ahí',
   d='🕐 <b>de lunes a viernes</b>, y ahí está el problema: el fin de semana cierra · 💶 22–28 € al mediodía · llegad a las 12:15 o no hay mesa'),
 dict(z='vieux', n='Notre Maison', s=['bouchon','local'],
   dir='Rue de Gadagne, 69005 · Vieux Lyon, al lado del museo Gadagne',
   geo='Notre Maison, rue de Gadagne, Lyon',
   t='Bouchon pequeño y familiar en una calleja del Vieux Lyon, lejos del tumulto de la rue '
     'Saint-Jean. Es de los pocos de su clase que <b>sirve el domingo al mediodía</b>, que para '
     'vosotros es justo el día difícil.',
   p='Quenelle o tablier de sapeur, y de postre la <i>tarte aux pralines</i>, rosa fosforito',
   d='🕐 abre <b>domingo al mediodía</b>, que aquí es rareza · 💶 25–32 € · sitio pequeño: llamad antes'),
 dict(z='vieux', n='Terre Adélice', s=['barato'],
   dir='1 place de la Baleine, 69005 · Vieux Lyon',
   geo='Terre Adelice, place de la Baleine, Lyon',
   t='Heladería artesana con <b>unos 150 sabores</b>, muchos ecológicos y unos cuantos que son '
     'una provocación: tomate-albahaca, queso azul, absenta. Está en una placita junto al río, '
     'a dos pasos de la catedral.',
   p='Una bola sensata y otra rara. El de <b>praline rosa</b> es el sabor de Lyon',
   d='🕐 todos los días hasta la noche · 💶 3–6 € · se coge y se pasea por el muelle'),

# ------------------------------------------------------------------ PRESQU’ÎLE
 dict(z='presquile', n='Café des Fédérations', s=['bouchon','leyenda'],
   dir='8-10 rue du Major Martin, 69001 · detrás de la place des Terreaux',
   geo='Cafe des Federations, rue du Major Martin, Lyon',
   t='El bouchon más conocido de Lyon y, aun así, de los que no defraudan: manteles de cuadros '
     'rojos, salchichones colgando del techo, camareros que llevan ahí media vida y una carta '
     'que no ha cambiado en décadas. Se empieza con una tabla de entradas que van dejando en la '
     'mesa —lentejas, morro, arenques, patata tibia— y ya con eso casi se llena uno.',
   p='El <b>menú completo</b> y un pot de Beaujolais. De plato, la <b>quenelle</b> o la <i>andouillette</i> si os atrevéis',
   d='🕐 <b>todos los días 12:00–14:00 y 19:30–22:00, domingo incluido</b> (lo han cambiado hace poco, antes cerraba el finde) · 💶 30–38 € · 📞 04 78 28 26 00 · <b>reservad</b>'),
 dict(z='presquile', n='Chez Hugon', s=['bouchon','leyenda','local'],
   dir='12 rue Pizay, 69001 · junto al Ópera',
   geo='Chez Hugon, rue Pizay, Lyon',
   t='Familia desde <b>1937</b>, doce mesas y la cocina a la vista desde la puerta. Es el bouchon '
     'que recomiendan los lyoneses cuando quieren zanjar la discusión. El <b>tablier de sapeur</b> '
     '—callos rebozados y fritos, mucho mejor de lo que suena— es el plato de la casa.',
   p='<b>Tablier de sapeur</b> con salsa gribiche, y de postre las <i>bugnes</i> si las tienen',
   d='🕐 <b>de lunes a viernes</b>, 12:00–14:00 y 19:30–22:00 · <b>cierra sábado y domingo</b>: si queréis venir, tiene que ser el viernes · 💶 30–38 € · 📞 04 78 28 10 94'),
 dict(z='presquile', n='Le Garet', s=['bouchon','leyenda','local'],
   dir='7 rue du Garet, 69001 · detrás del Ayuntamiento',
   geo='Le Garet, rue du Garet, Lyon',
   t='Otro clásico de los de toda la vida, a un minuto del Ópera. Famoso por el <b>saladier '
     'lyonnais</b>: una ronda de ensaladas de las de antes —morro, sesos, lentejas, arenque— que '
     'se comparten. Sala pequeña, ruido de platos y ni una concesión a la moda.',
   p='<b>Saladier lyonnais</b> para los dos y luego un plato a compartir, que las raciones son grandes',
   d='🕐 <b>de lunes a viernes</b> · cierra sábado y domingo · 💶 28–36 € · 📞 04 78 28 16 94'),
 dict(z='presquile', n='Café Comptoir Abel', s=['bouchon','leyenda'],
   dir='25 rue Guynemer, 69002 · barrio de Ainay',
   geo='Cafe Comptoir Abel, rue Guynemer, Lyon',
   t='La casa es de 1726 y el bouchon lleva funcionando <b>desde 1928</b>: suelos de baldosa, '
     'barra de zinc, vitrinas con la vajilla de la abuela. Es el más bonito de todos y, por '
     'suerte para vosotros, <b>abre el domingo</b>. El <i>saucisson brioché</i> y el pollo al '
     'vinagre son de manual.',
   p='<b>Saucisson brioché</b> de entrada y el <b>poulet au vinaigre</b>. Sentaos en la sala de abajo',
   d='🕐 <b>abre también el domingo</b>, 12:00–14:30 y 19:30–22:00 · 💶 30–40 € · 📞 04 78 37 46 18 · reservad'),
 dict(z='presquile', n='Le Poêlon d’Or', s=['bouchon','local'],
   dir='Rue des Remparts d’Ainay, 69002 · Ainay',
   geo='Le Poelon d Or, rue des Remparts d Ainay, Lyon',
   t='Menos turístico que los de Terreaux y muy querido en el barrio. Cocina de bouchon bien '
     'hecha, con quenelle soufflée y una carta corta que cambia. Ainay es además el trozo más '
     'tranquilo y elegante de la Presqu’île, con su iglesia románica del siglo XI.',
   p='La <b>quenelle soufflée</b>, que aquí la hacen inflada y ligera, nada que ver con la de lata',
   d='🕐 de martes a sábado · 💶 28–35 € · <b>confirmad el horario del sábado</b> antes de ir'),
 dict(z='presquile', n='Café du Jura', s=['bouchon','leyenda'],
   dir='Rue Tupin, 69002 · Cordeliers',
   geo='Cafe du Jura, rue Tupin, Lyon',
   t='Abierto <b>desde 1864</b>, con la decoración de los años treinta intacta y un cartel que '
     'parece de película. Es de los bouchons con más solera de la ciudad y de los que mejor '
     'clavan los clásicos: gratin de cardos con tuétano, cervelas trufado, ternera charolesa.',
   p='<b>Gratin de cardons à la moelle</b> si está en carta: es un plato que casi no se ve fuera de Lyon',
   d='🕐 comprobad los días, que cambian según temporada · 💶 28–36 € · a dos calles de la rue Mercière'),
 dict(z='presquile', n='Brasserie Georges', s=['leyenda'],
   dir='30 cours de Verdun, 69002 · junto a la estación de Perrache',
   geo='Brasserie Georges, cours de Verdun, Lyon',
   t='Una cervecería alsaciana de <b>1836</b>, enorme, con techos art déco de catorce metros, '
     'trescientas y pico plazas y camareros de chaleco. No es un bouchon: es una brasserie de las '
     'de verdad, con choucroute, marisco y su propia cerveza. <b>Abre todos los días y hasta '
     'tarde</b>, que en Lyon es oro en domingo.',
   p='La <b>choucroute</b> o un plateau de ostras, y la cerveza de la casa. De postre, el <i>vacherin</i> glacé',
   d='🕐 <b>todos los días</b>, hasta las 23:00 o más · 💶 25–40 € · cabe todo el mundo, no suele hacer falta reservar'),
 dict(z='presquile', n='Chez Paul', s=['bouchon','barato'],
   dir='Rue du Major Martin, 69001 · al lado del Café des Fédérations',
   geo='Chez Paul, rue du Major Martin, Lyon',
   t='En la misma calle que el Fédés y bastante más barato. Bouchon sin pretensiones, raciones '
     'generosas y clientela de barrio. El plan B perfecto cuando el de al lado está lleno, que '
     'lo está casi siempre.',
   p='El <b>menú del día</b>. Y si hay <i>quenelle</i>, es buena y cuesta la mitad que en la puerta de enfrente',
   d='🕐 comprobad el fin de semana · 💶 20–28 € · se come bien por poco dinero'),
 dict(z='presquile', n='La Mère Brazier', s=['cena'],
   dir='12 rue Royale, 69001 · Terreaux',
   geo='La Mere Brazier, rue Royale, Lyon',
   t='La casa de <b>Eugénie Brazier</b>, la primera persona del mundo con seis estrellas Michelin, '
     'en 1933, y la maestra de Bocuse. Hoy la lleva Mathieu Viannay y conserva dos estrellas. '
     'Esto ya no es comer: es ir a ver de dónde sale la cocina lyonesa. Carísimo, pero al '
     'mediodía hay menú y es la forma sensata de entrar.',
   p='Si os lo dais: el <b>menú del mediodía</b>. La <i>volaille de Bresse demi-deuil</i> —pollo con láminas de trufa bajo la piel— es el plato de Eugénie',
   d='🕐 de martes a sábado · 💶 menú mediodía desde unos 75 €, carta mucho más · reservar con semanas'),
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
 dict(z='croix', n='Le Bouchon des Filles', s=['bouchon','local'],
   dir='Rue Sergent Blandan, 69001 · al pie de las pendientes',
   geo='Le Bouchon des Filles, rue Sergent Blandan, Lyon',
   t='Bouchon llevado por mujeres, en la tradición de las <b>mères lyonnaises</b> que inventaron '
     'esta cocina. Sirven un menú único con una ronda larga de entradas y el plato a elegir. Es '
     'más ligero y más fino que el bouchon de manual —menos grasa, más verdura— y <b>abre todas '
     'las noches</b>, fin de semana incluido.',
   p='El <b>menú único</b>. Dejad sitio para el carrito de postres',
   d='🕐 <b>todas las noches</b>, solo cenas · 💶 unos 32 € el menú · pequeño y muy solicitado: reservad'),
 dict(z='croix', n='Substrat', s=['local','cena'],
   dir='Rue Pailleron, 69004 · Croix-Rousse',
   geo='Substrat restaurant, rue Pailleron, Lyon',
   t='Los dueños salen al bosque a por setas, hierbas y raíces y con eso montan la carta del día. '
     'Es la cocina joven de Lyon sin postureo: bistró de barrio, pizarra, buen vino y platos que '
     'no vais a encontrar en otro sitio. La Croix-Rousse está llena de sitios así.',
   p='Lo que haya en la pizarra. Si hay <b>setas</b>, octubre es su mes',
   d='🕐 cerrado domingo y lunes · 💶 30–40 € · reservad, que es pequeño'),
 dict(z='croix', n='Le Canut et les Gones', s=['local'],
   dir='Impasse Gigodot, 69004 · Croix-Rousse',
   geo='Le Canut et les Gones, impasse Gigodot, Lyon',
   t='Bistró con decoración de relojes viejos por todas partes y cocina de mercado que se sale de '
     'la ortodoxia del bouchon. Muy de barrio, muy de la Croix-Rousse, con carta corta y vinos '
     'naturales.',
   p='El menú del día y una copa de lo que os recomienden: aquí el vino lo eligen ellos bien',
   d='🕐 comprobad los días de cierre · 💶 28–38 € · reservad'),
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
 dict(z='brotteaux', n='Daniel et Denise Créqui', s=['bouchon','cena'],
   dir='156 rue de Créqui, 69003 · esquina con rue Le Royer',
   geo='Daniel et Denise Crequi, rue de Crequi, Lyon',
   t='La casa madre de Joseph Viola, más de barrio que la del Vieux Lyon y con la misma cocina. '
     'Si el del Vieux Lyon está lleno —que lo estará—, este es el mismo pâté en croûte a veinte '
     'minutos andando.',
   p='<b>Pâté en croûte</b> campeón del mundo y el plato del día de la pizarra',
   d='🕐 de lunes a viernes · <b>cierra el fin de semana</b> · 💶 35–45 € · 📞 04 78 60 66 53'),
 dict(z='brotteaux', n='À Ma Vigne', s=['local','barato'],
   dir='Rue Jean Larrivé, 69003 · cerca de Part-Dieu',
   geo='A Ma Vigne, rue Jean Larrive, Lyon',
   t='Sitio de barrio sin ninguna gracia decorativa y con fama de servir <b>la mejor andouillette '
     'de Lyon</b> —la AAAAA, la de la asociación que las certifica— y unas patatas fritas hechas '
     'a mano que la gente viene a buscar de lejos. Aquí no hay turistas.',
   p='<b>Andouillette AAAAA</b> con sus patatas. Aviso: la andouillette es fuerte, o encanta o espanta',
   d='🕐 de lunes a viernes, mediodía sobre todo · 💶 18–25 € · efectivo mejor que tarjeta'),
 dict(z='brotteaux', n='Bernachon', s=['leyenda'],
   dir='42 cours Franklin Roosevelt, 69006 · Brotteaux',
   geo='Bernachon, cours Franklin Roosevelt, Lyon',
   t='Una de las poquísimas casas de Francia que hace el chocolate <b>desde el grano de cacao</b>, '
     'en el propio obrador, desde 1953. El <i>Président</i> —la tarta de chocolate que le hicieron '
     'a Giscard— y los palets d’or son de los mejores bombones que vais a comer.',
   p='Una caja pequeña de <b>palets d’or</b>. Y si hay sitio en el salón, una porción de tarta con café',
   d='🕐 de martes a sábado · 💶 desde 8 € · cerrado domingo y lunes'),
 dict(z='brotteaux', n='Le Bouchon Sully', s=['bouchon'],
   dir='Rue Sully, 69006 · Brotteaux, cerca de la Tête d’Or',
   geo='Le Bouchon Sully, rue Sully, Lyon',
   t='Bouchon en el barrio burgués del este, a un paseo del parque de la Tête d’Or. Sirve la '
     'carta clásica en un comedor tranquilo, sin la aglomeración de los de Terreaux, y va bien '
     'para el día que paséis por el parque.',
   p='<b>Quenelle</b> o <i>tête de veau</i> si os va la casquería. Menú corto y correcto',
   d='🕐 comprobad el fin de semana · 💶 28–35 € · diez minutos andando desde la puerta del parque'),
 dict(z='brotteaux', n='Brasserie des Brotteaux', s=['leyenda'],
   dir='Place Jules Ferry, 69006 · en la antigua estación de los Brotteaux',
   geo='Brasserie des Brotteaux, place Jules Ferry, Lyon',
   t='Dentro de la <b>estación de los Brotteaux</b>, una joya art nouveau de 1908 que ya no tiene '
     'trenes: mosaicos, vidrieras y techos altos. La brasserie conserva la barra y los azulejos '
     'originales, y <b>abre el domingo por la noche</b>, cosa rara aquí.',
   p='Cocina de brasserie: <i>oeufs meurette</i>, pescado del día, tarta Tatin',
   d='🕐 <b>abre también el domingo por la noche</b> · 💶 25–38 € · la sala es el motivo para venir'),
]
