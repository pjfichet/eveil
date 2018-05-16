from eveil.template import Template

# Character generation rooms

# We create the first room 
room1 = game.map.new_room()
room1.shortdesc = "le sanctuaire des noms"
room1.longdesc = Template("""
<h3>{{room.shortdesc|capitalize}}</h3>
<p>Au fond d'une profonde vallée, sous l'ombre d'arbres
centenaires, en partie recouvertes de mousse, gîsent deux vieilles
pierres. Le peu de lumière perçant le feuillage illumine les runes
gravées sur leurs
{% if character.name %}
    flancs. {{character.name}} y reconnaît son nom, parmis de nombreux autres:
{% else %}
    flancs:
{% endif %}
Les noms de ceux qui vivèrent et de ceux qui vivront. L'une des
pierres porte les noms des hommes, l'autre ceux des femmes.</p>
<ul>
    <li>Pour lire les exemples de noms entrez
    <code>voir hommes</code>,
    <code>voir femmes</code>.</li>
    <li>Pour choisir le genre de votre personnage, entrez:
    <code>genre: [homme|femme]</code>.
    <li>Pour nommer votre personnage, entrez
    <code>nom: <i>nom_choisi</i></code>.</li>
</ul>
<p>
{% for link in room.targets %}
En {{link.dynadesc}}, {{character.name}} peut rejoindre {{link.target.shortdesc}}.
{% endfor %}
</p>
""", {'capitalize': str.capitalize})

# We create an empty second room to link it with the first
room2 = game.map.new_room()
link1 = game.map.new_link(room1, room2)
link1.dynadesc = "s'enfonçant dans la forêt"
link2 = game.map.new_link(room2, room1)
link2.dynadesc = "approchant de la lisière de la forêt"

# Second room description
room2.shortdesc = "une petite mare"
room2.longdesc = Template("""
<h3>{{room.shortdesc|capitalize}}</h3>
<p>Dans un creu formé par les racines entortillées d'un veil arbre, l'eau de
pluie s'est accumulée en une petite mare. Profonde et sombre, la lumière ne la
transperce pas, mais s'y reflète. En s'approchant de son rebors,
{{character.name}} voit son apparence miroiter.
{% if character.shortdesc %}
    À première vue, @character.pronom découvre {{character.shortdesc}}.
{% endif %}
{% if character.longdesc %}
En y regardant de plus près, {{character.pronom}} voit:</p>
    <blockquote>{{character.longdesc}}</blockquote>
{% else %}
    </p>
{% endif %}

<ul>
    <li>Pour décrire {{character.name}}
    <code>description: <i>Longue description...</i></code>.</li>
    <li>Pour définir la courte description de {{character.name}},
    entrez: <code>apparence: <i>quelques mots</i></code>.</li>
    <li>Pour voir {{character.name}}, entrez:
    <code>voir: <i>{{character.name}}</i></code>.</li>
</ul>
<p>
{% for link in room.targets %}
En {{link.dynadesc}}, {{character.name}} peut rejoindre {{link.target.shortdesc}}.
{% endfor %}
</p>

""", {"capitalize": str.capitalize})


