from step import Template

from eveil import room
from eveil import thing


# Character generation rooms

cg1 = room.Room(game)
cg1.shortdesc = Template("<h3>Le sanctuaire des noms</h3>")
cg1.longdesc = Template("""
<p>Au fond d'une profonde vallée, sous l'ombre d'arbres
centenaires, en partie recouvertes de mousse, gîsent deux vieilles
pierres. Le peu de lumière perçant le feuillage illumine les runes
gravées sur leurs
%if character.name:
    flancs. {{character.name}} y reconnaît son nom, parmis de nombreux autres:
%else:
    flancs:
%endif
Les noms de ceux qui vivèrent et de ceux qui vivront. L'une des
pierres porte les noms des hommes, l'autre ceux des femmes.</p>
<ul>
    <li>Pour lire les exemples de noms entrez
    <code>voir hommes</code>,
    <code>voir femmes</code>.</li>
    <li>Pour choisir le genre de votre personnage, entrez:
    <code>genre: [homme|femme]</code>.
    <li>Pour nommer votre personnage, entrez
    <code>nom: <i>nom_choisi<i></code>.</li>
</ul>
""")
hommes = thing.Thing()
hommes.desc = Template("""
<p>Sur la pierre des hommes qui fûrent ou qui seront, sont
gravés les noms: Abarta, Abcán, Abhean, Abgatiacus, Abortach, Accasbel,
Adammair, Aed, Aengus, Aesar, Aesun, Ai, Aidne, Ailill, Aillen, Alastir,
Allaoi, Alldui, Allod, Amergin, Anind, Anpao, Aoi, Ard-Greimme, Baile, Balor,
Bec-Felmas, Bel, Bethach, Bith, Bodb, Boibhniu, Breasal, Bres, Brian, Bron,
Bryan, Buarainech, Builg, Caicher, Caither, Catt, Cebhain, Cenn, Cermait,
Cethen, Cian, Cichol, Conand, Cond, Corb, Creidhne, Cridenbel, Crom, Cu,
Cucharn, Cumal, Curoi, Da, The, Dáire, Delbáeth, Delga, Dian, Diarmuid, Donn,
Dót, Dui, Easal, Easar, Echtach, Ecne, Egobail, Elatha, Elcmar, Eochu, Esar,
Eterlam, Eterlam, Ethal, Figol, Finvarra, Fiachna, Flesc, Gaible, Gavida,
Goibniu, Goll, Guaire, Iarbonel, Ibur, Indech, Indui, Iubdan, Iuchar, Iucharba,
Juchor, Juchorba, Labraid, Lám, Lén, Lir, Llyr, Luam, Luchtaine, King, Lugh,
Mac, Mac, Mac, Mac, Maeltne, Magmor, Manannán, Mean, Miach, Midir, Mug,
Nechtan, Neit, Nemglan, Nemon, Nuada, Nuadu, Nuagatt, Ochttriuil, Ogma, Ruadan,
Sawan, Seibur, Seonaidh, Shoney, Slaine, Somhlth, Tagd, Tat, Tavarn, Tethra,
Tuan, Tuireann, Ugnach.</p>""")

