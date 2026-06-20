#!python3
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
	ps.add_argument('-r','--range',nargs=2,default=[0,10000],
				 help='Range of database to generate, in mT')
	ps.add_argument('-q','--query',nargs=3,
				 help='Query to match, 3 commands: <column> <lower bound> <upper bound>')
	ps.add_argument('-n','--nuclei',nargs='*',default=['e-','1H'],
				 help='List of nuclei to show. If not supplied,  e- and 1H are shown.')
	args=ps.parse_args()
	
	# Numbers from wikipedia.org/wiki/Gyromagnetic_ratio, units of MHz/mT
	gamma = { # isotope: value
			'e-':   28024.9513861/1E6, # GHz/mT
			'1H':	42.57747846118/1E3,
			'13C':	10.7084/1E3,
			}
	gs = dict(zip(args.nuclei, map(gamma.get, args.nuclei)))
	data = pl.DataFrame({"B":
				pl.select(
					pl.linear_space(args.range[0],args.range[1],args.range[1]-args.range[0]+1)
				)
			})
	data = data.with_columns(
			[larmour(pl.col("B"),list(gs.values())[k]).alias(list(gs.keys())[k]) for k in range(len(gs))]
			)
	if args.query is not None:
		ans = data.filter(
			# find  query[1] <= query[0] <= query[2], where query 0 is the column name
			# and query 1 and 2 are the values.
			pl.col(args.query[0]).ge(float(args.query[1])) &
			pl.col(args.query[0]).le(float(args.query[2])))
		print(ans)
	
	else:
		from plotly import io as pio
		layout = {}
		layout['xaxis'] = {'title':'B (mT)','tickformat':'none'}
		traces = []
		offset = 0.1
		for j, col in enumerate(data.columns[1:]):
			traces.append({'x':data['B'],'y':data[col],'yaxis':f'y{j+1}','mode':'lines',
				'name':col})
			layout[f'yaxis{j+1}'] = {'side':'right', 'anchor':'free','position':1,
				'range':[0+data[col].max()*offset,data[col].max()*(1+offset)],
				'title':f'{col} Larmour (MHz)', 'exponentformat':'power','tickformat':".4g"}
			if col == 'e-':
				layout[f'yaxis{j+1}']['side']  = 'left'
				layout[f'yaxis{j+1}']['position']  = 0
				layout[f'yaxis{j+1}']['title'] = f'{col} Larmour (GHz)'
		pio.write_html({'data':traces,'layout':layout},'larmour.html',auto_open=True)

if __name__=="__main__":
	main()
