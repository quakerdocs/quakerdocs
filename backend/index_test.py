import pytest
from index2 import Trie


def all_in(container, *items):
    return all(i in container for i in items)


@pytest.fixture
def hello_trie():
    return Trie('hello', True)


def test_trie(hello_trie):
    """Utterly trivial test for __init__"""
    assert hello_trie.char == 'hello'
    assert hello_trie.end == True
    assert hello_trie.children == {}
    assert hello_trie.page_count == []


def test_match():
    assert Trie.match('hello', 'help') == ('hel', 'lo', 'p')


def test_insert_simple(hello_trie):
    hello_trie.insert('goodye', 1, 1)

    assert hello_trie.char == ''
    assert all_in(hello_trie.children, 'hello', 'goodbye')


def test_insert_overlap(hello_trie):
    hello_trie.insert('help', 1, 1)

    assert hello_trie.char == 'hel'
    assert all_in(hello_trie.children, 'lo', 'p')