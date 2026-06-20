#!python3
#from plotly import express as px
from numpy import linspace
from argparse import ArgumentParser
import polars as pl

# Goal: plot relationship between proton larmour and electron g value
def larmour(B,gamma):
	omega  = gamma*B
	return omega

def main():
	ps = ArgumentParser(prog='larmour',
			description='Allows querying of the relative value of proton (in MHz) and electron (in GHz) larmours at a certain field.',
			epilog='If query is not specified, the data is plotted in the browser with plotly. Queryable variables: B=the field, proton=the proton larmour value, electron=the electron larmour value'
			)
	ps.add_argument('-r','--range',nargs=2,help='Range of database to generate, in mT')
	ps.add_argument('-q','--query',nargs=3,help='Query to match, 3 commands: <column> <lower bound> <upper bound>')
	args=ps.parse_args()
	
	if args.range is not None:
		b = linspace(args.range[0],args.range[1],args.range[1]-args.range[0]+1) 
	else:
		b = linspace(0,10000,10001)
	
	# Numbers from wikipedia.org/wiki/Gyromagnetic_ratio, units of MHz/mT
	gamma = { # isotope: value
			'e-':  -28024.9513861/1E3,
			'1H':	42.57747846118/1E3,
			'13C':	10.7084/1E3,
			}

	data = pl.DataFrame({'B':b})
	data = data.with_columns([larmour(pl.col("B"),list(gamma.values())[k]).alias(list(gamma.keys())[k]) for k in range(len(gamma))])
	
	if args.query is not None:
		ans = data.filter(
			# find  query[1] <= query[0] <= query[2], where query 0 is the column name
			# and query 1 and 2 are the values.
			pl.col(args.query[0]).ge(float(args.query[1])) &
			pl.col(args.query[0]).le(float(args.query[2])))
		print(ans)
	
	else:
		from plotly import io as pio
		layout = {'title':'Proton vs. electron larmour'}
		layout['xaxis'] = {'title':'B (mT)','tickformat':'none'}
		traces = []
		traces.append({'x':b,'y':data['1H'],'yaxis':'y1','mode':'lines','name':r'1H'})
		traces.append({'x':b,'y':data['e-'],'yaxis':'y2','mode':'lines','name':r'e-'})
		layout['yaxis1'] = {'side':'left', 'anchor':'free','position':0,'range':[0,data['1H'].max()*1.1], 
			'title':r'1H Larmour (MHz)','exponentformat':'power','tickformat':".4g"}
		layout['yaxis2'] = {'side':'right', 'anchor':'free','position':1,'range':[-0.1*data['e-'].max(),data['e-'].max()],
			'overlaying':'y1','title':'e- Larmour (GHz)','exponentformat':'power',
			'tickformat':".4g"}
		pio.write_html({'data':traces,'layout':layout},'larmour.html',auto_open=True)

if __name__=="__main__":
	main()
