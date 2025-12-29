import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns 

#Data ETF READING
etf_df=pd.read_csv("Anonymized ETFs.csv")
etf_df.dropna(inplace=True)
etf_df.rename(columns = {'Unnamed: 0':'Dates'}, inplace = True)
#etf_df = etf_df.iloc[1:].reset_index(drop=True)
#etf_df = etf_df.set_index('Dates')

#Data MAIN ASSET CLASSES READING
main_asset_df=pd.read_csv("Main Asset Classes.csv", skiprows=4, parse_dates=True)
main_asset_df.dropna(how='all')
main_asset_df=main_asset_df.rename(columns={main_asset_df.columns[0]:'Dates'})
main_asset_df = main_asset_df.iloc[1:]
#print(main_asset_df.head(10))

#Data MYSTERY ALLLOCATIONS 
mystery_asset_one_df=pd.read_csv("Mystery Allocation 1.csv", header =0 , index_col= 0, parse_dates=True)
mystery_asset_two_df=pd.read_csv("Mystery Allocation 2.csv", header =0, index_col= 0, parse_dates=True)
#print(etf_df.head(10))

#PERIOD SPANNED BY ETF AND MAIN ASSET CLASSES
etf_df["Dates"]=pd.to_datetime(etf_df["Dates"], dayfirst= True)
etf_df=etf_df.set_index("Dates")
main_asset_df["Dates"]=pd.to_datetime(main_asset_df["Dates"], dayfirst= True)
main_asset_df=main_asset_df.set_index("Dates")
#print(main_asset_df.index)
#print(main_asset_df.index.dtype)
#print("start date:", etf_df.index.min()) 
#print("end date:", etf_df.index.max())
#print("start date:", main_asset_df.index.min()) 
#print("end date:", main_asset_df.index.max())


#ALIGNING DATA TO ETF DATE RANGE FOR COMPARABILITY AND CONSISTENCY OF ANALYSES 

start_date = etf_df.index.min()
end_date=etf_df.index.max()
#restriction of all data sets to etf daterange 
main_asset_df_aligned=main_asset_df.loc[start_date:end_date]
#print(main_asset_df_aligned)

full_index_etf=pd.date_range(start= start_date, end=end_date, freq='D')
missing_dates=full_index_etf.difference(main_asset_df_aligned.index)
#print(missing_dates)

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
                                                                                        



