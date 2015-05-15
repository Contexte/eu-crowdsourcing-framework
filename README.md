comeurop
========

Pour aller au tutorial pas à pas pour déployer un projet : [tutorial](#tutorial)

Configurer pbs
--------------

En principe, pbs est déjà configuré avec la clé du compte amdinistrateur principal ( l'administrateur principal est, par défaut, le premir utilisateur à s'inscrire dans PyBossa, il peut ensutie passer les droits d'admin à d'autres users ).

La configuration se fait dans le fichier <b>.pybossa.cfg</b>, qui doit se trouver dans le <b>HOME</b> et dont voici la structure :

	[default]
	server: http://theserver.com
	apikey: yourkey

Dans le cas où le fichier ne serait pas rempli, il est toujours possible d'effectuer toutes les commandes d'administration en les préfixant par :

	pbs --server http://your_server.com --api-key your_key subcommand



1) Création d'un projet
-----------------------

La création d'un projet peut se faire de deux manières : sur le site web ou en ligne de commande. Si la méthode avec le site web est choisie, il faudra tout faire avec ( ce qui implique créer un fichier CSV souvent relativement complexe, voir [charger des tâches](#charger_des_taches) ).

Mais un projet peut aussi être créé en utilisant pbs. 

Pour ce faire, il faut créer un dossier et créer un fichier [project.json](#project.json) à l'intérieur de celui-ci.
Puis créer le projet dans le site avec :

	pbs create_project

Lorsqu'un projet a été créé avec cette commande, il entre dans les <b>drafts</b> sur le site.

## Décomposition d'un projet

Un projet dans PyBossa est, en gros, un sujet sur lequel la population va intervenir par le biais de tâches. Le projet est matérialisé par un dossier à la racine du répertoire de pybossa. Tous les fichiers qui sont mentionnés plus bas entrent dans ce dossier.

Les tâches sont les éléments précis sur lesquels intervient un membre de la "foule" qui crowdsourcera le projet.

<a name="ce_que_doit_contenir_un_projet"/>
### Le Projet comprend (obligatoirement) :

<a name="project.json"/>
- Un Fichier JSON nommé <b>project.json</b>, qui sert à créer le projet et doit <b>obligatoirement</b> comprendre :
  - un champ "name"
  - un champ "short_name"
  - un champ "description"

  - d'autres champs sont optionnels et pourront être accédés dans le template


Exemple :

	{
		"name": "Test project",
		"short_name": "testproj",
		"description": "This is a test project",
		"question": "This is just a test project. Do you like it ?" #optionnel
	}


<b> Ce qui suit peut être intégré au dossier après l'ajout des tâches au projet et avant l'[update](#update) du projet avec le template</b>

- Un template de présentation de tâche ( le TaskPresenter de PyBossa ). Il s'agit d'un fichier nommé <b>template.html</b>, avec une grosse partie JS à l'intérieur.

  <b>NB :</b> dans pybossa, un script JS nommé PyBossa.JS est automatiquement appelé à chaque tâche. Ce script permet d'utiliser les fonctions : <i>pybossa.presentTask()</i>( invoquée pendant que se charge la tâche, et qui donc fait le lien avec la page HTML ) et <i>pybossa.taskLoaded</i>(Je ne sais pas encore exactement quand est-ce qu'elle est appelée, mais je suppose que c'est lorsque l'utilisateur change de tâche).

- Un fichier <b>tutotial.html</b>, qui est chargé (il me semble) la première fois que  l'utilisateur souhaite contribuer au projet.
 
- Un fichier <b>long_description.md</b>. Tout est dans le titre.



### Le projet est aussi supposé contenir :

- Un ( ou plusieurs ) fichier(s) JSON, de description des tâches. Leur nom est libre, mais ils doivent être invoqués avec une commande spéciale, voir [charger des tâches](#charger_des_taches).



<a name="charger_des_taches"/>
2) Charger des tâches
---------------------

Lorsque Le projet a été correctement initialisé, l'étape suivante consiste à charger les tâches à l'intérieur de celui-ci.

Pour ce faire, 2 méthodes :

- Par le site web avec un fichier CSV ( ou une Google SpreadSheet ) -- difficile lorsque les objets sont complexes, mais il est possible de passer par un logiciel tiers, si la ligne de commande est compliquée, par exemple [JSON to CSV converter](https://json-csv.com/). Dans ce cas, il vaut mieux faire toutes les tâches d'un seul coup, puisqu'un seul objet JSON peut contenir toutes le tâches du projet, voir l'exemple un peu plus bas).
- En ligne de commande en utilisant pbs ( avec la syntaxe : <i>
	pbs add_tasks --tasks-file my_tasks.csv|json --tasks-type=csv|json [redundancy=1] #Si on ne vuet qu'une réponse par tâch, défaut à 30
	</i>, où deux types de fichier sont utilisables : csv ou JSON (sahcant qu'en définitive, PyBossa utilisera forcément un fichier JSON).

Les fichiers devront contenir les informations spécifiques aux tâches, voici un exemple de fichier JSON :

	[{
		"document":"test.pdf", # Les PDF lus doivent être stockés sur la machine, voir  plus bas.
        	"page":3,
        	"questions":{
               		"do you want chewing gum?":["yep", "no"],
               		"do you like apple pies?":["ojh", "jhbgf"]
        	}
	},
	{
		"document":"truc.pdf",
		etc...
	}]


<b>NB :</b> De mes tests est ressorti que l'objet JSON doit obligatoirement être mis dans un tableau ( les [] en début et fin de fichier sont obligatoires). Sinon le fichier n'est simplement pas compris par PyBossa.

<b>NB2 : </b> Toutes les informations contenues dans un objet JSON vont dans l'attribut <i>info</i> de l'objet <i>task</i>, accessible dans le javascript du template par ce biais.

La mise en forme se fera ensuite dans le fichier <b>template.html</b>.

<a name="update"/>
3) Update du Projet
-------------------

Avant que le projet ne soit updaté, celui-ci doit contenir tous les fichiers demandés ( template.html, tutorial.html etc... )

La commande est :

	pbs update_project

Une fois cette commande lancée, le projet entre dans les projets disponibles sur le site.



### Le template

[Lien utile](#https://stackoverflow.com/questions/25035717/pybossa-loading-and-presenting-tasks/25055844#25055844)




<a name="ou_stocker_PDF"/>
4) Stocker des PDF
------------------

A la racine du dossier pybossa se trouve un dossier nommé <b>uploads</b> ce dossier contient les assets du site web et peut être changé dans le fichier <b>settings_local.py</b>(depuis la racine de pybossa), dans la constante <b>UPLOAD_FOLDER</b>.

Ce dossier peut être accédé dans le fichier <b>template.html</b> à l'adresse : ../../uploads. Autant, donc, créer un dossier "pdfs" à l'intérieur du dossier uploads et coller tous les PDF à l'intérieur. Ensuite, les ficheirs peuvent être facilement accédés par leur nom.

### PDF.JS

La technologie utilisée pour afficher les PDF est PDF.JS (Mozilla). Qui permet d'afficher un PDF ( à une page donnée ), dans un Canvas. Il y a donc toute une partie du JS dédiée à la partie affichage du PDF.
