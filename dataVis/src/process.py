#!python3
# This script reads csv files exported from the UNICORN control software
# used by GE/Cytiva Akta FPLCs, and plots the data for further analysis.
import pandas as pd 
from pathlib import Path
import plotly.io as pio

class dtrace:
	'''
	The dtrace holds one data trace. Several dtrace objects can be created to
	hold all the data in a csv import.

	Arguments
	---------
	rawdata: pd.DataFrame
		The dataframe representation of the unmodified csv.
	firstcol: int
		The first column (indexes) of the trace. The ``firstcol+1`` column will
		be used as the values.
	'''

	def __init__(self,rawdata:pd.DataFrame, firstcol:int):
		self.name	  = rawdata.columns[firstcol]
		self.idx_unit = rawdata.iloc[0,firstcol]
		self.val_unit = rawdata.iloc[0,firstcol+1]
		data		  = rawdata.iloc[1:,firstcol:firstcol+2].dropna()
		data.columns  = ['idx','val']
		for col in data.columns:
			if self.name !='Fraction':
				data[col] = pd.to_numeric(data[col], errors='coerce')
		self.data = data

	def __repr__(self):
		return f"\n----- Trace Object ------\nName: {self.name}\nIndex unit: {self.idx_unit}\nValue unit: {self.val_unit}\n--- Data\n{self.data.dtypes}\n{self.data}"

def process(filepath,instrument):
	# check filepath validity
	fpath = Path(filepath)
	assert fpath.suffix.lower() == '.csv', "File path supplied is not a csv file."
	
	# Check that a valid instrument has been supplied
	implemented=['akta','caryuv']
	#print(args.instrument[0], type(args.instrument[0]))
	assert instrument is not None, 'Please provide an instrument with the -i flag.'
	assert instrument.lower() in implemented, f'Invalid option for instrument. Currently implemented options are: {implemented}'
	
	# fork into different instrument paths
	match instrument.lower():
		case 'akta':
			layout,traces = akta(fpath, args)
		case 'caryuv':
			layout,traces = caryuv(fpath,args)
	#pio.show({'data': traces, 'layout': layout}, renderer='browser')
	pio.write_html({'data': traces, 'layout': layout}, fpath.with_suffix('.html'),auto_open=True)

def akta(fpath,args):
	#TODO fix only the first path plotting for akta data
	# load the data
	data = pd.read_csv(fpath,sep='\t',header=1,encoding='UTF-16',low_memory=False)
	assert(len(data.columns)%2==0)
	split = []
	for n in range(len(data.columns)//2):
		split.append(dtrace(data,2*n))
	
	# Build the PyPlot plot using pio.
	layout = {'title': f'Plot of FPLC data, {fpath}'}
	#layout['xaxis'] = {'title':'Total system volume (mL)','domain':[os*(ls-1),1]} # for showing axes
	layout['xaxis'] = {'title':'Total system volume (mL)','domain':[0,1]}
	layout['legend'] = {'orientation':'h','yanchor':'bottom','y':1.02}
	traces = []
	for d in range(len(split)):
		dt = split[d]
		if dt.name == 'Fraction':
			dt.data.idx = pd.to_numeric(dt.data.idx)
			dt.data['yax'] = 0.1
			dt.data['angle'] = -45
			dt.data['ob1'] = dt.data.idx.shift(periods=-1,fill_value=dt.data.idx.iloc[-1])
			dt.data['center'] = (dt.data.ob1+dt.data.idx)/2
			#traces.append({'y': dt.data.yax, 'x': dt.data.idx,'yaxis':f'y{d+1}','mode':'markers','marker_color':'black','marker_symbol':142})
			#traces.append({'y': dt.data.yax, 'x': dt.data.idx,'yaxis':f'y{d+1}','mode':'text','text':dt.data.val,'textposition':'top right'})
			traces.append({'y': dt.data.yax, 'x': dt.data.idx,'yaxis':f'y{d+1}','mode':'markers+lines+text','marker_color':'black','marker_symbol':142,
				  'text':dt.data.val,'textposition':'top right'})#'textangle':-90})
			layout[f'yaxis{d+1}'] = {'side':'left', 'range':[0,1],'anchor':'free','position':0,'showticklabels':False,'overlaying':'y1'}
			#print(dt)
		else:
			traces.append({'y': dt.data.val, 'x': dt.data.idx, 'name': dt.name, 'yaxis': f'y{d+1}'})
		#	layout[f'yaxis{d+1}'] = {'title':dt.name, 'side':'left', 'range':[dt.data.val.min(),dt.data.val.max()],'overlaying':'y1','position':os*d}
			layout[f'yaxis{d+1}'] = {'side':'left', 'range':[dt.data.val.min(),dt.data.val.max()],'anchor':'free','position':0,'showticklabels':False}
			if d > 0:
				layout[f'yaxis{d+1}']['overlaying']='y1'
				layout[f'yaxis{d+1}']['ticks']=""
		return layout,traces

def caryuv(fpath,args):
	# load the data - skip_blank_lines is true by default
	data = pd.read_csv(fpath,sep=',',header=16,low_memory=False)
	#names = data.columns[3:][::2]
	data.drop('Name',axis=1,inplace=True)
	data.drop([0,1,2,3,4,5,6],axis=0,inplace=True)
	data = data.astype('float')
	#print(data)
	assert(len(data.columns)%2==0)
	split = []
	maxes = []
	for n in range(len(data.columns)//2):
		split.append(dtrace(data,2*n))
		maxes.append(split[n].data.iloc[:,1].max())
	mmax=max(maxes)
	
	# Build the PyPlot plot using pio.
	layout = {'title': f'Plot of UV-Vis data, {fpath}'}
	layout['xaxis'] = {'title':r'Wavelength (nm)','domain':[0,1]}
	layout['legend'] = {'orientation':'h','yanchor':'bottom','y':1.02}
	traces = []
	for d in range(len(split)):
		dt = split[d]
		traces.append({'y': dt.data.val, 'x': dt.data.idx, 'name': dt.name, 'yaxis': f'y{d+1}'})
		layout[f'yaxis{d+1}'] = {'side':'left', 'range':[0,mmax],'anchor':'free','position':0,'showticklabels':False}
		if d == 0:
			layout[f'yaxis{d+1}']['showticklabels'] = True
			layout[f'yaxis{d+1}']['title'] = 'Abs (AU)'
		else:
			layout[f'yaxis{d+1}']['overlaying']='y1'
			layout[f'yaxis{d+1}']['ticks']=""
	return layout,traces

if __name__ == "__main__":
	main()
