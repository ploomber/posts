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

# %%
import pandas as pd

# %% tags=["parameters"]
upstream = None
product = None

# %%
df = pd.DataFrame({
    'name': ['Hemingway, Ernest', 'virginia woolf', 'charles dickens   '],
    'birth_year': [1899, 1882, 1812],
})

# %%
df.to_csv(product['data'], index=False)