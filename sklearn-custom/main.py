# ---
# title: Developing custom scikit-learn transformers and estimators
# date: 2020-03-05T17:15:00-05:00
# draft: true
# ---

# scikit-learn offers a wide range of Machine Learning models, but it goes way beyond that by providing other tools such as as hyperparameter optimization using `GridSearchCV` or composed estimators via `Pipeline`. One of the characteristics I like the most about scikit-learn is their consistent API, for example, all estimators implement the same basic methods (fit and predict). This consistency has been immensely useful to the ML open source community: if a custom estimator/transformer conforms to scikit-learn's API it will be easy to interface with compatible tools.
#
# Often we want to implement some specific functionality that does not exist in scikit-learn or any other packages, if we conform to scikit-learn's API we can limit ourselves to implement a custom transformer/estimator and still use all of the other scikit-learn modules.
#
# In this blog post, we will show how to build custom transformers and estimators, as well as discuss implementation details to do this correctly. [The official docs](https://scikit-learn.org/stable/developers/develop.html) contain all you need to know but here are the most important facts:
#
# 1. All constructor (the `__init__` function) parameters should have default values
# 2. Constructor parameters should be added as attributes *without any modifications*
# 3. Attributes estimated from data must have a name with a trailing underscore
#
# There are other rules but you can use utility functions provided by scikit-learn to take care of them. A `check_estimator` function is also provided to exhaustively verify that your implementation is correct. An [official code template](https://github.com/scikit-learn-contrib/project-template/blob/master/skltemplate/_template.py) is also provided.

# ## Transformer use case: verifying model's input
#
# scikit-learn estimators were originally designed to operate on numpy arrays (although there is current ongoing work to better interface with pandas Data Frames). For practical purposes, this means our estimators do not have a notion of column names (only input shape is verified to raise errors): if columns are shuffled, the transformer/estimator will not complain, but the prediction will be meaningless.
#
# Our custom transformer (an object that implements fit and transform) adds this capability: when used in a `Pipeline` object, it will verify that the we are getting the right input columns. The (commented) implementation looks as follows:

# + hide=true
import warnings
import logging
import pickle

import sklearn
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.estimator_checks import check_estimator
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.linear_model import ElasticNet, LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split, GridSearchCV
import pandas as pd
import numpy as np

warnings.filterwarnings('ignore')

dataset = load_boston()
X = pd.DataFrame(dataset.data, columns=dataset.feature_names)
y = dataset.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)


# -

# We inherit from TransformerMixin to get the fit_transform implementation.
# Transformers in scikit-learn also have to inherit from BaseEstimator
# see: https://github.com/scikit-learn/scikit-learn/blob/b194674c4/sklearn/preprocessing/_data.py#L520
class InputGuard(TransformerMixin, BaseEstimator):
    """
    Verify column names at predict time match the ones used when fitting

    Parameters
    ----------
    strict : bool, optional
        If True, it will raise an error if the input does not match
        exactly (same columns, same order), if False, it will ignore
        order and extra columns (will only show a warning), defaults
        to True

    Notes
    -----
    Must be used in a Pipeline object and must be the first step. fit
    and predict should be called with a pandas.DataFrame object
    """

    def __init__(self, strict=True):
        # no logic allowed here, just assign attributes
        # from __init__ args
        self.strict = strict

    def fit(self, X, y=None):
        # we need this to pass check_estimator
        X_out, y = check_X_y(X, y)
        X = X if hasattr(X, 'columns') else X_out

        # our estimator is designed to work on structures
        # that have a columns attribute (such as pandas Data Frame)
        if hasattr(X, 'columns'):
            self.expected_ = list(X.columns)
            self.expected_n_ = X.shape[1]
        # ...but we still need to support numpy.arrays to
        # pass check_estimator
        else:
            self.expected_ = None
            self.expected_n_ = X.shape[1]
            warnings.warn('Input does not have a columns attribute, '
                          'only number of columns will be validated')
        return self

    def transform(self, X):
        # these two are to pass check_estimator
        check_is_fitted(self)
        X_out = check_array(X)
        X = X if hasattr(X, 'columns') else X_out

        # if column names are available...
        if self.expected_:
            return self._transform(X)
        else:
            # this is raised to pass check_estimator
            if self.expected_n_ != X.shape[1] and self.strict:
                raise ValueError('Number of columns from fit {} is different from transform {}'
                                 .format(self.expected_n_, X.shape[1]))

            return X

    def _transform(self, X):
        # this function implements our core logic and it
        # will only be called when fit received an X with a columns attribute

        if not hasattr(X, 'columns'):
            raise ValueError('{}.fit ran with a X object that had '
                             'a columns attribute, but the current '
                             'X does not have it'.format(type(self).__name__))

        columns_got = list(X.columns)

        if self.strict:
            if self.expected_ != columns_got:
                missing = set(self.expected_) - set(columns_got)
                raise ValueError('Columns during fit were: {}, but got {} '
                                 'for predict.'
                                 ' Missing: {}'.format(self.expected_,
                                                       columns_got,
                                                       missing))
        else:
            missing = set(self.expected_) - set(columns_got)
            extra = set(columns_got) - set(self.expected_)

            if missing:
                raise ValueError('Missing columns: {}'.format(missing))
            elif extra:
                extra = set(columns_got) - set(self.expected_)
                warnings.warn('Got extra columns: {}, ignoring'
                              .format(extra))
                return X[self.expected_]

        return X


