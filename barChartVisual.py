#!/usr/bin/env python
import pandas as pd
import pygal
from decimal import *
#from pygal.style import DarkGreenBlueStyle
from pygal.style import DefaultStyle

graph = pd.read_csv("/home/ubuntu/flaskapp/bardata.csv")
#graph = graph.sort_values(by='count	',ascending=False)

bar_chart = pygal.Bar(style=DefaultStyle, x_title='Magnitude', y_title='Total Count', width=1280, height=720, show_legend=False, human_readable=True, title='Magnitude Count Chart')
#pie_chart = pygal.Pie(style=DarkGreenBlueStyle, width=1280, height=720, legend_at_bottom=True, human_readable=False, title='earthquake_pie')
#scatter_chart = pygal.XY(stroke=False,style=DarkGreenBlueStyle, width=1280, height=720, legend_at_bottom=False, human_readable=True, title='earthquake_scatter')

for index, row in graph.iterrows():
	bar_chart.add(row["mag"],Decimal(row["count"]))
	#pie_chart.add(str(row["mag"]), row["count	"])
	#scatter_chart.add("", [(row["mag"],row["count	"])])
	
#bar_chart.render_to_file('images/earthquakes_bar.svg')
#pie_chart.render_to_file('images/earthquakes_pie.svg')
bar_chart.render_to_file('/home/ubuntu/flaskapp/chart.svg')
