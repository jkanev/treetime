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

import copy
import json
from threading import Timer

class Item:
    """
    The list/forest item containing the actual data
    """

    def __init__(self, name, fieldstring='{}', treestring='[]'):
        self.name = name
        self.parentNames = []
        self.fields = json.loads(fieldstring)
        self.trees = json.loads(treestring)
        self.viewNodes = []
        self.nameChangeCallbacks = []
        self.fieldChangeCallbacks = []
        self.deletionCallbacks = []
        self.moveCallbacks = []
        self.selectionCallbacks = []
        self.clearCallbacks()

    def __deepcopy__(self, memo):
        ''' Overload of the deepcopy function, to avoid copying the node recursively.'''
        
        if memo is None:
            memo = {}
        
        itemType = self.__class__
        newItem = itemType.__new__(itemType)
        
        # fields and trees are complex
        newItem.fields = copy.deepcopy(self.fields)
        newItem.trees = copy.deepcopy(self.trees)
        
        # names are simple
        newItem.name = self.name
        newItem.parentNames = self.parentNames
        
        # everything else should be blank
        newItem.viewNodes = []
        newItem.nameChangeCallbacks = []
        newItem.fieldChangeCallbacks = []
        newItem.deletionCallbacks = []
        newItem.moveCallbacks = []
        newItem.selectionCallbacks = []
        newItem.clearCallbacks()
        
        memo[id(newItem)] = newItem
        return newItem

    def __repr__(self):
        string = "name: {} | fields: {} | trees: {}".format(self.name,
                                                            json.dumps(self.fields),
                                                            json.dumps(self.trees))
        return string

    def clearCallbacks(self):
        self.viewNodes = []
        self.nameChangeCallbacks = []
        self.fieldChangeCallbacks = []
        self.deletionCallbacks = []
        self.moveCallbacks = []
        self.selectionCallbacks = []
        for t in self.trees:
            self.viewNodes += [None]
            self.nameChangeCallbacks += [None]
            self.fieldChangeCallbacks += [None]
            self.deletionCallbacks += [None]
            self.moveCallbacks += [None]
            self.selectionCallbacks += [None]

    def addField(self, name, content):
        self.fields[name] = content

    def removeField(self, name, content):
        del self.fields[name]

    def writeToString(self):
        string = self.name + "\n"
        string += "    fields " + json.dumps(self.fields) + "\n"
        string += "    trees " + json.dumps(self.trees) + "\n"
        return string

    def readFromString(self, string):
        s = string.split("\n    fields ")
        self.name = s[0]
        s = s[1].split("\n    trees ")
        self.fields = json.loads(s[0])
        self.trees = json.loads(s[1])
        self.clearCallbacks()

    def printitem(self):
        print(self.name)
        for key in self.fields:
            print("    ", key)
            for subkey in self.fields[key]:
                print("        ", subkey, ":", self.fields[key][subkey])

    def registerViewNode(self, tree, node):
        self.viewNodes[tree] = node

    def registerNameChangeCallback(self, tree, callback):
        self.nameChangeCallbacks[tree] = callback

    def registerSelectionCallback(self, tree, callback):
        self.selectionCallbacks[tree] = callback

    def registerFieldChangeCallback(self, tree, callback):
        self.fieldChangeCallbacks[tree] = callback

    def registerDeletionCallback(self, tree, callback):
        self.deletionCallbacks[tree] = callback

    def registerMoveCallback(self, tree, callback):
        self.moveCallbacks[tree] = callback

    def changeName(self, newName):
        self.name = newName
        for c in self.nameChangeCallbacks:
            if c is not None:
                c(newName)
    
    def select(self, select):
        for c in self.selectionCallbacks:
            if c is not None:
                c(select)

    def changeFieldContent(self, fieldName, fieldContent):
        """
        Edit the content of a field. The content is expected to be a string and
        will be converted according to the field type.
        """

        if fieldName not in self.fields:
            return "A field with name " + fieldName + " does not exist in node " + self.name + "."
        else:
            # update field content
            field = self.fields[fieldName]
            type = field["type"]
            if fieldContent:

                # changing the content of a string field - read the string plainly
                if type in ("string", "text", "url"):
                    field["content"] = fieldContent

                # changing the content of a number - read the string into a value
                elif type == "integer":
                    try:
                        field["content"] = json.loads(fieldContent)
                    except json.JSONDecodeError:
                        field["content"] = None

                # changing the content of a timer - real change comes in a tuple, mere value update just
                # with a "True" flag
                elif type == "timer":
                    try:
                        # standard content change, indicated by a tuple
                        if len(fieldContent) == 2:
                            field["content"] = json.loads(fieldContent[0])
                            field["running_since"] = fieldContent[1]

                        # just send an empty update message if a timer is running
                        else:
                            pass

                    except json.JSONDecodeError:
                        field["content"] = None
                        field["running_since"] = None
                else:
                    return "A field of type " + type + " cannot be edited."
            else:
                field["content"] = None

            # notify changes
            self.notifyFieldChange(fieldName)

        return True

    def notifyFieldChange(self, fieldName):
        """
        notify GUI of field change
        """
        for f in self.fieldChangeCallbacks:
            if f is not None:
                f(fieldName)

    def removeFromTree(self, treeIndex):
        """
        Remove this item from the tree, and have it call all removal callbacks.
        There is no recursion, moving children up or removing them is the responsibility
        of the tree management layer
        """

        # set tree data to None
        self.trees[treeIndex] = []
        self.registerMoveCallback(treeIndex, None)
        self.registerFieldChangeCallback(treeIndex, None)
        self.registerNameChangeCallback(treeIndex, None)
        self.registerViewNode(treeIndex, None)
        self.registerSelectionCallback(treeIndex, None)

        # Notify own node and view node of deletion
        if self.deletionCallbacks[treeIndex] is not None:
            self.deletionCallbacks[treeIndex]()
            self.registerDeletionCallback(treeIndex, None)

        # Update nodes in other trees
        self.notifyFieldChange(False)

    def moveInTree(self, treeIndex, parentPath):
        """
        Move this item to a different parent at the new path
        """
        self.trees[treeIndex] = parentPath + [0]
        if self.moveCallbacks[treeIndex] is not None:
            self.moveCallbacks[treeIndex]()


