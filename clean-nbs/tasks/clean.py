# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.3
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---
import pandas as pd

from my_package.process import clean_name

# %% tags=["parameters"]
upstream = ['load']
product = None

# %%
df = pd.read_csv(upstream['load']['data'])

# %%
df['name'] = df.name.apply(clean_name)
df['years_since_birth'] = 2021 - df['birth_year']

# %%
df.to_csv(product['data'], index=False)