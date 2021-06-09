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
    return root

def test_trie(hello_trie):
    """Utterly trivial test for __init__"""
    assert hello_trie.char == 'hello'
    assert hello_trie.end == True
    assert hello_trie.children == {}
    assert hello_trie.page_count == []


@pytest.mark.skip
def test_match():
    assert Trie.match('hello', 'help') == ('hel', 'lo', 'p')


def test_insert_simple(hello_trie):
    hello_trie.insert('goodbye', 1, 1)

    assert hello_trie.char == ''
    assert all_in(hello_trie.children, 'hello', 'goodbye')


@pytest.mark.skip
def test_insert_overlap(hello_trie):
    hello_trie.insert('help', 1, 1)

    assert hello_trie.char == 'hel'
    assert all_in(hello_trie.children, 'lo', 'p')