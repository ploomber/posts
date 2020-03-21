from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.svm import NuSVR


def ridge():
    return Pipeline([('scaler', StandardScaler()),
                     ('reg', Ridge())])


def nusvr():
    return Pipeline([('scaler', StandardScaler()),
                     ('reg', NuSVR())])