# The `sklearn.utils.validation` module provides utility functions to pass some of `check_estimator` tests without having to implement the logic ourselves (I actually had to perform a few modifications to my original implementation, to fix errors thrown by `check_estimator`). These utility functions transform inputs (`check_X_y`, `check_array`) to return the expected format (numpy arrays) and throw the appropriate exceptions when this is not possible. `check_is_fitted` only raises an error if a call to `predict` is attempted without fitting the model first.
#
# We now verify that out transformer passes all the tests:

# if no exceptions are raises, we're good
check_estimator(InputGuard)

# Passing all tests is not absolutely necessary for your transformer (or estimator) to integrate correctly with other scikit-learn modules, but doing so assures that your implementation is robust by handling common scenarios on behalf of the user (e.g. passing a 2D array with one column as y instead of a 1D array) and throwing informative errors. Given the large user base scikit-learn has, this is a must, however, for some very customized implementation, passing all the tests is simply not be possible, as we will see in the the custom estimator use case.
#
# For now, let's verify that our transformer plays nicely with Pipeline and GridSearchCV:

# +
# our transformer *has* to be the first step in the pipeline,
# to make sure it gets a pandas Data Frame as input and not
# a numpy array (which strips column names)
pipe = Pipeline([('guard', InputGuard()),
                 ('scaler', StandardScaler()),
                 ('reg', ElasticNet())])

# perform hyperparameter tuning
grid = GridSearchCV(pipe, param_grid={'reg__alpha': [0.5, 1.0, 2.0]})
best_pipe = grid.fit(X_train, y_train).best_estimator_

# make predictions using the best model
y_pred = best_pipe.predict(X_test)
print(f'MAE: {np.abs(y_test - y_pred).mean():.2f}')
# -

# We now verify that our transformer throws an error if a column is missing:

# +
# drop a feature used during training
X_corrupted = X_test.drop('CRIM', axis='columns')

try:
    best_pipe.predict(X_corrupted)
except ValueError as e:
    print('Error message: ', e)
# -

# If we add a column but switch to non-strict mode, we get a warning instead of an error:

warnings.filterwarnings('default')

X_corrupted = X_test.copy()
X_corrupted['extra'] = 1
best_pipe.named_steps['guard'].strict = False
_ = best_pipe.predict(X_corrupted)

warnings.filterwarnings('ignore')


