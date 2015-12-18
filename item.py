# coding=utf-8
import copy
import json



"""The list/forest item containing the actual data"""
class Item:

	def __init__(self, name, fieldstring='{}', treestring='[]'):
		self.name = name
		self.parentNames = []
		self.fields = json.loads(fieldstring)
		self.trees = json.loads(treestring)
		self.viewNodes = []
		self.nameChangeCallbacks = []
		self.fieldChangeCallbacks = []
		self.deletionCallbacks = []
		self.clearCallbacks()
		
		
	def clearCallbacks(self):
		self.viewNodes = []
		self.nameChangeCallbacks = []
		self.fieldChangeCallbacks = []
		self.deletionCallbacks = []
		for t in self.trees:
			self.viewNodes += [None]
			self.nameChangeCallbacks += [None]
			self.fieldChangeCallbacks += [None]
			self.deletionCallbacks += [None]
		
	
	def addField(self, name, content):
		self.fields[name] = content
	
	
	def removeField(self, name, content):
		del self.fields[name]
	
	
	def writeToString(self):
		string = self.name + "\n"
		string += "   fields " + json.dumps(self.fields) + "\n"
		string += "   trees " + json.dumps(self.trees) + "\n"
		return string
	
	
	def readFromString(self, string):
		s = string.split("\n   fields ")
		self.name = s[0]
		s = s[1].split("\n   trees ")
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
			

	def registerFieldChangeCallback(self, tree, callback):
		self.fieldChangeCallbacks[tree] = callback
	
	
	def registerDeletionCallback(self, tree, callback):
		self.deletionCallbacks[tree] = callback
	
	
	def changeName(self, newName):
		self.name = newName
		for c in self.nameChangeCallbacks:
			if c is not None:
				c(newName)
	

	''' Edit the content of a field. The content is expected to be a string and will be converted accourding to the field type. '''
	def changeFieldContent(self, fieldName, fieldContent):
		
		if fieldName not in self.fields:
			return "A field with name " + fieldName + " does not exist in node " + self.name + "."
		else:
			# update field content
			field = self.fields[fieldName]
			type = field["type"]
			if type == "string":
				field["content"] = fieldContent
			elif type == "integer":
				field["content"] = json.loads(fieldContent)
			else:
				return "A field of type " + type + " cannot be edited."
			
			# notify GUI of field change
			for f in self.fieldChangeCallbacks:
				f(fieldName)
		
		return True
	
	
	''' Remove this item from the tree, and have it call all removal callbacks. '''
	def removeFromTree(self, treeIndex):
		
		self.trees[treeIndex] = [];
		self.deletionCallbacks[treeIndex]();
		

class ItemPool:
	def __init__(self):
		self.items = []
		self.defaultItem = None
		
	def writeToString(self):
		string = ""
		for it in self.items:
			string += "item " + it.writeToString() + "\n"
		return string
		
	def readFromString(self, string):
		string = string.split("\n\nitem ") # items are separated by empty lines and the keyword "item"
		for s in string:
			if s != "":
				it = Item("")
				it.readFromString(s)
				self.items += [it]
				if self.defaultItem is None:
					self.defaultItem = it
	
	def printpool(self):
		for it in self.items:
			it.printitem()
			

	"""Adds a copy of the default item to the list and returns a reference to it"""
	def addNewItem(self):
		return self.copyItem(self.defaultItem)
	
	
	"""Adds a copy of the default item to the list and returns a reference to it"""
	def copyItem(self, item):
		newitem = copy.deepcopy(item)
		newitem.viewNodes = []
		newitem.clearCallbacks()
		self.items += [newitem]
		return newitem
