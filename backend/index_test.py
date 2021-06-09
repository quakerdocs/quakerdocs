import pytest
from index2 import Trie


def all_in(container, *items):
    return all(i in container for i in items)


@pytest.fixture
def hello_trie():
    new = Trie('hello')
    new.end = True
    return new

@pytest.fixture
def root(hello_trie):
    r = Trie('')
    r.children['hello'] = hello_trie
    return r

def test_trie(hello_trie):
    """Utterly trivial test for __init__"""
    assert hello_trie.char == 'hello'
    assert hello_trie.end == True
    assert hello_trie.children == {}
    assert hello_trie.page_count == []


def test_match():
    assert Trie.match('hello', 'help') == ('hel', 'lo', 'p')


def test_insert_simple(root):
    root.insert('goodbye', 1, 1)

    assert root.char == ''
    assert all_in(root.children, 'hello', 'goodbye')


def test_insert_overlap(root):
    root.insert('help', 1, 1)

    assert 'hel' in root.children and len(root.children) == 1
    assert all_in(root.children['hel'].children, 'lo', 'p')