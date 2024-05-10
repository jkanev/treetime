#
# Tis file is part of TreeTime, a tree editor and data analyser
#
# Copyright (C) GPLv3, 2015, Jacob Kanev
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

# -*- coding:utf-8 -*-

from .item import *
from textwrap import wrap
import datetime
from math import floor, ceil, inf

class Field:
    """
    A set of instructions to view/display the content of data items.
    Fields are part of nodes, and are stored in templates.
    """

    def __init__(self, node=None, ownFields=[], childFields=[], siblingFields=[], parentFields=[], fieldType=None):
        """Initialises the class, links the source node, field type, and sets the evaluation method."""
        
        self.cache = None
        self.ownFields = ownFields
        self.siblingFields = siblingFields
        self.childFields = childFields
        self.parentFields = parentFields
        self.sourceNode = node
        self.getValue = None
        self.getString = None
        self.fieldType = fieldType
        if (self.fieldType != ""):
            self.initFieldType()

    def __deepcopy__(self, memo):
        ''' Overload of the deepcopy function, to avoid copying the node recursively.'''

        if memo is None:
            memo = {}
        
        fieldType = self.__class__
        newField = fieldType.__new__(fieldType)
        
        # cache doesn't get copied
        newField.cache = None
        
        # simple fields are copies
        newField.ownFields = copy.deepcopy(self.ownFields)
        newField.siblingFields = copy.deepcopy(self.siblingFields)
        newField.childFields = copy.deepcopy(self.childFields)
        newField.parentFields = copy.deepcopy(self.parentFields)
        newField.fieldType = copy.deepcopy(self.fieldType)
        
        # the source node is a link
        newField.sourceNode = self.sourceNode
        
        # functions are set
        if (newField.fieldType != ""):
            newField.initFieldType()
        
        memo[id(self)] = newField
        return newField

    @staticmethod
    def getFieldValue(field):
        """
        :param field: the field to get the value from
        :return: Depending on the field type, the current value. Mostly this is just the content of the "content" key,
        but with timers this is different.
        """
        if field["type"] == "timer":
            running_since = field.get("running_since")
            partial = field["content"]
            running_since = running_since and datetime.datetime.strptime(running_since,
                                                                      "%Y-%m-%d %H:%M:%S")
            if running_since:
                elapsed = datetime.datetime.now() - running_since
                return partial \
                       + elapsed.days * 24.0 \
                       + elapsed.seconds / 60.0 / 60.0 \
                       + elapsed.microseconds / 60.0 / 60.0 / 1000000.0
            else:
                return partial
        else:
            return field["content"]

    def getFieldValues(self, sort=False):
        """ Gets all values of all related fields in a list.
        Order is: own fields first, then child fields, then sibling fields, then parent fields.
        Item fields of the same name have precedence over tree fields.
        """

        values = []
        
        # look in own fields
        node = self.sourceNode
        if node.item is not None: # don't try to get values from the root node
            for f in self.ownFields:
                if f in node.fields:
                    values += [node.fields[f].getValue()]
                elif f in node.item.fields:
                    values += [Field.getFieldValue(node.item.fields[f])]
        
        # look in child fields
        node = self.sourceNode
        for f in self.childFields:
            for c in sort and sorted(node.children, key=lambda n: n.name) or node.children:
                if f in c.fields:
                    values += [c.fields[f].getValue()]
                elif c.item and c.item.fields and f in c.item.fields:
                    values += [Field.getFieldValue(c.item.fields[f])]

        node = self.sourceNode.parent
        if node:

            # look in sibling fields
            for f in self.siblingFields:
                for c in sort and sorted(node.children, key=lambda n: n.name) or node.children:
                    if c != self.sourceNode:
                        if f in c.fields:
                            values += [c.fields[f].getValue()]
                        elif f in c.item.fields:
                            values += [Field.getFieldValue(c.item.fields[f])]

            # look in parent fields
            for f in self.parentFields:
                if f in node.item.fields:
                    values += [node.fields[f].getValue()]
                elif f in node.fields:
                    values += [Field.getFieldValue(node.item.fields[f])]
        
        # return
        return values

    def initFieldType(self):
        
        if self.fieldType == "string":
            self.getValue = self.getValueString
            self.getString = self.getStringUnchanged
        elif self.fieldType == "url":
            self.getValue = self.getValueString
            self.getString = self.getStringUnchanged
        elif self.fieldType == "text":
            self.getValue = self.getValueString
            self.getString = self.getStringUnchanged
        elif self.fieldType == "sum":
            self.getValue = self.getValueSum
            self.getString = self.getStringRounded
        elif self.fieldType == "set":
            self.getValue = self.getValueSet
            self.getString = self.getStringSet
        elif self.fieldType == "sum-time":
            self.getValue = self.getValueSum
            self.getString = self.getStringTime
        elif self.fieldType == "difference":
            self.getValue = self.getValueDifference
            self.getString = self.getStringRounded
        elif self.fieldType == "difference-time":
            self.getValue = self.getValueDifference
            self.getString = self.getStringTime
        elif self.fieldType == "mean":
            self.getValue = self.getValueMean
            self.getString = self.getStringRounded
        elif self.fieldType == "mean-percent":
            self.getValue = self.getValueMean
            self.getString = self.getStringPercent
        elif self.fieldType == "min":
            self.getValue = self.getValueMin
            self.getString = self.getStringUnchanged
        elif self.fieldType == "max":
            self.getValue = self.getValueMax
            self.getString = self.getStringUnchanged
        elif self.fieldType == "min-string":
            self.getValue = self.getValueMinString
            self.getString = self.getStringUnchanged
        elif self.fieldType == "max-string":
            self.getValue = self.getValueMaxString
            self.getString = self.getStringUnchanged
        elif self.fieldType == "ratio":
            self.getValue = self.getValueRatio
            self.getString = self.getStringRounded
        elif self.fieldType == "ratio-percent":
            self.getValue = self.getValueRatio
            self.getString = self.getStringPercent
        elif self.fieldType == "node-name":
            self.getValue = self.getValueNodeName
            self.getString = self.getStringUnchanged
        elif self.fieldType == "node-path":
            self.getValue = self.getValueNodePath
            self.getString = self.getStringUnchanged

    def getStringPercent(self):
        if self.sourceNode and self.getValue:
            v = self.getValue()
            if v:
                whitespace = ""
                if v < 0.1:
                    whitespace = "  "
                elif v < 1.0:
                    whitespace = " "
                return whitespace + str(round(100*v)) + " %"
            else:
                return ""
        else:
            return ""

    def getStringSet(self):
        if self.sourceNode and self.getValue:
            return ', '.join(sorted([str(n) for n in self.getValue()]))
        else:
            return "[undefined]"

    def getStringTime(self):
        if self.sourceNode and self.getValue:
            v = self.getValue()
            if v:
                if v < 0:
                    adjust = 0.49999
                else:
                    adjust = -0.49999
                hours = round(v + adjust)
                minutes = round(60.0*(v - hours) + adjust)
                seconds = round(3600.0*((v - hours) - minutes/60.0) + adjust)
                sign = v < 0.0 and "- " or "  "
                return "{}{:02d}:{:02d}:{:02d}".format(sign, abs(hours), abs(minutes), abs(seconds))
            else:
                return ""
        else:
            return ""

    def getStringUnchanged(self):
        if self.sourceNode and self.getValue:
            return str(self.getValue())
        else:
            return "[undefined]"

    def getStringRounded(self):
        if self.sourceNode and self.getValue:
            value = self.getValue()
            if value:
                return str(round(value, 3))
            else:
                return ""
        else:
            return "[undefined]"

    def getValueNodeName(self):
        if self.cache is not None:
            return self.cache
        else:
            s = ""
            item = self.sourceNode.item
            if item is None:
                return s
            for t in self.parentFields:

                # find tree
                tree = self.sourceNode
                while tree.parent is not None:
                    tree = tree.parent
                if type(tree) == Forest:
                    tree = tree.children[t]

                # find node in tree
                if type(tree) == Tree:
                    path = item.trees[t]
                    node = tree.findNode(path)
                    if node is not None:
                        parent = node.parent
                        if parent is not None:
                            s += parent.name
            return s

    def getValueNodePath(self):
        if self.cache is not None:
            return self.cache
        else:
            s = ""
            item = self.sourceNode.item
            if item is None:
                return s
            for t in self.parentFields:

                # find tree
                tree = self.sourceNode
                while tree.parent is not None:
                    tree = tree.parent
                if type(tree) == Forest:
                    tree = tree.children[t]

                # find node in tree
                if type(tree) == Tree:
                    path = item.trees[t]
                    node = tree.findNode(path)
                    if node and node.parent:
                        parent = node.parent
                        s += parent.name
                        while parent.parent and parent.parent.parent and parent.parent.parent.parent : # don't display forest or tree names
                            parent = parent.parent
                            s = parent.name + " | " + s
            return s

    def getValueString(self):
        values = self.getFieldValues(sort=True)
        s = ''
        for v in values:
            if v:     # either sum up using the value
                s += v
            else:     # or the neutral element for addition ('')
                s += ''
        return s

    def getValueSet(self):
        values = self.getFieldValues(sort=True)
        result_set = set()
        for v in values:
            if isinstance(v, set):
                result_set = result_set | v
            elif v:     # either sum up using the value
                result_set.add(v)
        return result_set

    def getValueSum(self):
        values = self.getFieldValues()
        sum = 0
        for v in values:
            if v:     # either sum up using the value
                sum += v
            else:     # or the neutral element for addition (0)
                sum += 0
        return sum

    def getValueDifference(self):
        """
        Calculates different a - b - c - d of values a,b,c,d
        """
        values = self.getFieldValues()
        difference = 0
        first = True
        for v in values:
            if first:
                if v:
                    difference = v     # first element is positive
                else:
                    difference = 0     # or the neutral element for addition (0)
                first = False
            else:
                if v:
                    difference -= v     # all other elements are negative
                else:
                    difference += 0     # or the neutral element for addition (0)
        return difference

    def getValueMin(self):
        values = self.getFieldValues()
        minValue = inf
        for v in values:
            if v < minValue:     # either sum up using the value
                minValue = v
        return minValue

    def getValueMax(self):
        values = self.getFieldValues()
        maxValue = -inf
        for v in values:
            if v > maxValue:     # either sum up using the value
                maxValue = v
        return maxValue


    def getValueMinString(self):
        values = self.getFieldValues()
        minValue = ""
        # find minimum ignoring "" (otherwise empty fields will overrule everything)
        for v in values:
            if v and (not minValue or v < minValue):
                minValue = v
        return minValue

    def getValueMaxString(self):
        values = self.getFieldValues()
        maxValue = ""
        for v in values:
            if v > maxValue:
                maxValue = v
        return maxValue
    def getValueMean(self):
        values = self.getFieldValues()
        sum = 0.0
        n = 0.0
        for v in values:
            if v:     # in case of 'None', use neutal elements of 0 for addition, and 1 for multiplication
                n += 1.0
                sum += v
        if n > 0.0:
            return sum/n
        else:
            return None

    def getValueRatio(self):
        """
        Returns the ration a/(b+c+d+e+...) of field values a,b,c,d,e,...
        """
        values = self.getFieldValues()
        if len(values) < 2:
            return None
        else:
            denom = values[0]
            sum = 0
            for v in values[1:]:
                if v:
                    sum += v
            if sum != 0:
                return denom/sum
            else:
                return None
    
    def writeToString(self):
        string = "    field-type " + json.dumps(self.fieldType) + "\n"
        string += "        own-fields " + json.dumps(self.ownFields) + "\n"
        string += "        child-fields " + json.dumps(self.childFields) + "\n"
        string += "        sibling-fields " + json.dumps(self.siblingFields) + "\n"
        string += "        parent-fields " + json.dumps(self.parentFields) + "\n"
        return string

    def readFromString(self, string):
        
        s = string.split("\n        field-type ")
        name = json.loads(s[0])
        s = s[1].split("\n        own-fields ")
        try:
            self.fieldType = json.loads(s[0])
        except:
            self.printReadError(name, "field-type", s[0]);
        s = s[1].split("\n        child-fields ")
        try:
            self.ownFields = json.loads(s[0])
        except:
            self.printReadError(name, "own-fields", s[0]);
        s = s[1].split("\n        sibling-fields ")
        try:
            self.childFields = json.loads(s[0])
        except:
            self.printReadError(name, "child-fields", s[0]);
        s = s[1].split("\n        parent-fields ")
        try:
            self.siblingFields = json.loads(s[0])
        except:
            self.printReadError(name, "sibling-fields", s[0]);
        try:
            self.parentFields = json.loads(s[1])
        except:
            self.printReadError(name, "parent-fields", s[0]);

        self.initFieldType()
        
        return name

    def printReadError(self, name, parameter, string):
        print('error reading field parameter "' + parameter + '" of field "' + name + '": definition string "' + string + '" cannot be parsed.')


