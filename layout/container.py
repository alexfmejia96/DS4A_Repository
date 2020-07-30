import dash_html_components as html

def new(children, id=''):
	r =	html.Main(className="mdl-layout__content",
	    	children = html.Div(className="page-content", style={'height':'100%'},
	      		children = children,
                id=id
	      	)
	    )

	return(r)
