
Data Fields
===========

Data fields are defined by a dictionary ``{...}`` where the field names are the dictionary keys ``{"name1": ..., "name2": ..., "name3": ...}``, and their type as well as their default value are the dictionary valuues ``{"name1": {"content": "", "type": "longtext"}, "name2": {"content": "", "type": "url"}, "name3": ...}``.
The possible types are "string", "text", "longtext", "url", "integer", and "timer".

string
------

One line of text.::

    "Name": {"content": "Maria Sibylla Merian", "type": "string"}

The field contains strings (small texts). In the GUI, the field will span one line. Text can be entered.

text
----

Longer text.::

    "details": {"content": "Please do the following: ", "type": "text"}

The field can contain longer text. In the GUI, there are 10 lines and there's a scrollbar for entering longer texts.

longtext
--------

Quite long text.::

    "details": {"content": "We discussed the following...", "type": "longtext"}

Identical to the text field, but in the GUI there are 25 lines and a scrollbar.

url
---

A URl of any type (file, http, ...).::

    "external link": {"content": "https://tree-time.info", "type": "url"}
    
In the GUI there's a text field and a button saying "Open". Clicking the button will use the the content of the text field and call the open method defined in the operating system (e.g. a content of "https://tree-time.info" or "file:///home/myself/downloads/pass-word.info.html" would be opened with your default web browser).

integer
-------

A number.::

    "hours planned": {"content": 4, "type": "integer"}

A simple number, can be a floating point number such as -1.23456.

timer
-----

A stop watch counting hours/minutes/seconds.::

    "hours spent": {"content": 0, "running_since": false, "type": "timer"}

In the GUI there will be a "Start" button and the field will contain a number.

Hitting the "Start" button will change the text in the field to "stop watch running", and the text on the button changes to "Stop". The stored item in the fiel changes to: ``"hours spent": {"content": 1.2000021166666666, "running_since": "2024-04-17 10:25:03", "type": "timer"}``. The actual tree field values will get updated once a second, including all branches and parents, updating all values like ratios and sums. It makes sense to use tree fields like *ratio-time* and *sum-time* to see the value in hh:mm:ss format instead of floating point numbers. The stop watch keeps running even when the file is closed or the computer is shut down.

Hitting the "Stop" button will display the currently summed up value in the field, and the text on the button changes to "Start" again. In the file, the "running" flag is removed: ``"hours spent": {"content": 1.3, "running_since": false, "type": "timer"}``

Subsequent start/stops on the button will add to the total value. 
