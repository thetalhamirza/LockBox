from lockbox import validation, initializeKeys, executeChoice, addPassword
import pytest


def test_validation():
    assert validation("ABC") == False
    assert validation("abc") == False
    assert validation("123") == False

def test_initializeKeys():
    assert initializeKeys('newUser') == None
    assert initializeKeys('existingUser') == None

def test_executeChoice():
    with pytest.raises(ValueError):
        executeChoice(100)
    with pytest.raises(ValueError):
        executeChoice(5)
    