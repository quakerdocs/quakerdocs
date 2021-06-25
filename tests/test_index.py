"""
Module for testing functionality related to search index generation.

To run tests, go to project root and use
"python -m pytest --cov=src.quaker_lib.index --cov term-missing tests/"
"""

import pytest
from src.quaker_lib.index import *


def all_in(container, *items):
    return all(i in container for i in items)


@pytest.fixture
def hello_trie():
    new = Trie('hello')
    new.end = True
    return new


@pytest.fixture
def hello_root(hello_trie):
    r = Trie('')
    r.children['hello'] = hello_trie
    return r


@pytest.fixture
def bigger_trie(hello_root):
    hello_root.insert('help', 1, 1)
    hello_root.insert('goodbye', 1, 1)
    hello_root.insert('hi', 1, 1)

    for i in range(2000):
        hello_root.insert('hello', i, i)

    return hello_root


def test_trie(hello_trie):
    """Utterly trivial test for __init__"""
    assert hello_trie.char == 'hello'
    assert hello_trie.end is True
    assert hello_trie.children == {}
    assert hello_trie.pages == []


def test_match():
    assert Trie.match('hello', 'help') == ('hel', 'lo', 'p')
    assert Trie.match('hell', 'hello') == ('hell', '', 'o')
    assert Trie.match('hello', 'hello') == ('hello', '', '')


def test_match_empty():
    assert Trie.match('hello', '') == ('', 'hello', '')


def test_get_word(bigger_trie):
    assert bigger_trie.get_word('help') is bigger_trie.children['h'].children['el'].children['p']
    assert bigger_trie.get_word('hello') is bigger_trie.children['h'].children['el'].children['lo']

    assert len(bigger_trie.get_word('hello').pages) == 2000


def test_get_word_keyerror(bigger_trie):
    with pytest.raises(KeyError):
        bigger_trie.get_word('he')
    with pytest.raises(KeyError):
        bigger_trie.get_word('hel')


def test_insert_helper_exact(hello_root):
    assert hello_root.insert_helper('helloo', hello_root) == (
        'o', hello_root.children['hello'])


def test_insert_helper_partial(hello_root):
    word, node = hello_root.insert_helper('help', hello_root)
    assert word == ''
    hel = hello_root.children['hel']
    assert all_in(hel.children, 'lo', 'p')


def test_insert_helper_no_match(hello_root):
    word, node = hello_root.insert_helper('goodbye', hello_root)
    assert word == ''
    assert node == hello_root.children['goodbye']


def test_insert_simple(hello_root):
    hello_root.insert('goodbye', 1, 1)

    assert hello_root.char == ''
    assert all_in(hello_root.children, 'hello', 'goodbye')


def test_insert_overlap(hello_root):
    hello_root.insert('help', 1, 1)

    assert 'hel' in hello_root.children and len(hello_root.children) == 1
    assert all_in(hello_root.children['hel'].children, 'lo', 'p')


def test_insert_existing_word(hello_root):
    hello_root.insert('hello', 1, 1)
    hello_root.insert('hello', 2, 1)

    assert 'hello' in hello_root.children and len(hello_root.children) == 1

    hello = hello_root.children['hello']
    assert all_in(hello.pages, (1, 1), (2, 1))


def test_insert_chain():
    root = Trie('')
    root.insert('as', 1, 1)
    root.insert('assist', 1, 1)
    root.insert('assistance', 1, 1)

    assert 'as' in root.children
    as_node = root.children['as']
    assert 'sist' in as_node.children
    sist_node = as_node.children['sist']
    assert 'ance' in sist_node.children


def test_insert_ignore(hello_root):
    hello_root.insert_ignore('goodbye')
    assert hello_root.get_word('goodbye').pages == []

    hello_root.insert_ignore('help')
    assert hello_root.get_word('help').pages == []


@pytest.mark.parametrize('size, expected_id', [(1, 'B'),
                                               (200, 'B'),
                                               (500, 'H'),
                                               (100000, 'I'),
                                               (1e12, 'Q')])
def test_get_primitive(size, expected_id):
    assert get_primitive(size).id == expected_id


def test_get_primitive_too_large():
    with pytest.raises(ValueError):
        get_primitive(1e50)


def test_flatten_data(bigger_trie):
    # TODO ideally refactor flatten_data so exact values can be accessed,
    # instead of having to call get_primitive on everything
    data = bigger_trie.flatten_data()

    assert data.page_s == get_primitive(2000)
    assert data.child_s == get_primitive(2)

    assert data.page_p == get_primitive(2003)
    assert data.char_p == get_primitive(22)
