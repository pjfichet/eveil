from eveil.template import Template

# Character generation rooms

# We create the first room 
room1 = game.map.new_room()
room1.shortdesc = "le gouffre"
room1.longdesc = Template("""
<h3>{{room.shortdesc|capitalize}}</h3>
<p>Au fin fond du gouffre, le cœur sombre de la terre n'est peuplé que
d'ombres dormantes. Du profond de leur sommeil, les ombres sont habitées
d'une rumeur: Il est dit que c'est du fin fond du gouffre, que naissent
les âmes. Parfois, une ombre, s'éveille au son de
cet appel. Et celle qui n'était qu'ombre parmis les ombres, se reconnaît
un nom, un genre, une apparence... Et se reconnaît vivante.</p>
<ul>

{% if character.name %}
    <li>L'ombre se reconnaît un nom: {{character.name}}</li>
{% else %}
    <li>Pour nommer votre personnage, entrez
    <code>nom <i>nom_choisi</i></code>.</li>
{% endif %}

{% if character.gender %}
    <li>
    {% if character.name %}
        {{character.name}}
    {% else %}
        L'ombre
    {% endif %}
    reconnaît qu'{{character.pronoun('il')}}
    est {{character.pronoun('un')}}
    {{character.GENDERS[character.gender]}}.
    </li>
{% else %}
    <li>Pour choisir son genre entrez:
    <code>genre [homme|femme]</code>.</li>
{% endif %}

{% if character.shortdesc %}
    <li>{{character.pronoun('il')}} apparaît ainsi:
    {{character.shortdesc}}</li>
{% else %}
    <li>Pour définir son apparence, entrez:
    <code>apparence <i>quelques mots</i></code>.</li>
{% endif %}

{% if character.longdesc %}
    <li>{{character.longdesc}}</li>
{% else %}
    <li>Pour définir sa longue description, entrez:
    <code>description <i>Longue description...</i></code>.</li>
{% endif %}

<li>Entrez <code>voir</code> lorsque vous avez fini.</li>
</ul>

{% if character.name and character.gender %}
{% if character.shortdesc and character.longdesc %}
    <p>
    {% for link in room.targets %}
        En {{link.dynadesc}}, {{character.name}} peut rejoindre {{link.target.shortdesc}}.
    {% endfor %}
    </p>
{% endif %}
{% endif %}
""", {'capitalize': str.capitalize,})

# We create an empty second room to link it with the first
room2 = game.map.new_room()
link1 = game.map.new_link(room1, room2)
link1.dynadesc = "s'élevant vers la surface"
link2 = game.map.new_link(room2, room1)
link2.dynadesc = "descendant dans les profondeurs du gouffre"

# Second room description
room2.shortdesc = "Une caverne"
room2.longdesc = Template("""
<h3>{{room.shortdesc|capitalize}}</h3>
<p>TODO</p>
""", {"capitalize": str.capitalize})


