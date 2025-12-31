import numpy as np
import pandas as pd
from scipy.optimize import minimize
from risk_metrics_analysis import etf_log_returns 
from data_prep import mystery_allocation_one_df 

mystery_allocation_one_df.index=pd.to_datetime(mystery_allocation_one_df.index, format='mixed',dayfirst =True, errors='coerce')
mystery_allocation_one_df.index.name='Dates'
mystery_allocation_one_df.columns=['mystery allocation']
#print(mystery_allocation_one_df)
etf_log_returns.index=pd.to_datetime(etf_log_returns.index, format='mixed', dayfirst=True, errors='coerce')
#print(etf_log_returns)
#returns of mystery allocation one 
mystery_one_returns=np.log(mystery_allocation_one_df/mystery_allocation_one_df.shift(1)).dropna()

etf_log_returns.dropna()

print(mystery_one_returns)

#print(type(etf_log_returns.index))
#print(type(mystery_allocation_one_df.index))
combined_etf_mystery_one_returns = etf_log_returns.join(mystery_one_returns, how='inner')
#combined_etf_mystery_one_returns = combined_etf_mystery_one_returns.dropna(subset=[mystery_allocation_one_df.columns[0]])
print(combined_etf_mystery_one_returns)


X = combined_etf_mystery_one_returns.iloc[:, :-1].values
Y = combined_etf_mystery_one_returns.iloc[:, -1].values 

# objective function - minimize squared error of linear regression Y ~ X@w
def objective_fn(w, X, Y):
    return np.sum((Y - X @ w)**2)

# constraints: portfolio weights sum to 1
constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})

# bounds: weights between 0 and 1 (no shorting)
bounds = [(0, 1) for _ in range(X.shape[1])]

# initial guess: equal weights
w0 = np.ones(X.shape[1]) / X.shape[1]

# solve optimization problem
result = minimize(objective_fn, w0, args=(X, Y), method='SLSQP', 
                  bounds=bounds, constraints=constraints)

# optimal weights
optimal_weights = result.x

print("Optimal weights:", optimal_weights)
print("Weights sum:", np.sum(optimal_weights))
print("Success:", result.success)
print("MSE:", result.fun) 

