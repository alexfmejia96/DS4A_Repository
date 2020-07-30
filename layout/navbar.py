import dash_html_components as html
from pathlib import Path
import dash_bootstrap_components as dbc

btns_style = {
    'padding': 'inherit',
    'text-align': 'left' 
    }

def mdl_A(A_label, A_icon, A_style=dict(), A_href='#', id=''):
  icon_style = {'marginRight': '25px'}
  if 'color' in A_style.keys():
    icon_style['color'] = A_style['color']

  r=html.A(className='mdl-navigation__link mdl-list__item-primary-content', id=id, href=A_href, children=[
      html.I(className='material-icons mdl-list__item-icon', style=icon_style, children=A_icon),
      A_label
    ], style=A_style)

  return(r)

def panel_gdrive(msg=None, n_clicks=0):
  r=[
      html.H4(className='mdl-card__title-text', children='Google Drive',
        style={'font-size':'24px','margin-bottom':'16px','overflow':'visible','color':'white'}),
      dbc.Textarea(placeholder="Pegar Código del Token", id='code_input', value=msg,
        style={'outline-color':'var(--accent_d)','color':'var(--primary_d)','min-height':'40px'}),
      html.Div(style={'margin-top':'16px'}, children=[
        html.A('ACCEDER', className='mdl-button', style={'color':'white'}, target='_blank', id='get_code'),
        html.A('AUTENTICAR', className='mdl-button', style={'color':'white'}, n_clicks=n_clicks, id='set_code'),
      ])
    ]

  return(r)

def panel_folders():
  r=[
    html.H4(className='mdl-card__title-text', style={'font-size':'24px','margin-bottom':'8px','overflow':'visible','color':'white'},
      children='Lista de Carpetas'),
    dbc.Select(id='folder_list', style={'outline-color':'var(--accent_d)'}),
    mdl_A('DESCARGAR IMÁGENES', 'cloud_download', dict({'color':'white','outline': 'auto','margin-top':'10px'}, **btns_style), id='btn_driveld') 
  ]

  return(r)

def new():

  r=html.Div(className='mdl-layout__drawer', children=[
      html.Nav(className='mdl-navigation mdl-list__item', style={'height':'100%'}, children=[
        mdl_A('CARGAR IMÁGENES', 'publish', btns_style, id='btn_loadimg'),
        mdl_A('DATOS DE IMÁGENES', 'analytics', btns_style, id='btn_meta'),
        mdl_A('CLASIFICAR IMAGENES', 'image_search', btns_style, id='btn_class'),
        html.Hr(),

        html.Div(className='mdl-card mdl-shadow--2dp input-panel', id='view_gdrive', hidden=True,
          children=panel_gdrive()),

        html.Div(className='mdl-card mdl-shadow--2dp input-panel', id='view_folders', hidden=True, children=panel_folders(),
          style={'margin-top':'16px'}),

        html.Div(className='mdl-layout-spacer'),
        html.Label('-', id='dw_result', style={'color':'var(--accent_d)'}),
        html.Div(id='nav_bottom_box', children=[
          html.Div(id='debug_output', children=''),
          html.Hr(),
          mdl_A('RE-ENTRENAR', 'autorenew'),
          mdl_A('CONFIGURAR', 'settings'),
        ])
      ])
    ])

  return(r)
