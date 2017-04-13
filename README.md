#  <img src="https://raw.githubusercontent.com/jkanev/treetime/master/data/treetime-logo.png" alt="logo" width="64" height="64">&nbsp; &nbsp; &nbsp; &nbsp;Tree Time


Tired of trying to organise your data in spread sheets? Use trees instead. TreeTime is a time planner, to-do list manager, test report tool, project manager, family ancestry editor, mind-mapping tool, etc. Using TreeTime you can categorise and organise your data items in tree structures. You can define several trees at the same time, each with a different structure, but on the same data.You can use functions (calculate sums, ratios and means) recursively up the branches of a tree. 

<div id='id-contents'/>
### Table of Contents ###
- [Concept](#id-concept)
- [Installation](#id-installation)
- [Usage](#id-usage)
- [Road-Map](#id-roadmap)
- [Dependencies](#id-dependencies)


<div id='id-concept'/>
## Concept ##
[Table of Contents](#id-contents)

Think about your data and what you want to organise. Data is usually a bunch of simple items which can be grouped or sorted and which are related to each other. If you want to organise work in a company such a simple item could be a Task. In a spreadsheet that would be a line in a table, with several columns for different properties of the task. In TreeTime a Task would be a data item. It could have several fields like planned completion date, planned effort, actual completion date, current progress, a name and a short description. You can think of several ways to organise your data items:
- Tasks can be part of a work package which can be part of a project which can be part of a product release.
- Tasks can be done by persons which belong to a team which belongs to a department which belongs to a company.
- Tasks may be planned to finish on a certain date, which may be part of a weekly plan, which may be part of a quarterly plan, which may be part of a yearly plan.

Each of these ways to categorise the data is a tree in TreeTime. For each of these trees you may be interested in different things: 
- If you look at your Tasks organised into Projects and Workpackages you might want to see the effort per task, summed effort per Workpackage, or per Project.
- If you look at your Data organised into Persons and Departments you might want to see the ratio of effort in one team compared to all other teams, or the percentage of effort of one department compared to all other departments.
- If you look at your Tasks organised into planned completion periods you might want to see the total progress for tasks you planned for this year, this month or this week.

The concept of hierarchical categorisation can be applied to all sorts of data and will feel a lot more natural and easier to use than organising the same data in spread sheets. Examples are your family ancestory tree, your personal to-do list, a collection of facts you want to gather about a certain topic, a script for a play with different actors, stories and sub-stories, documentation and test instructions for software testing, and lots more.

In TreeTime, the data item fields, the trees, and the fields that are displayed in a tree are completely user defined. At the moment TreeTime can display texts as well as numbers and their sums, means and ratios, and names of the parent node in all different trees.

<div id='id-installation'/>
## Installation ##
[Table of Contents](#id-installation)

1. If you don't have it yet, install python3
   - Debian, Ubuntu and related: on the command line, type "apt-get install python3"
   - Other Linux distributions: install python3 with your default package manager
   - Windows, Mac and similar: download from https://www.python.org/downloads/
2. If you don't have it yet, install PyQt5
   - Debian, Ubuntu and related: on the command line, type "apt-get install python3-pyqt5"
   - Other Linux distributions: install pyqt5 with your default package manager
   - Windows, Mac and similar: "pip3 install pyqt5" (see http://pyqt.sourceforge.net/Docs/PyQt5/installation.html)
3. Download this project from GitHub
4. Install. In the command line, cd into the main directory, then type:
   - python3 setup.py build
   - sudo python3 setup.py install
5. Execute
   - on the command line, type: "python3 -m treetime"

<div id='id-usage'/>
## Usage ##
[Table of Contents](#id-contents)

Start the software by typing "python3 -m treetime". In the main dialog, go to "File Storage", click "Load other File" and select "items.trt". The GUI will come up with an example project. Several data items will have loaded (a project with three tasks and two week-planning entries) and are organised in three trees. The GUI is organised in three parts:
- A button box on the left. Execute tree structure operations from here.
- An editing grid in the middle, showing the contents of the selected data item. Edit single data items here.
- A tab view with tress spanning the center-right. View and analyse your data here.

![Screenshot 1](doc/screenshot01.png)

Access each single tree by clicking a tab on the main tree-view widget. Branches and children can be sorted, branches can be folded and unfolded. Data content is shown via analytic fields that are defined per tree. In the example project you will see a sum, a percentage, and text display. 

![Screenshot 2](doc/screenshot02.png)

Add and move single nodes and branches by using the buttons on the left (New Child, New Sibling, New Parent, Copy Node as Child, Copy Node as Sibling, Copy Node as Parent, Copy Branch as Sibling (not implemented yet), copy Children to Siblings (not implemented yet), Remove from this Tree (not implemented yet), Delete Item (not implemented yet).

Change the name of a node by selecting the node and editing the name in the top of the edit grid in the middle.
Change the parent of any node by typing a name of an existing node into the parent fields in the edit grid. The parent fields are the three lines underneath the item's name.

<div id='id-roadmap'/>
## Road-Map ##
[Table of Contents](#id-contents)

I deliberately didn't give any time estimates for this. I'm using the software myself to organise my own data, so I'm interested in keeping this going. Nevertheless I cannot promise any specific release dates. If you have any suggestions or would like me to implement some feature sooner than I suggested here, please just drop me an email.
- Done Feb. 2016: Implement selection (the same item gets selected in all trees, changing a tab shows the same item)
- Done Mar. 2016: Implement remaining local functionality (Copy Branch as Sibling, Copy Children to Siblings, Remove from this Tree, Delete Item)
- Done Aug. 2016: Created installable python package
- Running: Create complete installer for Linux, Windows, possibly Android
- Near Future: Bugfixing
- Near Future: Release Version 0.1
- Mid Future: Implement global functions (Linearise Tree, Level-Swap, Merge identical Siblings, Merge Identical Parents/Children, Remove all Orphans, Insert all Orphans as Children)
- Mid Future: Bugfixing
- Mid Future: Release Version 0.2
- Mid Future: Implement search functionality
- Mid Future: Implement more data item field types (URLs, timers, date/time/time-span)
- Mid Future: Implement more tree field types (standard deviation, min, max, string concatenation, 
- Mid Future: Bugfixing
- Mid Future: Release Version 0.3
- Far Future: Implement tree field editing with graphical dialog (add, remove, change tree fields)
- Far Future: Implement data item field editing with graphical dialog (add, remove, change data item fields)
- Far Future: Bugfixing
- Far Future: Release Version 1.0
- Far Future: Implement tree export to PDF, txt, and/or CSV
- Far Future: Implement safe usage by multiple simultaneous users
- Far Future: Implement a database backend instead of text file storage
- Far Future: Implement a web server
- Far Future: A whole lot of other fancy things that will probably never get done

<div id='id-dependencies'/>
## Dependencies ##
[Table of Contents](#id-contents)

TreeTime depends on [`Python 3`](https://www.python.org/downloads/), [`Qt5`](http://www.qt.io/download/), and [`PyQt5`](https://pypi.python.org/pypi/PyQt5).