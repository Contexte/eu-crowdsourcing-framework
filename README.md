Comeurop
========

<a name ="getting_started">
Getting started
===============

Using the command line (pbs), check it's properly [configured](#configure).

- Copy every unhidden file of this folder into another one ; anywhere, under any name. If you're cloning it from github, do not forget to clone it recursively, as this project has a submodule (PDF.js).

- Files modifications (empty files can stay that way) :

	- tutorial.html _default to empty_
	- long_description.md _default to empty_
	- project.json
	- model_tasks.json <i>Or create your JSON taskfile, using model_tasks.json</i>
	- template.html <i>Change the name (corresponding to the 'short_name' of your project.json) at the end of the file, in</i> pybossa.run(project short name) <i>and check the pdf folder is the right one </i>(/pybossa/uploads/pdfs by default)
- Run :
	pbs create_project

	pbs add_tasks --tasks-file tests_tasks.json --tasks-type=json --redundancy=1

	pbs update_project

<a name="configure"/>
Configure pbs
--------------

Pbs should already be configured with the admin key. If it's not, you can configure it in the hidden file <b>.pybossa.cfg</b>, located in the <b>home</b> directory. Here is how it should be written :

	[default]
	server: http://theserver.com
	apikey: yourkey

If it's not set and you don't wan't to set it, you still can run every admin command by doing :

	pbs --server http://your_server.com --api-key your_key subcommand

You also may want to create a <b>pdfs</b> folder at pybossa/uploads/, since the tempalte is going to search this folder for your pdf. See [PDF Storage](#PDF_storage)


1) Create your project
----------------------

To create your project with pbs (there are other ways, but we won't cover them here), you have to create a folder anywhere on the disk, and a file called project.json [(see the file's details)](#project.json) in it.

Then, you can create a draft with :

	pbs create_project

## Project's anatomy

<a name="project.json"/>
-  A JSON file called <b>project.json</b>, used to create the project and <b>must</b> contain :
  - a "name" field
  - a "short_name" field
  - a "description" field

  - It can contains other fields, such as the "statement" one, which allow you to display a custom sentence at the begining of each task taken by an user.


Example :

	{
		"name": "Full name of the project",
		"short_name": "project's slug, used by the RESTFUL API to access it",
		"description": "Short project's description",
	}

## Pybossa's Template

The <b>template.html</b> file is the connection between a project and his related tasks. It serves the purpose of preseting the task to the user and to saves their answers in the database.

In Pybossa, a script named PyBossa.JS is called on each task. It is the source of the functions _pybossa.presentTask()_ and _pybossa.taskLoaded_. Which are the functions you need to override in order to make your app works. The former is in charge of loading the task and the second of displaying it in the HTML page and saving the user's answers.

## Also

There are two other mandatory files :

-  <b>tutotial.html</b>, which is loaded (I think) the first time an user try to contribute on a project.
 
- <b>long_description.md</b> it speaks for itself.

They are only mandatory to call <i>pbs update_project</i>, since you don't really need them to run your project.


### What the project folder should contain :

- One (or more) JSON files to describe every tasks. You can give them any name. To use them, see [loading tasks](#loading_tasks).


<a name="loading_tasks"/>
2) Loading tasks
----------------

Once you have created your project, the next step is to put tasks in it.

There are two ways of doing it :

- Using the website and the CSV format (including a Google spreadshit). Note that the data uploaded using this method will be ultimately stored as JSON.

- In command line using pbs : <i>
	pbs add_tasks --tasks-file my_tasks.csv|json --tasks-type=csv|json [--redundancy=1] #, default to 30
	</i>, where you can use CSV or JSON ; again, it will ultimately stored as JSON.

<a name="tasks.json"/>
Les fichiers devront contenir les informations spécifiques aux tâches, voici un exemple de fichier JSON :

	[{
		"organization":"The organization who answered to the consultation. MUST BE UNIQUE in the whole project.",
	    "pdf":"my_pdf_name.pdf",
        "part":"A title for the part of the PDF being studied. Could be something like : 'Part 1' or : 'Part about the FISC'. If there is only 1 question asked for this part, it could be the question itself, but the purpose is to make a group out of several questions on the same part of a pdf.",
	    "page": 3,
		"statement": "Sentence to be displayed at the begining of every task in the project"
	        "questions":{
	                "First question (first paramater of answer determines its type : single or multiple answers possible)":["single", "yes", "no"],
	                "Second question (multiple answers possible)":["multiple", "first answer", "second answer", "third answer"]
	        }
	},
	{
		"organization":"European Bretzel Factory",
	    "pdf":"another_pdf_name.pdf",
        "part":"Favorite shape of bretzel in the morning",
	    "page": 6,
		"statement": "Please read the PDF we are providing you with and answer the questions."
	        "questions":{
               	 "First question (only one answer possible)":["single", "first answer", "second answer"]
               	 "Second question":["single", "a", "b"]
        	}
	}]

<b>NB :</b> In order to be properly taken by PyBossa, the JSON object should be put into an array.

<b>NB2 : </b> Any information you put into your tasks_filles will eventually end in the <i>info</i> part of the <i>task</i> associative array. You can access it in the template (see below) via <b>task.info.yourStuff</b>.

<a name="update"/>
3) Update du Projet
-------------------

Before you could even update the project, you will need all the mandatory files that we have spoken of earlier into your project folder.

Then you can type :

	pbs update_project

Once it's executed, the project will be available on the website, under the "projects" category.

This line should be executed every time you're modifying the template.

## The template

[Useful link (StackOverflow)](#https://stackoverflow.com/questions/25035717/pybossa-loading-and-presenting-tasks/25055844#25055844)

### The HTML Part

Light, most of it is generated via JS.

### pybossa.taskLoaded

One of the two methods provided by pybossa.JS, that we have to override.

This one's job is to load/preload a task. Once the user is on the task page, this function is called to load the first task. Then, while it will give the hand to the next one, pybossa is going to launch it again, in order to preload the next task. So the user will not have to wait for the PDF to load once again.

The next function is called by _deferred.resolve(task)_

<b>Summary</b> : here you only load/peload the PDF.

### pybossa.presentTask

This method does the heavy-lifting of presentig the task to the user, if the task is a valid one (i.e, if there is at least one task left into the project).

It contains 3 major code blocks, which are :

 - Draw the PDF on the canvas.
 - Populate the HTML page with a form.
 - Allow to save the result
    - This part also check that at least one answer is selected for every question.


<b>NB</b> : The submit button is not a real one, since its default behavior is prevented by : <i>event.preventDefault()</i>

<a name="PDF_Storage"/>
4) PDF storage
--------------

At the root of the pybossa folder, there is another folder called <b>uploads</b>. This folder contains every assets of the website and can be changed from the <b>settings_local.py</b> file. By modifying the value of <b>UPLOAD_FOLDER</b>.

This folder can be accessed from the file <b>template.html</b> at : ../../uploads. So, I recommand to create a folder called "pdfs" inside the upload folder. By default, the template of the project I wrote is going to scan this folder to get the PDFs.

### PDF.JS

PDF.JS (Mozilla) is used to display the PDFs on the HTML canvas.
