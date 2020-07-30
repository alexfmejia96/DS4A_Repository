import dash_html_components as html

def menu_li(children):
  r = 	html.Li(className='mdl-menu__item', children=children)
  return(r)

def menu(children):
	r = html.Label(className='mdl-menu mdl-menu--bottom-right mdl-js-menu mdl-js-ripple-effect',
		htmlFor='demo-menu-lower-right',
		children=children)
	return(r)

def icon_button(children, id=''):
	r =	html.Button(className='mdl-button mdl-js-button mdl-button--icon', id=id,
			children= html.I(className='material-icons', children=children)
		)
	return(r)

def empty_msg():
	r = html.Div(className='empty-msg', children=[
		html.I(className='material-icons', style={'font-size': '500px', 'width':'100%'}, children='filter_hdr'),
		html.H3(children='Aun no se han subido imágenes!')
		])
	return(r)

def content_update(title, children):
    children = [children] if type(children) != list else children

    r =	html.Div(className='demo-card-square mdl-card', style={'background':'transparent', 'height':'100%'}, children=[
          html.Div(className='mdl-card__title mdl-card--expand', children=[
              html.H2(className='mdl-card__title-text vertical-center', children=title),
              html.Div(className='mdl-layout-spacer', children=''),
              icon_button('visibility'),
              icon_button('delete'),
          ])
    ]+ children)
    
    return(r)

def result_card(img_title='', img_det='', img_class='', img_url=''):

  r=html.Div(className="demo-card-wide mdl-card mdl-shadow--2dp", children=[
        html.Div(className="mdl-card__title", style={'background': f'url(\'{img_url}\') center / cover'}, children=[
          html.H2(className="mdl-card__title-text result", style={'bottom':'10px', 'left':'10px'}, children=img_title)
        ]),
        html.Div(className="mdl-card__supporting-text", children=[    
          img_det
        ]),
        html.Div(className="mdl-card__actions mdl-card--border", children=[
          html.A(className="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect", style={'color':'green'}, children=[
          img_class
          ])
        ])
    ])

  return(r)