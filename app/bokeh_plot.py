from bokeh.plotting import line, hold, figure
from bokeh.widgets import HBox

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
        data_dict[sensor].sort()
        data_dict[sensor] = [list(
            [dt.datetime.fromtimestamp(int(i[0])), i[1]])
            for i in data_dict[sensor]]
    return data_dict


def bk_plot2(data):
    tid = time.time()
    color_picker = ColorPicker()
    #Resolution
    res = 100
    figure()
    hold(True)
    lines = HBox(
        children=
        [
            line(
                [i[0] for i in data[sensor][::res]],
                [i[1] for i in data[sensor][::res]],
                legend=sensor,
                color=color_picker.__next__(),
                x_axis_type='datetime'
                )
            for sensor in data]
        )
    hold(False)
    print(
        '{} seconds to  plot'.format(time.time()-tid)
    )
    return lines


def bk_plot(data):
    tid = time.time()
    color_picker = ColorPicker()
    #Resolution
    res = 100
    #figure()
    hold(True)
    lines = HBox(
        children=
        [
            line(
                [random.randint(1,100) for i in range(1, 100)],
                [random.randint(1,100) for i in range(101, 200)],
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


