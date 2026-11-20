#!python3
from argparse import ArgumentParser, Namespace
import pandas as pd
from numpy import linspace
from pathlib import Path
import sys


def larmour(B,gamma):
	omega  = gamma*B
	return omega

def parseArgs() -> tuple[Namespace,linspace]:
	"""
	Parse command line arguments.
	"""
	ps = ArgumentParser(prog='larmour',
			description='Allows querying of the relative value of proton (in\
					 MHz) and electron (in GHz) larmours at a certain field.',
			epilog='If query is not specified, the data is plotted in the \
			browser with plotly. Queryable variables: B=the field, proton=the\
			proton larmour value, electron=the electron larmour value'
			)
	ps.add_argument('-f','--field',nargs=2,help='Range of fields to generate, in mT')
	ps.add_argument('-p','--plot',action='store_true',help='Plot the data')
	ps.add_argument('--showisotopes',nargs='*',help='Print the isotope data for this isotope.')
	ps.add_argument('-q','--query',nargs='*',help='Pandas dataframe query string(s) to match. Use ` around isotopes.')
	ps.add_argument('-i','--isotopes',nargs='*',help='List of isotopes to display. If not supplied, all are displayed.')
	# print help if no arguments supplied
	if len(sys.argv)==1:
		ps.print_help(sys.stderr)
		sys.exit(1)
	# parse args
	args=ps.parse_args()
	
	if args.field is not None:
		lrange = float(args.field[0])
		hrange = float(args.field[1])
		field = linspace(lrange,hrange,int(hrange-lrange+1)) 
	else:
		field = linspace(0,10000,10001)
	# allow any case for input
		#if args.isotopes is not None:
		#	args.isotopes = list(map(str.upper, args.isotopes))
		#if args.showisotopes is not None:
		#	args.showisotopes = list(map(str.upper, args.showisotopes))
	return args,field

def parseQuery(query,data:pd.DataFrame)->pd.DataFrame:
	"""
	Use the --query argument to filter the frequencies.
	"""
	for j in query:
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
		else:
			raise ValueError(f'No close match to query string {query} found.')
	return ans

def generatePlot(data:pd.DataFrame,field) -> str:
	from plotly import io as pio
	layout = {'title':'Proton vs. electron larmour'}
	layout['xaxis'] = {'title':'B (mT)','tickformat':'none'}#,'range':[data.index.min()*-2,data.index.max()+2]}
	layout['yaxis'] = {'side':'left', 'anchor':'free','position':0,
		'title':r'Larmour (MHz)',
		'exponentformat':'power','tickformat':".4g"}
	traces = []
	for d in data.columns:
		traces.append({'x':field,'y':data[d],'yaxis':'y1','mode':'lines','name':d})
	pio.write_html({'data':traces,'layout':layout},'larmour.html',auto_open=True)
	return "Plotting done."

def loadIsotopes(filename):
	"""
	Load an EasySpin isotopedata.txt file & parse it into isotope info.
	"""
	g2larmour = 7.62259328547 # MHz/T, mu_N/h
	colnames = ["NProtons","NNucleons","Radioactive","Symbol","Name",
		"I","mu","Abundance","Q"]
	isotopes = pd.read_csv(filename,sep='\\s+',comment='%',names=colnames)
	isotopes = isotopes[isotopes['NProtons'] > 0 ]
	isotopes = isotopes[ isotopes['NNucleons'] > 0 ]
	isotopes["Radioactive"] = isotopes["Radioactive"].replace("*",True).replace("-",False)
	isotopes["g"] = isotopes['mu'] / isotopes['I']
	isotopes["gamma"] = isotopes['g']*g2larmour
	isotopes['Symbol'] = isotopes['NNucleons'].astype(str)+ isotopes['Symbol']
	return isotopes

def getFreqs(isotopedata,field,isotopes):
	larpar = isotopedata[['Symbol','gamma']]
	if isotopes is not None:
		larpar = larpar[larpar['Symbol'].isin(isotopes)]
	larpar = larpar.dropna()
	larpar = larpar.set_index('Symbol',drop=True)['gamma']
	datalist = []
	for iso in larpar.index:
		datalist.append(pd.Series(larpar[iso]*field/1000,index=field,name=iso))
	data = pd.concat(datalist,axis=1)
	data.index.name = 'B (mT)'
	return data

def main():
	args,field = parseArgs()
	isodatafile = Path(__file__).parent / 'isotopedata.txt'
	isotopes = loadIsotopes(isodatafile)
	if args.showisotopes is not None:
		if len(args.showisotopes) == 1 and args.showisotopes[0] == '*':
			print(isotopes.to_string())
		else:
			print(isotopes[isotopes['Symbol'].isin(args.showisotopes)].to_string())
	else:
		freqs = getFreqs(isotopes,field,args.isotopes)
		if args.query is not None:
			val = parseQuery(args.query,freqs)
		elif args.plot:
			val = generatePlot(freqs,field)
		else:
			print(freqs.to_string())
			val = None
		print(val) if val is not None else None

if __name__=="__main__":
	main()
