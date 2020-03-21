# ---
# title: Model selection with scikit-learn and ploomber
# ---

# *Note*: This blog post assumes you are familiar with the model selection framework via [nested cross-validation](https://sebastianraschka.com/blog/2018/model-evaluation-selection-part4.html#nested-cross-validation) and with the following scikit-learn modules (click for documentation): [`GridSearchCV`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html), [`cross_val_predict`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_predict.html) and [`Pipeline`](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html).
#
# Model selection is an important part of any Machine Learning task. Since each model encodes their own [inductive bias](https://en.wikipedia.org/wiki/Inductive_bias), it is important to compare them to understand their subtleties and choose the best one for the problem at hand. While knowing the details of each learning algorithm is important to have an intuition about which ones we want to try, it is always helpful to visualize actual results in our data.
#
# The quick and dirty approach for model selection would be to have a long Jupyter notebook, where we train all models and output charts for each one. In this post we will show how to achieve this in a cleaner way by using scikit-learn and [ploomber](https://github.com/ploomber/ploomber).
#
# ## Project layout
#
# We split the code in three files:
#
# 1. `pipelines.py`. Contains functions to instantiate scikit-learn pipelines
# 2. `report.py`. Contains the source code that performs hyperparameter tuning and model evaluation, imports pipelines defined in `pipelines.py`
# 3. `main.py`. Contains the loop that executes `report.py` for each pipeline using ploomber
#
# Unless otherwise noted, the snippets shown in this post belong to `main.py`.
#
# ## Functions to instantiate pipelines (`pipelines.py`)
#
# We start declaring each of our *model pipelines*, which are callables (objects in Python that we can call such as a function `function` (by doing `function()`) or a class `MyClass` by doing (`MyClass()`). Each model pipeline will return a scikit-learn `Pipeline` instance that will be used in a nested cross-validation loop to choose the best hyperparameters and estimate generalization performance. Content is as follows:
#
# {{expand('factories.py')}}
#
# We have one factory for NuSVR and another one Ridge Regression. Since these two models are sensitive to scaling, we include them in a scikit-learn pipeline that scales all features before feeding the data into the model.
#
# ## Hyperparameter tuning and performance estimation (`report.py`)
#
# We will process each model separately, generating three HTML reports in total, the reports will be generated using the following source code:
#
# {{expand('report.py')}}
#
#
# ## Running the execution loop (`main.py`)
#
# We now turn our attention to main script that will take the model pipelines, the report source code and execute them. First we have to define the parameters we want to try for each model. We define one dictionary for each, the key `m_init` has the pipeline location (we will dynamically  import this using the [`importlib`](https://docs.python.org/3/library/importlib.html#module-importlib) library, finally, the `m_params` key contains the hyperparameters to try, not that for Ridge Regression and NuSVR, we have to add a `ref__` prefix to each parameter, this is because the factories return scikit-learn `Pipeline` objects and we need to specify to which step the parameters belong to.

# +
from pathlib import Path
from sklearn.model_selection import ParameterGrid
from IPython.display import Markdown, display, HTML

from ploomber.tasks import NotebookRunner
from ploomber.products import File
from ploomber import DAG

# Ridge Regression grid
params_ridge = {
    'm_init': 'pipelines.ridge',
    'm_params': {
        'reg__alpha': [0.5, 1.0, 1.5, 2.0, 3.0]
    }
}

# Random Forest Regression grid
params_rf = {
    'm_init': 'sklearn.ensemble.RandomForestRegressor',
    'm_params': {
        'n_estimators': [5, 50, 100],
        'min_samples_leaf': [5, 10, 20],
    }
}

# Nu Support Vector Regression grid
params_nusvr = {
    'm_init': 'pipelines.nusvr',
    'm_params': {
        'reg__nu': [0.3, 0.5, 0.8],
        'reg__C': [0.5, 1.0, 1.5, 2.0],
        'reg__kernel': ['rbf', 'sigmoid']
    }
}
# -

# Note that we do not have a pipeline for `RandomForestRegressor`, Random Forest is not sensitive to scaling so we use the model directly.
#
# We now add the execution loop, we will execute it using [ploomber](https://github.com/ploomber/ploomber). We just have to tell `ploomber` where to load the source code from, which parameters to use on each iteration and where to save the output:

# +
# load report source code
notebook = Path('nb.py').read_text()

# we will save all notebooks in the artifacts/ folder
out = Path('artifacts')
out.mkdir(exist_ok=True)

params_all = {'ridge': params_ridge, 'rf': params_rf, 'nusvr': params_nusvr}

dag = DAG()

# loop over params and create one notebook task for each...
for name, params in params_all.items():
    # NotebookRunner is able to execute ipynb files using
    # papermill under the hood, if the input file has a
    # different extension (like in our case), it will first
    # convert it to an ipynb file using jupytext
    NotebookRunner(notebook,
                   # save it in artifacts/{name}.html
                   # NotebookRunner will generate ipynb files by
                   # default, but you can choose other formats,
                   # any format supported by the official nbconvert
                   # package is supported here
                   product=File(out / (name + '.html')),
                   dag=dag,
                   name=name,
                   # pass the parameters
                   params=params,
                   # we are passing pyhon code
                   # that will first be converted
                   # to a jupyter notebook using
                   # jupytext, then executed
                   # with the passed parameters
                   # using papermill and finally,
                   # converted to HTML using nbconvert
                   # with ploomber coordinating execution
                   ext_in='py',
                   kernelspec_name='python3')
# -

# Build the DAG:

dag.build()

# That's it. After building the DAG, each model will generate one report, you can see them here (TODO: add link).
#
# Splitting logic into separate files improves readability and maintainability, if we want to add another model we only have to add a new dictionary with the parameter grid, if preprocessing is needed, we just add a factory in `pipelines.py`.
#
# Using ploomber provides a concise and clean framework for generating reports, in just a few lines of code, we generated all our reports, however, we made a big simplifications in our `report.py` file: we are loading, training and evaluating in a single source file, if we made even a small change to our charts we would have to re-train every model again. A better approach is to split that logic in several steps, and that scenario is where ploomber is very effective:
#
# 1. Clean raw data (save clean dataset)
# 2. Train model and predict (save predictions)
# 3. Evaluate predictions
#
# If we split each model pipeline in three steps, and run build, we will obtain the same results, now let's say you want to add a new chart, so you modify step 3. All you have to do to update your reports is `dag.build()`, ploomber will figure out that it does not have to re-run steps 1-2 and overwrite the old reports with the new ones.
#
# ## Closing remarks
#
# Developing Machine Learning model is an iterative process, by breaking down the entire pipeline logic in small steps and maximizing code reusability, we can develop short and maintainable pipelines. Jupyter is a superb tool (I use it every day and I'm actually writing this blog post from Jupyter), but do not fall into the habit of coding everything in a big notebook, which inevitably leads to unmaintainable code, prefer many short notebooks (or .py files) over a big single one.
#
# This blog post was generated using versions:

# + hide=True
# ! pip freeze | grep -E "$(cat requirements.txt | paste -sd "," -  |  sed -E 's/,/=|/g')"
# -
