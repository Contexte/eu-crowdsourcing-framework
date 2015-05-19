comeurop
========

Pour déployer rapidement un projet, voir : [Déploiement rapide](#deploiement_rapide)

<a name="configure"/>
Configurer pbs
--------------

En principe, pbs est déjà configuré avec la clé du compte amdinistrateur principal ( l'administrateur principal est, par défaut, le premir utilisateur à s'inscrire dans PyBossa, il peut ensuite passer les droits d'admin à d'autres users ).

La configuration se fait dans le fichier <b>.pybossa.cfg</b>, qui doit se trouver dans le <b>HOME</b> et dont voici la structure :

	[default]
	server: http://theserver.com
	apikey: yourkey

Dans le cas où le fichier ne serait pas rempli, il est toujours possible d'effectuer toutes les commandes d'administration en les préfixant par :

	pbs --server http://your_server.com --api-key your_key subcommand


1) Création d'un projet
-----------------------

La création d'un projet peut se faire de deux manières : sur le site web ou en ligne de commande. Si la méthode avec le site web est choisie, il faudra tout faire avec ( ce qui implique créer un fichier CSV souvent relativement complexe, voir [charger des tâches](#charger_des_taches) ).

Mais un projet peut aussi être créé, plus simplement, en ligne de commande en utilisant pbs. 

Il faut créer un dossier, ainsi qu'un fichier [project.json (voir les détails du fichier)](#project.json) à l'intérieur de celui-ci.
Puis générer le projet dans le site avec :

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
  - un champ "statement"

  - d'autres champs sont optionnels et pourront être accédés dans le template


Exemple :

	{
		"name": "Nom Complet de Mon Projet",
		"short_name": "slug du projet, utilisé par l'api RESTFUL pour y accéder",
		"description": "Description courte du projet ; la longue se fait ailleurs",
		"statement": "Phrase affichée sur toutes les tâches du projet."
	}


<b> Ce qui suit peut être intégré au dossier après l'ajout des tâches au projet et avant l'[update](#update) du projet avec le template</b>

- Un template de présentation de tâche ( le TaskPresenter de PyBossa ). Il s'agit d'un fichier nommé <b>template.html</b>, avec une grosse partie JS à l'intérieur.

  <b>NB :</b> dans pybossa, un script JS nommé PyBossa.JS est automatiquement appelé à chaque tâche. Ce script permet d'utiliser les fonctions : <i>pybossa.presentTask()</i>( invoquée pendant que se charge la tâche, et qui donc fait le lien avec la page HTML ) et <i>pybossa.taskLoaded</i>(Je ne sais pas encore exactement quand est-ce qu'elle est appelée, mais je suppose que c'est lorsque l'utilisateur change de tâche).

- Un fichier <b>tutotial.html</b>, qui est chargé (il me semble) la première fois que l'utilisateur souhaite contribuer au projet.
 
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
	pbs add_tasks --tasks-file my_tasks.csv|json --tasks-type=csv|json [redundancy=1] #Si on ne veut qu'une réponse par tâch, défaut à 30
	</i>, où deux types de fichier sont utilisables : csv ou JSON (sahcant qu'en définitive, PyBossa utilisera forcément un fichier JSON).

<a name="tasks.json"/>
Les fichiers devront contenir les informations spécifiques aux tâches, voici un exemple de fichier JSON :

	[{
	        "pdf":"my_pdf_name.pdf",
	        "page": 3,
	        "questions":{
	                "First question (first paramater of answer determines its type : single or multiple answers possible)":["single", "yes", "no"],
	                "Second question (multiple answers possible)":["multiple", "first answer", "second answer", "third answer"]
	        }
	},
	{
	        "pdf":"another_pdf_name.pdf",
	        "page": 6,
	        "questions":{
               	 "First question (only one answer possible)":["single", "first answer", "second answer"]
               	 "Second question":["single", "a", "b"]
        	}
	}]

<b>NB :</b> De mes tests est ressorti que l'objet JSON doit obligatoirement être mis dans un tableau ( les [] en début et fin de fichier sont obligatoires). Sinon le fichier n'est simplement pas compris par PyBossa.

<b>NB2 : </b> Toutes les informations contenues dans un objet JSON vont dans l'attribut <i>info</i> de l'objet <i>task</i>, accessible dans le javascript du template par ce biais. <b>task.info.yourStuff</b>

La mise en forme se fera ensuite dans le fichier <b>template.html</b>.

<a name="update"/>
3) Update du Projet
-------------------

