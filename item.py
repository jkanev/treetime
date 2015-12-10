# coding=utf-8
import copy
import json



class Item:
	"""The list/tree item containing the actual data"""

	def __init__(self, name, fieldstring='{}', treestring='[]'):
		self.name = name
		self.fields = json.loads(fieldstring)
		self.trees = json.loads(treestring)
		self.viewNodes = []
		
	
	def addField(self, name, content):
		self.fields[name] = content
	
	
	def removeField(self, name, content):
		del self.fields[name]
	
	
	def writeToString(self):
		string = "\n     " + self.name
		string += "\n     " + json.dumps(self.fields)
		string += "\n     " + json.dumps(self.trees)
		return string
	
	
	def readFromString(self, string):
		s = string.split("\n     ")
		self.name = s[1]
		self.fields = json.loads(s[2])
		self.trees = json.loads(s[3])
		return self
	
	
	def printitem(self):
		print(self.name)
		for key in self.fields:
			print("    ", key)
			for subkey in self.fields[key]:
				print("        ", subkey, ":", self.fields[key][subkey])



class ItemPool:
	def __init__(self):
		self.items = []
		
	def writeToString(self):
		string = ""
		for it in self.items:
			string += "\n          " + it.writeToString()
		return string
		
	def readFromString(self, string):
		string = string.split("\n          ") # items are separated by ten spaces on single lines
		for s in string:
			if s != "":
				it = Item("")
				self.items += [it.readFromString(s)]
	
	def writeToFile(self, filename):
		string = self.writeToString()
		with open(filename, "w") as f:
			f.write(string)
		
	def readFromFile(self, filename):
		with open(filename, "r") as f:
			string = f.read()
		self.readFromString(string)
		
	def printpool(self):
		for it in self.items:
			it.printitem()
			
	def addNewItem(self):
		"""Adds a copy of the default item to the list and returns a reference to it"""
		
		item = copy.deepcopy(self.defaultItem)
		self.items += [item]
		return item



class Node:
	"""A tree structure consisting of nodes that are parents of nodes etc. A node is a view-object to display one item."""
	def __init__(self, parent, branch, path):
		self.parent = parent
		self.children = []
		self.item = None
		self.name = ""
		self.fields = {}
		self.fieldOrder = []
		self.fieldOrder = ["description", "single sums", "single percentage", "total percentage"]
		self.branch = branch
		self.path = path;
		
	
	def printTree(self, indent=0):
		
		# create leading white space
		s = ""
		for i in range(indent):
			s += "    "
		s += " → " + str(self.branch)
		for p in self.path:
			s += "[" + str(p) + "]"
		s += " " + self.__class__.__name__ + " "
		
		# append item content and print
		s += self.name
		for name,field in self.fields.items():
			s += " [" + name + "] " + field.getString()
		print(s)
		
		# recurse
		for i in range(len(self.children)):
			self.children[i].printTree(indent + 1)
	
	
	def createPathTo(self, item, branchindex, nodeindex):
		
		# either recurse deeper
		if nodeindex < len(item.trees[branchindex]):
			n = item.trees[branchindex][nodeindex]
			while n >= len(self.children):
				self.addChild()
			self.children[n].createPathTo(item,branchindex,nodeindex+1)
		
		# or, if in final node, link item
		else:
			self.item = item
			self.name = item.name
			self.fields = {}
			self.fields["description"] = Field(self, ["description"], [], "itemString")
			self.fields["single sums"] = Field(self, ["amount"], ["single sums"], "itemSum")
			self.fields["single percentage"] = Field(self, ["amount"], [], "itemPercentage")
			self.fields["total percentage"] = Field(self, [], ["single sums"], "nodePercentage")
			item.viewNode = self
	
	
	def addChild(self):
		node = Node(self, self.branch, self.path + [len(self.children)])
		self.children += [node]
		return node
	
	
	def addItemAsChild(self, item):
		"""Creates a node and links it to the item. Updates the item's tree indexes."""
		
		node = self.addChild()
		node.item = item
		item.trees[node.branch] = node.path



class Field:
	"""A set of instructions to view/display the content of data items. Fields are part of nodes, and are stored in templates."""

	def __init__(self, node, sourceItemFields, sourceNodeFields, fieldType):
		"""Initialises the class, links the source node, field type, and sets the evaluation method."""
		
		self.sourceItemFields = sourceItemFields
		self.sourceNodeFields = sourceNodeFields
		self.sourceNode = node
		self.getValue = None
		self.getString = None
		if fieldType is "itemString":
			self.getValue = self.getValueItemString
			self.getString = self.getStringUnchanged
		elif fieldType is "itemSum":
			self.getValue = self.getValueItemSum
			self.getString = self.getStringUnchanged
		elif fieldType is "itemPercentage":
			self.getValue = self.getValueItemPercentage
			self.getString = self.getStringPercentage
		elif fieldType is "nodePercentage":
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
		return self.sourceNode.item.fields[self.sourceItemFields[0]]["content"]
	
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



class Branch(Node):
	"""A branch of a tree. Branches are just underneath the trunk. One item can appear several times in the tree,
	but only once in each branch."""
	
	
	def __init__(self, parent, index, viewTemplate):
		"""Initialise"""
		
		super().__init__(parent, index, [])
		self.viewTemplate = viewTemplate
	
	
	def createPathTo(self, item, branchindex):
		"""Sort the item into the tree, creating existing nodes on the fly if missing."""
		
		# per branch: loop over all nodes, creating if necessary
		# per node: create final node and link it to item
		if item.trees[branchindex]:
			n = item.trees[branchindex][0]
			while n >= len(self.children):
				self.addChild()
			self.children[n].createPathTo(item,branchindex,1)



class Tree(Node):
	""" The trunk node containing branches, that contain the nodes. Also manages the node templates."""
	
	
	def __init__(self):
		"""Initialise"""
		
		super().__init__(None, None, [])
	
	
	def createPaths(self, itempool):
		"""Sort all items from the itempool into the tree, creating the tree structure as defined by the
		items' node indexes"""
		
		for item in itempool.items:
			self.createPathTo(item)
	
	
	def createPathTo(self, item):
		
		# start: loop over all branches, creating if necessary
		for b in range(len(item.trees)):
			if b >= len(self.children):
				self.addBranch("tisti-tasti-testi")
			if item.trees[b]:
				self.children[b].createPathTo(item,b)
	
	
	def addBranch(self, viewTemplate):
		self.children += [Branch(self, len(self.children), viewTemplate)]


