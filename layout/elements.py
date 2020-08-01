import dash_html_components as html
import dash_bootstrap_components as dbc
from pathlib import Path
import json, glob
from folium import FeatureGroup, LayerControl, Map, Marker
from utils import misc

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
		html.H3(children='Aun no se han cargado imágenes!')
		])
	return(r)

def content_update(title, children):
    children = [children] if type(children) != list else children

    r =	html.Div(className='demo-card-square mdl-card', style={'background':'transparent', 'height':'100%'}, children=[
          html.Div(className='mdl-card__title mdl-card--expand', children=[
              html.H2(className='mdl-card__title-text vertical-center', children=title),
              html.Div(className='mdl-layout-spacer', children=''),
              #icon_button('visibility'),
              #icon_button('delete'),
          ])
    ]+ children)
    
    return(r)

def result_card(img_title='', img_det='', img_class='', img_url=''):

  r=html.Div(className='demo-card-wide mdl-card mdl-shadow--2dp', children=[
        html.Div(className='mdl-card__title', style={'background': f'url(\'{img_url}\') center / cover'}, children=[
          html.H2(className='mdl-card__title-text result', style={'bottom':'10px', 'left':'10px'}, children=img_title.upper())
        ]),
        #html.Img(className='mdl-card__title', src=img_url),
        html.Div(className='mdl-card__supporting-text', children=[    
          img_det
        ]),
        # html.Div(className='mdl-card__actions mdl-card--border', children=[
        #   html.A(className='mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect', style={'color':'green'}, children=[
        #   img_class
        #   ])
        # ])
    ])

  return(r)

def result_card_list(main_dir):
  dir_list = list(Path(main_dir).rglob('*.[Jj][Pp][Gg]'))
  card_list = []
  detection = {}

  for img_dir in dir_list:
    _img_dir = str(img_dir).replace('\\','/')
    img_name = img_dir.name.split('.')[0]
    json_dir = _img_dir.replace('jpg','json')

    if Path(json_dir).is_file():
      with open(json_dir) as json_file:
        json_dict = json.load(json_file)
        detection = dict(**detection, **json_dict)
        card_det = []

        for i, isolator in enumerate(json_dict[img_name]):
          card_det.append(html.Div(style={'margin-left':'16px'},
            children=f"Aislador {['Malo','Bueno'][isolator['cls_id']]}#{i+1}: Probabilidad {isolator['conf']*100:.2f}%"))
          
        
        good, bad = good, bad = misc.detect_count(json_dict)
        state, color = ['BUEN', 'green'] if good==1 else ['MAL', 'red']
        img_det = html.Div([
          html.Div(f'AISLADORES EN {state} ESTADO',
            style={'color':color,'font-weight':'bold','font-family':"'Saira Condensed',sans-serif",'font-size':'20px','margin-bottom':'4px'}),
          html.Div(card_det)
        ])

    else:
      img_det = html.Div('No se detectaron Aisladores!')

    card = result_card(
      img_title=str(img_dir.name),
      img_det= img_det,
      img_class='None',
      img_url=_img_dir
    )

    card_list.append(card)

  return([card_list, detection])

def generate_options(path_list):
  img_options = [{'label':'>TODAS LAS IMÁGES', 'value':'all'}]

  for path in path_list:
    _path = str(path).replace('\\','/')
    json_path = _path.replace('jpg','json') 
    sign = '+' if Path(json_path).is_file() else '' 
    
    option = {'label':f'{sign}{path.name.upper()}', 'value':_path}
    img_options.append(option)

  return(img_options)

def meta_row(key='', value=''):
  r=html.Tr(children=[
      html.Td(className='mdl-data-table__cell--non-numeric', children=key),
      html.Td(className='mdl-data-table__cell--non-numeric', children=value)
    ])
  return(r)

def img_details_view(asd):
  img_list = list(Path('assets/').rglob('*.jpg'))
  img_list.sort(key=lambda x: x.name)

  r=html.Div(style={'height':'100%'}, children=[
      html.Div(style={'display':'flex'}, children=[
        html.Div(className='mdl-card mdl-shadow--2dp', id='meta_map',
          style={'width':'65%','margin-right':'8px','background':'white'}),
        html.Div(className='mdl-card mdl-shadow--2dp', style={'witd':'100%'}, children=[
          dbc.Select(id='img_list', options=generate_options(img_list), value='all'),

          html.Table(className='mdl-data-table mdl-js-data-table mdl-data-table',
            style={'border-left':'0','border-right':'0','bottom':'-1px'}, children=[

            html.Tbody(id='meta_table', children=[meta_row()]*5)
          ])
        ])
      ]),

      html.Img(className='mdl-card mdl-shadow--2dp', id='meta_img',
        style={'margin':'8px 0','width':"100%"}, src='')
    ])

  return(r)

def img_map(img_data):
  coord = [float(i) for i in img_data['Coord'].split(' , ')]
  map = Map(location=coord, zoom_start=10,
            width='100%', height='100%',
            tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', attr='Google')

  Marker(coord).add_to(map)
  return(map._repr_html_())
