import dash_html_components as html
from layout import elements

def new(header_title=''):

  r=html.Header(className='mdl-layout__header', children=[
      html.Div(className='mdl-layout__header-row', id='header', children=[
        html.Span(className='mdl-layout-title', id='header_title', children=header_title),
        html.Div(className='mdl-layout-spacer', children=''),

        html.Div(className='dropdown', children=[
          html.Button(className="mdl-button mdl-button--icon", children=[
            html.I(className="material-icons", children='expand_more')
          ]),

          html.Div(className='dropdown-content', style={'float':'right'}, children=[
            html.Div(style={'padding':'8px 0px'}, children=[
              html.A('Google Dive', href='#', id='btn_gdrive'),
              html.A('Cerrar Sesión', className='disable-item', id='btn_signOut'),
              html.Hr(),
              html.A('Configuración', href='#'),
              html.A('Acerca de', href='#')
            ])
          ])
        ])
      ])
    ])

  return(r)

