# coding=utf-8
import copy
import json
import item
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
        elif self.fieldType == "percentage":
            self.getValue = self.getValuePercentage
            self.getString = self.getStringPercentage
        elif self.fieldType == "node-name":
            self.getValue = self.getValueNodeName
            self.getString = self.getStringUnchanged
        
        
    def getStringPercentage(self):
        if self.sourceNode and self.getValue:
            v = self.getValue();
            if v:
                return str(round(self.getValue())) + " %"
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

    def getValuePercentage(self):
        values = self.getFieldValues()
        sum = 0
        for v in values:
            sum += v
        if sum != 0:
            return values[0]*100.0/sum
        else:
            return None
        
        
    def writeToString(self):
        string = "   field-type " + json.dumps(self.fieldType) + "\n"
        string += "      own-fields " + json.dumps(self.ownFields) + "\n"
        string += "      child-fields " + json.dumps(self.childFields) + "\n"
        string += "      sibling-fields " + json.dumps(self.siblingFields) + "\n"
        string += "      parent-fields " + json.dumps(self.parentFields) + "\n"
        return string


    def readFromString(self, string):
        
        s = string.split("\n      field-type ")
        name = json.loads(s[0])
        s = s[1].split("\n      own-fields ")
        self.fieldType = json.loads(s[0])
        s = s[1].split("\n      child-fields ")
        self.ownFields = json.loads(s[0])
        s = s[1].split("\n      sibling-fields ")
        self.childFields = json.loads(s[0])
        s = s[1].split("\n      parent-fields ")
        self.siblingFields = json.loads(s[0])
        self.parentFields = json.loads(s[1])
        self.initFieldType()
        
        return name





class Node:

    """A tree structure consisting of nodes that are parents of nodes etc. A node is a view-object to display one item."""
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



    '''Applies the function to each node in the tree. The function must receive one parameter and return one parameter. The return value is used as parameter for the next function call. The value Parameter is used in the first call.'''
    def map(self, function, parameter, depthFirst):
        
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
        # register callbacks with source node
        if self.item is not None:
            self.item.registerNameChangeCallback(self.tree, self.notifyNameChange)
            self.item.registerFieldChangeCallback(self.tree, lambda x: self.notifyFieldChange(x, True))
            self.item.registerDeletionCallback(self.tree, self.notifyDeletion)
            self.item.registerViewNode(self.tree, self)

    def registerViewNode(self, viewNode):
        self.viewNode = viewNode
        
    def findNode(self, path, currentIndex):
        
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
        node = Node(self, self.tree, self.path + [len(self.children)])
        self.children += [node]
        return node


    def addNodeAsChild(self, node):
        self.children += [node]
        node.parent = self
        self.renumberChildren()
        for f in self.fields:
            self.notifyFieldChange(f, True)
        
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


    """Creates a node and links it to the item. Updates the item's forest indexes."""
    def addItemAsChild(self, item):
        
        node = self.addChild()
        node.item = item
        node.name = item.name
        node.initFields(self.fields)
        node.registerCallbacks()
        item.trees[node.tree] = node.path
        return node


    def initFields(self, fields):
        self.fields = copy.deepcopy(fields)
        
        # first set all fields to myself
        for name,field in self.fields.items():
            field.sourceNode = self
        
        # and only then send notification
        for name,field in self.fields.items():
            self.notifyFieldChange(name, True)


    '''Finds the first node of a given name in the tree.'''
    def findNodeByName(self, name):
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


    def notifyNameChange(self, newName):
        self.name = newName
        if self.nameChangeCallback is not None:
            self.nameChangeCallback(newName)
        for c in self.children:
            for n in c.item.viewNodes:
                if n is not None:
                    n.notifyParentNameChange(self.tree, newName)
            
            
    def notifyParentNameChange(self, tree, newName):
        for f in self.fields:
            if self.fields[f].fieldType == "node-name":
                if tree in self.fields[f].parentFields:
                    self.fields[f].cache = newName
                    self.notifyFieldChange(f,False)


    '''Callback, called whenever a field in a related item has changed.'''
    def notifyFieldChange(self, fieldName, recursion):
        
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
            


    '''Callback, called whenever the underlying item was deleted.'''
    def notifyDeletion(self):
        
        # unlink item
        self.item = None
        
        # remove myself from my parent
        if self.deletionCallback is not None:
            self.deletionCallback()
            
        # make parent renumber children
        self.parent.removeChild(self)



'''A tree inside a forest. One item can appear several times in the forest, but only once in each tree.'''
class Tree(Node):


    def __init__(self, parent, index):
        """Initialise"""
        
        super().__init__(parent, index, [])
        self.fields = {}
        self.name = ""
        #self.fields["description"] = Field(None, ["description"], [], "itemString")
        #self.fields["single sums"] = Field(None, ["amount"], ["single sums"], "itemSum")
        #self.fields["single percentage"] = Field(None, ["amount"], [], "itemPercentage")
        #self.fields["total percentage"] = Field(None, [], ["single sums"], "nodePercentage")


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
            string += "   field " + json.dumps(n) + "\n"
            string += "   " + f.writeToString()
        return string


    def readFromString(self, string):
        fieldStrings = string.split("\n   field ")
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
            self.itemPool = item.ItemPool()
            self.itemPool.readFromString(s[1])
            self.createPaths()
            self.readFromString(s[0])
        self.createPaths()
        

