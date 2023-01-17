import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pymc as pm
import seaborn as sns


def data_scatterplot(data, eligibility_threshold):

    """
    Take spoofed scatterplot data (features: X, treatment indicator, Y) and then plot
    utilizing matplotlib.

    INPUTS
    ------
    - df: pandas dataframe

    OUTPUTS
    -------
    - Scatterplot demarcating treatment and control groups, in addition to eligibility threshold
    """

    # set dimensions of graph, theme for contrast
    sns.set_style("darkgrid")
    fig, ax = plt.subplots(figsize=(16, 9))

    # plot treated values as scatter
    ax.scatter(
        data.X[data.treatment],
        data.Y[data.treatment],
        alpha=0.4,
        s=5,
        label="Treated Group",
    )

    # plot untreated values as scatter
    ax.scatter(
        data.X[~data.treatment],
        data.Y[~data.treatment],
        alpha=0.4,
        s=5,
        label="Untreated Group",
    )

    # plot vertical line denoting cutoff
    plt.axvline(
        x=eligibility_threshold, ls="-", color="black", label="Eligibility Threshold"
    )

    # labels and legends
    ax.set_xlabel("X Values - Pre/Post Program")
    ax.set_ylabel("Y Values - Post Program")
    ax.set_title("General Sharp RDD Setup")
    ax.legend()

    return ax


def diagnostic_plots(inf_data, treatment_effect, std):

    """
    Check the validity of our priors based on returned inference data

    INPUTS
    ------
    - inf_data: inference data object returned from train_model function
    - treatment_effect: specified treatment effect that we defined in our data
    - std: variation in points around our linear regressions defined in our data

    OUTPUTS:
    --------
    A set of plots mapping the validity of our delta and sigma priors.
    Plots should converge without difficults, and means should be within a 95% confidence interval
    """

    # MCMC Trace
    az.plot_trace(inf_data, var_names=["effect", "sigma"])

    # Posterior Histogram
    az.plot_posterior(
        inf_data,
        var_names=["effect", "sigma"],
        ref_val=[treatment_effect, std],
        hdi_prob=0.95,
    )


def regression_discontinuity_plot(
    data, eligibility_threshold, trained_mod, inf_data
):

    """
    Plots linear regression lines on top of data_scatterplot function to illustrate
    regression discontinuity effects. Samples posterior data from by train_model function
    in model.py to construct high density interval from our regression lines.

    INPUTS
    ------
    - df: data generated from dataset.py
    - trained_mod: our model trained in model.py
    - inf_data: our inference data generated in model.py

    OUTPUT
    ------
    Plot illustrating treatment group regression, control group regression, and
    scatterplot data from data_scatterplot.
    """

    sns.set_style("darkgrid")

    # instantiate data for future sampling
    mu_x = np.linspace(np.min(data.X), np.max(data.X), 500)
    lab_treated = np.zeros(mu_x.shape)

    # use aliases found in model.py file for lines
    with trained_mod:
        pm.set_data({"x_vals": mu_x, "treated_obs": lab_treated})
        ppc = pm.sample_posterior_predictive(inf_data, var_names=["mu", "y"])

    # scatterplot for treatment,control,eligibility threshold
    ax = data_scatterplot(data, eligibility_threshold)

    # plot control group's regression line, labels for mu
    az.plot_hdi(
        mu_x,
        ppc.posterior_predictive["mu"],
        color="C1",
        hdi_prob=0.95,
        ax=ax,
        fill_kwargs={"label": r"$\mu$ untreated (Counterfactual)"},
    )

    # instantiate data for future sampling
    mu_x = np.linspace(np.min(data.X), np.max(data.X), 500)
    lab_treated = np.ones(mu_x.shape)

    # use aliases found in model.py file
    with trained_mod:
        pm.set_data({"x_vals": mu_x, "treated_obs": lab_treated})
        ppc = pm.sample_posterior_predictive(inf_data, var_names=["mu", "y"])

    # plot treatment's regression line, labels for mu
    az.plot_hdi(
        mu_x,
        ppc.posterior_predictive["mu"],
        color="C0",
        hdi_prob=0.95,
        ax=ax,
        fill_kwargs={"label": r"$\mu$ treated (Actual Trend)"},
    )

    plt.legend()
    plt.show()
