import pymc as pm

def train_model(data, eligibility_threshold, random_seed, positive_slope = True):

    """ 
    Train the Bayesian regression discontinuity model. 

    Inputs
    ------

    - data: dataframe consiting of X-values, treatment status, and Y values 
    - eligibility_threshold: predefined eligibility
    - random_seed: random seed specified for reproducability purposes
    - positive_slope: binary parameter based on previously generated data, model trains depending
    on the data's overall distribution 

    Outputs
    -------

    - trained_mod: Bayesian regression discontinuity model object 
    - inf_data: inference data we can sample to estimate the posterior distribution 
    """
    with pm.Model() as trained_mod:

        # pass in observations
        treated_obs = pm.MutableData("treated_obs", data.treatment, dims="obs_id")
        x_vals = pm.MutableData("x_vals", data.X, dims="obs_id")

        # model parameters
        effect_size = pm.Cauchy("effect", alpha=eligibility_threshold, beta=1)
        s = pm.HalfNormal("sigma", 1)

        if positive_slope == True: 
            u = pm.Deterministic("mu", x_vals + (effect_size * treated_obs), dims="obs_id")
        else: 
            u = pm.Deterministic("mu", - x_vals + (effect_size * treated_obs), dims="obs_id")
            
        obs = pm.Normal("y", mu=u, sigma=s, observed=data.Y, dims="obs_id")

    # get inference data
    with trained_mod:
        inf_data = pm.sample(cores=1, random_seed=random_seed)

    return trained_mod, inf_data
