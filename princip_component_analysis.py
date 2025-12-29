import numpy as np 
import pandas as pd 
from sklearn.decomposition import PCA 
from sklearn.preprocessing import StandardScaler 

from risk_metrics_analysis import (etf_log_returns, asset_log_returns)


asset_clean = asset_log_returns.ffill().bfill()
asset_log_returns_scaled = StandardScaler().fit_transform(asset_clean)
asset_scaled_df = pd.DataFrame(
    asset_log_returns_scaled,
    index=asset_clean.index,
    columns=asset_clean.columns
)
#print(asset_scaled_df.isna().sum())
pca_assets = PCA()
pca_assets.fit(asset_scaled_df)

loadings = pd.DataFrame(
    pca_assets.components_.T,
    index=asset_scaled_df.columns,
    columns=[f'PC{i+1}' for i in range(asset_scaled_df.shape[1])]
)

explained_variance_ratio = pca_assets.explained_variance_ratio_
print(loadings['PC1'].sort_values(ascending=False))
