
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

![](edit-meta-structure.png)

The entries below are tree entries. When selecting a tree entry on the right and double clicking its title on the left you can edit a tree name. You can also create and delete trees. 

Data Fields
-----------

Data fields can be renamed, created, and deleted. Note that the order in which fields are displayed in the data part of _TreeTime_ is alphabetical. To add or remove a field you can click on the respective buttons on the left.

![](edit-data-field.png)

When selecting a field, a dropdown box gives you a selection of possible types.

Tree Fields
-----------

A tree field has four properties:

1. Its name, 
2. its type,
3. whether it's hidden or visible (useful for intermediate calculation results),
4. its parameter list (list of input fields).

![](edit-tree-field.png)

You can select the type from a dropdown list. The different types are explained in the next chapter. The visibility is a single flag that can be checked or unchecked.

The input list is split into four parts:

1. Own fields. This is a list of fields that are taken from the node itself. Example: You have a data field "planned time" and a data field "spent time" and you want to create a tree field "progress", which is the ratio of spent time over planned time. The type "ratio" takes two arguments, the first being the numerator and the second the denominator. You would add the field "spent time" as first, and "planned time" as second, in the "own fields" list. Your new field, displayed for each node, will be the spent time over the planned time of that very node.
2. Child fields. This is a list of fields taken from the node's children. Example: You have a data field "spent time" and want to sum it up over all branches. You would create a tree field "Total Spent Time", select "spent time" in the "own fields" list, and "Total Spent Time" in the child fields list. That way it will display the sum of its own "spent time" value plus all the "Total Spent Time" of its children, which are in return their sums of "spent time" and children's "Total Spent Time", etc, recursively down the tree.
3. Sibling fields. This is a list of fields taken from the node's siblings. Example: You have a data field "spent time" and want to see the percentage of spent time of all siblings (for example, tasks) of the same parent (for example, the current week), and call it "Relative Effort". The "ratio-percent" field type computes the ratio _y_ from its inputs _x1_, _x2_, ... in the following way: _y_ = _x1_ / (_x2_ + _x3_ + ... + _xn_). In the "own fields" you select "spent time" (that's your _x1_), then you add another entry and also add "spent time" (that's your _x2_), then in the sibling field list you select one entry "spent time" (that's your _x3_, _x4_, ..., depending on how many siblings the node has). As a result, each node will display a field: "Relativ Effort" = "spent time" of the node / ("spent time" of the node + "spent time" of the first sibling + "spent time" of the next sibling + etc).
4. Parent fields. These are mainly useful for the "node-path" and "node-name" type fields. When using them with other types, be very careful not to create circular dependencies. With these fields, they work in the same way as the other lists, only they take values from the node's parent. For "node-path" and "node-name", select the id of a tree from the dropdown (count trees starting with 0). The tree field will then display the node's parent name in that other tree. Example: You have a tree "Tasks" and a tree "Priority". The "Priority" tree has all different priorities as branches. If you want to see the priority in the task list, create a field "node-name", and select the ID of the "Priority" tree in the "parent fields" list. You will then, in the task list, see the parent of that node in the priority list.

In general: the _x1_, _x2_, _x3_, ..., parameters are taken in order from the four lists: _x1_, _x2_, _x3_, ..., = [own field] + [child fields] + [sibling fields] + [parent fields].

Note: To avoid circular dependencies, and tell tree fields and data fields apart, it is good practice to name data fields in lower case ("spent time"), and tree fields with capitalisation ("Spent Time").
