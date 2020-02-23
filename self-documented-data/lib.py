import json
from warnings import warn
from functools import wraps

from numpydoc.docscrape import NumpyDocString


def add_metadata(table, metadata, key='my_metadata'):
    """
    Add json metadata to a pyarrow table under a given key

    Notes
    -----
    Based on: https://stackoverflow.com/a/58978449/709975
    """
    metadata_b = json.dumps(metadata).encode('utf-8')
    key = bytes(key, encoding='utf-8')
    new_schema_metadata = {**{key: metadata_b},
                           **table.schema.metadata}
    table_w_metadata = table.replace_schema_metadata(new_schema_metadata)
    return table_w_metadata


def validate_dictionary(dictionary, table, name):
    """
    Validate dictionary against pandas.DataFrame, warn on missing or extra
    columns
    """

    expected = set(p['name'] for p in dictionary['returns'])
    actual = set(table.column_names)

    missing = expected - actual
    extra = actual - expected

    if missing:
        warn('Data dictionary for function "{}" has missing columns: {}'
             .format(name, missing))

    if extra:
        warn('Data dictionary for function "{}" has extra columns: {}'
             .format(name, extra))


def add_dictionary(fn):
    """
    Decorator that adds dictionary and summary to a function that returns a
    pyarrow.Table
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        dictionary = docstring2list(fn.__doc__)
        table = fn(*args, **kwargs)
        validate_dictionary(dictionary, table, fn.__name__)
        return add_metadata(table, dictionary, key='my_metadata')

    return wrapper


def docstring2list(doc):
    """
    Convert numpydoc docstring to a list of dictionaries
    """
    doc = NumpyDocString(doc)
    returns = [{'name': p.name, 'desc': ' '.join(p.desc), 'type': p.type}
               for p in doc['Returns']]
    summary = doc['Summary']
    return {'returns': returns, 'summary': summary}