class Node:
    """
    A tree structure consisting of nodes that are parents of nodes etc. A node is a view-object to display one item.
    """
    
    def __init__(self, parent, tree, path):
        self.parent = parent
        self.children = []
        self.item = None
        self.name = ""
        self.fields = {}
        self.fieldOrder = []
        self.tree = tree
        self.path = path
        self.viewNode = None
        self.nameChangeCallback = None
        self.fieldChangeCallback = None
        self.deletionCallback = None
        self.moveCallback = None

    @staticmethod
    def _wrap_lines(raw_lines):
        """
        Helper function to wrap long text
        :param string: Input string, in one single line
        :return: Array with text wrapped at 70 chars, preserving newlines, but trimming space (no double new lines)
        """
        lines = []
        for line in [s.strip() for s in raw_lines.split('\n')]:
            lines += wrap(line, 70) or '\n'
        return lines

    def _evaluateContext(self, fields, context):
        """
        Helper function, calculates fieds, context, and whether we're in the current node, based on the context path.
        :param fields: the initial "fields" variable. If the context is "False", that variable will be
            returned in the "fields" return value unchanged. This is important in non-context display settings.
        :param context: The path of the node that is to be displayed as "node with context".
        :return: fields, children, context_current - three bools indicating whether the calling node should display
            its children (yes, if it is a sibling in the ancestry path, otherwise no), its fields (yes, if it is the
            target node and we have fields enabled in the gui, otherwise no), and whether it is the target
            node (interesting for separate css things)
        """
        children = True
        fields_local = fields
        context_current = False
        if context:
            fields_local = False
            children = False

            # display children if we're a direct ancestor
            if len(self.path) <= len(context) and self.path == context[:len(self.path)]:
                children = True

                # display fields if we're the actual target node
                if len(self.path) == len(context):
                    fields_local = fields
                    context_current = True

        return fields_local, children, context_current

    def map(self, function, parameter, depthFirst):
        ''' Applies the function to each node in the tree. The function must receive one parameter and return one
        parameter. The return value is used as parameter for the next function call. The value Parameter is used in the
        first call.'''
        
        # if depthFirst then recurse first and apply later
        if depthFirst:
            for c in self.children:
                parameter = c.map(function, parameter, depthFirst)
                
            return function(self, parameter)
        else:
            parameter = function(self, parameter)
            for c in self.children:
                parameter = c.map(function, parameter, depthFirst)
                
            return parameter

    def printForest(self, indent=0):
        
        # create leading white space
        s = ""
        for i in range(indent):
            s += "    "
        s += " → " + str(self.tree)
        for p in self.path:
            s += "[" + str(p) + "]"
        s += "    "
        if self.item is not None:
            for p in self.item.trees[self.tree]:
                s += "[" + str(p) + "]"
        s += " " + self.__class__.__name__ + " "
        
        # append item content and print
        s += self.name
        for name,field in self.fields.items():
            s += " [" + name + "] " + str(field.getString())
        print(s)
        
        # recurse
        for i in range(len(self.children)):
            self.children[i].printForest(indent + 1)

    def to_csv(self, fields=True, context=False, first=True, depth=-1):
        """
        Create a csv representation of the current branch.
        :fieldOrder: The order of fields in the tree
        :first: If this is the first call (first=True), add a title line with field names,
                on recursive calls (=False) don't
        :depth: A number listing how many levels should be in the export
        :return: CSV. Quotes become double-quotes, fields with commas, line breaks or quotes are quoted,
            the first field is called "Tree" and contains the tree structure by pre-pending parents to each node, the
            second field is called "Name" and contains the node name. All other fields from the tree definition follow.
            Children are sorted alphabetically.

            Tree,Name,"Spent Hours"
            "Projects | Build Robot","Build Robot",10
            "Projects | Build Robot | Start Working",Design,20
        """

        def clean_field(text):
            text.replace('"', '""')
            if '"' in text or '\n' in text or ',' in text:
                text = '"' + text + '"'
            return text

        # evaluate context
        fields_local, children, context_current = self._evaluateContext(fields, context)
        csv = ""

        # find root node
        tree = self
        while tree.parent.parent is not None:
            tree = tree.parent

        # add title line
        if first:
            csv = 'Tree,Name'
            for f in tree.fieldOrder:
                csv += ','
                csv += clean_field(f)
            csv += '\n'

        # add node path
        field = ''
        pipe = False
        if len(self.path) > 1:
            for n in range(1, len(self.path)):
                field += pipe and ' | ' or ''
                field += tree.findNode(self.path[:n]).name
                pipe = True
        field += pipe and ' | ' or ''
        field += self.name
        csv += clean_field(field) + ','

        # add node name
        csv += self.name

        # add fields
        if fields_local:
            for f in tree.fieldOrder:
                csv += ',' + clean_field(self.fields[f].getString())
        csv += '\n'

        # add children
        if depth and children:
            for c in sorted(self.children, key=lambda x: x.name):
                csv += c.to_csv(first=False, fields=fields, context=context, depth=depth - 1)

        # return
        return csv

    def to_txt(self, fields=True, context=False, lastitem=[], depth=-1):
        """
        Create a text representation of the current branch.
        :param lastitem: A list of booleans showing whether the great-grandparent, grandparent, parent, is the
                         last item of the list of siblings
        :param fields: if true, all fields are included, if false, only node names are exported (no fields)
        :return: a string like this:

                    █ abc
                      def

                    █ abc
                    │ def
                    │
                    ┝━━█ abc
                    │  │ def
                    │  │
                    │  ┝━━█ abc
                    │  │    def
                    │  │
                    │  ┕━━█ abc
                    │        def
                    │
                    ┕━━█ abc
                       │ def
                       │
                       ┝━━█ abc
                       │    def
                       │
                       ┕━━█ abc
                            def
        """

        text = ""

        # evaluate context
        fields_local, children, context_current = self._evaluateContext(fields, context)

        # create leading tree graphics
        # please pay attention: The spaces in the graphic strings are special unicode figure spaces
        if children and self.children and depth:
            pre_node_prefix = ""
            first_line_prefix = "●  "
            line_prefix = "│  "
        else:
            pre_node_prefix = ""
            first_line_prefix = "●  "
            line_prefix = "   "
        n = 0
        for last in lastitem[::-1]:
            if not last:
                if n:
                    pre_node_prefix = "│  " + pre_node_prefix
                    first_line_prefix = "│  " + first_line_prefix
                    line_prefix = "│  " + line_prefix
                else:
                    pre_node_prefix = "│  " + pre_node_prefix
                    first_line_prefix = "├──" + first_line_prefix
                    line_prefix = "│  " + line_prefix
            else:
                if n:
                    pre_node_prefix = "   " + pre_node_prefix
                    first_line_prefix = "   " + first_line_prefix
                    line_prefix = "   " + line_prefix
                else:
                    pre_node_prefix = "│  " + pre_node_prefix
                    first_line_prefix = "└──" + first_line_prefix
                    line_prefix = "   " + line_prefix
            n += 1

        # append item content and print
        text += pre_node_prefix + "\n"

        # add node name (possibly multi-line)
        first = True
        for line in Node._wrap_lines(self.name):
            line = line == '\n' and line or line + '\n'
            if first:
                text += first_line_prefix + line
                first = False
            else:
                text += line_prefix + "    " + line

        if fields_local:
            for name, field in self.fields.items():

                # wrap field content, larger bits of text start with a newline
                lines = Node._wrap_lines(field.getString())

                # empty array if only whitespace content
                if lines == ['\n']:
                    lines = []

                if len(lines) > 1:
                    lines = [''] + lines

                # assemble final text with tree decorations
                first = True
                for line in lines:
                    line = line == '\n' and line or line + '\n'
                    if first:
                        text += line_prefix + name + ": " + line
                        first = False
                    else:
                        text += line_prefix + "    " + line

        # recurse
        if children and depth:
            sorted_children = sorted(self.children, key=lambda c: c.name)
        else:
            sorted_children = []
        if len(sorted_children) > 1:
            childprefix = lastitem.copy()
            childprefix.append(False)
            for i in range(len(sorted_children)-1):
                text += sorted_children[i].to_txt(fields=fields, context=context, lastitem=childprefix, depth=depth-1)
        if len(sorted_children):
            childprefix = lastitem.copy()
            childprefix.append(True)
            text += sorted_children[-1].to_txt(fields=fields, context=context, lastitem=childprefix, depth=depth-1)

        # return
        return text

    def to_html(self, header=False, footer=False, fields=True, context=False, continuous=False, style='tiles', background='blue',
                depth=-1, current_depth=0):

        # evaluate context
        fields_local, children, context_current = self._evaluateContext(fields, context)

        # background colours
        next_background = {'blue': 'green', 'green': 'red', 'red': 'blue'}

        # page header
        if header and style == 'tiles' and not context:
            html = '<!DOCTYPE html><html lang="en">' \
                   + (continuous and '<meta http-equiv="refresh" content="1">' or '') \
                   + '<meta charset="utf-8"><title>TreeTime Export</title><style>' \
                   'body {font-family: sans-serif; color: black; background-color: white; font-size: 0.8em;} '\
                   'em {color: #555;}' \
                   'div.red {background-color: rgba(80, 0, 0, 0.03);}' \
                   'div.green {background-color: rgba(0, 80, 0, 0.03);}' \
                   'div.blue {background-color: rgba(0, 0, 80, 0.03);}' \
                   'div.node {position: relative; float: left; border: 1px solid; margin: 0.6em; padding: 0.6em; width: min-content; border-radius: 1em; border-color: #CCC;}' \
                   'div.name {padding: 0.2em; margin: 0.2em; position: relative; float: left; width: 100%;} ' \
                   'div.fields {position: relative; float: left; clear: left; width: min-content; border-top: 1px solid; border-color: #808080;} ' \
                   'div.children {position: relative; float: left; clear: left; width: max-content;} ' \
                   'div.string {position: relative; float: left; width: 10em; margin: 0.3em; padding: 0.3em; }' \
                   'div.min-string {position: relative; float: left; width: 10em; margin: 0.3em; padding: 0.3em; }' \
                   'div.max-string {position: relative; float: left; width: 10em; margin: 0.3em; padding: 0.3em; }' \
                   'div.set {position: relative; float: left; width: 10em; margin: 0.3em; padding: 0.3em; }' \
                   'div.text {position: relative; float: left; width: 20em; margin: 0.3em; padding: 0.3em; }' \
                   'div.url {position: relative; float: left; width: 20em; margin: 0.3em; padding: 0.3em; }' \
                   'div.sum {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.sum-time {position: relative; float: left; width: 10em; margin: 0.3em; padding: 0.3em; }' \
                   'div.difference {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.difference-time {position: relative; float: left; width: 10em; margin: 0.3em; padding: 0.3em; }' \
                   'div.min {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.max {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.mean {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.mean-percent {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.ratio {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.ratio-percent {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.node-name {position: relative; float: left; width: 10em; margin: 0.3em; padding: 0.3em; }' \
                   'div.node-path {position: relative; float: left; width: 20em; margin: 0.3em; padding: 0.3em; }' \
                   '</style></head><body>'
        elif header and style == 'tiles' and context:
            html = '<!DOCTYPE html><html lang="en">' \
                   + (continuous and '<meta http-equiv="refresh" content="1">' or '') \
                   + '<meta charset="utf-8"><title>TreeTime Export</title><style>' \
                   'body {font-family: sans-serif; color: black; background-color: white; font-size: 1.2em;} ' \
                   'em {color: #555;}' \
                   'div.red {background-color: rgba(80, 0, 0, 0.03);}' \
                   'div.green {background-color: rgba(0, 80, 0, 0.03);}' \
                   'div.blue {background-color: rgba(0, 0, 80, 0.03);}' \
                   'div.node {position: relative; float: left; border: 1px solid; margin: 0.6em; padding: 0.6em; width: min-content; border-radius: 1em; border-color: #CCC;}' \
                   'div.name {padding: 0.2em; margin: 0.2em; position: relative; float: left; width: 12em;} ' \
                   'div.name_current {padding: 0.2em; margin: 0.2em; position: relative; float: left; width: 48.5em;} ' \
                   'div.fields {position: relative; float: left; clear: left; width: 74em; border-top: 1px solid; border-color: #808080;} ' \
                   'div.children {position: relative; float: left; clear: left; width: max-content;} ' \
                   'div.string {position: relative; float: left; width: 20em; margin: 0.3em; padding: 0.3em; }' \
                   'div.min-string {position: relative; float: left; width: 20em; margin: 0.3em; padding: 0.3em; }' \
                   'div.max-string {position: relative; float: left; width: 20em; margin: 0.3em; padding: 0.3em; }' \
                   'div.set {position: relative; float: left; width: 20em; margin: 0.3em; padding: 0.3em; }' \
                   'div.text {position: relative; float: left; width: 40em; margin: 0.3em; padding: 0.3em; }' \
                   'div.url {position: relative; float: left; width: 20em; margin: 0.3em; padding: 0.3em; }' \
                   'div.sum {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.sum-time {position: relative; float: left; width: 10em; margin: 0.3em; padding: 0.3em; }' \
                   'div.difference {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.difference-time {position: relative; float: left; width: 10em; margin: 0.3em; padding: 0.3em; }' \
                   'div.min {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.max {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.mean {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.mean-percent {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.ratio {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.ratio-percent {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.node-name {position: relative; float: left; width: 20em; margin: 0.3em; padding: 0.3em; }' \
                   'div.node-path {position: relative; float: left; width: 40em; margin: 0.3em; padding: 0.3em; }' \
                   '</style></head><body>'
        elif header and style == 'list':
            html = '<!DOCTYPE html><html lang="en">' \
                   + (continuous and '<meta http-equiv="refresh" content="1">' or '') \
                   + '<meta charset="utf-8"><title>TreeTime Export</title><style>' \
                   'body {font-family: sans-serif; color: black; background-color: white; font-size: 0.8em;} ' \
                   'em {color: #555;}' \
                   'div.red {background-color: rgba(80, 0, 0, 0.03);}' \
                   'div.green {background-color: rgba(0, 80, 0, 0.03);}' \
                   'div.blue {background-color: rgba(0, 0, 80, 0.03);}' \
                   'div.node {position: relative; float: left; clear: left; border-left: 2px solid; margin: 0.6em; padding: 0.6em; width: max-content; border-color: #808080;}' \
                   'div.name {padding: 0.2em; margin: 0.2em; position: relative; float: left;} ' \
                   'div.fields {position: relative; float: left; width: max-content; border-color: #808080;}' \
                   'div.children {position: relative; float: left; clear: left; width: max-content;} ' \
                   'div.string {position: relative; float: left; width: 10em; margin: 0.3em; padding: 0.3em; }' \
                   'div.min-string {position: relative; float: left; width: 10em; margin: 0.3em; padding: 0.3em; }' \
                   'div.max-string {position: relative; float: left; width: 10em; margin: 0.3em; padding: 0.3em; }' \
                   'div.set {position: relative; float: left; width: 10em; margin: 0.3em; padding: 0.3em; }' \
                   'div.text {position: relative; float: left; width: 30em; margin: 0.3em; padding: 0.3em; }' \
                   'div.url {position: relative; float: left; width: 20em; margin: 0.3em; padding: 0.3em; }' \
                   'div.sum {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.sum-time {position: relative; float: left; width: 10em; margin: 0.3em; padding: 0.3em; }' \
                   'div.difference {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.difference-time {position: relative; float: left; width: 10em; margin: 0.3em; padding: 0.3em; }' \
                   'div.min {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.max {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.mean {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.mean-percent {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.ratio {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.ratio-percent {position: relative; float: left; width: 5em; margin: 0.3em; padding: 0.3em; }' \
                   'div.node-name {position: relative; float: left; width: 10em; margin: 0.3em; padding: 0.3em; }' \
                   'div.node-path {position: relative; float: left; width: 20em; margin: 0.3em; padding: 0.3em; }' \
                   '</style></head><body>'
        else:
            html = ''

        # node header
        html += '<div class="node {}">'.format(background)
        needed_columns = context_current and 5 or 1    # the amount of columns needed by this child

        # node name
        if context:
            if context_current:
                font_size = 1.5
            else:
                font_size = 0.5 + 1.0 / (2.0 + max((len(context) - len(self.path)), 0))  # 1 em for target, decay to 0.5
        else:
            font_size = 1.0 + 1.0 / (1.0 + current_depth)  # start with 2 em, exponentially decay to 0.5 em
        if style == 'tiles':
            if context_current:
                html += '<div class="name_current" style="font-size: {:0.2f}em">{}</div>'.format(font_size, self.name)
            else:
                html += '<div class="name" style="font-size: {:0.2f}em">{}</div>'.format(font_size, self.name)
        if style == 'list':
            html += '<div class="name" style="font-size: {:0.2f}em; ' \
                    'width: {:0.2f}em;">{}</div>'.format(font_size, (20.0 - (1.2*current_depth))/font_size, self.name)

        # node fields
        if fields_local:
            html += '<div class="fields">'
            for name, field in self.fields.items():
                content = field.getString().strip()
                if content or (style == 'list'):   # in tile mode empty fields are hidden, in list mode always displayed
                    content = content.replace('\n', '<br/>')
                    if field.fieldType == "url":
                        html += '<div class="{}"><em>{}</em><br/><a href="{}">{}</a></div>'.format(
                            field.fieldType, name, content, len(content) > 40 and content[:37]+"..." or content)
                    else:
                        html += '<div class="{}"><em>{}</em><br/>{}</div>'.format(field.fieldType, name, content)
            html += '</div>'

        child_html = ""

        # children
        if children:

            child_count = 0
            sorted_children = sorted(self.children, key=lambda c: c.name)
            group_open = False
            for i in range(len(sorted_children)):

                # write next child
                background = next_background[background]
                child_columns = 1     # number of columns needed by child sub-branch
                if depth:
                    child_columns, child_html = sorted_children[i].to_html(background=background, depth=depth-1,
                                                                           fields=fields, context=context,
                                                                           current_depth=current_depth+1, style=style)

                # start new child group on first child in group of 5, or if child needs more columns than available
                if child_columns > 5-child_count:
                    child_count = 0
                if child_count == 0:
                    if group_open:
                        html += '</div>'
                    html += '<div class="children">'
                    group_open = True

                # add html to main html
                html += child_html
                child_count += child_columns
                needed_columns = max(needed_columns, min(child_count, 5))

                # close child group after fourth child of after node with children
                if child_count >= 5:
                    child_count = 0
                if child_count == 0:
                    html += '</div>'
                    group_open = False

            # node footer
            if group_open:
                html += '</div>'
        html += "</div>"

        # page footer
        if footer:
            html += '</body></html>'

        # finished.
        return needed_columns, html

    def createPathTo(self, item, treeindex, nodeindex, viewtemplate):
        """
        Links an item into a tree, using the given path. Empty nodes get created on the way.
        """
        
        # either recurse deeper
        if nodeindex < len(item.trees[treeindex]):
            n = item.trees[treeindex][nodeindex]
            while n >= len(self.children):
                self.addChild()
            self.children[n].createPathTo(item,treeindex,nodeindex+1,viewtemplate)
        
        # or, if in final node, link item
        else:
            self.item = item
            self.name = item.name
            self.initFields(viewtemplate)
            self.registerCallbacks()

    def registerCallbacks(self):
        """
        Register callbacks from the parent (QNode), so changes from the tree layer
        can be shown in the QT GUI layer
        """
        if self.item is not None:
            self.item.registerNameChangeCallback(self.tree, self.notifyNameChange)
            self.item.registerFieldChangeCallback(self.tree, lambda x: self.notifyFieldChange(x, True))
            self.item.registerDeletionCallback(self.tree, self.notifyDeletion)
            self.item.registerMoveCallback(self.tree, self.notifyMove)
            self.item.registerSelectionCallback(self.tree, lambda x: self.notifySelection(x))
            self.item.registerViewNode(self.tree, self)

    def registerViewNode(self, viewNode):
        """
        Register the respective QT GUI view node with the node
        """
        self.viewNode = viewNode

    def findNode(self, path, currentIndex=None):
        """
        Recursive function to walk down a path in a tree and return the node at the last step
        """

        # if currentIndex==False this function was called with the intention of calling Tree.findNode().
        # return None in this case.
        if currentIndex is None:
            return None

        # either recurse deeper
        if currentIndex < len(path):
            childNumber = path[currentIndex]
            if childNumber >= len(self.children):
                return None
            return self.children[childNumber].findNode(path, currentIndex+1)
        
        # or, return myself
        else:
            return self

    def addChild(self):
        """
        Add a child to a node. The child is a new copy of the default node.
        """
        node = Node(self, self.tree, self.path + [len(self.children)])
        self.children += [node]
        return node

    def addNodeAsChild(self, node):
        """
        Add an existing node to a new parent.
        """
        self.children += [node]
        node.parent = self
        self.renumberChildren()
        node.item.notifyFieldChange("")
        self.notifyNameChange(self.name)

    def removeChild(self, child):
        if child in self.children:
            self.children.remove(child)
            self.renumberChildren()
            for f in self.fields:
                self.notifyFieldChange(f, True)
            child.parent = None

    def renumberChildren(self):
        """
        Correct the paths after children have been removed or added.
        """
        for i, c in enumerate(self.children):
            c.path = self.path + [i]
            if c.item:
                # print("{} {}".format(c.path, c.item.name))
                c.item.trees[self.tree] = self.path + [i]
                c.renumberChildren()

    def addItemAsChild(self, item):
        """
        Creates a node and links it to the item. Updates the item's forest indexes.
        """
        node = self.addChild()
        node.item = item
        node.name = item.name
        node.registerCallbacks()
        item.trees[node.tree] = node.path
        node.initFields(self.fields)
        return node

    def initFields(self, fields):
        self.fields = copy.deepcopy(fields)
        
        # first set all fields to myself
        for name, field in self.fields.items():
            field.sourceNode = self
        
        # and only then send notification
        for name, field in self.fields.items():
            self.notifyFieldChange(name, True)

    def findNodeByName(self, name):
        """
        Finds the first node of a given name in the tree.
        """
        if self.name == name:
            return self
        else:
            for c in self.children:
                found = c.findNodeByName(name)
                if found is not None:
                    return found
        return None

    def registerNameChangeCallback(self, callback):
        self.nameChangeCallback = callback

    def registerFieldChangeCallback(self, callback):
        self.fieldChangeCallback = callback

    def registerDeletionCallback(self, callback):
        self.deletionCallback = callback

    def registerMoveCallback(self, callback):
        self.moveCallback = callback

    def registerSelectionCallback(self, callback):
        self.selectionCallback = callback

    def notifyNameChange(self, newName):
        """
        Callback used to notify a node of a name change. Changes the name, then
        recreates strings for the fiels 'node-name' and 'node-path'.
        Recurses down the tree to update the node-path strings of all children by calling the function
        notifyParentNameChange.
        """

        # if name is not false, set new name and notify GUI
        if newName:
            self.name = newName
            if self.nameChangeCallback is not None:
                self.nameChangeCallback(newName)

        # always adapt all my fields in all trees (better: call the callback from the item without recursion)
        if self.item:
            for v in self.item.viewNodes:
                v and v.notifyFieldChange(False, False)

        # notify all children, recursive, but only update their fields
        for c in self.children:
            c.notifyNameChange(False)

    def notifyFieldChange(self, fieldName, recursion):
        """
        Callback, called whenever a field in a related item has changed.
        """

        if self.fieldChangeCallback is not None:
            for f in self.fields:
                self.fieldChangeCallback(f, self.fields[f].getString())
        
        if recursion:
            if self.parent is not None:
                # notify all siblings, non-recursive
                for c in self.parent.children:
                    if c is not self:
                        c.notifyFieldChange(fieldName, False)
                # notify all parents, recursive
                self.parent.notifyFieldChange(fieldName, True)

    def notifyDeletion(self):
        """
        Callback, called when the underlying item was deleted or removed from this tree.
        Recursion removes the complete child branch in this tree.
        """

        # unlink item
        self.item = None
        
        # tell the GUI layer to remove my QNode from its parent
        if self.deletionCallback is not None:
            self.deletionCallback()
            
        # make parent renumber children
        self.parent.removeChild(self)

    def notifyMove(self):
        """
        Callback, called when the underlying item moved to a different parent within the tree.
        Recursion renumbers all children in the new and in the old parent.
        """

        # find new parent and remember old parent
        oldParent = self.parent
        tree = self
        while tree.parent.parent is not None:
            tree = tree.parent
        path = self.item.trees[self.tree]
        newParent = tree.findNode(path[0:-1])

        # move node
        oldParent.removeChild(self)
        newParent.addNodeAsChild(self)

        # tell the GUI layer to move my QNode to its new parent
        if self.moveCallback is not None:
            self.moveCallback()

    def notifySelection(self, select):
        """
        Callback, called whenever the underlying item was selected.
        """

        # tell the GUI layer to select my QNode
        if self.selectionCallback is not None:
            self.selectionCallback(select)

    def removeEmptyNodes(self):
        """
        Recurse to find nodes that have no items. If found, those nodes are removed and their siblings renumbered.
        Called after initial loading of the file.
        """
        for c in self.children:
            c.removeEmptyNodes()
        if not self.item:
            self.notifyDeletion()


