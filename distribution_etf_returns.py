import numpy as np
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import gaussian_kde


from data_prep import (etf_df)
from risk_metrics_analysis import (etf_cum_log_returns)

#total perfromance per etf 

total_returns=etf_cum_log_returns.iloc[-1] 
mean_return=total_returns.mean()
median_return=total_returns.median()
std_return=total_returns.std()
total_returns_df=pd.DataFrame({'Total Return':total_returns})

#histogram


fig = px.histogram(total_returns_df, x='Total Return', nbins=20,color_discrete_sequence=['purple'],opacity=0.7)
fig.add_vline(x=median_return,line=dict(color='red',dash='dash'),name='Median')
fig.add_vline(x=mean_return,line=dict(color='blue',dash='dash'),name='Mean')
fig.add_vline(x=mean_return + std_return ,line=dict(color='yellow',dash='dash'),name='+1 std')
fig.add_vline(x=mean_return - std_return ,line=dict(color='yellow',dash='dash'),name='-1 std')

x_vals=np.linspace(total_returns_df['Total Return'].min(), total_returns_df['Total Return'].max(), 200)
kernel_density=gaussian_kde(total_returns_df['Total Return'])

y_vals=kernel_density(x_vals)*len(total_returns_df)*(total_returns_df['Total Return'].max()-total_returns_df['Total Return'].min())/10

fig.add_scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='blue'), name='Density Curve')

fig.update_layout(
            title ='Distribution of Total ETF Returns', 
            xaxis_title='Total Return',
            yaxis_title='Count',
            xaxis=dict(range=[-0.5,1.5],
                       dtick=2.5),
            yaxis=dict(dtick=2),
            width=900,
            height=500 

)


#fig.show()

