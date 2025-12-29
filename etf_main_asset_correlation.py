import numpy as np 
import pandas as pd 
import plotly.express as px 

from risk_metrics_analysis import (etf_log_returns, asset_log_returns)
#print(etf_log_returns.shape, asset_log_returns.shape)

concat_etf_asset_returns=pd.concat([etf_log_returns, asset_log_returns], axis = 1)
#print(concat_etf_asset_returns)
correlation_matrix=concat_etf_asset_returns.corr()
#print(correlation_matrix)


#ETF Vs Asset return
etf_columns=etf_log_returns.columns
asset_columns=asset_log_returns.columns 

#asset-etf submatrix correlation 

etf_asset_submatrix=correlation_matrix.loc[etf_columns, asset_columns]
#print(etf_asset_submatrix.shape)
print(etf_asset_submatrix)

fig=px.imshow(etf_asset_submatrix, color_continuous_scale='RdBu_r', zmin=-1,zmax=1,
              x=etf_asset_submatrix.columns, y=etf_asset_submatrix.index)

fig.update_layout(title="ETF Correlation with Main Asset Classes",
                  yaxis=dict(autorange= 'reversed'),width=1200,
                  height=1800

)
#fig.show()

