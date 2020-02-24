from pprint import pprint
import json

import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd

from lib import add_dictionary


@add_dictionary
def clean_data():
    """
    Clean the data


    Returns
    -------
    column : int
        Column description
    another_column : float
        Another column description
    """
    df = pd.DataFrame({'column': [0, 1], 'extra_column': [0, 1]})
    table = pa.Table.from_pandas(df)
    return table


# this functions returns a self-documented table
table = clean_data()

# print metadata
metadata = json.loads(table.schema.metadata[b'my_metadata'])
print('Table has metadata: ')
pprint(metadata)

# metadata is persisted when you reload the file
pq.write_table(table, 'table.parquet')
table = pq.read_table('table.parquet')
json.loads(table.schema.metadata[b'my_metadata'].decode('utf-8'))

# you can also load the metadata instead of the complete file
schema = pq.read_schema('table.parquet')
json.loads(schema.metadata[b'my_metadata'].decode('utf-8'))