femmes = thing.Thing()
femmes.desc = Template("""
<p>Sur la pierre des femmes qui furent ou qui seront, sont gravés
les noms: Achall, Achtland, Adair, Aebh, Áed, Aeval, Aibell,
Aibheaog, Aimend, Aífe, Aima, Áine, Airmed, Almha, Ana, Anann,
Argoen, Badb, Ban-Chuideachaidh, Ban, Banba, Beag, Bebhion,
Bébinn, Bé, Be, Bechoil, Becuma, Befind, Beira, Biddy, Biróg,
Birren, Blai, Blathnat, Bo, Bo, Bo, Boann, Bodb, Bodhmall, Breg,
Bréifne, Bridghiendto, Bríg, Brigid, Maman, Bodhmall, Bronach,
Búanann, Caer, Cailleach, Caíntigern, Caireen, Cairpre, Caitlín,
Cally, Canola, Caolainn, Carman, Carravogue, Cathleen, Ceacht,
Cebhfhionn, Cessair, Cethlenn, Chlaus, Cleena, Clíodhna, Clothru,
Corchen, Credhe, Creide, Crobh, Crochan, Danand, Danann, Danu,
Danus, Dechtere, Deirdre, Dianann, Dígde, Dil, Domnu, Donann,
Dreco, Duan, Dubh, Dwumwem, Eadon, Ebhlinne, Ebliu, Echtghe,
Echtgne, Edarlamh, Eibhir, Éle, Emer, Eri, Ériu, Ernin, Ernmas,
Ernmas, Esaire, Étaín, Etan, Etan, Ethlinn, Ethnea, Ethniu, Fand,
Fata, Fè, Fea, Fiall, Finnabair, Finncaev, Fionnuala, Flaitheas,
Fland, Flidais, Fuamnach, Fódla, Garbh, Glas, Grain, Grainne,
Grian, Inghean, Irnan, Kele-De, Lassair, Latiaran, Lí, Liban,
Logia, Lot, Luaths, Macha, Magh, Mal, Medb, Medb, Meg, Men, Mess,
Mongán, Mongfind, Morrígan, Morrigu, Mór, Muireartach, Muirenn,
Munanna, Murigen, Naas, Nair, Nemain, Nemon, Niamh, Nicnevin,
Plor, Re, Sadhbh, Scathach, Scenmend, Sheela, Sin, Shannon,
Smirgat, Tailtiu, Telta, Tephi, Tlachtga, Tuiren, Turrean,
Uairebhuidhe, Uathach, Uirne, Vera.</p>""")

cg2 = room.Room(game)
cg2.shortdesc = Template("<h3>Une petite mare</h3>")
cg2.longdesc = Template("""
<p>Dans un creu formé par les racines entortillées d'un veil arbre,
l'eau de pluie s'est accumulée en une petite mare. Profonde et sombre,
la lumière ne la transperce pas, mais s'y reflète.
#if @character.name:
    En s'approchant de son rebors, @character.name voit son apparence miroiter.
#else
    L'ombre s'approchant de son rebors voit son apparence miroiter.
#end
#if @character.longdesc:
    À première vue, @character.pronom découvre @character.shortdesc. En y
    regardant de plus près, @character.pronom voit:</p>
    <blockquote>@character.longdesc</blockquote>
#else
    </p>
#end
<ul>
    <li>Pour décrire
    #if @character.name:
        @character.name,
    #else
        votre personnage,
    #end
    entrez:
    <code>description: <i>Longue description...</i></code>.</li>
    <li>Pour définir la courte description de votre personnage,
    entrez: <code>apparence: <i>quelques mots</i></code>.</li>
    <li>Pour voir @character.name, entrez:
    <code>voir: @character.name</code>.</li>
</ul>""")

cg3 = room.Room(game)
cg3.shortdesc = Template("<h3>Un cercle de pierres</h3>")
cg3.longdesc = Template("""
<p>La densité de la forêt ne diminue pas, mais ici, entouré de
vaillants et hauts arbres, un cercle de pierres repose,
semble-t-il depuis toujours. Sur chacune des pierres est gravée
une rune: celle de l'artisan, celle du chasseur, celle du druide,
celle du guerrier, celle du barde. Sur chacune de ces pierres,
sont gravées des scènes de vies.</p>
#if character.skill == "crafter":
    <p>Un rayon de lumière éclaire la pierre de l'artisan.</p>
#elseif character.skill == "hunter":
    <p>Un rayon de lumière éclaire la pierre du chasseur.</p>
#elseif character.skill == "druid":
    <p>Un rayon de lumière éclaire la pierre du druide.</p>
#elseif character.skill == "warrior":
    <p>Un rayon de lumière éclaire la pierre du guerrier.</p>
#elseif character.skill == "bard":
    <p>Un rayon de lumière éclaire la pierre du barde.</p>
#end
<ul>
    <li>Pour choisir un métier, entrez:
    <code>métier:
    <i>artisan|chasseur|druide|guerrier|barde</i></code>.</li>
    <li>Pour choisir un talent, entrez:
    <code>talent:
    <i>sagesse|intelligence|constitution|force|agileté</i></code>.</li>
</ul>""")

cg4 = room.Room(game)
cg4.shortdesc = Template("<h3>La source du torrent</h3>")
cg4.longdesc = Template("""
<p>Du flanc de la colline, entre pierres et racines, jaillit
l'eau du torrent. Elle coule d'abord en une petite cascade
jusque dans un petit bassin, avant de se faufiler entre les
rochers et de dévaler la pente. Sa fraicheur et sa pureté
sont une invitation à se déshaltérer.</p>""")

