import numpy as np 
import pandas as pd 
import plotly.express as px 

from risk_metrics_analysis import (etf_annualized_return, etf_annual_vol) 

'''print(etf_annualized_return.shape)
print(etf_annual_vol.shape)'''

etf_risk_dataframe= pd.DataFrame({'annual_return': etf_annualized_return, 'annual_volatility': etf_annual_vol}) 

fig= px.scatter( x =etf_risk_dataframe['annual_return'], y =etf_risk_dataframe['annual_volatility']
                , title ='Risk -Return Relationship for ETFs')

fig.update_layout(xaxis=dict(range=[0.00,0.25]), yaxis=dict(range=[0.00, 0.25]), template ='plotly_white')

#fig.show()
            