class ItemPool:
    """
    A pool of items. Used to store all the tree nodes (items). The tree-related information is handled in the node
    classes.
    """

    def __init__(self):
        """
        Construct
        """
        self.items = []
        self.existing_paths = []     # all existing paths for each tree, used during loading to check for duplicates

    def writeToString(self):
        """
        Writes the whole pool to a re-loadable string
        """
        string = ""
        for it in sorted(self.items, key=lambda e: e.trees):
            string += "item " + it.writeToString() + "\n"
        return string
        
    def readFromString(self, string):
        """
        Reads the pool from a string
        """

        # split string and iterate over all parts
        string = string.split("\n\nitem ")     # items are separated by empty lines and the keyword "item"
        for s in string:
            if s != "":

                # read single item
                it = Item("")
                try:
                    it.readFromString(s)
                except json.decoder.JSONDecodeError as e:
                    raise KeyError("Corrupt data file. "
                                   "The item defined by {} in the file could not be read. "
                                   "Problem: {} when reading {}. "
                                   "Please correct manually in a text editor and then reload the file. "
                                   "".format(s, e.msg, e.doc))

                # sanity check: look for duplicated paths
                for i, t in enumerate(it.trees):
                    if len(self.existing_paths) <= i:
                        self.existing_paths.append([])
                    if t:

                        # if we found a duplicated path, raise an exception
                        if t in self.existing_paths[i]:
                            found_item = None
                            for f in self.items:
                                if f.trees[i] == t:
                                    found_item = f
                                    break
                            raise KeyError("Corrupt data file. "
                                           "The path {} in the tree {}, used by \"{}\" is already in use by \"{}\". "
                                           "Please correct manually in a text editor and then reload the file. "
                                           "".format(t, i, it.name, found_item.name))

                        # if all is fine, add item and proceed
                        else:
                            self.existing_paths[i].append(t)
                self.items += [it]

    def printpool(self):
        """
        Prints a list of items. This is a debug function.
        """
        for it in self.items:
            it.printitem()

    def copyItem(self, item):
        """
        Adds a copy of an item to the list and returns a reference to it
        """
        newitem = copy.deepcopy(item)
        newitem.viewNodes = []
        newitem.clearCallbacks()
        self.items += [newitem]
        return newitem

    def deleteItem(self, item):
        """
        Removes an item from the pool
        """
        for i, t in enumerate(item.trees):
            item.removeFromTree(i)
        self.items.remove(item)
