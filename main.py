
import os, platform, glob
import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State

from layout import header, navbar, table, elements, container
from utils import misc, gdrive

import pandas as pd

PLATFORM = platform.system().lower()
CONFIG = {
  'weights':'weights/best_yolov5s_results.pt',
  'img': 416,
  'conf': 0.4,
  'source': 'assets/img_input',
  'output': 'assets/img_output'
}

SERVICE = gdrive.Service()
META_KEYS = list(misc.meta_keys_dic.keys())
IMG_DATA = None
DETECTION = None
COL_NAMES = {
    'filename': 'Nombre de Imágen',
    'path': 'Ruta',
    'Coord': 'Coordenadas',
    'Alt': 'Altitud',
    'C_Date': 'Fecha de Creación'
}

CURRENT_VIEW = elements.empty_msg()
BTN_COUNT = dict()

external_stylesheets = [
  'https://fonts.googleapis.com/icon?family=Material+Icons',
  'https://fonts.googleapis.com/css2?family=Saira+Condensed:wght@800&display=swap',
  'https://code.getmdl.io/1.3.0/material.blue_grey-light_blue.min.css',
  ]


dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash_app.server

dash_app.layout = html.Div(className="mdl-layout mdl-js-layout mdl-layout--fixed-header", style={'position': 'absolute'}, children=[
  header.new('DS4A Team 85'),
  container.new(children=[
    html.Div(className="mdl-layout mdl-js-layout mdl-layout--fixed-drawer", children=[
      navbar.new(),
      container.new(CURRENT_VIEW, id='main_debug'),
    ])
  ])
])

def btn_check(x, y):
  global BTN_COUNT
  
  BTN_COUNT[y] = None if y not in BTN_COUNT.keys() else BTN_COUNT[y]
  x1 = BTN_COUNT[y]

  if x != None:
    if x>0 and x!=x1:
      print(f'>Click Event on: {y}')
      BTN_COUNT[y] = x
      return(True)

  return(False)

def remove_files():
  global CONFIG
  files = glob.glob(f"{CONFIG['output']}/*") + glob.glob(f"{CONFIG['source']}/*")
  for f in files:
      os.remove(f)
  print('>files were removed')

def detect(weights, img, conf, source, output):
  global PLATFORM; py= 'python' if PLATFORM=='windows' else 'python3'
  os.chdir('model/')
  r = os.system(f'{py} detect.py --weights {weights} --img {img} --conf {conf} --source ../{source} --output ../{output} --save-txt')
  os.chdir('..')    

  return(r)

#---- CALLBACKS ---#
@dash_app.callback(
    Output('main_debug', 'children'),
    [Input('btn_loadimg', 'n_clicks'),Input('btn_meta', 'n_clicks'),Input('btn_class', 'n_clicks')])
def clicks(btn_load, btn_meta, btn_class):
  global CURRENT_VIEW, IMG_DATA, CONFIG
  print('>>Nav callback')

  if btn_check(btn_load, 'btn_load'):
    CURRENT_VIEW = elements.content_update('Lista de Imágenes', 
      html.Div(style={'height':'100%'}, children=
        table.new(IMG_DATA.as_df(), COL_NAMES)
      )
    )

  elif btn_check(btn_meta, 'btn_meta'):
    CURRENT_VIEW = elements.content_update('Detalle de Imágenes', 
      elements.img_details_view('assets')
    )

  elif btn_check(btn_class, 'btn_class'):
    param = ['weights','img','conf','source','output'] 
    detect(*[CONFIG[p] for p in param])
    
    CURRENT_VIEW = elements.content_update('Resultados',
      html.Div(className="mdl-cell mdl-cell--4-col",
        children = elements.result_card_list(CONFIG['output']))
    )

  else:
    print('>Else!')
    none_check = [BTN_COUNT[k] for k in ['btn_load', 'btn_meta', 'btn_class']]
    CURRENT_VIEW = elements.empty_msg() if not any(none_check) == None else CURRENT_VIEW
  
  return(CURRENT_VIEW)

@dash_app.callback(
  [Output('btn_signOut', 'className'), Output('btn_signOut', 'href'), Output('view_gdrive', 'hidden'), Output('get_code', 'href')],
  [Input('btn_gdrive', 'n_clicks')])
