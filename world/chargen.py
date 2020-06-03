from eveil.template import Template
from eveil.character import SHADOW

# We create the first room 
room1 = game.map.new_room("la création du personnage")
room1.set_desc("""
<p>Plusieurs paramètres définissent un personnage: son nom, son genre,
son apparence et sa description. Par défaut, les autres personnages ne
voient pas le nom du vôtre, ils ne voient que son <i>apparence</i>.
L'<i>apparence</i> est donc une courte description physique, qui ne
doit comporter aucune mention du caractère ni des vêtements. La
<i>description</i> est celle qui est communiquée lorsque l'on
<code>regarde</code> explicitement votre personnage. Vous pouvez définir
nom, genre, apparence et description avec les commandes suivantes:</p>
<ul>

{% if character.data.name != shadow %}
    <li><code>nom <i>{{character.data.name}}</i></code></li>
{% else %}
    <li><code>nom <i>nom_choisi</i></code></li>
{% endif %}

{% if character.data.gender %}
    <li><code>genre <i>{{character.grammar.data.gender}}</i></code></li>
{% else %}
    <li><code>genre <i>[masculin|féminin]</i></code>.</li>
{% endif %}

{% if character.data.shortdesc %}
    <li><code>apparence <i>{{character.data.shortdesc}}</i></code></li>
{% else %}
    <li><code>apparence <i>quelques mots</i></code></li>
{% endif %}

{% if character.data.longdesc %}
    <li><code>description <i>{{character.data.longdesc}}</i></code></li>
{% else %}
    <li><code>description <i>Longue description...</i></code></li>
{% endif %}
</ul>
<p>Ceci fait, vous pouvez déplacer {{character.data.name.capitalize}} d'un
espace à un autre avec la commande <code>aller vers <i>mot
clé</i></code>. Les mots clés sont indiqués en italique en fin de
description de l'environnement. L'étape suivante du tutoriel explique
quelques <i>commandes de base</i>.</p>
""", {'capitalize': str.capitalize, 'shadow': SHADOW})

# We create an empty second room to link it with the first
room2 = game.map.new_room("les commandes de base")
link1_2 = game.map.new_link(room1, room2)
link2_1 = game.map.new_link(room2, room1)

# Second room description
room2.set_desc("""
<p>Pour voir à nouveau la
description de l'environnement (ce texte), utilisez
<code>regarder</code>. Cette même commande sert à regarder quelqu'un
ou quelque chose: 
    {% if character.data.name == shadow %}
    <code>regarder <i>mot clé</i></code>.
    {% else %}
    <code>regarder <i>{{character.data.name}}</i></code> par exemple.
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
<p>{{character.data.name}} peut retourner à la <i>création du personnage</i>
ou poursuivre vers la <i>fabrication des vêtements</i>.</p>
""", {'capitalize': str.capitalize, 'shadow': SHADOW})

# We create an empty third room to link it with the second
room3 = game.map.new_room("la fabrication des vêtements")
link2_3 = game.map.new_link(room2, room3)
link3_2 = game.map.new_link(room3, room2)
 
# Third room description
room3.set_desc("""
<p>{{character.data.name}} peut créer se propres vêtements avec
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
<p>Enfin, {{character.data.name}} peut porter ses vêtements avec la commande
<code>porter <i>mot_clé_de_l'item</i></code>.</p>""")
