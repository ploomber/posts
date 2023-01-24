# %%
import numpy as np
import pandas as pd


from visuals import data_scatterplot, diagnostic_plots, regression_discontinuity_plot
from dataset import generate_data
from model import train_model

## DECLARE PARAMETERS

# initialize random state value for data generation, also Ploomber
SEED = 16121515132518
random_state = np.random.default_rng(SEED)

# standard parameters utilized throughout
N = 10**4  # number of observations
STD = 0.3  # change between pre-post boundary test (no measurement error)
TE = 2  # treatment effect we are evaluating post-policy
ELIGIBILITY_THRESHOLD = 5


# %%
## generate, observe data
df = generate_data(
    SEED, N, STD, ELIGIBILITY_THRESHOLD, TE, positive_slope=True, after_cutoff=True
)
df.head(15)


# %%
## visaualize data
data_scatterplot(df, ELIGIBILITY_THRESHOLD)

# %%
# build model
mod, inference_data = train_model(df, ELIGIBILITY_THRESHOLD, SEED, positive_slope=True)


# %%
# build out diagnostics of mode
diagnostic_plots(inference_data, TE, STD)

# %%
# visualize regression discontinuity
regression_discontinuity_plot(df, ELIGIBILITY_THRESHOLD, mod, inference_data)
