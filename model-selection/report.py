from IPython.display import Markdown
import importlib
from sklearn.datasets import load_boston
from sklearn.model_selection import cross_val_predict, GridSearchCV
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# + tags=["parameters"]
m_init = None
m_params = None
# -

Markdown('# Report for {}'.format(m_init))

print('Params: ', m_params)

# +
# m_init is module.sub_module.constructor import it from the string
parts = m_init.split('.')
mod_str, constructor = '.'.join(parts[:-1]), parts[-1]
mod = importlib.import_module(mod_str)

# instantiate it
model = getattr(mod, constructor)()
print(model)
# -

# load data
dataset = load_boston()
X = pd.DataFrame(dataset.data, columns=dataset.feature_names)
y = dataset.target

# +
# Perform grid search over the passed parameters
grid = GridSearchCV(model, m_params, n_jobs=-1)

# We want to estimate generalization performance *and* tune hyperparameters
# so we are using nested cross-validation
y_pred = cross_val_predict(grid, X, y)
# -

# prev vs actual scatter plot
fig, ax = plt.subplots()
fig.set_size_inches(6, 6)
ax.scatter(y_pred, y)
ax.grid()
ax.set_xlabel('Predicted')
ax.set_ylabel('Actual')

# residuals
fig, ax = plt.subplots()
fig.set_size_inches(6, 6)
res = y - y_pred
ax.scatter(np.arange(len(res)), res)
ax.grid()
ax.set_ylabel('Residual')

# residuals distribution
fig, ax = plt.subplots()
fig.set_size_inches(8, 6)
sns.distplot(res, ax=ax)
ax.grid()
ax.set_title('Residual distribution')

# print metrics
mae = np.abs(y - y_pred).mean()
mse = ((y - y_pred) ** 2).mean()
print(f'MAE: {mae:.2f}')
print(f'MSE: {mse:.2f}')