def gdrive_connect(btn_gdrive):
  global SERVICE
  print('>>Drive callback')

  if btn_check(btn_gdrive, 'btn_gdrive'):
    return(['', '/', False, SERVICE.auth_url])

  if SERVICE.is_valid != None:
    if not SERVICE.is_valid:
      return(['', '/', False, SERVICE.auth_url])

  return(['disable-item', None, True, ''])

@dash_app.callback(
    [Output('view_gdrive','children'), Output('view_folders','hidden'), Output('folder_list','options')],
    [Input('set_code', 'n_clicks')],
    [State('code_input', 'value')])
def set_code(btn_setcode, token_code):
  global SERVICE, BTN_COUNT

  if btn_check(btn_setcode, 'btn_setcode'):
    SERVICE.auth_service(token_code)

    print(f'>SERVICE.is_valid: {SERVICE.is_valid}')
    if SERVICE.is_valid:
      r=html.H4(className='mdl-card__title-text',children=[
          'Google Drive',
          html.I(className='material-icons mdl-list__item-icon', children='check_circle',
            style={'color':'white','transform':'scale(1.1)','margin-left':'32px','vertical-align':'sub'})
        ], style={'font-size':'24px','display':'-webkit-inline-box','overflow':'visible','color':'white'})

      r1 = [{'label':folder['name'], 'value':folder['id']} for folder in SERVICE.get_folder_list()]
      return([r, False, r1])

  n_clicks = BTN_COUNT['btn_setcode']
  if SERVICE.is_valid != None:
    if not SERVICE.is_valid:
      print('>tk Invalido')
      return([navbar.panel_gdrive('Token Invalido!', n_clicks=n_clicks), True, ''])

  return([navbar.panel_gdrive(n_clicks=n_clicks), True, ''])

@dash_app.callback(
    Output('view_folders','children'),
    [Input('btn_driveld', 'n_clicks')],
    [State('folder_list', 'value')])
def gdrive_download(btn_driveld, sel_folder):
  global SERVICE, IMG_DATA, CONFIG

  if btn_check(btn_driveld, 'btn_driveld'):
    remove_files()

    img_list = SERVICE.get_files_infolder(sel_folder)
    IMG_DATA = misc.data_object(SERVICE, img_list, META_KEYS, CONFIG['source'])

    r=html.H4(className='mdl-card__title-text',children=[
        'Datos Descargados',
        html.I(className='material-icons mdl-list__item-icon', children='check_circle',
          style={'color':'white','transform':'scale(1.1)','margin-left':'32px','vertical-align':'sub'})
      ], style={'font-size':'24px','display':'-webkit-inline-box','overflow':'visible','color':'white'})
    return(r)

  return(navbar.panel_folders())

@dash_app.callback(
    [Output('meta_table','children'),Output('meta_map','children'),Output('meta_img','src')],
    [Input('img_list', 'value')])
def meta_view(sel_img):
  global IMG_DATA, CONFIG

  df = pd.DataFrame({
    'filename':['dji_0016.jpg','dji_0961.jpg'],
    'Coord': ['5.8584 , -75.6777']*2,
    'C_Date': ['05/07/2020 13:20']*2,
    'Alt': ['150.00 m']*2
    })

  print(IMG_DATA.as_df().set_index('filename'))

  df = IMG_DATA.as_df().set_index('filename')
  img_name = sel_img.split('/')[-1].upper()
  img_data = df.loc[img_name]


  meta_table = [
    elements.meta_row('Clase', '---'),
    elements.meta_row('Fecha de Captura', img_data['C_Date'].split(' ')[0]),
    elements.meta_row('Hora de Captura', img_data['C_Date'].split(' ')[1]),
    elements.meta_row('Coordenadas', img_data['Coord']),
    elements.meta_row('Altitud', img_data['Alt']),
    ]

  img_map = misc.map2html(elements.img_map(df.loc[img_name]))
  img_map = html.Iframe(**{'data-html':img_map}, id='meta_frame', style={'width':'100%','height':'100%'})

  return([meta_table, img_map, sel_img])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)
    #dash_app.run_server(host='0.0.0.0', port='8000', debug=True)