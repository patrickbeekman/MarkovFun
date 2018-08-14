import pytest
import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../src/")
from TwitterBot import TwitterBot

pytest.tb = TwitterBot()

def test_choose_unique():
    x = pytest.tb.choose_most_unique(['hello hello hello hello', 'my name is hello'])
    print(x[:-1])
    pass

