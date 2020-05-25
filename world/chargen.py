from eveil.template import Template
from eveil.character import SHADOW

# We create the first room 
room1 = game.map.new_room()
room1.shortdesc = "la création du personnage"
room1.longdesc = Template("""
<p>Plusieurs paramètres définissent un personnage: son nom, son genre,
son apparence et sa description. Par défaut, les autres personnages ne
voient pas le nom du vôtre, ils ne voient que son <i>apparence</i>.
L'<i>apparence</i> est donc une courte description physique, qui ne
doit comporter aucune mention du caractère ni des vêtements. La
<i>description</i> est celle qui est communiquée lorsque l'on
<code>regarde</code> explicitement votre personnage. Vous pouvez définir
nom, genre, apparence et description avec les commandes suivantes:</p>
<ul>

{% if character.name != shadow %}
    <li><code>nom <i>{{character.name}}</i></code></li>
{% else %}
    <li><code>nom <i>nom_choisi</i></code></li>
{% endif %}

{% if character.gender %}
    <li><code>genre <i>{{character.grammar.gender}}</i></code></li>
{% else %}
    <li><code>genre <i>[masculin|féminin]</i></code>.</li>
{% endif %}

{% if character.shortdesc %}
    <li><code>apparence <i>{{character.shortdesc}}</i></code></li>
{% else %}
    <li><code>apparence <i>quelques mots</i></code></li>
{% endif %}

{% if character.longdesc %}
    <li><code>description <i>{{character.longdesc}}</i></code></li>
{% else %}
    <li><code>description <i>Longue description...</i></code></li>
{% endif %}
</ul>
<p>Pour passer à l'étape suivante, entrez <code>aller vers
<i>mot_clé</i></code>.</p>
""", {'capitalize': str.capitalize, 'shadow': SHADOW})

# We create an empty second room to link it with the first
room2 = game.map.new_room()
link1_2 = game.map.new_link(room1, room2)
link1_2.dynadesc = "passant à la seconde étape"
link2_1 = game.map.new_link(room2, room1)
link2_1.dynadesc = "retournant à la première étape"

# Second room description
room2.shortdesc = "les commandes de base"
room2.longdesc = Template("""
<p>Vous pouvez déplacer {{character.name.capitalize}} d'un espace à un
autre avec la commande
<code>aller vers <i>mot clé</i></code>. Pour voir à nouveau la
description de l'environnement (ce texte), utilisez
<code>regarder</code>. Cette même commande sert à regarder quelqu'un
ou quelque chose: 
    {% if character.name == shadow %}
    <code>regarder <i>mot clé</i></code>.
    {% else %}
    <code>regarder <i>{{character.name}}</i></code> par exemple.
    {% endif %}
</p>
<p>La commande la plus utilisée est <code>exposer</code>. Cette commande
vous permet de d'exposer les actions, gestes, émotions et paroles de
votre personnage. En son sein, les phrases entre guillemets sont des paroles.
Les mots-clé <code>/il</code> et <code>/elle</code> sont
remplacés par le nom pour les personnages qui connaissent votre
personnage et par sa courte description pour les autres. De la même
manière, pour référer un autre personnage, utilisez <code>/</code>
devant son nom.</p>
</ul>
""", {'capitalize': str.capitalize, 'shadow': SHADOW})

# We create an empty third room to link it with the second
room3 = game.map.new_room()
link2_3 = game.map.new_link(room2, room3)
link2_3.dynadesc = "passant à la troisième étape"
link3_2 = game.map.new_link(room3, room2)
link3_2.dynadesc = "retournant à la seconde étape"
 
# Third room description
room3.shortdesc = "la création des vêtements"
room3.longdesc = Template("""
<p>{{character.name.capitalize}} peut créer se propres vêtements avec
la commande <code>item vêtement</créer></code>. Ensuite, la commande
<code>def</code> permet de définir les propriétés d'un item. <code>def
<i>item_à_définir</i></code> définit l'item sur lequel la commande
<code>def</code> agira, et indique les propriétés de l'item. Ainsi,
vous pouvez créer des vêtements avec les commandes suivantes:</p>
<ul>
    <li><code>item <i>vêtement</i></code></li>
    <li><code>def vêtement</code></li>
    <li><code>def apparence <i>courte description du vêtement tel que
    vu dans l'inventaire</i></code></li>
    <li><code>def description <i>longue description visible lorsqu'on
    regarde le vêtement</i></code></li>
    <li><code>def porté <i>description du vêtement vue lorsqu'il est
    porté par un personnage.</i></code></li>
</ul>
<p>Enfin, {{character.name}} peut porter ses vêtements avec la commande
<code>porter <i>mot_clé_de_l'item</i></code>.</p>""")