# ## Estimator use case: logging model's predictions
#
# Say we want to log all our predictions to monitor a production model, for the sake of example, we will just use the `logging` module but this same logic applies to other methods such as saving predictions to a database. There are a few nuances here. `Pipeline` requires all intermediate steps to be transformers (fit/transform), which means we can only add our model (the one that implements predict) at the end.
#
# Since we cannot split our logging in two steps, we have to wrap an existing estimator and add the logging functionality to it, from the outside, our custom estimator will just look like another standard estimator.
#
# The 3 considerations that apply for transformers apply for estimators, plus a fourth one (copied directly from scikit-learn's documentation):
#
# 4. Estimators have `get_params` and `set_params` functions. The get_params function takes no arguments and returns a dict of the `__init__` parameters of the estimator, together with their values. It must take one keyword argument, `deep`, which receives a boolean value that determines whether the method should return the parameters of sub-estimators (for most estimators, this can be ignored). The default value for deep should be true.

class LoggingEstimator(BaseEstimator):
    """
    A wrapper for scikit-learn estimators that logs every prediction

    Parameters
    ----------
    est_class
        The estimator class to use
    **kwargs
        Keyword arguments to initialize the estimator
    """

    # NOTE: we arbitrarily selected a default estimator class
    # so check_estimator does not fail when doing LoggingEstimator()
    def __init__(self, est_class=LinearRegression, **kwargs):

        self.est_class = est_class

        # kwargs depend on the model used, so assign them whatever they are
        for key, value in kwargs.items():
            setattr(self, key, value)

        # these attributes support the logging functionality
        self._logger = logging.getLogger(__name__)
        self._logging_enabled = False
        self._param_names = ['est_class'] + list(kwargs.keys())

    # in the transformer case, we did not implement get_params
    # nor set_params since we inherited them from BaseEstimator
    # but such implementation will not work here due to the **kwargs
    # in the constructor, so we implemented it

    def get_params(self, deep=True):
        # Note: we are ignoring the deep parameter
        # this will not work with estimators that have sub-estimators
        # see https://scikit-learn.org/stable/developers/develop.html#get-params-and-set-params
        return {param: getattr(self, param)
                for param in self._param_names}

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)

        return self

    # our fit method instantiates the actual model, and
    # it forwards any extra keyword arguments
    def fit(self, X, y, **kwargs):
        est_kwargs = self.get_params()
        del est_kwargs['est_class']
        # remember the trailing underscore
        self.model_ = self.est_class(**est_kwargs)
        self.model_.fit(X, y, **kwargs)
        # fit must return self
        return self

    def predict(self, X):
        check_is_fitted(self)

        # we use the fitted model and log if logging is enabled
        y_pred = self.model_.predict(X)

        if self._logging_enabled:
            self._logger.info('Logging predicted values: %s', y_pred)

        return y_pred

    # requiring a score method is not documented but throws an
    # error if not implemented
    def score(self, X, y, **kwargs):
        return self.model_.score(X, y, **kwargs)

    # some models implement custom methods. Anything that is not implemented here
    # will be delegated to the underlying model. There is one condition we have
    # to cover: if the underlying estimator has class attributes they won't
    # be accessible until we fit the model (since we instantiate the model there)
    # to fix it, we try to look it up attributes in the instance, if there
    # is no instance, we look up the class. More info here:
    # https://scikit-learn.org/stable/developers/develop.html#estimator-types
    def __getattr__(self, key):
        if key != 'model_':
            if hasattr(self, 'model_'):
                return getattr(self.model_, key)
            else:
                return getattr(self.est_class, key)
        else:
            raise AttributeError(
                "'{}' object has no attribute 'model_'".format(type(self).__name__))

    # these two control logging

    def enable_logging(self):
        self._logging_enabled = True

    def disable_logging(self):
        self._logging_enabled = False

    # ignore the following two for now, more info in the Appendix

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_logger']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._logger = logging.getLogger(__name__)


# `check_estimator` has a `generate_only` parameter that let us run checks one by one instead of failing at the first error. Let's use that option to check `LoggingEstimator`.

for est, check in check_estimator(LoggingEstimator, generate_only=True):
    try:
        check(est)
    except AssertionError as e:
        print('Failed: ', check, e)

