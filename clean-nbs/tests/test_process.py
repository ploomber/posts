import pytest
from my_package import process


@pytest.mark.parametrize(
    'name, expected',
    [
        ['Hemingway, Ernest', 'Ernest Hemingway'],
        ['virginia woolf', 'Virginia Woolf'],
        ['charles dickens   ', 'Charles Dickens'],
    ],
)
def test_clean_name(name, expected):
    assert process.clean_name(name) == expected