class Tree(Node):
    """
    A tree inside a forest. One item can appear several times in the forest, but only once in each tree.
    """

    def __init__(self, parent, index):
        """Initialise"""
        
        super().__init__(parent, index, [])
        self.fields = {}
        self.name = ""

    def createPathTo(self, item, treeindex):
        """
        Sort the item into the forest, creating existing nodes on the fly if missing.
        """

        # per tree: loop over all nodes, creating if necessary
        # per node: create final node and link it to item
        if item.trees[treeindex]:
            n = item.trees[treeindex][0]
            while n >= len(self.children):
                self.addChild()
            self.children[n].createPathTo(item, treeindex, 1, self.fields)

    def findNode(self, path):
        """
        Find the node at a given path. Calls the respective function of the Node class.
        """

        # per tree: loop over all nodes, creating if necessary
        return super().findNode(path, 0)

    def writeToString(self):
        string = "tree " + json.dumps(self.name) + "\n"
        for n,f in self.fields.items():
            string += "    field " + json.dumps(n) + "\n"
            string += "    " + f.writeToString()
        return string

    def readFromString(self, string):
        fieldStrings = string.split("\n    field ")
        for n,fs in enumerate(fieldStrings):
            if n==0:
                self.name = json.loads(fs)
            else:
                f = Field()
                name = f.readFromString(fs)
                self.fields[name] = f
                self.fieldOrder += [name]

    def removeEmptyNodes(self):
        """
        Recurse to find nodes that have no items. If found, those nodes are removed and their siblings renumbered.
        Overrides same function in node, does not remove self (trees have no item anyway).
        """
        for c in self.children:
            c.removeEmptyNodes()


