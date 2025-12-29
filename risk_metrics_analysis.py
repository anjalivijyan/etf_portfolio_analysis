import numpy as np
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go 

from data_prep import etf_df, main_asset_df_aligned
from max_drawdown import Max_Drawdown 
#assume number of trading days per year 252 for annualised returns and volatiliy 

#Daily log returns for ETFs 
etf_log_returns = np.log(etf_df/etf_df.shift(1))
#Daily log returns for main asset classes 
asset_log_returns=np.log(main_asset_df_aligned/main_asset_df_aligned.shift(1))

#volatility of daily log returns of ETFs 
etf_daily_std=etf_log_returns.std()
#volatility of daily log returns of asset classes 
asset_daily_std=asset_log_returns.std()

#Annualised ETF returns 
etf_annualized_return=etf_log_returns.mean()*252 
#Annualised Asset returns
assset_annualised_returns=asset_log_returns.mean()*252 
#ETF annualised volatility 
etf_annual_vol=etf_log_returns.std()*np.sqrt(252)
#Asset annualised volatility 
asset_annual_vol = asset_log_returns.std()*np.sqrt(252)

#Sharpe retio 
#assume risk free rate = 0 
risk_free_rate=0
etf_sharpe = (etf_annualized_return-risk_free_rate)/etf_annual_vol 
asset_sharpe =(assset_annualised_returns-risk_free_rate)/asset_annual_vol 

#Sortino Ratio
etf_downside_std=etf_log_returns[etf_log_returns<0].std()*np.sqrt(252)
etf_sortino=(etf_annualized_return-risk_free_rate)/etf_downside_std

asset_downside_std=asset_log_returns[asset_log_returns<0].std()*np.sqrt(252)
asset_sortino=(assset_annualised_returns-risk_free_rate)/asset_downside_std 

#cumulative log returns 
etf_cum_log_returns=etf_log_returns.cumsum()
median_cum_log_returns=etf_cum_log_returns.median(axis=1)
asset_cum_log_returns=asset_log_returns.cumsum()

#maximum drawdown 

etf_simple_returns = np.exp(etf_log_returns) - 1
asset_simple_returns = np.exp(asset_log_returns) - 1
# cumulative wealth index
etf_wealth = (1 + etf_simple_returns).cumprod()
asset_wealth = (1 + asset_simple_returns).cumprod()
etf_max_dd= Max_Drawdown(etf_wealth)
asset_max_dd= Max_Drawdown(asset_wealth) 

#Key metrics dataframe 

metrics_df = pd.DataFrame({'Asset' : main_asset_df_aligned.columns, 'Annualised returns': assset_annualised_returns.values,
                                'Annualised volatility': asset_annual_vol.values, 'Sharpe Ratio' : asset_sharpe.values, 'Max Drawdown': asset_max_dd
                            })

metrics_long = metrics_df.melt(
                    id_vars = 'Asset', 
                    value_vars= ['Annualised returns', 'Annualised volatility','Sharpe Ratio','Max Drawdown' ],
                    var_name ='Metric',
                    value_name= 'Value'
)
metrics_long['Value'] = pd.to_numeric(metrics_long['Value'], errors='coerce')
fig = px.bar(metrics_long,
             x='Value',
             y='Asset',
             barmode='group',
             color='Metric',
             orientation='h',
color_discrete_map = {'Annualised returns': 'blue',
           'Annualised volatility':'orange',
           'Sharpe Ratio': 'green',
           'Max Drawdown':'red'
           })

fig.update_layout(
    title='Asset Class Key Metrics', 
    xaxis_title='Value',
    yaxis_title='Asset',
    xaxis=dict(range=[-0.6,0.8],dtick=0.2),
    legend_title='Metric',
    height=600,
    width=1000
)
#fig.show()

#Cumulative log returns on ETF plot
etf_cum_reset = etf_cum_log_returns.reset_index()
etf_cum_reset.rename(columns={'index': 'Dates'}, inplace=True)
etf_cum_long=etf_cum_reset.melt(id_vars='Dates', var_name='ETF',value_name='Cumulative Log Return')
etf_cum_long['Type']='Individual'

etf_cum_reset = etf_cum_log_returns.reset_index()
etf_cum_reset.rename(columns={'index': 'Dates'}, inplace=True)


etf_cum_reset['Dates'] = pd.to_datetime(etf_cum_reset['Dates'])

median_df = pd.DataFrame({
    'Dates': etf_cum_reset['Dates'],
    'ETF': 'Median',
    'Cumulative Log Return': median_cum_log_returns.values,
    'Type': 'Median'
})
plot_df = pd.concat([etf_cum_long, median_df], ignore_index=True)


fig = px.line(
    plot_df,
    x='Dates',
    y='Cumulative Log Return',
    color='Type',
    line_group='ETF',
    color_discrete_map={
        'Individual': 'lightgrey',
        'Median': 'red'
    },
    title='Cumulative Log Returns of ETFs'
)
fig.update_yaxes(
    range=[-0.25, 1.50],
    tick0=-0.25,
    dtick=0.25,
    title='Cumulative Log Return'
)
fig.update_yaxes(
    range=[-0.25, 1.50],
    tick0=-0.25,
    dtick=0.25,
    title='Cumulative Log Return'
)
#fig.show()