import pytest
from treetime.item import Item

def test_item_creation():
    item = Item("Test Item")
    assert item.name == "Test Item"
    assert item.fields == {}
    assert item.trees == []

def test_item_add_field():
    item = Item("Test Item")
    item.addField("Priority", "High")
    assert "Priority" in item.fields
    assert item.fields["Priority"] == "High"

def test_item_change_name():
    item = Item("Old Name")
    item.changeName("New Name")
    assert item.name == "New Name"
