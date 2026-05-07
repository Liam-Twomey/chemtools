#!python3
import pandas as pd 
#import matplotlib.pyplot as plt
from pathlib import Path
#import plotly.graph_objects as go
import plotly.io as pio

class dtrace:
	def __init__(self,rawdata:pd.DataFrame, firstcol:tuple):
		self.name     = rawdata.iloc[0,firstcol]
		self.idx_unit = rawdata.iloc[1,firstcol]
		self.val_unit = rawdata.iloc[1,firstcol+1]
		data          = rawdata.iloc[2:,firstcol:firstcol+2].dropna()
		data.columns  = ['idx','val']
		for col in data.columns:
			if self.name !='Fraction':
				data[col] = pd.to_numeric(data[col], errors='coerce')
		self.data = data

	def __repr__(self):
		return f"\n----- Trace Object ------\nName: {self.name}\nIndex unit: {self.idx_unit}\nValue unit: {self.val_unit}\n--- Data\n{self.data.dtypes}\n{self.data}"

# load the data
fpath = Path('./2026-05-04-run2.csv')
data = pd.read_csv(fpath,sep='\t',encoding='UTF-16',low_memory=False)
tracen = list(data.loc[0].dropna())
#traced = [x for pair in zip(tracen,tracen) for x in pair]
dclean = data.loc[2:]#.to_numpy()
assert(len(data.columns)%2==0)
split = []
for n in range(len(data.columns)//2):
	split.append(dtrace(data,2*n))
#print(split)

ls = len(split)
os = 0.05
layout = {'title': f'Plot of FPLC data, {fpath}'}
#layout['xaxis'] = {'title':'Total system volume (mL)','domain':[os*(ls-1),1]} # for showing axes
layout['xaxis'] = {'title':'Total system volume (mL)','domain':[0,1]}
layout['legend'] = {'orientation':'h','yanchor':'bottom','y':1.02}
traces = []
for d in range(len(split)):
	dt = split[d]
	if dt.name == 'Fraction':
		None
	else:
		traces.append({'y': dt.data.val, 'x': dt.data.idx, 'name': dt.name, 'yaxis': f'y{d+1}'})
	#	layout[f'yaxis{d+1}'] = {'title':dt.name, 'side':'left', 'range':[dt.data.val.min(),dt.data.val.max()],'overlaying':'y1','position':os*d}
		layout[f'yaxis{d+1}'] = {'side':'left', 'range':[dt.data.val.min(),dt.data.val.max()],'anchor':'free','position':0,'showticklabels':False}
		if d > 0:
			layout[f'yaxis{d+1}']['overlaying']='y1' 

pio.show({'data': traces, 'layout': layout})
