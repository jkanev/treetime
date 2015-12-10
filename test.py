# coding=utf-8
import item

# create four single items and test read/write
a = item.Item("a", '{"description": {"content": "Item A", "type": "string"} }','[[0],[],[0]]')

b = item.Item("b", '{"description": {"content": "Item B", "type": "string"} }','[[0,0],[],[1]]')

c = item.Item("c", '{}', '[[0,1],[],[]]')
c.addField("description", {"type":"string", "content":"Item C"})
c.addField("amount", {"type":"integer", "content":4})

d = item.Item("d", "{}","[[0,0,0],[],[]]")
d.addField("description", {"type":"string", "content":"Item D"})
d.addField("amount", {"type":"integer", "content":1})

e = item.Item("e", "{}","[[0,0,1],[],[]]")
e.addField("description", {"type":"string", "content":"Item E"})
e.addField("amount", {"type":"integer", "content":2})

x = item.Item("x", '{"description": {"content": "default node", "type": "string"}, "amount": {"content": 23, "type": "integer"} }','[[],[],[]]')

print("creating tree with amounts in d,e,c:")
print("      a      ")
print("     / \     ")
print("    b   c(4) ")
print("   /  \      ")
print(" d(1)  e(2)  ")

p = item.ItemPool()
p.items = [x,a,b,c,d,e]
p.defaultItem = x

# central tree object with no parent and no children
print("creating tree:")
tree_p = item.Tree()
tree_p.createPaths(p)
tree_p.printTree()

# add new items as child of node e
tree_p.children[2].addItemAsChild( p.addNewItem() )
tree_p.children[2].addItemAsChild( p.addNewItem() )
tree_p.children[2].addItemAsChild( p.addNewItem() )
tree_p.children[2].addItemAsChild( p.addNewItem() )

print("writing pool to file and reading it back in")
p.writeToFile("items.data")
q = item.ItemPool()
q.readFromFile("items.data")
# central tree object with no parent and no children
print("creating tree:")
tree_q = item.Tree()
tree_q.createPaths(q)
tree_q.printTree()


