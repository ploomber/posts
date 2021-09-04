from pathlib import Path
import pickle


def predictions(test, product):
    model = pickle.loads(Path(product['model']).read_bytes())

    # check output against recorded output...
    if test:
        print('checking output against reference values...')
    # record output...
    else:
        print('recording reference values...')
