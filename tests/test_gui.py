import sys
import os
from PyQt6 import QtWidgets, QtCore

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from treetime.treetime import TreeTimeWindow

class TestGui:
    """
    Test class for GUI operations in TreeTime.
    Contains tests for adding nodes and verifying their presence.
    """
    
    def setup_method(self):
        """Initializes the QApplication and TreeTimeWindow for each test."""
        self.app = QtWidgets.QApplication.instance()
        if self.app is None:
            self.app = QtWidgets.QApplication(sys.argv)
        self.window = TreeTimeWindow()
        
        # Mocking writing to file to avoid IO side effects during tests
        self.window.delayedWriteToFile = lambda *args, **kwargs: None
        
        # Ensure a clean state by starting a new file
        self.window.newFile("test_temp.trt")
        if os.path.exists("test_temp.trt"):
            os.remove("test_temp.trt")

    def teardown_method(self):
        """Cleans up the window after each test."""
        self.window.close()

    def add_sibling(self):
        """
        Adding a node as sibling and assert that item count has increased
        """
        node = self.window.currentItem.viewNodes[self.window.currentTree]
        amount = len(node.parent.children)
        self.window.pushButtonNewSibling.click()
        assert len(node.parent.children) == amount+1, "No new item was added"

    def add_child(self):
        """
        Adding a node as child and assert that item count has increased
        """
        node = self.window.currentItem.viewNodes[self.window.currentTree]
        amount = len(node.children)
        self.window.pushButtonNewChild.click()
        assert len(node.children) == amount+1, "No new item was added"

    def change_name(self, name):
        """
        Sets the name of the current node and checks if it was set correctly
        """
        # set name
        self.window.tableWidget.setItem(1, 3, QtWidgets.QTableWidgetItem(name))
        assert self.window.currentItem.name == name, "Sibling node was not added successfully."

    def select_node(self, name):
        """
        Selects a node in the currently open tree
        :param name: the node name
        """
        treeWidget = self.window.treeWidgets[self.window.currentTree]
        items = treeWidget.findItems(name, QtCore.Qt.MatchFlag.MatchExactly | QtCore.Qt.MatchFlag.MatchRecursive)
        if items:
            treeWidget.setCurrentItem(items[0])
            treeWidget.itemClicked.emit(items[0], 0)
        assert self.window.currentItem.name == name, "Node selection failed."

    def test_add_delete_simple_tree(self):
        """
        Adds a couple of siblings and checks them
        """
        self.add_sibling()
        self.change_name('node 0')
        self.add_sibling()
        self.change_name('node 1')
        self.add_sibling()
        self.change_name('node 2')
        self.add_sibling()
        self.change_name('node 3')

        self.select_node('node 0')
        self.add_child()
        self.change_name('node 0.0')
        self.add_sibling()
        self.change_name('node 0.1')
        self.add_sibling()
        self.change_name('node 0.2')
        self.add_sibling()
        self.change_name('node 0.3')

        self.select_node('node 1')
        self.add_child()
        self.change_name('node 1.0')
        self.add_sibling()
        self.change_name('node 1.1')
        self.add_sibling()
        self.change_name('node 1.2')
        self.add_sibling()
        self.change_name('node 1.3')


if __name__ == "__main__":
    # Standard pytest execution
    import pytest
    pytest.main([__file__])
