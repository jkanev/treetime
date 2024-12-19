History and Road Map
====================

Past
----

2015
^^^^

* November: First implementation, simple data types, simple GUI

2016
^^^^

* February: Implemented selection (the same item gets selected in all trees, changing a tab shows the same item)
* March: Implemented remaining local functionality (Copy Branch as Sibling, Copy Children to Siblings, Remove from this Tree, Delete Item)
* August: Created installable python package

2017
^^^^

* May: Implemented new field type *text*
* June: Create deployable packages for Linux and Windows
* June: Made **pre-release v0.0** available
* October: Implemented new field type *node-path*, re-wrote the way nodes move to new parents
* November: Uploaded package to pypi.python.org, *TreeTime* can now be installed using pip

2018
^^^^

* October: Re-implemented the parent selection mechanism. The old cascaded menus have been replaced with single drop down lists.
* October: Re-furbished the GUI and removed a couple of bugs. Slighty changed the data file format. Implemented theme selection. Tested pyqtdeploy for deployment instead of pyinstaller. Updated the description.
* November: Released **version 2018-10**

2019
^^^^

* January: Implemented new field type "URL"

2020
^^^^

* June: Fixed problem with protected cells (typing into a cell without data could cause a crash), and fixed file selection dialog (now only offers .trt files).
* July: Implemented text export - single branches or complete trees can now be exported to txt files.
* August: Implemented time counters - nodes can record the time using a special field of type "timer" (experimental). GUI buttons can start and stop the stopwatch function.
* September: Added move-to-top-level option for first level nodes
* October: Added a dark and a light palette for GUI colours, selectable in addition to the theme selection.
* November: Fixed too slow editing in text fields when tree files are big (>1.5 MB).

2021
^^^^

* January: Released **version 2021.01**.
* January: Bugfixing (timer crash)
* February: Released **version 2021.2**.
* March: New functions "Delete node" and "Remove node from tree" now move descendants one level up.
  "Remove branch" removes the respective branch in all trees, "Delete branch" deletes a
  branch, all child branches and inter-connections in all trees.
* March: If a file with running timers is saved, those timers will be running when the file is loaded.
* March: Added tooltips for main buttons
* March: Implemented HTML export of branches and complete trees
* March: Added auto-delete for orphans
* March: Released **version 2021.3**
* April: Added file option
* April: Implemented four-column layout and rainbow colours for html export
* April: Released **version 2021.4**
* May: Improvement to html and txt export (changed colours, headings have no different sizes)
* May: On export of both html and txt, user can now decide how many tree levels (depth) should be exported.
* May: Released **version 2021.5**
* July: Fixed broken application logo
* July: Implemented CSV export
* August: Released **version 2021.8**
* September: Added new export option "Text to Clipboard"
* November: Added new export option "Html (List) to File"
* December: Added two primitive template files (a text-only single tree and dual tree mindmap)
* December: Released **version 2021.9**

2022
^^^^

* March: Fixed crash bug on non-export
* March 2022: Improved sorting and grouping in html export, changed to five columns
* June 2022: Added a tutorial file
* June 2022: Added first-use dialog when no file is loaded, instead of the file-open dialog
* June 2022: Released **version 2022.1**

2023
^^^^

* February 2023: Added new tree field types "concatenation" and "set".
* February 2023: Implemented adjustable width for the data item and the tree table main view.
* February 2023: Release **version 2023.1**
* April 2023: Removed deprecated tree field ("concatenation"), fixed missing logo.
* May 2023: Ported to PyQt 6.0
* May 2023: Implemented auto-adjusting name column
* June 2023: Created new default theme "Organic", a mix between Fusion and Breeze
* June 2023: Implemented display of tree field definitions and of data field definitions
* July 2023: Release **version 2023.2**
* October 2023: Fixed crash when exporting text to clipboard.

2024
^^^^

* January 2024: Changed node symbol to small circle in text eport (after asking users on social media).
* February 2024: Implemented min, max, min-string, max-string fields.
* March 2024: Implemented longtext data field.
* April 2024: Extended documentation on readthedocs.io. Release **version 2024.1**
* April 2024: Restructured export area, added name-only export. Made all export options (full tree / branch / node with contect) (all fields / names only) available for all file formats and for both file and clipboard export.
* April 2024: Release **version 2024.2**
* Done March 2024: Implemented changeable font size (zoom) of data display
* Done May 2024:  Implemented continuous text and html export
* July 2024: Release **version 2024.3**
* October 2024: Fixed crash bug and improved html output
* November 2024: Improved colours in html output, implemented continuous change to export for textfields even if the focus stays in, fixed broken layout of html export
* December 2024: Changed colours in html output (again?), increased font size
* December 2024: Release **version 2024.4**

Present
-------

* Bugfixing
* Extend documentation on readthedocs.io
* Add more fields
* Add more examples and more template data files
* Structure editing/viewing in extra tab (editing the structure, number and definitions and trees and tree fields and data fields)

Future
------

Near Future
^^^^^^^^^^^

* Implement search function

Mid Future
^^^^^^^^^^

* Implement global functions (Linearise Tree, Level-Swap, Merge identical Siblings, Merge Identical Parents/Children, Remove all Orphans, Insert all Orphans as Children)

Far Future
^^^^^^^^^^

* Implement safe usage by multiple simultaneous users
* Implement a database backend instead of text file storage
* A whole lot of other fancy things that will probably never get done

