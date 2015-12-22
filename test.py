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

import tree
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
tree_p = tree.Forest("items.data")
tree_p.printForest()

# add new items as child of node e
tree_p.children[2].addItemAsChild( p.addNewItem() )
tree_p.children[2].addItemAsChild( p.addNewItem() )
tree_p.children[2].addItemAsChild( p.addNewItem() )
tree_p.children[2].addItemAsChild( p.addNewItem() )

print("writing pool to file and reading it back in")
tree_p.writeToFile("items2.data")

tree_q = tree.Forest("items2.data")
# central tree object with no parent and no children
print("creating tree:")
tree_q.printForest()


