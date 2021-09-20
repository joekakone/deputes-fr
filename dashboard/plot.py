# coding : utf-8

import pandas as pd
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.palettes import Category20c
from bokeh.models import ColumnDataSource, DataTable, TableColumn, HoverTool, LabelSet


## PIE CHART ##
def draw_piechart(data, name):
    # transform
    data_frame = data["civ"].value_counts(sort=True)
    data_frame = data_frame.reset_index()
    data_frame.columns = ["CIV", "part"]
    data_frame = data_frame.sort_values(by="part")
    data_frame['percent'] = data_frame['part']/data_frame['part'].sum() * 100
    data_frame['percent']  = data_frame['percent'].apply(lambda x: str(round(x, 2))+'%')
    data_frame['angle'] = data_frame['part']/data_frame['part'].sum() * 2*3.14
    data_frame['color'] = ['pink', 'gray']
    
    # hover
    tooltips = f'@{"CIV"}: @{"part"}'
    
    pie = figure(x_range=(-1, 1),
                 plot_width=250,
                 height=250,
                 toolbar_location=None,
                 tools="",
                 tooltips=tooltips,
                 name=name)
    
    # convert into ColumnDataSource
    source = ColumnDataSource(data_frame)

    pie.annular_wedge(x=0,
                      y=1,
                      inner_radius=0.5,
                      outer_radius=0.8,
                      start_angle=cumsum('angle',include_zero=True),
                      end_angle=cumsum('angle'),
                      color='color',
                      alpha=0.7,
                      source=source)
    # Proportion de femmes
    women_proportion = len(data[data["civ"]=="Mme"]) / len(data)
    women_proportion = round(women_proportion*100, 2)
    label = LabelSet(x=-.3,
                     y=1,
                     x_offset=0,
                     y_offset=0,
                     text=[str(women_proportion)+"%"],
                     text_baseline="middle",
                     text_font_size="24px")
    pie.add_layout(label)

    # others params
    pie.axis.axis_label = None
    pie.axis.visible = False
    pie.grid.grid_line_color = None

    return pie


### Start Line Plot ###
def draw_barplot(data, name):
    data_frame = data["groupeAbrev"].value_counts()
    data_frame = data_frame.reset_index()
    data_frame.columns = ["groupeAbrev", "size"]
    
    plot = bar = figure(x_range=data_frame["groupeAbrev"],
                        plot_width=540,
                        height=250,
                        toolbar_location=None,
                        tools="",
                        name=name)
    
    # convert into ColumnDataSource
    source = ColumnDataSource(data_frame)
    
    plot.vbar(x="groupeAbrev", top="size", width=.5, color='gray', alpha=0.7, source=source)
    
    label = LabelSet(x="groupeAbrev",
                     y="size",
                     x_offset=-6,
                     y_offset=5,
                     text="size",
                     text_baseline="middle",
                     text_font_size="12px",
                     source=source)
    plot.add_layout(label)
    
    # others params
    plot.yaxis.visible = False
    plot.y_range.start = 0
    plot.ygrid.grid_line_color = None
    plot.xaxis.axis_line_color = None
    plot.xgrid.grid_line_color = None
    
    return plot

## Age bar ##
def draw_age_bar(data, name):
    def format_age(intervalle):
        a, b = intervalle[1:-1].replace(",","").split()
        a, b = int(float(a)), int(float(b))
        return f"{a}-{b}"
    bar_data = data["age"].value_counts(bins=5, sort=False)
    bar_data = bar_data.reset_index()
    bar_data.columns = ["age", "size"]
    bar_data["age"] = bar_data["age"].astype("str")
    bar_data["age"] = bar_data["age"].apply(format_age)
    
    tooltips = f'@{"age"}: @{"size"}'
    
    bar = figure(y_range=bar_data["age"],
                     plot_width=250,
                     height=250,
                     toolbar_location=None,
                     tools="",
                     tooltips=tooltips,
                     name=name)

    # convert into ColumnDataSource
    source = ColumnDataSource(bar_data)

    bar.hbar(y="age", right="size", height=0.5, color='gray', alpha=0.7, source=source)

    # others params
    bar.x_range.start = 0
    bar.xaxis.visible = False
    bar.yaxis.axis_line_color = None
    bar.grid.grid_line_color = None
    
    return bar


## TABLE ##
def create_table(data, name):
    # Table
    source = ColumnDataSource(data)
    columns = [
        TableColumn(field="nomComplet", title="Nom complet"),
        TableColumn(field="groupe", title="Groupe parlementaire"),
        TableColumn(field="departementNom", title="Département"),
        TableColumn(field="age", title="Age"),
        TableColumn(field="nombreMandats", title="Nombre de mandats"),
    ]
    table = DataTable(source=source, columns=columns, height=240, width=1100, name=name)
    
    return table
