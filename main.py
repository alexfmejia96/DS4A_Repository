from pathlib import Path
import os, subprocess, json

import dash, dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from bs4 import BeautifulSoup as BS

from layout import header, navbar, table, elements, container
from utils import misc, gdrive

META_KEYS = list(misc.meta_keys_dic.keys())
COL_NAMES = {
    'filename': 'Nombre de Imágen',
    'path': 'Ruta',
    'Coord': 'Coordenadas',
    'Alt': 'Altitud',
    'C_Date': 'Fecha de Creación'
}

SERVICE = gdrive.Service()
DL_DIR = 'assets/img_input/'
IMG_DATA = None
CURRENT_VIEW = elements.empty_msg()

BTN_COUNT = dict()


scripts = ['https://code.getmdl.io/1.3.0/material.min.js']
external_stylesheets = [
  'https://fonts.googleapis.com/icon?family=Material+Icons',
  'https://fonts.googleapis.com/css2?family=Saira+Condensed:wght@800&display=swap',
  'https://code.getmdl.io/1.3.0/material.blue_grey-light_blue.min.css',
  'https://dl.dropboxusercontent.com/s/uv0jj64e3wku5f2/team85_style.css?dl=1'
  ]


dash_app = dash.Dash(__name__,
  external_scripts=scripts,
  external_stylesheets=external_stylesheets)

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

#---- NAVIGATION BAR ---#
@dash_app.callback(
    Output('main_debug', 'children'),
    [
    Input('btn_loadimg', 'n_clicks'),
    Input('btn_meta', 'n_clicks'),
    Input('btn_class', 'n_clicks')
    ])
def clicks(btn_load, btn_meta, btn_class):
  global CURRENT_VIEW, IMG_DATA
  print('>>Nav callback')

  if btn_check(btn_load, 'btn_load'):
    CURRENT_VIEW = elements.content_update('Lista de Imágenes', 
              html.Div(style={'height':'100%'}, children=
                  table.new(IMG_DATA.as_df(), COL_NAMES)
              )
        )

  elif btn_check(btn_class, 'btn_class'):

    os.chdir('model/')
    os.system('''python detect.py --weights weights/last_yolov5s_results.pt --img 416 --conf 0.4 --source ../assets/img_input --output ../assets/img_output --save-txt''')
    os.chdir('..')
    
    dir_list = list(Path('assets/img_output').rglob("*.[Jj][Pp][Gg]"))
    card_list = []

    for img_dir in dir_list:
      _img_dir = str(img_dir).replace('\\','/')
      json_dir = _img_dir.lower().replace('jpg','json')

      if Path(json_dir).is_file():
        with open(json_dir) as json_file:
          card_det = json.load(json_file)

      else:
        card_det = 'Ningún Aislador fue detectado!'

      card = elements.result_card(
        img_title=str(img_dir.name),
        img_det=str(card_det),
        img_class='None',
        img_url=dash_app.get_asset_url(_img_dir.replace('assets/',''))
      )

      card_list.append(card)

    CURRENT_VIEW = elements.content_update('Resultados',
      html.Div(className="mdl-cell mdl-cell--4-col", children=card_list)
    )

  elif btn_check(btn_meta, 'btn_meta'):
    pass

  else:
    print('>Else!')
    none_check = [BTN_COUNT[k] for k in ['btn_load', 'btn_meta', 'btn_class']]
    CURRENT_VIEW = elements.empty_msg() if not any(none_check) == None else CURRENT_VIEW

  print(BTN_COUNT)
  return(CURRENT_VIEW)


@dash_app.callback(
  [
  Output('btn_signOut', 'className'),
  Output('btn_signOut', 'href'),
  Output('view_gdrive', 'hidden'),
  Output('get_code', 'href')
  ],
  [Input('btn_gdrive', 'n_clicks')]
  )
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
    [Output('view_gdrive','children'),
     Output('view_folders','hidden'),
     Output('folder_list','options')],
    [Input('set_code', 'n_clicks')],
    [State('code_input', 'value')])
def set_code(btn_setcode, token_code):
  global SERVICE, BTN_COUNT
  print('>>CODE callback')

  print(BTN_COUNT, btn_setcode)

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
  global SERVICE, IMG_DATA, DL_DIR

  if btn_check(btn_driveld, 'btn_driveld'):
    img_list = SERVICE.get_files_infolder(sel_folder)
    IMG_DATA = misc.data_object(SERVICE, img_list, META_KEYS, DL_DIR)

    r=html.H4(className='mdl-card__title-text',children=[
        'Datos Descargados',
        html.I(className='material-icons mdl-list__item-icon', children='check_circle',
          style={'color':'white','transform':'scale(1.1)','margin-left':'32px','vertical-align':'sub'})
      ], style={'font-size':'24px','display':'-webkit-inline-box','overflow':'visible','color':'white'})
    return(r)

  return(navbar.panel_folders())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000')