class Forest(Node):
    """
    The trunk node containing trees, that contain the nodes. Also manages the node templates.
    """

    def __init__(self, filename):
        """Initialise"""
        
        super().__init__(None, None, [])
        self.itemPool = None
        self.itemTypes = None
        self.readFromFile(filename)

    def createPaths(self):
        """
        Sort all items from the itempool into the forest,
        creating the forest structure as defined by the items' node indexes
        """
        for item in self.itemPool.items:
            self.createPathTo(item)

    def createPathTo(self, item):
        
        # start: loop over all trees, creating if necessary
        for b in range(len(item.trees)):
            if b >= len(self.children):
                self.addTree()
            if item.trees[b]:
                self.children[b].createPathTo(item,b)

    def addTree(self):
        self.children += [Tree(self, len(self.children))]

    def renumberChildren(self):
        """
        Correct the paths after children have been removed or added.
        """
        for i, c in enumerate(self.children):
            c.renumberChildren()

    def removeEmptyNodes(self):
        """
        Recurse to find nodes that have no items. If found, those nodes are removed and their siblings renumbered.
        Overrides same function in node, does not remove self (forests have no item anyway).
        """
        for c in self.children:
            c.removeEmptyNodes()

    def writeToString(self):
        s = ""
        for b in self.children:
            s += b.writeToString() + "\n"
        return s

    def readFromString(self, string):
        string = string.split("\n\ntree ")
        n = 0
        for s in string:
            if s != "":
                self.children[n].readFromString(s)
                n += 1

    def writeToFile(self, filename):
        treeString = self.writeToString()
        typeString = self.itemTypes.writeToString()
        itemString = self.itemPool.writeToString()
        with open(filename, "w") as f:
            f.write("--trees--\n\n")
            f.write(treeString)
            f.write("--item-types--\n\n")
            f.write(typeString)
            f.write("--item-pool--\n\n")
            f.write(itemString)

    def readFromFile(self, filename):
        with open(filename, "r") as f:

            # chop up string into trees, types, and items part
            s = f.read()
            s = s.split("--trees--")[1]
            s = s.split("--item-types--")
            treeString = s[0]
            s = s[1].split("--item-pool--")
            typeString = s[0]
            itemString = s[1]

        # create item pool
        self.itemTypes = ItemPool()
        self.itemTypes.readFromString(typeString)

        # create type pool
        self.itemPool = ItemPool()
        self.itemPool.readFromString(itemString)
        self.createPaths()

        # create trees
        self.readFromString(treeString)
        self.createPaths()     # atm we still need this twice. Fix it.

        # remove empty nodes
        self.removeEmptyNodes()
