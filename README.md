# Tree Time

Tired of trying to organise your data in spread sheets? Use trees instead.

TreeTime is a to-do list manager, test report tool, project manager, family ancestry editor, mind-mapping tool, etc. Using TreeTime you can categorise and organise your data items in tree structures, calculate sums, ratios and means from single nodes up to branches up the tree. 

# Table of Contents
<div id='id-contents'/>
- [Concept](#id-concept)
- [Usage](#id-usage)
- [Road-Map](#id-roadmap)
- [Dependencies](#id-dependencies)


## Concept
<div id='id-concept'/>
[Table of Contents](#id-contents)

Think about your data and what you want to organise. Think of the smallest data structure. If you want to organise work in a company that could be a Task. In TreeTime a Task would be a data item. It could have several fields like planned completion date, planned effort, actual completion date, current progress, a name and a short description. You can think of several ways to organise your data items:
- Tasks can be part of a work package which can be part of a project which can be part of a product release.
- Tasks can be done by persons which belong to a team which belongs to a department which belongs to a company.
- Tasks may be planned to finish on a certain date, which may be part of a weekly plan, which may be part of a quarterly plan, which may be part of a yearly plan.

Each of these ways to categorise the data is a tree in TreeTime. For each of these trees you may be interested in different things: 
- If you look at your Tasks organised into Projects and Workpackages you might want to see the effort per task, summed effort per Workpackage, or per Project.
- If you look at your Data organised into Persons and Departments you might want to see the ratio of effort in one team compared to all other teams, or the percentage of effort of one department compared to all other departments.
- If you look at your Tasks organised into planned completion periods you might want to see the total progress for tasks you planned for this year, this month or this week.

The concept of hierarchical categorisation can be applied to all sorts of data and is a lot more natural and easier to use than organising the same data in spread sheets. Think of your family ancestory tree, your personal to-do list, a collection of facts you want to gather about a certain topic, a script for a play with different actors, stories and sub-stories, think documentation and test instructions for software testing, and lots more.

In TreeTime, the data item fields, the trees, and the fields that are displayed in a tree are completely user defined. At the moment TreeTime can display texts as well as numbers and their sums, means and ratios, and names of the parent node in all different trees.

## Usage
<div id='id-usage'/>
[Table of Contents](#id-contents)

Start the python script "treetime". Go to "File Storage", click "Load other File" and select "items.trt". The GUI will come up with an example project. Several data items will have loaded (a project with three tasks and two week-planning entries) and are organised in three trees. The GUI is organised in three parts:
- A button box on the left. Execute tree structure operations from here.
- An editing grid in the middle, showing the contents of the selected data item. Edit single data items here.
- A tab view with tress spanning the center-right. View and analyse your data here.

![Screenshot 1](doc/screenshot01.png)

Access each single tree by clicking a tab on the main tree-view widget. Branches and children can be sorted, branches can be folded and unfolded. Data content is shown via analytic fields that are defined per tree. In the example project you will see a sum, a percentage, and text display. 

![Screenshot 2](doc/screenshot02.png)

Add and move single nodes and branches by using the buttons on the left (New Child, New Sibling, New Parent, Copy Node as Child, Copy Node as Sibling, Copy Node as Parent, Copy Branch as Sibling (not implemented yet), copy Children to Siblings (not implemented yet), Remove from this Tree (not implemented yet), Delete Item (not implemented yet).

Change the name of a node by selecting the node and editing the name in the top of the edit grid in the middle.
Change the parent of any node by typing a name of an existing node into the parent fields in the edit grid. The parent fields are the three lines underneath the item's name.

## Road-Map
<div id='id-roadmap'/>
[Table of Contents](#id-contents)

- Implement selection (the same item gets selected in all trees, changing a tab shows the same item)
- Create installer for Linux, Windows, possibly Android
- Bugfixing
- Release Version 0.0
- Implement remaining local functionality (Copy Branch as Sibling, Copy Children to Siblings, Remove from this Tree, Delete Item)
- Bugfixing
- Release Version 0.1
- Implement global functions (Linearise Tree, Level-Swap, Merge identical Siblings, Merge Identical Parents/Children, Remove all Orphans, Insert all Orphans as Children)
- Bugfixing
- Release Version 0.2
- Implement tree field editing with graphical dialog (add, remove, change tree fields)
- Implement data item field editing with graphical dialog (add, remove, change data item fields)
- Bugfixing
- Release Version 1.0
- Implement tree export to PDF, txt, and/or CSV

## Dependencies
<div id='id-dependencies'/>
[Table of Contents](#id-content)

TreeTime depends on [`Python 3`](https://www.python.org/downloads/), [`Qt5`](http://www.qt.io/download/), and [`PyQt5`](https://pypi.python.org/pypi/PyQt5).