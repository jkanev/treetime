
<img src="https://raw.githubusercontent.com/jkanev/treetime/master/data/treetime-logo-small.png" alt="logo" style="position: relative; float: left; margin: 0 2em 1em 0;"/>

#### _TreeTime_ is a time planner, to-do list manager, mind-map editor, test report tool, project planner, family ancestry editor, and more. 

_TreeTime_ is like a spreadsheet editor on steroids, it is like a mini-database, or an extremely fancy list editor. _TreeTime_ uses trees. Several linked trees.

A tree arranges data into units and sub-units instead of using flat lists. Mathematical functions like sums, differences, or ratios can be calculated recursively. Multiple linked trees can share data between them. In _TreeTime_, any data object may be part of several trees at the same time. 

<a href="https://raw.githubusercontent.com/jkanev/treetime/master/docs/screenshot03.png" style="display: block; position: relative; float: left; max-width: content; margin: 2em;">
    <img src="https://raw.githubusercontent.com/jkanev/treetime/master/docs/screenshot03.png" style="width: 500px;"/>
</a>

With _TreeTime_ you organise your data, your notes, your plan for an article, some domain knowledge, your todo list, naturally and efficently. Good bye spread sheets and lists, welcome trees.

## What is a Tree? 

A "tree" is a way to sort information hierarchically into boxes and sub-boxes and sub-sub-boxes.
You could make a time plan that divides a year into quarters, that consist of weeks, each containing a number of activities.
You can have an address book where you have a hierarchy of friends / colleagues / aquaintances, or you can sort knowledge about animals into kingdom / class / family / species.__

The core concept of _TreeTime_ are *linked* trees. 
One piece of information (a task, note, person, week, generally a _node_) can be in several trees at the same time, but in each tree in different place.

If you want to organise your work tasks you could sort them into weekly activities, that are part of work packages, that are part of projects. That would be one tree.
At the same time you can organise those tasks by responsible persons, who are part of teams, that are part of departments, that are part of branches. That would be another tree. In _TreeTime_ you can easily switch between the two. Selecting a node selects and highlights it in all trees.
  
_TreeTime_ supports calculations on branches and trees.
Planned hours can be summed up per work package and then project, or per person and team, or per week and month.
A mean priority can be shown per work package and project. The relative amount of hours, in percent, can be shown per package compared to all other packages. And more.  
  
## Features

<a href="https://raw.githubusercontent.com/jkanev/treetime/master/docs/screenshot01.png" style="display: block; position: relative; float: left; max-width: content; margin: 2em;">
    <img src="https://raw.githubusercontent.com/jkanev/treetime/master/docs/screenshot01.png" style="width: 300px;"/>
</a>

### Files and Saving
* Start new files from templates
* Load files
* No need for saving -- the current file is saved continuously all the time
* Save under a different name

### Data Export
#### What can you export?
* Export three different flavours of Html (tiles, lists, document)
* Export pure text (ascii/unicode) with line graphics
* Export PNG images in three different flavours (top-down tree, circular graph, spread-out graph)
* Export SVG images (with clickable links) in three different flavours (top-down tree, circular graph, spread-out graph)
* Export CSV for import into spread sheets

#### Where can you export to?
* Export to file
* Export to clipboard
* Export to web server -- visible either on your local machine, or in your network, or shared across the internet (needs port sharing in your router)

#### How can you export?
* Export once -- for exporting a file
* Export continuously -- ideal for sharing notes during a meeting

### Edit Data

* Create parents, siblings, children
* Edit text, dates, values in nodes
* Copy nodes to siblings, children, parents
* Copy branches to siblings down to a pre-defined level
* Remove nodes from single trees
* Remove nodes from all trees
* Remove branches from single trees
* Remove branches recursively from all trees

### Analyse Data

* Measure time using node timers in nodes
* Add total time up branches
* Calculate sums, differences, ratios and percentages between branches, siblings or children
* Concatenate text of children or siblings
* Build sets of items, and sets of sets up the tree
* Auto-update of all functions up the tree on node change

<a href="https://raw.githubusercontent.com/jkanev/treetime/master/docs/screenshot02.png" style="display: block; position: relative; float: left; max-width: content; margin: 2em;">
    <img src="https://raw.githubusercontent.com/jkanev/treetime/master/docs/screenshot02.png" style="width: 300px;"/>
</a>

<a href="https://raw.githubusercontent.com/jkanev/treetime/master/docs/screenshot04.png" style="display: block; position: relative; float: left; max-width: content; margin: 2em;">
    <img src="https://raw.githubusercontent.com/jkanev/treetime/master/docs/screenshot04.png" style="width: 300px;"/>
</a>

## Documentation ##

[TreeTime Documentation](https://treetime-data-manager.readthedocs.io/en/latest) on readthedocs.io is constantly being kept up to date.

## Get TreeTime ##

#### Unpack-and-run Zip Files ####

- Windows, Linux: Go to [codeberg.org/jkanev/treetime/releases/tag/2025.3](https://codeberg.org/jkanev/treetime/releases/tag/2025.3) and download a zipped package for Windows 10, 64 bit, or for Linux 64 bit from there. Unzip it into your program directory and run _TreeTime_ or _TreeTime.exe_ from the new folder. Unzip the data package too. Add the program folder to your path.  
  
  Executable bundles have been created with pyinstaller ([www.pyinstaller.org](http://www.pyinstaller.org)).

- Mac: Mac users please use the Python code (see below). There is no executable for Mac.
(If anybody can help building an executable for other platforms I'd be delighted.)

#### Python / PyPi ####

1. Install python3
2. Install PyQt6 -- on an elevated command prompt (Windows), or on the standard command line (Mac, Linux), type:
    `pip install PyQt6`
3. Install _TreeTime_ -- on an elevated command prompt (Windows), or on the standard command line (Mac, Linux), type:
    `pip install treetime`

#### Python / Source Code ####

1. Install python3
2. Install PyQt6 -- on an elevated command prompt (Windows), or on the standard command line (Mac, Linux), type: `pip install PyQt6`
3. Download this project from GitHub as a zip file (https://github.com/jkanev/treetime/archive/master.zip) and unzip
4. Install _TreeTime_: in the command line, cd into the main directory, then type:
   - Linux:  
       `python3 setup.py build`  
       `sudo python3 setup.py install`  
   - Windows:  
       `py setup.py build`  
       `py setup.py install`  

#### Run TreeTime ####

- Windows: Hit the Windows key and type "TreeTime", then click the "run command treetime" that comes up.
- Linux, Mac: On the command line, type "TreeTime". You can also start this any other way your operating system supports. Plus, there's a .desktop file (for KDE and Gnome) in the data directory to create desktop or menu link.

## Bugs and Problems ##

A list of bugs can be found [here](https://github.com/jkanev/treetime/issues).

## Licensing and Payment ##

_TreeTime_ is free, both in the _beer_ and in the _freedom_ sense. The source code is published under a GPL 3.0 license. If you want to contribute code or join the project, you're highly welcome.

