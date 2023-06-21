import pandas as pd

old_data = pd.read_csv('old_data.csv')
new_data = pd.read_csv('new_data.csv')

old_data2 = old_data[['Name','Platform','Year','Genre','Publisher','Global_Sales']].copy()
old_data2.columns = ['Title','Platform(s)','Year','Genre','Publisher','Sales Unit']
old_data2.loc[:,'Sales'] = ['Unknown']*len(old_data2)

new_data2 = new_data[['Title','Platform(s)','Year','Genre','Sales']].copy()
new_data2.columns = ['Title','Platform(s)','Year','Genre','Sales']
new_data2.loc[:,'Publisher'] = ['Unknown']*len(new_data2)
new_data2.loc[:,'Sales Unit'] = ['Unknown']*len(new_data2)

new_data2 = new_data2[['Title','Platform(s)','Year','Genre','Sales','Publisher','Sales Unit']]
old_data2 = old_data2[['Title','Platform(s)','Year','Genre','Sales','Publisher','Sales Unit']]

final_data = pd.concat([old_data2,new_data2],axis=0)
final_data.to_csv('final_data.csv',index=False)
