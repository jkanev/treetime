#  <img src="https://raw.githubusercontent.com/jkanev/treetime/master/data/treetime-logo.png" alt="logo" width="64" height="64">&nbsp; &nbsp; &nbsp; &nbsp;Tree Time


TreeTime is a general data oranisation and data management tool. You can use it to plan your time, as a to-do list
manager, test report tool, project manager, family ancestry editor, mind-mapping tool, and similar. In TreeTime, data
is not organised in lists or spreadsheets, but in trees. A tree is a hierarchical structure that lets you systemise
your data into units and sub-units. Trees are a far more natural concept than lists. TreeTime uses several trees to categorise data at the same time. In addition,
you can use functions (calculate sums, ratios and means) recursively up and down the trees.

<div id='id-contents'/>

### Table of Contents  ###

- [Concept](#id-concept)
- [Installation](#id-installation)
- [Usage](#id-usage)
- [Road-Map](#id-roadmap)
- [Dependencies](#id-dependencies)


<div id='id-concept'/>

## Concept ##
[Table of Contents](#id-contents)

### What is a Tree? ###

A "tree" is a data structure, much like a table or a list. Using a tree you can naturally package your information into
boxes and sub-boxes and sub-sub-boxes. Some examples:

If you want to organise your work tasks you could sort them into work packages, that are part of projects, that
are part of products. Alternatively, if you plan a larger project, you can sort all tasks by responsible persons, who
are part of teams, that are part of departments, that are part of branches. You can also make a time plan, where a 
year consists of quarters, that consist of weeks, that contain a number of tasks. You can have an address book where you
have a hierarchy of friends / colleagues / aquaintances, or you can sort knowledge about animals into kingdom / class /
species.

The nice thing about trees is that you can define mathematical functions on them. The planned hours can be added up,
the task priority can be used to calculate mean priority per work package and project, work hours can be calculated
per person and team.

The concept of hierarchical categorisation can be applied to all sorts of data and will feel a lot more natural and
easier to use than organising the same data in spread sheets. 

### How do I use TreeTime? ###

The core concept of TreeTime is the idea to use severa different trees on the same data items. Different trees are in
different tabs of the tree. If you, for instance, organise information about animals, you can have kingdom / class / species in one
tab, habitat (continent / country / area) in another, and switch between them. If you organise tasks, you can switch
between a year/quarter/week/day breakdown, a company/department/team/person tree, or a product/project/package/task
overview.

In TreeTime, the structure of your data (whether you store priority, hours, and a description for a task, or expected
life span, habitat and number of legs for an animal), the trees themselves, the calculated values in the trees are
completely user defined. 

<div id='id-installation'/>

##  Installation  ##
[Table of Contents](#id-installation)

### Using pre-compiled Binaries ###

Go to [github.com/jkanev/treetime/releases/tag/v0.0](https://github.com/jkanev/treetime/releases/tag/v0.0) and download a zipped package for Windows 10, 64 bit, or for Linux 64 bit from there. Unzip it into your program directroy and run TreeTime.exe from the new folder.
Executable bundles have been created with pyinstaller ([www.pyinstaller.org](http://www.pyinstaller.org)).

Mac users please use the Python code (see below). There is no executable for Mac.
(If anybody can help building an executable for other platforms I'd be delighted.)

### Using pip ###

On the command line, first type "pip install PyQt5", then type "pip install TreeTime" (or "pip3 install TreeTime",
depending on your installation).

### Using script code with Python ###

1. If you don't have it yet, install python3
2. If you don't have it yet, install PyQt5 (use pip on the command line)
3. Download this project from GitHub as a zip file (https://github.com/jkanev/treetime/archive/master.zip) and unzip
4. Install: in the command line, cd into the main directory, then type:
   - Linux:
      - python3 setup.py build
      - sudo python3 setup.py install
   - Windows:
      - py setup.py build
      - py setup.py install
5. You can now execute the software normally, 

<div id='id-usage'/>

##  Usage  ##
[Table of Contents](#id-contents)

Start the software by typing "python3 -m treetime" or using your OSes main menu (see 'Execute' from the previous
section). In the main dialog, go to "File" / "New from Template", select "Simple-Task-List.trt" and in the next dialog give a file name for the new file.
The GUI is organised in three parts:
- A button box on the left. Execute tree structure operations from here.
- An editing grid in the middle, showing the contents of the selected data item. Edit single data items here.
- A tab view with tress spanning the center-right. View and analyse your data here.

![Screenshot 1](doc/screenshot01.png)

Access each single tree by clicking a tab on the main tree-view widget. Branches and children can be sorted, branches
can be folded and unfolded. Data content is shown via analytic fields that are defined per tree. In the example project
you will see a sum, a percentage, and text display. 

![Screenshot 2](doc/screenshot02.png)

Add and move single nodes and branches by using the buttons on the left (New Child, New Sibling, New Parent, Copy Node
as Child, Copy Node as Sibling, Copy Node as Parent, Copy Branch as Sibling, copy Children to Siblings, Remove from this Tree (this can also be done from the data item's parent menus), Delete Item. Change the name of a node by selecting the node and editing the name in the top of the edit grid in the middle.

Change the parent of any node by typing a name of an existing node into the parent fields in the edit grid. The parent
menus (for selecting or changing a node's parent) are the lines underneath the item's name.

![Screenshot 2](doc/screenshot03.png)

TreeTime lets you select different themes and will try to use the default colours that are defined with your operating
system.

![Screenshot 2](doc/screenshot04.png)

<div id='id-roadmap'/>

##  Road-Map  ##
[Table of Contents](#id-contents)

I deliberately didn't give any time estimates for this. I'm using the software myself to organise my own data, so I'm interested in keeping this going. Nevertheless I cannot promise any specific release dates. If you have any suggestions or would like me to implement some feature sooner than I suggested here, please just drop me an email.
- Done February 2016: Implement selection (the same item gets selected in all trees, changing a tab shows the same item)
- Done March 2016: Implement remaining local functionality (Copy Branch as Sibling, Copy Children to Siblings, Remove from this Tree, Delete Item)
- Done August 2016: Created installable python package
- Done May 2017: Implemented new field type _text_
- Done June 2017: Create deployable packages for Linux and Windows
- Done June 2017: Made pre-release v0.0 available
- Done October 2017: Implemented new field type _node-path_, re-wrote the way nodes move to new parents
- Done November 2017: Uploaded package to pypi.python.org, TreeTime can now be installed using pip
- Done October 2018: Re-implemented the parent selection mechanism. The old cascaded menus have been replaced with single drop down lists.
- Done October 2018: Re-furbished the GUI and removed a couple of bugs. Slighty changed the data file format. Tested pyqtdeploy for deployment instead of pyinstaller.
- Running: Bugfixing
- Running: Write documentation on readthedocs.io and create example data files
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

##  Dependencies  ##
[Table of Contents](#id-contents)

TreeTime depends on [`Python 3`](https://www.python.org/downloads/), [`Qt5`](http://www.qt.io/download/), and [`PyQt5`](https://pypi.python.org/pypi/PyQt5).