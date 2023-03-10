
Tree Fields
===========

General Syntax
--------------

Each tree field is a function with a list of input fields. These fields can be either tree fields or data fields. To avoid ambiguities it is good practice to name tree fields starting with a capital letter and data fields with a lower case letter. A tree field is always defined as part of a tree (see previous chapter). The definition states the name, the field type, and the input parameters::

        field "Name"
            field-type "type"
            own-fields [...]
            child-fields [...]
            sibling-fields [...]
            parent-fields [...]

The field is started by the line ``field "Name"`` where "Name" is the name of the field. This will appear as the column heading in the tree list.
After this, indented with four spaces, is the field type: ``field-type "type"``, where "type" is the type (see next for an overview).
After this, the lines ``own-fields [...]``, ``child-fields [...]``, ``sibling-fields [...]``, and ``parent-fields [...]`` each define a list of field names. These are the input parameters for the function. They are evaluated in the order they are mentioned. A real-world example::

        field "Progress"
            field-type "ratio-percent"
            own-fields ["Spent Hours", "Planned Hours"]
            child-fields []
            sibling-fields []
            parent-fields []
  
The tree field "Progress" is a ratio, defined as parameter1 / (parameter2 + parameter3 + ...). In the tree view it will be displayed as a percentage. It shows the ratio of the tree fields "Spent Hours" / "Planned Hours".

concatenation
-------------

Concatenates strings.
Syntax::

        field "Name"
            field-type "concatenation"
            own-fields ["field1", "field2", ...]
            child-fields ["field3", ...]
            sibling-fields [...]
            parent-fields [...]

were "field1", "field2", "field3", ..., are the names of data or tree fields.
Result: The strings found in *field1, field2, field3, ...*, put together, in the order they are mentioned.

difference
----------

Difference of numbers.
Syntax::

        field "Name"
            field-type "difference"
            own-fields ["field1", "field2", ...]
            child-fields ["field3", ...]
            sibling-fields [...]
            parent-fields [...]

were "field1", "field2", "field3", ..., are the names of data or tree fields.
Result: The value *field1 - (field2 + field3 + ...)*, in the order they are mentioned.

difference-time
---------------

Same as "difference", but will show the result as hour format, e.g. the value *1.5* will be displayed and exported as *1:30:00*.

mean
----

The statistical mean of all input fields.
Syntax::

        field "Name"
            field-type "mean"
            own-fields ["field1", "field2", ...]
            child-fields ["field3", ...]
            sibling-fields [...]
            parent-fields [...]

were "field1", "field2", "field3", ..., are the names of data or tree fields.
Result: The value *(field1 + field2 + field3 + ...) / N*, where *N* is the number of fields.

mean-percent
------------

Same as "mean", but will show the result as a percentage, e.g. the value *0.75* will show as *75 %*.

node-name
---------

The name of the node's parent in another tree.
Syntax::

        field "Name"
            field-type "node-name"
            own-fields []
            child-fields []
            sibling-fields []
            parent-fields [N]

were *N* is an integer number.
Result: Displays the name of the node's parent in tree *N*. Trees are counted starting with 0.

Example: This field is called "Project" and is defined in a tree "Time", which is the first tree (i.e. Tree 0). There is another tree called "Projects", which is the third tree (i.e. Tree 2)::

    tree "Time"
        field "Project"
            field-type "node-name"
            own-fields []
            child-fields []
            sibling-fields []
            parent-fields [2]

    tree "Tasks"
        ...
        
    tree "Projects"
        ...

This would create the column "Project" in the tree view of the "Time" tree. The line ``parent-fields[2]`` means each entry shows the respective node's parent in the "Project" tree (e.g. "TreeTime").
 
node-path
---------

Same as "node-name", but instead of the paren't name, the entire path is shown, using "\|" as delimiter (e.g. "Coding \| Open Source \| TreeTime").

ratio
-----

Documentation still in progress.

ratio-percent
-------------

Documentation still in progress.

set
---

Documentation still in progress.

string
------

Documentation still in progress.

sum
---

Documentation still in progress.

sum-time
--------

Documentation still in progress.

text
----

Documentation still in progress.

url
---

Documentation still in progress.
