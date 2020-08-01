import dash_html_components as html
from pathlib import Path
import dash_bootstrap_components as dbc
import dash_core_components as dcc

btns_style = {
    'padding': '12px 16px',
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
        style={'font-size':'24px','margin-bottom':'16px','color':'white'}),
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
    html.H4(className='mdl-card__title-text', style={'font-size':'24px','margin-bottom':'8px','color':'white'},
      children='Lista de Carpetas'),
    dbc.Select(id='folder_list', style={'outline-color':'var(--accent_d)'}),
    mdl_A('DESCARGAR IMÁGENES', 'cloud_download', id='btn_driveld',
      A_style={'color':'white','outline':'auto','margin-top':'10px','padding':'12px 8px'}) 
  ]

  return(r)

def panel_param():
  r=[
      html.H4(className='mdl-card__title-text', style={'font-size':'24px','margin-bottom':'4px','overflow':'visible','color':'white'},
        children='Parámetros de Detección'),
      dbc.Form([
        dbc.FormGroup([
          html.Div('+ Modelo', className='label'),
          dbc.RadioItems(id='p_model', options=[{'label': 'YOLOv5 Best', 'value':'weights/best_yolov5s_results.pt'}],
            value='weights/best_yolov5s_results.pt')
        ]),
        dbc.FormGroup([
          html.Div('+ Tamaño de Imágen', className='label'),
          dbc.Input(type='number', id='p_img', step=32, value=416, min=32, max=1024) #min=0, max=10
        ]),
        
        dbc.FormGroup([
          html.Div('+ Confianza:   0.4', className='label', id='lab_conf'),
          dcc.Slider(id='p_conf', min=0.1, max=0.9, step=0.1, value=0.4)
        ]),
      ]),

      # html.Div(style={'margin-top':'8px'}, children=[
      #   html.A('CANCELAR', className='mdl-button', style={'color':'white'}, id='p_cancel'),
      #   html.A('GUARDAR', className='mdl-button', style={'color':'white'}, id='p_save'),
      # ])
    ]

  return(r)

def new():

  r=html.Div(className='mdl-layout__drawer', children=[
      html.Nav(className='mdl-navigation mdl-list__item', style={'height':'100%'}, children=[
        mdl_A('CARGAR IMÁGENES', 'publish', btns_style, id='btn_loadimg'),
        mdl_A('DETALLE DE IMÁGENES', 'analytics', btns_style, id='btn_meta'),
        mdl_A('CLASIFICAR IMÁGENES', 'image_search', btns_style, id='btn_class'),
        html.Hr(style={'margin-bottom':'0'}),

        html.Div([

          html.Div(className='mdl-card mdl-shadow--2dp input-panel',id='view_gdrive', hidden=True, children=panel_gdrive(),
            style={'margin-top':'12px'}),
          html.Div(className='mdl-card mdl-shadow--2dp input-panel',id='view_folders', hidden=True, children=panel_folders(),
            style={'margin-top':'12px'}),
          html.Div(className='mdl-card mdl-shadow--2dp input-panel', id='view_param', hidden=False, children=panel_param(),
            style={'margin-top':'12px'}),
        ], id='view_container'),

        html.Div(className='mdl-layout-spacer'),
        # html.Div(id='nav_bottom_box', children=[
        #   html.Div(id='debug_output', children=''),
          
        #   #html.Hr(style={'margin-bottom': '12px'}),
        #   #mdl_A('RE-ENTRENAR', 'autorenew'),
        #   #mdl_A('PARÁMETROS', 'settings'),
        # ])
      ])
    ])

  return(r)
