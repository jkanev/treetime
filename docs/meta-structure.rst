
Meta Structure
==============

Principles
----------

Data -- text, numbers, URLs, time records -- are stored in data items. You can edit those in the left part of the GUI.
You can decide how many data fields your data has and of what type they are -- maybe you want a "summary" (text) and a "details" (long text) and a "planned hours" (integer) and a "spent hours" (timer).  

Calculations -- products, ratios, sums, differences -- are calculated on the fly, according to the "tree fields" in your tree.  
You can decide what mathematical operation each tree field performs, and what its input it. A mathematical operation on a node can take its input from dedicated fields of the same node ("own fields"), of the child nodes ("child fields"), of sibling nodes ("sibling fields") and of parent nodes ("parent fields").  

When hitting the tab "[Meta Structure]" or the tool button page "Edit Meta Structure" you can design the meta structure of your file: How many trees there are, what kind of data is stored in a data item, and what fields are in each tree. You can create calculations on your data and have results displayed in the tree.


Trees and the Data Item
-----------------------

The first entry in the tree on the left is the data item. You can change its name by double clicking on the title in the left. This is the default name of any new item that's added when you hit any of the "new node" / "new parent" / "new sibling" buttons. 

.. image:: edit-meta-structure.png
   :align: center

The entries below are tree entries. When selecting a tree entry on the right and double clicking its title on the left you can edit a tree name. You can also create and delete trees. 

Data Fields
-----------

Data fields can be renamed, created, and deleted. Note that the order in which fields are displayed in the data part of *TreeTime* is alphabetical. To add or remove a field you can click on the respective buttons on the left.


.. image:: edit-data-field.png
   :align: center

When selecting a field, a dropdown box gives you a selection of possible types.

Tree Fields
-----------

A tree field has four properties:

1. Its name, 
2. its type,
3. whether it's hidden or visible (useful for intermediate calculation results),
4. its parameter list (list of input fields).

.. image:: edit-tree-field.png
   :align: center

You can select the type from a dropdown list. The different types are explained in the next chapter. The visibility is a single flag that can be checked or unchecked.

The input list is split into four parts:

1. Own fields
.............

This is a list of fields that are taken from the node itself. 

→ Example: You have a data field "planned time" and a data field "spent time" and you want to create a tree field "progress", which is the ratio of spent time over planned time. The type "ratio" takes two arguments, the first being the numerator and the second the denominator. You would add the field "spent time" as first, and "planned time" as second, in the "own fields" list. Your new field, displayed for each node, will be the spent time over the planned time of that very node.

2. Child fields
...............

This is a list of fields taken from the node's children.

→ Example: You have a data field "spent time" and want to sum it up over all branches. You would create a tree field "Total Spent Time", select "spent time" in the "own fields" list, and "Total Spent Time" in the child fields list. That way it will display the sum of its own "spent time" value plus all the "Total Spent Time" of its children, which are in return their sums of "spent time" and children's "Total Spent Time", etc, recursively down the tree.

3. Sibling fields
.................

This is a list of fields taken from the node's siblings.

→ Example: You have a data field "spent time" and want to see the percentage of spent time of all siblings (for example, tasks) of the same parent (for example, the current week), and call it "Relative Effort". The "ratio-percent" field type computes the ratio *y* from its inputs *x1*, *x2*, ... in the following way: *y* = *x1* / (*x2* + *x3* + ... + *xn*). In the "own fields" you select "spent time" (that's your *x1*), then you add another entry and also add "spent time" (that's your *x2*), then in the sibling field list you select one entry "spent time" (that's your *x3*, *x4*, ..., depending on how many siblings the node has). As a result, each node will display a field: "Relativ Effort" = "spent time" of the node / ("spent time" of the node + "spent time" of the first sibling + "spent time" of the next sibling + etc).

4. Parent fields
................

These are mainly useful for the "node-path" and "node-name" type fields. When using them with other types, be very careful not to create circular dependencies. With these fields, they work in the same way as the other lists, only they take values from the node's parent. For "node-path" and "node-name", select the id of a tree from the dropdown (count trees starting with 0). The tree field will then display the node's parent name in that other tree. 

→ Example: You have a tree "Tasks" and a tree "Priority". The "Priority" tree has all different priorities as branches. If you want to see the priority in the task list, create a field "node-name", and select the ID of the "Priority" tree in the "parent fields" list. You will then, in the task list, see the parent of that node in the priority list.

In general: the *x1*, *x2*, *x3*, ..., parameters are collected in order they are mentioned from the four lists
1. own fields,
2. child fields,
3. sibling fields,
4. parent fields.

Recursion
---------

If you have a data field *x* and define a tree field *y = sum( children.x )* then the tree field *y* in each node will show the sum of all *x* of each node's children. Only the direct children, grandchildren and everything further down is ignored. In most cases this is not what you want.

Recursion is a method of calculating where a method executes itself. As if you had a piece of paper with some instructions, and one of those instructions reads "do what's on the instruction paper". Or, as someone once phrased it: "Before you can understand recursion, you must first understand recursion". A recursive method consists of two parts:

- A watertight stopping criterion
- A call to itself

When calculating values in a tree, the first part (stopping criterion) is implicit by calculating values of children ("stop when there are no more children") or parents ("stop when there are no more parents"). The second part (call to itself) is present if the tree field definition contains the tree field itself.

In the above case of the sum over a nodes' childrens' *x* this would be:  

*y = own.x + children.y*.  

The value of *y* of each node is calculated by the node's *x*, adding the node *y* of each child. The value *y* of each child is calculated by adding its own value *x* plus the value *y* of each of that child's children. And so forth.

It is important that the recursion is not defined in own-fields, because then the recursion would not stop: If *y = own.y + children.x* then to calculate that sum, *TreeTime* would calculate a node's *y* field by first collecting the value of the its *y* field, for which in turn it would collect the value of its *y* field, for which in turn it would  firstcollect the value of its *y* field... There's no stopping criterion. That's what's called a "circular dependency". To prevent that, the tree field will not be offered in its own own-fields and sibling-fields drop-down lists.

Recursion can also be defined indirectly, where *a* depends on *b*, *b* depends on *c*, and *c* depends on *a*. *TreeTime* doesn't check this (at this version, we might add a check later).

To avoid circular dependencies, and tell tree fields and data fields apart, it is good practice to name data fields in lower case ("spent time"), and tree fields with capitalisation ("Spent Time"). By then making sure all capitalised fields are only mentioned in child-fields parameter lists you will avoid infinite recursion.


Input/Output Types
------------------

Not any field can be used as input. You cannot divide two texts, you cannot mutiply a URL with a word, and you cannot concatenate two numbers.

If you select a field for your list, *TreeTime* does some type checking for you. There are three global types: "text", "numerical" and "any". Tree fields like "URL" or "Text" will accept only text input, fields like "sum" and "ratio" will only accept numerical input, fields like "set" will accept any. Non-matching input fields will not appear in the dropdown box when you select your input.
