import numpy as np
import pandas as pd 
import plotly.express as px 

from data_prep import (
    etf_df,
    main_asset_df_aligned,
    start_date,
    end_date
)

#visualising ETF with stanbdardized Z-scores 
etf_z = (etf_df - etf_df.mean()) / etf_df.std() 
etf_z_reset = etf_z.reset_index().rename(columns={'index': 'Dates'})
etf_long=etf_z_reset.melt(id_vars='Dates', var_name= 'ETF', value_name='Z-scores')


fig = px.line(etf_long, x = 'Dates', y ='Z-scores', title= 'standardized price series(Z-scores) of ETFs') 

fig.update_traces(line=dict(color='black'), opacity = 0.6)

fig.update_layout(
        yaxis=dict(title ='Z- scores', tickmode='linear', tick0=-4,dtick=1,range=[-4,4]), 
        xaxis=dict(title ='Year', range = ['2019-01-01', '2024-05-20'],dtick="M12",tickformat="%Y",ticklabelmode="period"), height = 600, width = 1200)
                   
#fig.show()

#list of equities and assets other
equities=["S&P 500","Nasdaq 100","US Small Caps","Euro Stoxx 50","UK FTSE","MSCI EM","Japan"]
other_assets=["US IG","US HY","EU IG","EU HY","EM Bond","Gold","Commodity"]

main_asset_z =(main_asset_df_aligned - main_asset_df_aligned.mean())/main_asset_df_aligned.std()#z scores of main asset classes 
main_asset_z_reset = main_asset_z.reset_index().rename(columns={'index':'Dates'})
main_asset_z_long=main_asset_z_reset.melt(id_vars ='Dates', var_name='Asset',value_name='Z_score')
main_asset_z_long['Asset Type']=main_asset_z_long['Asset'].apply(lambda x: 'Equity' if x in equities else 'Other')

#visualizing equities and other assets with standardized z scores

fig_assets = px.line(
    main_asset_z_long, x = 'Dates', y ='Z_score', color='Asset Type', color_discrete_map={'Equity':'blue', 'Other': 'red'}
) 
fig_assets.update_traces(opacity=0.7)

fig_assets.update_layout( yaxis=dict(title='Z-scores', tickmode='linear',tick0=-4, dtick=1,range=[-4,4]), xaxis=dict(title='Year',
                                                               range=[start_date, end_date],tickformat='%Y'), height = 600, width=1200,
                                                               legend_title_text='Asset Type') 


#fig_assets.show()                                                                                                              
                     
