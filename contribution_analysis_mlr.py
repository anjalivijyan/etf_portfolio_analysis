#how much each asset class contributes to the performance of each etf 
#equation used R(i,t)=alpha(i)+gamma(i)X(t) +e(i,t)

import numpy as np 
import pandas as pd 
from sklearn.linear_model import LinearRegression 
from sklearn.impute import SimpleImputer 
from risk_metrics_analysis import (etf_log_returns, asset_log_returns)


etf_log_returns=etf_log_returns.replace([np.inf, -np.inf], np.nan)
asset_log_returns=asset_log_returns.replace([np.inf, -np.inf], np.nan)

imputer =SimpleImputer(strategy='mean')
X=imputer.fit_transform(asset_log_returns)

mlr_coeff=pd.DataFrame(index=asset_log_returns.columns, columns=etf_log_returns.columns)
for etf in etf_log_returns.columns:
    y= etf_log_returns[[etf]].values 
    y=np.nan_to_num(y, nan=np.nanmean(y))
    model=LinearRegression()
    model.fit(X, y)

    mlr_coeff[etf]=model.coef_.flatten()


#print(mlr_coeff) 