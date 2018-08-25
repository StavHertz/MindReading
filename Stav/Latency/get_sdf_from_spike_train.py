from scipy import stats
import statsmodels.api as sm

def get_sdf_from_spike_train(spike_train):
    kde = sm.nonparametric.KDEUnivariate(spike_train)
    kde.fit()
    return kde.density
