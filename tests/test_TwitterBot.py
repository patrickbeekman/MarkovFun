import pytest
import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../src/")
from TwitterBot import TwitterBot

pytest.tb = TwitterBot()


def test_choose_unique():
    x = pytest.tb.choose_most_unique(['hello hello hello hello', 'my name is hello'])
    assert x[0][0] == 'my name is hello'


def test_choose_unique_empty():
    x = pytest.tb.choose_most_unique([])
    assert x == []


def test_clean_text_links():
    out = pytest.tb.clean_text('http://hi.com hello')
    assert out == 'hello'


def test_clean_text_at():
    out = pytest.tb.clean_text('@Patrick hello')
    assert out == 'hello'


def test_clean_text_rt_at():
    out = pytest.tb.clean_text('RT rt Rt @Patrick hello')
    assert out == 'hello'


def test_clean_text_special_characters():
    out = pytest.tb.clean_text(' ... \n \r . ! ? hello ')
    assert out == 'hello'

