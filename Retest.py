import pandas as pd
import numpy as np
import os
import re

#path
user = os.getenv('USERNAME');
curdir = os.getcwd();
curpath = curdir + "\\";

tp_data = pd.read_csv(curdir+"\\Raw_Data_HDBI.csv",index_col=[0])


def flag_retest(file):
	if (file['within_session_seq_no']>=1 and file['within_lato_latest_flag']=="N"):
		return 1
	else:
		return 0
			
def recovery(file):

	vector=[""]
	detected=file
	if (file['within_session_seq_no']>1 and file['within_lato_latest_flag']=="Y" and file['unit_good_bad_flag']=="G"):	
		vector.append(file['visual_id'])
	

	while("" in vector) :
		vector.remove("")
		return vector
	

tp_data = tp_data.assign(Flag_Retest=tp_data.apply(flag_retest, axis=1))


vector=[""]

back_data=tp_data
back_data.loc[(back_data['within_session_seq_no']>1 ) & (back_data['unit_good_bad_flag']=="G") & (back_data['within_lato_latest_flag']=="Y") , 'Status'] = "Found"

vector=back_data[back_data['Status']=="Found"]['visual_id']

for x in vector:

	tp_data.loc[(tp_data['within_session_seq_no']>=1 ) & (tp_data['visual_id']==x) & (tp_data['within_lato_latest_flag']=="N") , 'Recovery'] = 1



tp_data.loc[(tp_data['within_lato_latest_flag']=="Y") , 'Solid_Bins'] = 1

tp_data["Recovery"].fillna(0, inplace = True)
tp_data["Status"].fillna("N/A", inplace = True)
tp_data.to_csv(curdir+ "\\tp_data_Final.csv")



#tp_data_pivot = pd.pivot_table(tp_data,index=['unit_functional_bin','visual_id','unit_good_bad_flag'],aggfunc={'Flag_Retest':np.sum})

pivot_table = pd.pivot_table(tp_data,index=['unit_functional_bin'],aggfunc={'Flag_Retest':np.sum,'Recovery':np.sum,'Solid_Bins':np.sum})
pivot_table['Qty'] = tp_data['visual_id'].nunique()
pivot_table['Retest'] = pivot_table['Flag_Retest']/pivot_table['Qty']
pivot_table['Recovery_percentage']= pivot_table['Recovery']/pivot_table['Flag_Retest']
pivot_table.to_csv(curdir+ "\\pivot.csv")

##TOP 5 TABLE

def top_5(archieve):
	
	top5_retest = archieve.nlargest(n=5, columns=['Retest'])
	return top5_retest
	

print(top_5(pivot_table))

	
#print(tp_data_pivot)


