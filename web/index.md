
<img src="https://raw.githubusercontent.com/jkanev/treetime/master/data/treetime-logo.png" alt="logo" width="64" height="64"> 

#### _TreeTime_ is a time planner, to-do list manager, mind-map editor, test report tool, project planner, family ancestry editor, and more.

_TreeTime_ is like a spreadsheet editor using linked trees instead of tables.

A tree arranges data into units and sub-units instead of using flat lists. Mathematical functions like sums, differences, or ratios can be calculated recursively.

Linked trees are distinct trees that share data between them. In _TreeTime_, any data object may be part of several trees at the same time. 

![Screenshot 3](https://raw.githubusercontent.com/jkanev/treetime/master/docs/screenshot03.png)  

## What is a Tree? ##

A "tree" is a data structure, much like a table or a list.
A tree sorts information hierarchically into boxes and sub-boxes and sub-sub-boxes.

If you want to organise your work tasks you could sort them into work packages, that are part of projects, that are part of products.
If you plan a larger project, you can sort all tasks by responsible persons, who are part of teams, that are part of departments, that are part of branches.
You can also make a time plan, where a year consists of quarters, that consist of weeks, that contain a number of tasks.
You can have an address book where you have a hierarchy of friends / colleagues / aquaintances, or you can sort knowledge about animals into kingdom / class / family / species.  
  
The nice thing about trees is that you can define mathematical functions on them.
Planned hours can be summed up per work package and project, or per person and team, or per week and month.
A mean priority can be shown per work package and project.  
  
The hierarchical categorisation can be applied to all sorts of data and will feel a lot more natural and easier to use than organising the same data in spread sheets. However, the core concept of _TreeTime_ are linked trees. 
Linked trees are separate trees that share the same data.
One piece of information (a _node_) can be in several trees at the same time, but in different place of the tree.
As a single tree is a way of sorting information, different linked trees sort the same data in different ways.

## Features ##

* Files and Saving: Start new files from templates / Load files / Save files / Text export / CSV export / Html export
* Editing trees: Create parents, siblings, children / Edit text, dates, values in nodes / Copy nodes to siblings, children, parents / Copy branches to siblings down to a pre-defined level / Remove nodes from single trees / Remove nodes from all trees
* Data analyis: Count seconds using node timers / Sum, difference, concatenation, ratio/percentage between branches, siblings or children / Auto-update of all functions up the tree on node change

## Documentation ##

[TreeTime Documentation](https://treetime-data-manager.readthedocs.io/en/latest) on readthedocs.io is constantly being kept up to date.

## Get TreeTime ##

#### Unpack-and-run Zip Files ####

- Windows, Linux: Go to [github.com/jkanev/treetime/releases/tag/2021.8](https://github.com/jkanev/treetime/releases/tag/2021.8) and download a zipped package for Windows 10, 64 bit, or for Linux 64 bit from there. Unzip it into your program directory and run _TreeTime_ or _TreeTime.exe_ from the new folder. Unzip the data package too. Add the program folder to your path.  
  
  Executable bundles have been created with pyinstaller ([www.pyinstaller.org](http://www.pyinstaller.org)).

- Mac: Mac users please use the Python code (see below). There is no executable for Mac.
(If anybody can help building an executable for other platforms I'd be delighted.)

#### Python / PyPi ####

1. If you don't have it yet, install python3
2. Install PyQt5 -- on an elevated command prompt (Windows), or on the standard command line (Mac, Linux), type:  
    `pip install pyqt5`
3. Install _TreeTime_ -- on an elevated command prompt (Windows), or on the standard command line (Mac, Linux), type:
    `pip install treetime`

#### Python / Source Code ####

1. If you don't have it yet, install python3
2. Install PyQt5 -- on an elevated command prompt (Windows), or on the standard command line (Mac, Linux), type: `pip install pyqt5`
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

![Screenshot 1](https://raw.githubusercontent.com/jkanev/treetime/master/docs/screenshot01.png)  
![Screenshot 2](https://raw.githubusercontent.com/jkanev/treetime/master/docs/screenshot02.png)  
![Screenshot 4](https://raw.githubusercontent.com/jkanev/treetime/master/docs/screenshot04.png)  

