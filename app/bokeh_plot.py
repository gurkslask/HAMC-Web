from bokeh.plotting import image_rgba, line, annular_wedge, grid, show, output_file, hold
from bokeh.widgets import HBox

import sqlite3 as lite
import datetime as dt
import time


def ColorPicker():
    colors = ['#B2DF8A',
              '#A6CEE3',
              '#33A02C',
              '#FB9A99'
              ]
    for i in colors:
        yield i


class SensorPicker(object):
    def __init__(self, sensorlist):
        self.sensorlist = sensorlist

    def gen(self):
        for i in self.sensorlist:
            self.current_value = i
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
        data_dict[sensor] = [list([dt.datetime.fromtimestamp(int(i[0])), i[1]]) for i in data_dict[sensor]]
    return data_dict


def bk_plot2(data):
    tid = time.time()
    color_picker = ColorPicker()
    #Resolution
    res = 100
    #pt.figure(x_axis_type='datetime')
    hold()
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
    '''for sensor in data:
        colour = color_picker.__next__()
        line([i[0] for i in data[sensor][::res]], [i[1] for i in data[sensor][::res]], legend=sensor, color=colour)
    '''
    #plotten = line([i[0] for i in data[::res]], [i[1] for i in data[::res]])
    print(
        '{} seconds to  plot'.format(time.time()-tid)
    )
    '''script, div = components(pt, CDN)
    return script, div'''
    return lines


def bk_plot_to_screen(data):
    tid = time.time()
    color_picker = ColorPicker()
    #Resolution
    res = 100
    output_file("iris.html")
    #figure(x_axis_type='datetime')
    #hold()
    for sensor in data:
        colour = color_picker.__next__()
        hold()
        line([i[0] for i in data[sensor][::res]], [i[1] for i in data[sensor][::res]], legend=sensor, color=colour)
    print(
        '{} seconds to  plot'.format(time.time()-tid)
    )
    show()

if __name__ == '__main__':
    db_loc = '''/home/alexander/Projects/Home-automation/data.db'''
    data = LoadFromSQL(5184000, db_loc, 'VS1_GT1', 'VS1_GT3')
    bk_plot_to_screen(data)
    #pass
