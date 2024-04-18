from scipy.stats import spearmanr
import pandas as pd

def spearman_cor_test(data):
    # calculate spearman's correlation
    correlation = pd.DataFrame()
    coef, p = spearmanr(data['risk'], data['KA'])
    coef1, p1 = spearmanr(data['risk'], data['Normal'])
    coef2, p2 = spearmanr(data['risk'], data['c_ses'])
    coef3, p3 = spearmanr(data['risk'], data['var'])
    r = [coef, coef1, coef2, coef3, p, p1, p2, p3]
    correlation = correlation.append(r, ignore_index=True)
    correlation = correlation.transpose()

    return correlation