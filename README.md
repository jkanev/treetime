#  <img src="https://raw.githubusercontent.com/jkanev/treetime/master/data/treetime-logo.png" alt="logo" width="64" height="64">&nbsp; &nbsp; &nbsp; &nbsp;TreeTime


Note: If your looking for the phylogenetics software of the same name, you can find it here: [github.com/neherlab/treetime](https://github.com/neherlab/treetime).

_TreeTime_ is a general data organisation, management and analysis tool using linked trees instead of flat lists of tables.
A tree is a hierarchical structure that arranges your data into units and sub-units.
Mathematical functions (sum, difference, mean, ratio) can be calculated recursively.
Linked trees are distinct trees that share data between them.
In _TreeTime_, a data object is part of several trees at the same time.
_TreeTime_ is a time planner, a to-do list manager, a test report tool, a project planner, a family ancestry editor, a mind-mapping tool, and similar.

<div id='id-contents'/>

### Table of Contents  ###

- [Concept](#id-concept)
- [Basic Use](#id-usage)
- [Data Files](#id-file-syntax)
- [Installation](#id-installation)
- [Road-Map](#id-roadmap)
- [Dependencies](#id-dependencies)


<div id='id-concept'/>

## Concept ##
[Table of Contents](#id-contents)

### What is a Tree? ###

A "tree" is a data structure, much like a table or a list.
A tree sorts information hierarchically into boxes and sub-boxes and sub-sub-boxes.

If you want to organise your work tasks you could sort them into work packages, that are part of projects, that are part of products.
If you plan a larger project, you can sort all tasks by responsible persons, who are part of teams, that are part of departments, that are part of branches.
You can also make a time plan, where a year consists of quarters, that consist of weeks, that contain a number of tasks.
You can have an address book where you have a hierarchy of friends / colleagues / aquaintances, or you can sort knowledge about animals into kingdom / class / family / species.  
  
The nice thing about trees is that you can define mathematical functions on them.
Planned hours can be summed up per work package and project, or per person and team, or per week and month.
A mean priority can be shown per work package and project.  
  
The concept of hierarchical categorisation can be applied to all sorts of data and will feel a lot more natural and easier to use than organising the same data in spread sheets.  

### What are linked Trees? ### 

The core concept of _TreeTime_ are linked trees.
Linked trees are separate trees that share the same data.
One piece of information (a _node_) can be in several trees at the same time, but in different place of the tree.
As a single tree is a way of sorting information, different linked trees sort the same data in different ways.  
![Tree 1](https://raw.githubusercontent.com/jkanev/treetime/master/docs/linked-trees.png)  
In _Tree 1_, Node _E_ is right at the bottom, as a child of _B_ and a grandchild of _A_. In _Tree 2_ it is a child of _D_.

In _TreeTime_, a _node_ or _item_ can hold different information like text, numbers, dates, internet links.
These are saved in the _item's_ _fields_.

Here we have a field we call "value". Each node in all trees has a value field that can hold a number (like a cell in a spread sheet).
The node A has the value=1, B=2, etc.
In addition we have a field we call "Sum".
Its content is calculated automatically, summing up the item's own value plus the values of all children.
In _TreeTime_, looking at item _E_ and _Tree 1_ this looks like this:  
![Tree 2](https://raw.githubusercontent.com/jkanev/treetime/master/docs/abcde01.png)  
Clicking on the other tab shows the second tree while the same items stays selected:  
![Tree 3](https://raw.githubusercontent.com/jkanev/treetime/master/docs/abcde02.png)  
Note how the values are summed up the branches.
Apart from sums, _TreeTime_ also offers means, ratios, or differences, using different combinations of parent, child, or sibling fields.  
  
Linked trees are a natural and powerful way to structure data.
If you, for instance, organise information about animals, you might want to see the animal's taxonomy (kingdom/class/family/species), but also their habitat (continent/country/area), and switch between both views.
If you organise tasks, you could switch between a year/quarter/week/day breakdown, a company/department/team/person tree, and a product/project/package/task overview.  
  
In _TreeTime_, the structure of your data (whether you store priority, hours, and a description for a task, or expected life span, habitat and number of legs for an animal), the trees themselves, and the calculated values within the trees are completely user defined. Data is stored in text files, changes are saved on the fly, and when opening _TreeTime_, the software is automatically connected to the last used file.  
  
<div id='id-usage'/>

##  Basic Use  ##
[Table of Contents](#id-contents)

Start the software (see 'Execute' from the section [Installation](#id-installation)). In the main dialog, go to "File" / "New from Template", select "Simple-Task-List.trt" and in the next dialog give a file name for the new file. An example file with a simple project task list structure will open.  
  
The GUI consists of three parts:  
- A button box on the left. Execute tree structure operations from here.
- An editing grid in the middle, showing the contents of the selected data item. Edit single data items here.
- A tab view with tress spanning the center-right. View and analyse your data here.
  
![Screenshot 1](https://raw.githubusercontent.com/jkanev/treetime/master/docs/screenshot01.png)  
Access each single tree by clicking a tab on the main tree-view widget (the picture above shows the tree _Time Plan_, the picture below the tree _Projects_).  
![Screenshot 2](https://raw.githubusercontent.com/jkanev/treetime/master/docs/screenshot02.png)  
Branches and children can be sorted, branches can be folded and unfolded. Data content is shown via analytic fields that are defined per tree. In the example project you will see a sum, a percentage, and text display.  
  
Add, move and remove single nodes and complete branches by using the buttons on the left. Change the name of a node by selecting the node and editing the name in the top of the edit grid in the middle. Change all other values (numbers or text) by clicking into the field and start typing.  
  
The parents of an item are listed underneath the item name. Each tree has a separate line. Change the position of a node within a tree by clicking on any of the parent buttons.  
![Screenshot 3](https://raw.githubusercontent.com/jkanev/treetime/master/docs/screenshot03.png)  
In this example a new node in the tree _Time Plan_ has just been created, and is now added to the tree _Projects_.  
  
_TreeTime_ lets you select different themes and will try to use the default colours that are defined with your operating system.  
  
![Screenshot 4](https://raw.githubusercontent.com/jkanev/treetime/master/docs/screenshot04.png)  

<dif id='id-file-syntax'/>

## Data Files ##

_TreeTime_'s data is stored in ._trt_ files. These are plain editable text files. Please have a look at the file _Simple-Task-List.trt_ to understand the syntax. A detailed description will follow later. (Sorry...)

<div id='id-installation'/>

##  Installation  ##
[Table of Contents](#id-installation)

### Using pre-compiled Binaries ###

- Windows, Linux: Go to [github.com/jkanev/treetime/releases/tag/2024.3](https://github.com/jkanev/treetime/releases/tag/2024.3) and download a zipped package for Windows 10, 64 bit, or for Linux 64 bit from there. Unzip it into your program directory and run _TreeTime_ or _TreeTime.exe_ from the new folder. Unzip the data package too. Add the program folder to your path.  
  
  Executable bundles have been created with pyinstaller ([www.pyinstaller.org](http://www.pyinstaller.org)).

- Mac: Mac users please use the Python code (see below). There is no executable for Mac.
(If anybody can help building an executable for other platforms I'd be delighted.)

### Using a PyPi package in Python ###

1. If you don't have it yet, install python3
2. Install PyQt6 -- on an elevated command prompt (Windows), or on the standard command line (Mac, Linux), type:  
    `pip install PyQt6`
3. Install _TreeTime_ -- on an elevated command prompt (Windows), or on the standard command line (Mac, Linux), type:
    `pip install treetime`

### Using script code with Python ###

1. If you don't have it yet, install python3
2. Install PyQt6 -- on an elevated command prompt (Windows), or on the standard command line (Mac, Linux), type: `pip install PyQt6`
3. Download this project from GitHub as a zip file (https://github.com/jkanev/treetime/archive/master.zip) and unzip
4. Install _TreeTime_: in the command line, cd into the main directory, then type:
   - Linux:  
       `python3 setup.py build`  
       `python3 setup.py install --user`  
   - Windows:  
       `py setup.py build`  
       `py setup.py install`  

### Execute ###

- Windows: Hit the Windows key and type "TreeTime", then click the "run command treetime" that comes up.
- Linux, Mac: On the command line, type "TreeTime". You can also start this any other way your operating system supports. Plus, there's a .desktop file (for KDE and Gnome) in the data directory to create desktop or menu link.


<div id='id-roadmap'/>

##  Road-Map  ##
[Table of Contents](#id-contents)

I deliberately didn't give any time estimates for this. I'm using the software myself to organise my own data, so I'm interested in keeping this going. Nevertheless I cannot promise any specific release dates. If you have any suggestions or would like me to implement some feature sooner than I suggested here, please just drop me an email.

Past
- Done February 2016: Implemented selection (the same item gets selected in all trees, changing a tab shows the same item)
- Done March 2016: Implemented remaining local functionality (Copy Branch as Sibling, Copy Children to Siblings, Remove from this Tree, Delete Item)
- Done August 2016: Created installable python package
- Done May 2017: Implemented new field type _text_
- Done June 2017: Create deployable packages for Linux and Windows
- Done June 2017: Made pre-release v0.0 available
- Done October 2017: Implemented new field type _node-path_, re-wrote the way nodes move to new parents
- Done November 2017: Uploaded package to pypi.python.org, _TreeTime_ can now be installed using pip
- Done October 2018: Re-implemented the parent selection mechanism. The old cascaded menus have been replaced with single drop down lists.
- Done October 2018: Re-furbished the GUI and removed a couple of bugs. Slighty changed the data file format. Implemented theme selection. Tested pyqtdeploy for deployment instead of pyinstaller. Updated the description.
- Done November 2018: Released version 2018-10
- Done January 2019: Implemented new field type "URL"
- Done June 2020: Fixed problem with protected cells (typing into a cell without data could cause a crash), and fixed file selection dialog (now only offers *.trt files).
- Done July 2020: Implemented text export - single branches or complete trees can now be exported to txt files.
- Done August 2020: Implemented time counters - nodes can record the time using a special field of type "timer" (experimental). GUI buttons can start and stop the stopwatch function.
- Done September 2020: Added move-to-top-level option for first level nodes
- Done October 2020: Added a dark and a light palette for GUI colours, selectable in addition to the theme selection.
- Done November 2020: Fixed too slow editing in text fields when tree files are big (>1.5 MB).
- Done January 2021: Released version 2021.01.
- Done January 2021: Bugfixing (timer crash)
- Done February 2021: Released version 2021.2.
- Done March 2021: New functions "Delete node" and "Remove node from tree" now move descendants one level up.
  "Remove branch" removes the respective branch in all trees. "Delete branch" completely deletes a
  branch, plus all child branches and inter-connections in all trees.
- Done March 2021: If a file with running timers is saved, those timers will be running when the file is loaded.
- Done March 2021: Added tooltips for main buttons
- Done March 2021: Implemented HTML export of branches and complete trees
- Done March 2021: Added auto-delete for orphans
- Done March 2021: Released version 2021.3
- Done April 2021: Added file option
- Done April 2021: Added four-column export for html and rainbow colours
- Done April 2021: Released version 2021.4
- Done May 2021: Improved HTML layout
- Done May 2021: Implemented customisable level export for html and text export
- Done May 2021: Released version 2021.5
- Done July 2021: Fixed broken application logo
- Done July 2021: Implemented CSV export
- Done August 2021: Released version 2021.8
- Done September 2021: Added new export option "Text to Clipboard"
- Done November 2021: Added new export option "Html (List) to File"
- Done December 2021: Added two primitive template files (a text-only single tree and dual tree mindmap)
- Done December 2021: Released version 2021.9
- Done March 2022: Fixed crash bug on non-export
- Done March 2022: Improved sorting and grouping in html export, changed to five columns.
- Done June 2022: Added a tutorial file.
- Done June 2022: Added first-use dialog when no file is loaded, instead of the file-open dialog.
- Done June 2022: Release 2022.1
- Done February 2023: Added new tree field types "concatenation" and "set".
- Done February 2023: Implemented adjustable width for the data item and the tree table main view.
- Done February 2023: Release 2023.1
* Done April 2023: Removed deprecated tree field ("concatenation"), fixed missing logo.
* Done May 2023: Ported to PyQt 6.0
* Done May 2023: Implemented auto-adjusting name column
* Done June 2023: Created new default theme "Organic", a mix between Fusion and Breeze
* Done June 2023: Implemented display of tree field definitions and of data field definitions
* Done July 2023: Release **version 2023.2**
* Done October 2023: Bugfix: crash when exporting text to clipboard.
* Done January 2024: Changed node symbol to small circle in text eport (after asking users on social media).
* Done February 2024: Implemented min, max, min-string, max-string fields.
* Done March 2024: Implemented longtext data field.
* Done April 2024: Extended documentation on readthedocs.io. Release **version 2024.1**
* Done April 2024: Restructured export area, added name-only export. Made all export options (full tree / branch / node with contect) (all fields / names only) available for all file formats and for both file and clipboard export.
* Done April 2024: Release **version 2024.2**
* Done March 2024: Implemented changeable font size (zoom) of data display
* Done May 2024:  Implemented continuous text and html export
* Done July 2024: Release **version 2024.3**

Present
- Running: Bugfixing
- Running: Extend documentation on readthedocs.io
- Running: 
- Running: Add more examples and more template data files
- Running: Structure editing/viewing in extra tab (editing the structure, number and definitions and trees and tree fields and data fields)

  
Future
- Near Future: Implement search function
- Mid Future: Implement global functions (Linearise Tree, Level-Swap, Merge identical Siblings, Merge Identical Parents/Children, Remove all Orphans, Insert all Orphans as Children)
- Far Future: Implement safe usage by multiple simultaneous users
- Far Future: Implement a database backend instead of text file storage
- Far Future: Implement a web server
- Far Future: A whole lot of other fancy things that will probably never get done

<div id='id-dependencies'/>

##  Dependencies  ##
[Table of Contents](#id-contents)

_TreeTime_ depends on [`Python 3`](https://www.python.org/downloads/), [`Qt6`](http://www.qt.io/download/), and [`PyQt6`](https://pypi.python.org/pypi/PyQt6).
