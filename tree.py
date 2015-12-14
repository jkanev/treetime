# coding=utf-8
import copy
import json
import item

class Field:
	"""A set of instructions to view/display the content of data items. Fields are part of nodes, and are stored in templates."""

	def __init__(self, node=None, sourceItemFields=[], sourceNodeFields=[], fieldType=None):
		"""Initialises the class, links the source node, field type, and sets the evaluation method."""
		
		self.sourceItemFields = sourceItemFields
		self.sourceNodeFields = sourceNodeFields
		self.sourceNode = node
		self.getValue = None
		self.getString = None
		self.fieldType = fieldType
		if (self.fieldType != ""):
			self.initFieldType()
		
		
	def initFieldType(self):
		
		if self.fieldType == "itemString":
			self.getValue = self.getValueItemString
			self.getString = self.getStringUnchanged
		elif self.fieldType == "itemSum":
			self.getValue = self.getValueItemSum
			self.getString = self.getStringUnchanged
		elif self.fieldType == "itemPercentage":
			self.getValue = self.getValueItemPercentage
			self.getString = self.getStringPercentage
		elif self.fieldType == "nodePercentage":
			self.getValue = self.getValueNodePercentage
			self.getString = self.getStringPercentage
			
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
	
	def getValueItemString(self):
		key = self.sourceItemFields[0]
		if key in self.sourceNode.item.fields:
			return self.sourceNode.item.fields[key]["content"]
		else:
			return ""
	
	def getValueItemSum(self):
		value = self.sourceNode.item.fields.get(self.sourceItemFields[0])
		if value:
			value = value["content"]
		else:
			value = 0
			
		for child in self.sourceNode.children:
			field = child.fields[self.sourceNodeFields[0]]
			value += field.getValue()
					
		return value
	
	def getValueItemPercentage(self):
		sumSiblings = 0;
		for sibling in self.sourceNode.parent.children:
			sourceField = sibling.item.fields.get(self.sourceItemFields[0])
			if sourceField:
				sumSiblings += sourceField["content"]
			else:
				break
		ownValue = self.sourceNode.item.fields.get(self.sourceItemFields[0])
		if ownValue:
			ownValue = ownValue["content"]
		else:
			return None
		if sumSiblings != 0:
			return ownValue / sumSiblings * 100
		else:
			return None
	
	def getValueNodePercentage(self):
		sumSiblings = 0;
		for sibling in self.sourceNode.parent.children:
			
			sourceField = sibling.fields.get(self.sourceNodeFields[0])
			if sourceField:
				sumSiblings += sourceField.getValue()
			else:
				break
		ownValue = self.sourceNode.fields.get(self.sourceNodeFields[0])
		if ownValue:
			ownValue = ownValue.getValue()
		else:
			return None
		if sumSiblings != 0:
			return ownValue / sumSiblings * 100
		else:
			return None
	
	
	def writeToString(self):
		string = "   field-type " + json.dumps(self.fieldType) + "\n"
		string += "      item-fields " + json.dumps(self.sourceItemFields) + "\n"
		string += "      tree-fields " + json.dumps(self.sourceNodeFields) + "\n"
		return string
	
	
	def readFromString(self, string):
		
		s = string.split("\n      field-type ")
		name = json.loads(s[0])
		s = s[1].split("\n      item-fields ")
		self.fieldType = json.loads(s[0])
		s = s[1].split("\n      tree-fields ")
		self.sourceItemFields = json.loads(s[0])
		self.sourceNodeFields = json.loads(s[1])
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
		self.nameChangeCallback = None
		self.fieldChangeCallback = None
		self.deletionCallback = None
		
	
	def printForest(self, indent=0):
		
		# create leading white space
		s = ""
		for i in range(indent):
			s += "    "
		s += " → " + str(self.tree)
		for p in self.path:
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
	

	def registerCallbacks(self):
		# register callbacks with source node
		if self.item is not None:
			self.item.registerNameChangeCallback(self.notifyNameChange)
			self.item.registerFieldChangeCallback(lambda x: self.notifyFieldChange(x, True))
			self.item.registerDeletionCallback(self.notifyDeletion)
	

	def findNode(self, path, currentIndex):
		
		# either recurse deeper
		if currentIndex < len(path):
			childNumber = path[currentIndex]
			return self.children[childNumber].findNode(path, currentIndex+1)
		
		# or, return myself
		else:
			return self
	
	
	def addChild(self):
		node = Node(self, self.tree, self.path + [len(self.children)])
		self.children += [node]
		return node
	
	
	def addItemAsChild(self, item):
		"""Creates a node and links it to the item. Updates the item's forest indexes."""
		
		node = self.addChild()
		node.item = item
		node.name = item.name
		node.initFields(self.fields)
		node.registerCallbacks()
		item.trees[node.tree] = node.path
		return node
	
	
	def initFields(self, viewTemplate):
		self.fields = copy.deepcopy(viewTemplate)
		for name,field in self.fields.items():
			field.sourceNode = self
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
		if self.nameChangeCallback is not None:
			self.nameChangeCallback(newName)
	
	
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
	def notifyDeletion(self, fieldName, fieldContent):
		if self.deletionCallback is not None:
			self.deletionCallback()



'''A tree inside a forest. One item can appear several times in the forest, but only once in each tree.'''
class Tree(Node):
	
	
	def __init__(self, parent, index):
		"""Initialise"""
		
		super().__init__(parent, index, [])
		self.viewTemplate = {}
		self.name = ""
		self.viewTemplate["description"] = Field(None, ["description"], [], "itemString")
		self.viewTemplate["single sums"] = Field(None, ["amount"], ["single sums"], "itemSum")
		self.viewTemplate["single percentage"] = Field(None, ["amount"], [], "itemPercentage")
		self.viewTemplate["total percentage"] = Field(None, [], ["single sums"], "nodePercentage")
	

	"""Sort the item into the forest, creating existing nodes on the fly if missing."""
	def createPathTo(self, item, treeindex):
		
		# per tree: loop over all nodes, creating if necessary
		# per node: create final node and link it to item
		if item.trees[treeindex]:
			n = item.trees[treeindex][0]
			while n >= len(self.children):
				self.addChild()
			self.children[n].createPathTo(item, treeindex, 1, self.viewTemplate)
	
	"""Sort the item into the forest, creating existing nodes on the fly if missing."""
	def findNode(self, path):
		
		# per tree: loop over all nodes, creating if necessary
		return super().findNode(path, 0)
	
	def writeToString(self):
		string = "tree " + json.dumps(self.name) + "\n"
		for n,f in self.viewTemplate.items():
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
				self.viewTemplate[name] = f
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
		

