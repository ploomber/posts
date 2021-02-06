import json
from warnings import warn
from functools import wraps

from numpydoc.docscrape import NumpyDocString
import pyarrow.parquet as pq


def add_metadata(fn, validate=False):
    """
    Decorator that adds dictionary and summary to a function that returns a
    pyarrow.Table

    Parameters
    ----------
    validate : bool
        Shows warnings if there are extra or missing columns in the docstring
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # the special __doc__ attribute returns the docstring defined for the
        # decorator's argument, parse it to convert it to a dictionary
        doc = parse_docstring(fn.__doc__)

        # just run the function with whatever arguments the user passed
        table = fn(*args, **kwargs)

        # use the returned value to validate the parsed docstring, showing
        # warnings if any
        if validate:
            validate_dictionary(doc, table, fn.__name__)

        # add the metadata to the table objecy
        return add_metadata_to_table(table, doc, key='my_metadata')

    return wrapper


def parse_docstring(doc):
    """
    Convert numpydoc docstring to a dictionary
    """
    # parse docstring
    doc = NumpyDocString(doc)

    # get the "Returns" section
    returns = [{
        'name': p.name,
        'desc': ' '.join(p.desc),
        'type': p.type
    } for p in doc['Returns']]

    # ...and the "Summary" section
    summary = doc['Summary']
    return {'returns': returns, 'summary': summary}


def validate_dictionary(doc, table, name):
    """
    Validate dictionary against pyarrow.Table, warn on missing or extra
    columns
    """
    # get the declared names in the "Returns" section
    expected = set(p['name'] for p in doc['returns'])
    # and the names in the table
    actual = set(table.column_names)

    # compare both sets and warn if there are missig or extra columns

    missing = expected - actual
    extra = actual - expected

    if missing:
        warn(
            'Data dictionary for function "{}" has missing columns: {}'.format(
                name, missing))

    if extra:
        warn('Data dictionary for function "{}" has extra columns: {}'.format(
            name, extra))


def add_metadata_to_table(table, metadata, key='my_metadata'):
    """
    Add json metadata to a pyarrow.Table under a given key

    Notes
    -----
    Based on: https://stackoverflow.com/a/58978449/709975
    """
    # convert dictionary to json representation (str object),
    # then convert it to a bytes object encoded in utf-8
    metadata_b = json.dumps(metadata).encode('utf-8')

    # the key also has to be converted to bytes
    key = bytes(key, encoding='utf-8')

    # take old table's metadata (if any) and append
    # a new key with our metadata under the "my_metadata" key
    new_schema_metadata = {**{key: metadata_b}, **table.schema.metadata}

    # replace old metadata with the new version
    table_w_metadata = table.replace_schema_metadata(new_schema_metadata)
    return table_w_metadata


def read_metadata(table):
    """Read metadata from a table object
    """
    return json.loads(table.schema.metadata[b'my_metadata'])


def peek_metadata(path_to_table):
    """Read metadata without loading the data file
    """
    schema = pq.read_schema(path_to_table)
    return json.loads(schema.metadata[b'my_metadata'].decode('utf-8'))
