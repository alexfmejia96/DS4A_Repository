import dash_html_components as html
from layout import elements

def table_row(val_list):
	td_list = [html.Td(className='mdl-data-table__cell--non-numeric', children=val) for val in val_list]
	r = html.Tr(children=td_list)
	return(r)


def new(df, col_names):
	table_head = html.Tr([html.Th(col_names[col], className='mdl-data-table__cell--non-numeric') for col in df.columns])

	r =	html.Table(className='mdl-data-table mdl-js-data-table', id='t_table', style={'width':'100%'}, children=[
	    	html.Thead(children= table_head),
	        html.Tbody(id='t_body', children= [table_row(df.iloc[i]) for i in df.index])
		])

	return(r)