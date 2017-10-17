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
from .item import *
import datetime

class Field:
    """A set of instructions to view/display the content of data items. Fields are part of nodes, and are stored in templates."""

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


    ''' Gets all values of all related fields in a list. Order is: own fields first, then child fields, then sibling fields, then parent fields. Item fields of the same name have precence over tree fields.'''
    def getFieldValues(self):
        
        values = []
        
        # look in own fields
        node = self.sourceNode
        if node.item is not None: # don't try to get values from the root node
            for f in self.ownFields:
                if f in node.fields:
                    values += [node.fields[f].getValue()]
                elif f in node.item.fields:
                    values += [node.item.fields[f]["content"]]
        
        # look in child fields
        node = self.sourceNode
        for f in self.childFields:
            for c in node.children:
                if f in c.fields:
                    values += [c.fields[f].getValue()]
                elif f in c.item.fields:
                    values += [c.item.fields[f]["content"]]
        
        # look in sibling fields
        node = self.sourceNode.parent
        for f in self.siblingFields:
            for c in node.children:
                if c != self.sourceNode:
                    if f in c.fields:
                        values += [c.fields[f].getValue()]
                    elif f in c.item.fields:
                        values += [c.item.fields[f]["content"]]

        # look in parent fields
        node = self.sourceNode.parent
        for f in self.parentFields:
            if f in node.item.fields:
                values += [node.fields[f].getValue()]
            elif f in node.fields:
                values += [node.item.fields[f]["content"]]
        
        # return
        return values


    def initFieldType(self):
        
        if self.fieldType == "string":
            self.getValue = self.getValueString
            self.getString = self.getStringUnchanged
        elif self.fieldType == "sum":
            self.getValue = self.getValueSum
            self.getString = self.getStringUnchanged
        elif self.fieldType == "mean":
            self.getValue = self.getValueMean
            self.getString = self.getStringUnchanged
        elif self.fieldType == "mean-percent":
            self.getValue = self.getValueMean
            self.getString = self.getStringPercent
        elif self.fieldType == "ratio":
            self.getValue = self.getValueRatio
            self.getString = self.getStringUnchanged
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
            v = self.getValue();
            if v:
                whitespace = ""
                if v<0.1:
                    whitespace = "  "
                elif v<1.0:
                    whitespace = " "
                return whitespace + str(round(100*v)) + " %"
            else:
                return ""
        else:
            return ""


    def getStringUnchanged(self):
        if self.sourceNode and self.getValue:
            return str(self.getValue())
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
                tree = tree.children[t]
                # find node in tree
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
                tree = tree.children[t]
                # find node in tree
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
        values = self.getFieldValues()
        s = ""
        for v in values:
            s += str(v)
        return s


    def getValueSum(self):
        values = self.getFieldValues()
        sum = 0
        for v in values:
            sum += v
        return sum


    def getValueMean(self):
        values = self.getFieldValues()
        sum = 0.0
        n = 0.0
        for v in values:
            n += 1.0
            sum += v
        if n > 0.0:
            return sum/n
        else:
            return 0.0

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



    def map(self, function, parameter, depthFirst):
        ''' Applies the function to each node in the tree. The function must receive one parameter and return one parameter. The return value is used as parameter for the next function call. The value Parameter is used in the first call.'''
        
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


    
    def createPathTo(self, item, treeindex, nodeindex, viewtemplate):
        """ Links an item into a tree, using the given path. Empty nodes get created on the way."""
        
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

        
    def registerCallbacks(self, register=True):
        """
        Register callbacks from the parent (QNode), so changes from the tree layer
        can be shown in the QT GUI layer
        """
        if self.item is not None:
            self.item.registerNameChangeCallback(self.tree, self.notifyNameChange)
            self.item.registerFieldChangeCallback(self.tree, lambda x: self.notifyFieldChange(x, True))
            self.item.registerDeletionCallback(self.tree, self.notifyDeletion)
            self.item.registerSelectionCallback(self.tree, lambda x: self.notifySelection(x))
            self.item.registerViewNode(self.tree, self)

    def registerViewNode(self, viewNode):
        """
        Register the respective QT GUI view node with the node
        """
        self.viewNode = viewNode
        

    def findNode(self, path, currentIndex):
        """
        Recursive function to walk down a path in a tree and return the node at the last step
        """
        
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
            self.registerCallbacks(False)
            self.children.remove(child)
            self.renumberChildren()
            for f in self.fields:
                self.notifyFieldChange(f, True)


    def renumberChildren(self):
        for i,c in enumerate(self.children):
            c.path = self.path + [i]
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
        for name,field in self.fields.items():
            field.sourceNode = self
        
        # and only then send notification
        for name,field in self.fields.items():
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

    def registerSelectionCallback(self, callback):
        self.selectionCallback = callback


    def notifyNameChange(self, newName):
        """
        Callback used to notify a node of a name change. Changes the name, then
        recreates strings for the fiels 'node-name' and 'node-path'.
        Recurses down the tree to update the node-path strings of all children.
        """

        # function to recurse down the tree
        def notifyParentNameChange(node, tree):
            for f in node.fields:
                if node.fields[f].fieldType in ('node-name', 'node-path'):
                    if tree in node.fields[f].parentFields:
                        node.fields[f].cache = node.fields[f].getString()
                        node.notifyFieldChange(f, False)
                    for c in node.children:
                        for n in c.item.viewNodes:
                            if n is not None:
                                notifyParentNameChange(n, self.tree)

        # notify name change and start recursion
        self.name = newName
        if self.nameChangeCallback is not None:
            self.nameChangeCallback(newName)
        for c in self.children:
            for n in c.item.viewNodes:
                if n is not None:
                    notifyParentNameChange(n, self.tree)
            
            
    def notifyFieldChange(self, fieldName, recursion):
        """
        Callback, called whenever a field in a related item has changed.
        """

        if self.fieldChangeCallback is not None:
            for f in self.fields:
                self.fieldChangeCallback(f, self.fields[f].getString())
        
        # build list of children
        if recursion:
                    
            # notify all siblings, non-recursive
            if self.parent is not None:
                for c in self.parent.children:
                    if c is not self:
                        c.notifyFieldChange(fieldName, False)
                    
                # notify all parents, recursive
                self.parent.notifyFieldChange(fieldName, True)
            


    def notifyDeletion(self):
        """
        Callback, called whenever the underlying item was deleted.
        """

        # unlink item
        self.item = None
        
        # remove myself from my parent
        if self.deletionCallback is not None:
            self.deletionCallback()
            
        # make parent renumber children
        self.parent.removeChild(self)


    '''Callback, called whenever the underlying item was selected.'''
    def notifySelection(self, select):
        
        # remove myself from my parent
        if self.selectionCallback is not None:
            self.selectionCallback(select)


