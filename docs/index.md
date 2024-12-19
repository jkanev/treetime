
<img src="https://raw.githubusercontent.com/jkanev/treetime/master/data/treetime-logo.png" alt="logo" width="96px" height="96px" style="position: relative; float: left; margin: 0 2em 1em 0;"> 

#### _TreeTime_ is a time planner, to-do list manager, mind-map editor, test report tool, project planner, family ancestry editor, and more. ####

_TreeTime_ is like a spreadsheet editor using linked trees instead of tables.

A tree arranges data into units and sub-units instead of using flat lists. Mathematical functions like sums, differences, or ratios can be calculated recursively.

Linked trees are distinct trees that share data between them. In _TreeTime_, any data object may be part of several trees at the same time. 

<img src="https://raw.githubusercontent.com/jkanev/treetime/master/docs/screenshot03.png" width="100%">

## What is a Tree? ##

A "tree" is a data structure, much like a table or a list.
A tree sorts information hierarchically into boxes and sub-boxes and sub-sub-boxes.
You could make a time plan that divides a year into quarters, that consist of weeks, each containing a number of activities.
You can have an address book where you have a hierarchy of friends / colleagues / aquaintances, or you can sort knowledge about animals into kingdom / class / family / species.  

The core concept of _TreeTime_ are *linked* trees. 
Linked trees are different trees sharing the same data.
One piece of information (a task, note, person, week, generally a _node_) can be in several trees at the same time, but in different place of the tree.

If you want to organise your work tasks you could sort them into weekly activities, that are part of work packages, that are part of projects.
At the same time you can organise those tasks by responsible persons, who are part of teams, that are part of departments, that are part of branches. In _TreeTime_ you can easily switch between the two. Selecting a node selects and highlights it in all trees.
  
The nice thing about trees is that you can define mathematical functions on them.
Planned hours can be summed up per work package and project, or per person and team, or per week and month.
A mean priority can be shown per work package and project.  
  
## Features ##

* Files and Saving: Start new files from templates / Load files / Save files / Text export / CSV export / Html export / Export single branches or entire trees
* Editing trees: Create parents, siblings, children / Edit text, dates, values in nodes / Copy nodes to siblings, children, parents / Copy branches to siblings down to a pre-defined level / Remove nodes from single trees / Remove nodes from all trees / Remove branches from single trees / Remove branches recursively from all trees
* Data analyis: Measure time using node timers in nodes / Add total time up branches / Calculate sums, differences, ratios and percentages between branches, siblings or children / Concatenate text of children or siblings / Auto-update of all functions up the tree on node change

## Documentation ##

[TreeTime Documentation](https://treetime-data-manager.readthedocs.io/en/latest) on readthedocs.io is constantly being kept up to date.

## Get TreeTime ##

#### Unpack-and-run Zip Files ####

- Windows, Linux: Go to [github.com/jkanev/treetime/releases/tag/2024.4](https://github.com/jkanev/treetime/releases/tag/2024.4) and download a zipped package for Windows 10, 64 bit, or for Linux 64 bit from there. Unzip it into your program directory and run _TreeTime_ or _TreeTime.exe_ from the new folder. Unzip the data package too. Add the program folder to your path.  
  
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

## TreeTime Images ##

Right-click and select _Open in new tab_ to see full-scale screenshots  

<img src="https://raw.githubusercontent.com/jkanev/treetime/master/docs/screenshot01.png" width="32%">
<img src="https://raw.githubusercontent.com/jkanev/treetime/master/docs/screenshot02.png" width="32%">
<img src="https://raw.githubusercontent.com/jkanev/treetime/master/docs/screenshot04.png" width="32%">

## Bugs and Problems ##

A list of bugs can be found [here](https://github.com/jkanev/treetime/issues).

## Licensing and Payment ##

_TreeTime_ is free, both in the _beer_ and in the _freedom_ sense. The source code is published under a GPL 3.0 license. If you want to contribute code or join the project, you're highly welcome.

