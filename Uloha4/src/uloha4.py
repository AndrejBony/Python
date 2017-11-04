#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from bokeh.plotting import figure, output_file, show
from numpy import pi
from bokeh.models import ColumnDataSource, ranges, LabelSet

f = open('election.json', encoding = "utf-8")
json_str = f.read()
data = json.loads(json_str)

color = []
name = []
share = []

for i in range(0, len(data)):
    if "color" not in data[i]:
        color.append("")
    for k, v in data[i].items():
        if k == "name":
            if len(v.strip()) > 40:
                name.append(v.strip()[:40] + "..." )
            else: name.append(v.strip())
        elif k == "share":
            share.append(v)
        elif k == "short":
            name[i] = v.strip()
        elif k == "color":
            color.append(v.strip())

# 1. exercise
source = ColumnDataSource(data=dict(x = name, y = share, color = color) )
    
p1 = figure(title = "Bar plot of share of parties", 
           x_axis_label = "Party", 
           y_axis_label = "Share", 
           x_range = name, 
           y_range = ranges.Range1d(start = 0, end = 31),
           plot_width = 6000)
           
labels = LabelSet(x='x', y='y', text='y', level='glyph', x_offset= -13.5, y_offset=0, source=source, render_mode='canvas')
           
p1.vbar( x = 'x', top = 'y', color = 'color', line_color = 'black', width = 0.8, source = source)
p1.add_layout(labels)

output_file("bar_plot.html")
show(p1)

# 2. exercise
name2 = []
share2 = []
color2 = []
others = 0
for i in range(len(name)):
    if share[i] < 1:
        others += share[i]
    else: 
        name2.append(name[i])
        share2.append(share[i])
        color2.append(color[i])
name2.append("Iní")
share2.append(others)
color2.append("grey")

source = ColumnDataSource(data=dict(x = name2, y = share2, color = color2) )
        
p2 = figure(title = "Bar plot of share of big parties", 
           x_axis_label = "Party", 
           y_axis_label = "Share", 
           x_range = name2, 
           y_range = ranges.Range1d(start = 0, end = 31))
           
p2.vbar( x = 'x', top = 'y', color = 'color', line_color = 'black', width = 0.8, legend = 'x', source = source)
p2.legend.location = "top_left"

output_file("bar_plot_big_parties.html")
show(p2)

# 3. exercise
percents = []
count = 0
for i in range(0, len(share2)):
    percents.append(count/100)
    count += share2[i]
    if i == len(share2) - 1:
        percents.append(1)
start = [p*2*pi for p in percents[:-1]]
end = [p*2*pi for p in percents[1:]]

source = ColumnDataSource(data=dict(start = start, end = end, color = color2, label = name2) )

p3 = figure(title = "Pie chart of share of parties", x_range = [-10, 10])
p3.wedge(x = 0, y = 0, radius = 5,
         start_angle = 'start',
         end_angle = 'end',
         color = 'color',
         legend = 'label',
         source = source )

output_file("pie_chart.html")
show(p3)
