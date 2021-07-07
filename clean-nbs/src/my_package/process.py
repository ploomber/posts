# example of a function that does not mutate its input
def add_one_to_series(series):
    """Adds one to a series
    """
    # we are not mutating the original data, but returning a copy with new values
    return series + 1


# example of a function that does not mutate its data frame input
def add_one_to_data_frame(df):
    """Adds one to the "zeros" column in the input data frame
    """
    # do not mutate the input data frame, create a copy
    another = df.copy()
    another['zeros'] = another['zeros'] + 1
    return another


def clean_name(name):
    """Clean a name string
    """
    # flip if in last name, first name format
    tokens = name.split(',')

    if len(tokens) == 2:
        first, last = tokens[1], tokens[0]
    else:
        first, last = name.split(' ')[:2]

    # remove punctuation
    first_clean = first.strip().capitalize()
    last_clean = last.strip().capitalize()

    return f'{first_clean} {last_clean}'
