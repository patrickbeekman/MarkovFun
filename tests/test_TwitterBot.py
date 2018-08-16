import pytest
import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../src/")
from TwitterBot import TwitterBot

pytest.tb = TwitterBot()


def test_choose_unique():
    x = pytest.tb.choose_most_unique(['hello hello hello hello', 'my name is hello'])
    assert x[-1][0] == 'my name is hello'


def test_choose_unique_empty():
    x = pytest.tb.choose_most_unique([])
    assert x == []
