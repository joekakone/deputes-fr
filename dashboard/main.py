# coding : utf-8

import pandas as pd
from bokeh.io import curdoc

# Charts module
from plot import draw_piechart, draw_barplot, draw_age_bar, create_table

# Paths & Config
DATA_PATH = "dashboard/data/deputes-active.csv"

##### title ####
curdoc().title = 'Tableau de board | Assemblée Nationale'

# 1. Import data
data = pd.read_csv(DATA_PATH)

# 2. Prepare data
# Remove "ans" in the `experienceDepute` column
data["experienceDepute"] = data["experienceDepute"].apply(lambda x: int(x.split()[0]))
# Add Full name column
data["nomComplet"] = data["prenom"] + " " + data["nom"]

##### KPIS #####
# Nombre de députés
total_deputies = len(data)
# Nombre de groupes
total_groups = len(data["groupe"].unique())
# Age moyen
mean_age = data["age"].mean()
mean_age = round(mean_age, 1)
# Expérience moyenne
mean_experience = data["experienceDepute"].mean()
mean_experience = round(mean_experience, 1)

# make variables available in html templates
curdoc().template_variables['totalDeputies'] = str(total_deputies)
curdoc().template_variables['totalGroups'] = str(total_groups)
curdoc().template_variables['meanAge'] = str(mean_age)
curdoc().template_variables['meanExperienceDepute'] = str(mean_experience)

##### Bokeh Plots ####

### Start Pie Chart ###
piechart = draw_piechart(data, 'piechart')
curdoc().add_root(piechart)
### End Pie Chart ###

### Start Line Plot ###
bar = draw_barplot(data, "age_bar")
curdoc().add_root(bar)
### End Line Plot ###


##### Charts #####
barchart = draw_age_bar(data, 'barchart')
curdoc().add_root(barchart)
### End Bar Chart ###


# ### Map Plot ###
# def gen_geo_data():
#     geodata = {
#         'city': ['Cotonou', 'Porto-Novo', 'Ouidah'],
#         'latitude': [6.366667, 6.497222, 6.366667],
#         'longitude': [2.433333, 2.605, 2.083333]
#     }
#     geodata = pd.DataFrame(geodata)
    
#     return geodata

# geodata = gen_geo_data()

# def MapPlot(data):
#     def wgs84_to_web_mercator(df, lon="longitude", lat="latitude"):
#         """Converts decimal longitude/latitude to Web Mercator format"""
#         k = 6378137
#         df["x"] = df[lon] * (k * np.pi/180.0)
#         df["y"] = np.log(np.tan((90 + df[lat]) * np.pi/360.0)) * k
#         return df
    
#     data = wgs84_to_web_mercator(data)
    
#     x_range = (data['x'].min()-10000, data['x'].max()+10000)
#     y_range = (data['y'].min() ,data['y'].max())
    
#     # convert into ColumnDataSource
#     source = ColumnDataSource(data)
    
#     mapplot = figure(plot_width=540,
#                      plot_height=250,
#                      x_range=x_range,
#                      y_range=y_range,
#                      x_axis_type="mercator",
#                      y_axis_type="mercator",
#                      toolbar_location=None,
#                      tools='',
#                      name='geoplot')

#     # credits
#     MAP_URL = 'http://a.basemaps.cartocdn.com/rastertiles/voyager/{Z}/{X}/{Y}.png'
#     attribution = "Tiles by Carto, under CC BY 3.0. Data by OSM, under ODbL"
#     mapplot.add_tile(WMTSTileSource(url=MAP_URL, attribution=attribution))

#     mapplot.circle(x='x', y='y', fill_color='pink', size=20, fill_alpha=0.3, line_color=None, source=source)

#     # hover
#     mapplot.add_tools(HoverTool(tooltips=[
#         ('City', '@city'),
#         ('Latitude', "@latitude"),
#         ('Longitude', "@longitude")
#         ]))
    
#     # others params
#     mapplot.axis.visible = False
    
#     return mapplot

# mapplot = MapPlot(geodata)

# curdoc().add_root(mapplot)
# ### End Map Plot ###


### Start Table ###
def gen_client_top10():
    clients = {
        'client': [
            'Sam Smith',
            'Sarah Guido',
            'Bruce Lee',
            'Elon Musk',
            'Claire Mathieu',
            'Gérard Berry',
            'Donald Trump',
            'Donnie Yen',
            'La Fouine',
            'Charles De Gaule'
        ],
        'orders': [1200, 3750, 2500, 2080, 2275, 750, 2000, 6200, 4500, 4850]
    }
    clients = pd.DataFrame(clients)

    clients = clients.sort_values(by='orders', ascending=False)
    
    return clients


table = create_table(data, 'table')
curdoc().add_root(table)
### End Table ###
