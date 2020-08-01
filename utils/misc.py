import folium
from folium import FeatureGroup, LayerControl, Map, Marker
import pandas as pd
from bs4 import BeautifulSoup as BS
import base64
from pathlib import Path

#Error unique img file
#Img with no atts

meta_keys_dic = {
	'GPS': 34853,
	'C_Date': 36867
}

def clean_coord(ref):
	try:
		return(ref[0]/ref[1])
	except:
		if ref > 10:
		  return ref/10

def parse_GPS_info(GPS_info):
	GPS_info = [GPS_info[2], GPS_info[4], GPS_info[6]]
	coord = [None]*3

	if type(GPS_info[0][0]) == tuple:
		raw_coord = [[clean_coord(ref) for ref in val] for val in GPS_info]
		coord[2] = raw_coord[2][0]
	else:
		raw_coord = GPS_info
		coord[2] = raw_coord[2]

	coord[0] = float(raw_coord[0][0] + raw_coord[0][1]/60 + raw_coord[0][2]/60**2)
	coord[1] = -float(raw_coord[1][0] + raw_coord[1][1]/60 + raw_coord[1][2]/60**2)

	return(coord)

def parse_medatada(raw_metadata, meta_keys):
	clean_meta = []
	
	for meta_key in meta_keys:
		data = raw_metadata.get(meta_keys_dic[meta_key])
		if meta_key == 'GPS':
			data = parse_GPS_info(data)
			
		clean_meta.append(data)

	return(clean_meta)



class data_object:

	def __init__(self, SERVICE, img_items, meta_keys=None, dl_dir=None, in_ram=False):
		self.meta_keys = meta_keys
		self.all_meta_keys = meta_keys_dic
		self.dl_dir = dl_dir
		self.in_ram = in_ram

		self.img_names = [img['name'].upper() for img in img_items]
		self.img_ids = [img['id'] for img in img_items]
		self.image_list, metadata_list = SERVICE.download_files(img_items, dl_dir)

		self.metadata = {}
		for i, raw_metadata in enumerate(metadata_list):
			self.metadata[self.img_names[i]] = parse_medatada(raw_metadata, meta_keys)

	def as_df(self):
		metadata = pd.DataFrame(self.metadata)
		df = pd.DataFrame()
		df['filename'] = self.img_names
		
		if not self.in_ram:
			df['path'] = self.image_list

		for i , meta_key in enumerate(self.meta_keys):
			if meta_key == 'GPS':
				try:
					coord = [[float(k) for k in j] for j in metadata.iloc[i]]
					df['Coord'] = [f'{j[0]:.7f} , {j[1]:.7f}' for j in coord]
					df['Alt'] = [f'{j[2]:.2f}' for j in coord]
				except:
					df['Coord'] = '0.0'
					df['Alt'] = '0.0'
			else:
				df[meta_key] = list(metadata.iloc[i])

		return(df)

	def as_map(self, img_name=None):

		if img_name == None:
			coord_index = self.meta_keys.index('GPS')
			coord_list = [self.metadata[key][coord_index][0:2]+[key] for key in self.metadata.keys()]
			print(coord_list)

			cood_t = list( map(list, zip(*coord_list)) )
			center = [ (max(cood_t[0])+min(cood_t[0]))/2, (max(cood_t[1])+min(cood_t[1]))/2]

			print(center)
			print(coord_list)

			img_map = Map(location=center, zoom_start=10,
	        width='100%', height='100%',
	        tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', attr='Google')

			for x, y, img in coord_list:
				Marker(location=[x,y], popup='', tooltip=img).add_to(img_map)

			return(img_map._repr_html_())

		return('')


##----OTHER FUNCTIONS ----

def map2html(img_map):
	doc = BS(img_map)
	doc = doc.div.div.iframe['data-html']
	return(doc)

def img_path2_dash(path):
    r = html.Img(src=app.get_asset_url(path),
        style={'width':'100%'})
    return(r)
        
def df2_dash(df, id=''):
    r = dash_table.DataTable(
        id=id,
        columns=[{'name': i, 'id': i} for i in df.columns],
        data=df.to_dict('records')
    )
    return(r)

def detect_count(DETECTION):
	good = 0
	bad = 0
	if DETECTION!=None:
		for img_name in DETECTION.keys():
			all_good = all([i['cls']=='insulatorg' for i in DETECTION[img_name]])
			if all_good:
				good += 1
			else:
				bad += 1

	return([good, bad])



    