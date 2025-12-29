import numpy as np
import pandas as pd 

#READ DATA 

#Data ETF READING
etf_df=pd.read_csv("Anonymized ETFs.csv")
etf_df.dropna(inplace=True)
etf_df.rename(columns = {'Unnamed: 0':'Dates'}, inplace = True) 

#Data MAIN ASSET CLASSES READING
main_asset_df=pd.read_csv("Main Asset Classes.csv", skiprows=4, parse_dates=True)
main_asset_df.dropna(how='all')
main_asset_df=main_asset_df.rename(columns={main_asset_df.columns[0]:'Dates'})
main_asset_df = main_asset_df.iloc[1:] 


#Data MYSTERY ALLLOCATIONS 
mystery_asset_one_df=pd.read_csv("Mystery Allocation 1.csv", header =0 , index_col= 0, parse_dates=True)
mystery_asset_two_df=pd.read_csv("Mystery Allocation 2.csv", header =0, index_col= 0, parse_dates=True)

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

