from bokeh.plotting import figure
from bokeh.models import HoverTool

import sqlite3 as lite
import datetime as dt
import time
import random


def ColorPicker():
    colors = [
        '#1f77b4',
        '#ff7f0e',
        #'#2ca02c',
        '#d62728',
        '#9467bd',
        '#8c564b',
        '#e377c2',
        '#7f7f7f',
        '#bcbd22',
        '#17becf',
        '#B2DF8A',
        '#A6CEE3',
        '#33A02C',
        '#FB9A99'
        ]
    for i in colors:
        yield i


def LoadFromSQL(interval, db, *sensors):
    SQL_time = time.time()
    conn = lite.connect(db)
    cur = conn.cursor()
    data_dict = {}
    with conn:
        for sensor in sensors:
            cur.execute("""
                select *
                from {0}
                where Time between "{1}" and "{2}"
                """
                        .format(
                            sensor,
                            time.time() - int(interval),
                            time.time()
                            ))

            data_dict[sensor] = cur.fetchall()
    for sensor in data_dict:
        # data_dict[sensor].sort()
        data_dict[sensor] = [list(
            [dt.datetime.fromtimestamp(int(i[0])), i[1]])
            for i in data_dict[sensor]]
    print('Time to fetch SQL data: {}'.format(time.time() - SQL_time))
    return data_dict


def bk_plot_timeline(data):
    # This is a plot that takes time on the x-axis
    tid = time.time()
    color_picker = ColorPicker()
    # Resolution
    res = 10
    p1 = figure(tools='resize, reset, box_zoom, crosshair')
    p1.title = 'Temperatures!'
    for sensor in data:
        x = []
        y = []
        for values in data[sensor][::res]:
            x.append(values[0])
            y.append(values[1])
        hover = HoverTool(
            tooltips=[
                ('(x,y)', '($x, $y)')
            ]
        )
        p1.line(
            x,
            y,
            tools=[hover],
            color=color_picker.__next__(),
            x_axis_type='datetime'
        )
    bk_object = make_figure()
    print(
        '{} seconds to  plot'.format(time.time()-tid)
    )
    return bk_object


def bk_plot(data):
    #This is a regular plot
    tid = time.time()
    color_picker = ColorPicker()
    figure()
    hold(True)
    x = [i for i in data]
    y = [data[i] for i in data]
    lines = line(
                x,
                y,
                color=color_picker.__next__(),
                )
    hold(False)
    print(
        '{} seconds to  plot'.format(time.time()-tid)
    )
    return lines


def test_bk_plot(data):
    #This is a plot that only plots random numbers, for testing
    tid = time.time()
    color_picker = ColorPicker()
    #Resolution
    #figure()
    hold(True)
    lines = HBox(
        children=
        [
            line(
                [random.randint(1, 100) for i in range(1, 100)],
                [random.randint(1, 100) for i in range(101, 200)],
                color=color_picker.__next__()
                )
            for i in range(3)]
        )
    print(
        '{} seconds to  plot'.format(time.time()-tid)
    )
    return lines


if __name__ == '__main__':
    db_loc = '''/home/alexander/Projects/Home-automation/data.db'''
    data = LoadFromSQL(
        4000000,
        db_loc,
        'VS1_GT1',
        'VS1_GT3'
        ,'VS1_GT2'
        )


