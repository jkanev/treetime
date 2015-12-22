# Tree Time

Tired of trying to organise your data in spread sheets? Use trees instead.

TreeTime is usable as to-do list manager, test report tool, project manager, time tracker, family ancestry editor, mind-mapping tool, etc. Calculate sums and percentages from single nodes up to branches up the tree. Data comes as data items, each may have several string or number fields. Data items are organised in several trees. Each tree can have different fields (sums, percentages, string fields) showing the data item fields.

## Usage

Start the python script "treetime.py". The GUI will come up with an example project. Several data items will have loaded (a project with three tasks and two week-planning entries) and are organised in three trees. The GUI is organised in three parts:
- A button box on the left. Execute tree structure operations from here.
- An editing grid in the middle, showing the contents of the selected data item. Edit single data items here.
- A tab view with tress spanning the center-right. View and analyse your data here.

Access each single tree by clicking a tab on the main tree-view widget. Branches and children can be sorted, branches can be folded and unfolded. Data content is shown via analytic fields that are defined per tree. In the example project you will see a sum, a percentage, and text display. Planned hours and actual

Add and move single nodes and branches by using the buttons on the left (New Child, New Sibling, New Parent, Copy Node as Child, Copy Node as Sibling, Copy Node as Prent, Copy Branch as Sibling (not implemented yet), copy Children to Siblings (not implemented yet), Remove from this Tree (not implemented yet), Delete Item (not implemented yet).

Change the name of a node by selecting the node and editing the name in the top of the edit grid in the middle.
Change the parent of any node by typing a name of an existing node into the parent fields in the edit grid. The parent fields are the three lines underneath the item's name.

## Dependencies

TreeTime depends on [`Python 3`](https://www.python.org/downloads/), [`Qt5`](http://www.qt.io/download/), and [`PyQt5`](https://pypi.python.org/pypi/PyQt5).