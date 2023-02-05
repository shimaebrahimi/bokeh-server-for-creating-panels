from bokeh.palettes import Category20_16
from bokeh.models.widgets import CheckboxGroup, CheckboxButtonGroup
import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.models.widgets import Slider, RangeSlider, Select
from bokeh.layouts import column, row, WidgetBox
from bokeh.models import Panel
import pandas as pd
from itertools import chain
from bokeh.models import FuncTickFormatter

def route_tab(data):

    def md(origin, dest):
        subset = data[(data['origin'] == origin) & (data['dest'] == dest)]
        airlines = list(set(subset['name']))
        xs = []
        ys = []
        dic = {}
        for i, j in enumerate(airlines):
            airline_flights = subset[subset['name'] == j]
            xs.append(list(airline_flights['arr_delay']))
            ys.append([i for _ in range(len(airline_flights))])
            dic[i] = j
        
        xs = list(chain(*xs))
        ys = list(chain(*ys))

        return ColumnDataSource(data = {'x': xs, 'y': ys}), dic

    def mp(src, o_init, d_init, dic):
        p = figure()
        p.circle('x', 'y', source=src, size=10)
        p.yaxis[0].ticker.desired_num_ticks = len(dic)
        p.yaxis.formatter = FuncTickFormatter(
            code="""
            var labels = %s;
            return labels[tick];
            """ % dic
        )
        return p

    def update(attr, old, new):
        origin = os.value
        dest = ds.value
        new_src, new_dic = md(origin, dest)
        src.data.update(new_src.data)
        p.yaxis[0].ticker.desired_num_ticks = len(new_dic)
        p.yaxis.formatter = FuncTickFormatter(
            code="""
            var labels = %s;
            return labels[tick];
            """ % new_dic
        )

    origins = list(set(data['origin']))
    dests = list(set(data['dest']))
    
    os = Select(title='مبداها', value='EWR', options=origins)
    ds = Select(title='مقصدها', value='IAH', options=dests)
    os.on_change('value', update)
    ds.on_change('value', update)

    o_init = os.value
    d_init = ds.value

    src, dic = md(o_init, d_init)

    p = mp(src, o_init, d_init, dic)

    w = WidgetBox(os, ds)
    l = row(w, p)
    tab = Panel(child=l, title='مبدا/مقصد')
    return tab