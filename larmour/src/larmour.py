#!python3
#from plotly import express as px
from numpy import linspace
from argparse import ArgumentParser,Namespace
import pandas as pd

def larmour(B,gamma):
	omega  = gamma*B
	return omega

def parseArgs() -> tuple[Namespace,linspace]:
	ps = ArgumentParser(prog='larmour',
			description='Allows querying of the relative value of proton (in\
					 MHz) and electron (in GHz) larmours at a certain field.',
			epilog='If query is not specified, the data is plotted in the \
			browser with plotly. Queryable variables: B=the field, proton=the\
			proton larmour value, electron=the electron larmour value'
			)
	ps.add_argument('-r','--range',nargs=2,help='Range of database to generate, in mT')
	ps.add_argument('-d','--data',action='store_true',help='Print the whole generated dataframe of larmours.')
	ps.add_argument('-q','--query',nargs='*',help='Pandas dataframe query string(s) to match. Use ` around isotopes.')
	args=ps.parse_args()
	
	if args.range is not None:
		lrange = float(args.range[0])
		hrange = float(args.range[1])
		field = linspace(lrange,hrange,int(hrange-lrange+1)) 
	else:
		field = linspace(0,10000,10001)
	return args,field

def parseQuery(args,data:pd.DataFrame)->pd.DataFrame:
	for j in args.query:
		print('\nQuery:',j,'\n','-'*30)
		try:
			ans = data.query(j)
		except ValueError:
			raise ValueError('Did you use = instead of == to check for equality?')
		# handle case where there is no exact match
		if ans.empty and '==' in j:
			sq = j.split('==')
			#print(data.index.inferred_type)
			ans = data.iloc[(data[sq[0].replace('`','')]-float(sq[1])).abs().argsort()[:1]]
	return ans

def generatePlot(data:pd.DataFrame,field) -> str:
	from plotly import io as pio
	layout = {'title':'Proton vs. electron larmour'}
	layout['xaxis'] = {'title':'B (mT)','tickformat':'none'}
	traces = []
	traces.append({'x':field,'y':data['1H'],'yaxis':'y1','mode':'lines','name':r'1H'})
	traces.append({'x':field,'y':data['e-'],'yaxis':'y2','mode':'lines','name':r'e-'})
	traces.append({'x':field,'y':data['13C'],'yaxis':'y2','mode':'lines','name':r'13C'})
	layout['yaxis1'] = {'side':'left', 'anchor':'free','position':0,'range':[0,data['1H'].max()*1.1], 
		'title':r'1H Larmour (MHz)','exponentformat':'power','tickformat':".4g"}
	layout['yaxis2'] = {'side':'right', 'anchor':'free','position':1,'range':[-0.1*data['e-'].max(),data['e-'].max()],
		'overlaying':'y1','title':'e- Larmour (GHz)','exponentformat':'power',
		'tickformat':".4g"}
	pio.write_html({'data':traces,'layout':layout},'larmour.html',auto_open=True)
	return "Plotting done."


def main():
	args,field = parseArgs()
	# Numbers from wikipedia.org/wiki/Gyromagnetic_ratio, units of MHz/mT
	gamma = { # isotope: value
		'e-':  -28024.9513861/1E3,
		'1H':	42.57747846118/1E3,
		'13C':	10.7084/1E3,
		}
	
	freqs = [larmour(field,gamma[x]) for x in gamma]
	freqs[0]=-1*freqs[0]/1E3
	freqd = dict(zip(gamma.keys(),freqs))
	
	data = pd.DataFrame(freqd,index=field)
	data.index.name = 'B'
	
	if args.query is not None:
		val = parseQuery(args.query,data)
	elif args.data:
		print(data.to_string())
		val = None
	else:
		val = generatePlot(data,field)
	print(val)

if __name__=="__main__":
	main()
