# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
from pathlib import Path
import pickle

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn_evaluation.plot import confusion_matrix

# + tags=["parameters"]
# extract_upstream=True in your pipeline.yaml file, if this task has
# dependencies, list them them here (e.g. upstream = ['some_task']), otherwise
# leave as None
upstream = ['get', 'petal-area', 'sepal-area']

# extract_product=False in your pipeline.yaml file, leave this as None, the
# value in the YAML spec  will be added here during task execution
product = None
# -

df = pd.read_csv(upstream['get']['data'])

petal = pd.read_csv(upstream['petal-area']['data'])

sepal = pd.read_csv(upstream['sepal-area']['data'])

train = df.join(petal).join(sepal)

X = train.drop('target', axis='columns')
y = train.target

model = RandomForestClassifier()

model.fit(X, y)

y_pred = model.predict(X)

confusion_matrix(y, y_pred)

Path(product['model']).write_bytes(pickle.dumps(model))
