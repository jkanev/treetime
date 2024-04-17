
Data Format
===========

Global Structure
^^^^^^^^^^^^^^^^

TreeTime data files are plain text (Unicode/UTF8) and can be edited with any text editor. The global structure consists of three parts: The tree definition, the item definition, and the item pool.

- The tree definition is preceded with the marker ``--trees--`` followed by a newline. This defines the number and data structure of the trees in the file.
- The data item definition is preceded by the marker ``--item-types--`` followed by a newline. This defines the data fields of each data item.
- The item pool is preceded by the marker ``--item-pool--`` followed by a newline. This section contains the actual data.

The file content of the simple example file in the Introduction chapter looks like this::

    --trees--

    tree "Tree 1"
        field "Value"
            field-type "sum"
            own-fields ["value"]
            child-fields []
            sibling-fields []
            parent-fields []
        field "Sum"
            field-type "sum"
            own-fields ["value"]
            child-fields ["Sum"]
            sibling-fields []
            parent-fields []

    tree "Tree 2"
        field "Value"
            field-type "sum"
            own-fields ["value"]
            child-fields []
            sibling-fields []
            parent-fields []
        field "Sum"
            field-type "sum"
            own-fields ["value"]
            child-fields ["Sum"]
            sibling-fields []
            parent-fields []

    --item-types--

    item Node
        fields {"value": {"content": 0, "type": "integer"}}
        trees [[], []]

    --item-pool--

    item A
        fields {"value": {"content": 1, "type": "integer"}}
        trees [[0], [0, 0, 0]]

    item B
        fields {"value": {"content": 2, "type": "integer"}}
        trees [[0, 0], [0, 0]]

    item C
        fields {"value": {"content": 3, "type": "integer"}}
        trees [[0, 1], [0, 0, 1]]

    item D
        fields {"value": {"content": 4, "type": "integer"}}
        trees [[0, 0, 0], [0]]

    item E
        fields {"value": {"content": 5, "type": "integer"}}
        trees [[0, 0, 1], [0, 1]]


Tree Definition
^^^^^^^^^^^^^^^

A single tree is defined by the name of the tree and a list of tree fields. A node's tree field values are calculated from data fields or tree fields of the node itself, its siblings, parent and children. Each of these are mentioned in the field definition. There are various different field types, some use values in the current tree, some use values from other trees. You can for example display the name of a node's parent in a different tree. Trees are numbered starting with 0. Look at the first tree in the example::

    tree "Tree 1"
        field "Value"
            field-type "sum"
            own-fields ["value"]
            child-fields []
            sibling-fields []
            parent-fields []
        field "Sum"
            field-type "sum"
            own-fields ["value"]
            child-fields ["Sum"]
            sibling-fields []
            parent-fields []

The tree itself is called "Tree 1". It has two tree fields, "Value" and "Sum". The tree field "Value" is of type "sum", and it displays anything that is found in the data item field "value". The tree field "Sum" is also of type "Sum" and for each node it adds everything in the node's item field "value", plus all values in the tree field "Sum" of its children.

More about how to define tree fields in the next chapter.

Data Item Definition
^^^^^^^^^^^^^^^^^^^^

Each node in a tree is stored as a "data item". In the data file a "data item" is stored like this::

    item A
        fields {"value": {"content": 1, "type": "integer"}}
        trees [[], []]

After four spaces indent, there's the keyword "item" and the name (in this case "A"). This is the name that's displayed in the heading of the data item pane in the GUI, and as the node name in the tree pane of the GUI.
The next line, after an indent of 8 spaces, has the keyword "fields" followed by a json dictionary::

            "field name 1": {"content": 1, "type": "integer"}, "field name 2": ...
            
In this dictionary, each data field has a sub-dictionary listing its default content, the field type, and possibly some other values (timers have a running/stopped flag and a last-started flag). When a new item/node is created, this default content will be in all data fields. In the example above, a new node will contain one single field called "value" with the content "1".

For a description of all possible data field types, see the Data Fields chapter.

The last line, "trees ...", must contain an array of *N* empty arrays, where *N* is the number of trees in your file. If you have four trees in your tree fiel, that line must read::

        trees [[], [], [], []]

This makes your field definition available in all trees (and creates an error otherwise).

The Data Pool
^^^^^^^^^^^^^

The Data Pool is the last of the three sections of the tree file, and in most cases the largest. This is where the actual data is stored.
It consists of a list of items in the tree, with a syntax like in the data item definition section::

    item D
        fields {"value": {"content": 4, "type": "integer"}}
        trees [[0, 0, 0], [0]]

    item E
        fields {"value": {"content": 5, "type": "integer"}}
        trees [[0, 0, 1], [0, 1]]

The content here is the actual content in the field. The tree structure is stored in the last line: ::

        trees [[0, 0, 1], [0, 1]]

This is an array of arrays, each of which is a path in the tree. In the example above the node can be found following the path 0-0-1 in the first tree starting at the root node, and 0-1 in the second tree. Children are numbered using fixed indexes, starting at 0. A path of 0-0-1 means: My node is the second child (-1) of the first child (-0-1) of the first child (0-0-1) of the root node in the (first) tree. And in the second tree, the path 0-1 says the node is the second child of the first child of the root.