'''A tree inside a forest. One item can appear several times in the forest, but only once in each tree.'''
class Tree(Node):


    def __init__(self, parent, index):
        """Initialise"""
        
        super().__init__(parent, index, [])
        self.fields = {}
        self.name = ""
        #self.fields["description"] = Field(None, ["description"], [], "itemString")
        #self.fields["single sums"] = Field(None, ["amount"], ["single sums"], "itemSum")
        #self.fields["single percentage"] = Field(None, ["amount"], [], "itemPercent")
        #self.fields["total percentage"] = Field(None, [], ["single sums"], "nodePercent")


    """Sort the item into the forest, creating existing nodes on the fly if missing."""
    def createPathTo(self, item, treeindex):
        
        # per tree: loop over all nodes, creating if necessary
        # per node: create final node and link it to item
        if item.trees[treeindex]:
            n = item.trees[treeindex][0]
            while n >= len(self.children):
                self.addChild()
            self.children[n].createPathTo(item, treeindex, 1, self.fields)

    """Sort the item into the forest, creating existing nodes on the fly if missing."""
    def findNode(self, path):
        
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
                f = Field();
                name = f.readFromString(fs)
                self.fields[name] = f
                self.fieldOrder += [name]


class Forest(Node):
    """ The trunk node containing trees, that contain the nodes. Also manages the node templates."""


    def __init__(self, filename):
        """Initialise"""
        
        super().__init__(None, None, [])
        self.itemPool = None
        self.readFromFile(filename)


    """Sort all items from the itempool into the forest, creating the forest structure as defined by the
    items' node indexes"""
    def createPaths(self):
        
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
        itemString = self.itemPool.writeToString()
        with open(filename, "w") as f:
            f.write("--trees--\n\n")
            f.write(treeString)
            f.write("--item-pool--\n\n")
            f.write(itemString)


    def readFromFile(self, filename):
        with open(filename, "r") as f:
            s = f.read()
            s = s.split("--trees--")[1]
            s = s.split("--item-pool--")
            self.itemPool = ItemPool()
            self.itemPool.readFromString(s[1])
            self.createPaths()
            self.readFromString(s[0])
        self.createPaths()
        