Avant que le projet ne soit updaté, celui-ci doit contenir tous les fichiers demandés ( template.html, tutorial.html etc... )

La commande est :

	pbs update_project

Une fois cette commande lancée, le projet entre dans les projets disponibles sur le site.

A chaque modification du template, elle a besoin d'être relancée.

## Le template

[Lien utile (StackOverflow)](#https://stackoverflow.com/questions/25035717/pybossa-loading-and-presenting-tasks/25055844#25055844)

Le template actuel contient plusieurs sections.

### Le HTML

Très léger, la plupart des lignes n'aparaissent que suite à des events : plus de tâches disponibles, tâche accomplie, etc...

Il est largement modifié / complété par le JS qui se trouve dans le même fichier.

### pybossa.taskLoaded

Permet de charger/précharger une tâche. Lorsque l'utilisateur arrive sur sa première tâche, cette fonction est appelée une première fois pour la tâche en cours, puis une seconde fois pour pré-charger la seconde tâche.

Lorsque la tâche ( ici il ne s'agit en réalité que du PDF ) a été chargée, on appelle deferred.resolve(task), qui lance la prochaine étape.

<b>Resumé</b> : Ici on ne fait que charger/précharger le PDF.

### pybossa.presentTask

Cette méthode contient toute la logique d'affichage et de présentation de la tâche à l'utilisateur.

Si la tâche est valide (i.e, si il reste des tâches dans le projet), elle contient 3 grandes catégories, qui sont :

- Dessiner le PDF sur le canvas
- Générer le formulaire HTML
- Permettre de sauvegarder (et de modifier l'affichage du document HTML en conséquence)
	- Cette partie vérifie aussi qu'une checkbox au moins a été cochée pour chaque question.

<b>NB</b> : le bouton Submit, utilisé pour sauvegarder les données n'est pas un vrai bouton submit de formulaire, dans la mesure où on l'empêche de faire son taff ordinaire (avec <i>event.preventDefault()</i>).

<a name="ou_stocker_PDF"/>
4) Stocker des PDF
------------------

A la racine du dossier pybossa se trouve un dossier nommé <b>uploads</b> ce dossier contient les assets du site web et peut être changé dans le fichier <b>settings_local.py</b>(depuis la racine de pybossa), dans la constante <b>UPLOAD_FOLDER</b>.

Ce dossier peut être accédé dans le fichier <b>template.html</b> à l'adresse : ../../uploads. Autant, donc, créer un dossier "pdfs" à l'intérieur du dossier uploads et coller tous les PDF à l'intérieur. Ensuite, les ficheirs peuvent être facilement accédés par leur nom.

### PDF.JS

La technologie utilisée pour afficher les PDF est PDF.JS (Mozilla). Qui permet d'afficher un PDF (à une page donnée), dans un canvas HTML5. Il y a donc toute une partie du JS dédiée à la partie affichage du PDF.


<a name ="deploiement_rapide">
Déploiement rapide
==================

En ligne de commande, utilisant l'outil pbs [configuré](#configure).

- Copier l'intégralité des fichiers non-cachés de ce dossier n'importe où, avec n'importe quel nom.

- Modifier les fichiers (Les fichiers vides peuvent le rester)

	- tutorial.html _vide par défaut_
	- long_description.md _vide par défaut_
	- project.json
	- model_tasks.json <i>Ou créez votre fichier de tâche en JSON correspondant à model_tasks.json</i>
	- template.html _En changeant UNIQUEMENT le nom (short name dans project.json et PAS name) à la fin du fichier dans pybossa.run(project short name)_

- Lancer :
	pbs create_project
	pbs add_tasks --tasks-file tests_tasks.json --tasks-type=json redundancy=1
	pbs update_project
