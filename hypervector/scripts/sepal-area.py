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

import pandas as pd

# + tags=["parameters"]
# extract_upstream=True in your pipeline.yaml file, if this task has
# dependencies, list them them here (e.g. upstream = ['some_task']), otherwise
# leave as None
upstream = ['get']

# extract_product=False in your pipeline.yaml file, leave this as None, the
# value in the YAML spec  will be added here during task execution
product = None
# -

df = pd.read_csv(upstream['get']['data'])

df.head()

df['sepal-area'] = df['sepal length (cm)'] * df['sepal width (cm)']

df[['sepal-area']].to_csv(product['data'], index=False)