# Names aren't very informative, so I took a look at the [source code](https://github.com/scikit-learn/scikit-learn/blob/b194674c4/sklearn/utils/estimator_checks.py).
#
# `check_parameters_default_constructible` checks that the estimator `__init__` parameters are of certain type, our estimator passes a class as an argument, that's why it breaks, but it shouldn't be an issue when interfacing with other components. I don't know why they restrict the types of arguments, my guess is that they want to avoid problems with objects that don't play nicely with the `multiprocessing` module.
#
# `check_no_attributes_set_in_init` is also about `__init__` arguments, according to the spec, we should not set any attributes other than the arguments, but we need them for logging to work, it should not affect either.
#
# Finally `check_supervised_y_2d`, checks that if a 2D numpy array is passed to `fit` a warning is issued, since it has to be converted to a 1D array, our custom estimator wraps any estimator, which could have multi-output, so we cannot use the utility functions to fix this.
#
# The bottom line is that `check_estimator` runs a very strict test suite, if your estimator does not pass all the tests, it does not mean it won't work, but you'll have to be more careful about your implementation.
#
# Let's now see our pipeline in action, note that we are also including our `InputGuard`, we change the underlying model in `LoggingEstimator` to demonstrate that it works with any estimator.

# +
pipe = Pipeline([('guard', InputGuard()),
                 ('scaler', StandardScaler()),
                 ('reg', LoggingEstimator(est_class=ElasticNet))])

# perform hyperparameter tuning
grid = GridSearchCV(
    pipe, param_grid={'reg__alpha': [0.5, 1.0, 2.0]}, n_jobs=-1)
best_pipe = grid.fit(X_train, y_train).best_estimator_

# make predictions using the best model
y_pred = best_pipe.predict(X_test)
print(f'MAE: {np.abs(y_test - y_pred).mean():.2f}')
# -

# Let's now configure the `logging` module and enable it in our custom estimator:

logging.basicConfig(level=logging.INFO)
best_pipe.named_steps['reg'].enable_logging()

# The following line shows our logging in effect:

best_pipe.predict(X_test.iloc[0:2])

# Since we implemented `__getattr__`, any model-specific attribute also works, let's get the linear model coefficients:

best_pipe.named_steps['reg'].coef_

# ### Appendix: making our estimator work with  `pickle` (or any other pickling mechanism)
#
# Pickling an object means saving it to disk. This is useful if we want to fit and then deploy a model ([be careful when doing this!](https://scikit-learn.org/stable/modules/model_persistence.html#security-maintainability-limitations)) but it is also needed if we want our model to work with the `multiprocessing` module. Some objects are *picklable* but some others are not (this also depends on which library you are using). `logger` objects do not work with the `pickle` module but we can easily fix this by deleting it before saving to disk and initializing it after loading, this boils down to adding two more methods: `__getstate__` and `__setstate__`, if you are interested in the details, [read this](https://docs.python.org/3/library/pickle.html#handling-stateful-objects).

# showing pickling and unpickling works
pickle.loads(pickle.dumps(best_pipe))

# ## Closing remarks

# In this post we showed how to develop transformers and estimators compatible with scikit-learn. Given how many details the API has, using the `check_estimator` function will guide you through the process. However, if your implementations contains non-standard behavior (like ours), your custom objects will fail the tests even if they integrate correctly with other modules. In such case, you'll have to be careful about your implementation, using `check_estimator` with `generate_only=True` is useful for getting a list of failing tests and deciding whether it is acceptable or not.
#
# Following the scikit-learn API spec gives you access to a wide set of ML tools so you can focus on implementing your custom model and still use other modules for grid search, cross validation, etc. This is a huge time saver for ML projects.
#
# Source code for this post is available [here]({{url_source}}).
#
# Found an error in this post? [Click here to let us know]({{url_issue}}).
#
# Looking for commercial support? [Drop us a line](mailto:support@ploomber.io).
#
# This post was generated using scikit-learn version:

# + hide=true
print(sklearn.__version__)
