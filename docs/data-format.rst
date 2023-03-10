
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

Documentation still in progress.

More about how to define data fields in the next chapter.

The Data Pool
^^^^^^^^^^^^^

Documentation still in progress.
