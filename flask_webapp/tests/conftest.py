"""
File:
    conftest.py
Description:

Classes:

Author:
    Adoany Berhe
"""
import __init__
import inspect
import pytest
from src import messages

@pytest.fixture
def message_classes():
    def _msg_obj_iterator():
        for name, obj in inspect.getmembers(messages):
            if inspect.isclass(obj) and ("Message" in name):
                yield obj

    return _msg_obj_iterator()

@pytest.fixture
def message_structure_names():
    names = []
    for name, obj in inspect.getmembers(messages):
        if inspect.isclass(obj) and not("Union" in name) and ("Message" in name):
            names.append(name)
    return names

#import pdb; pdb.set_trace()