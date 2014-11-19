import bokeh.plotting as pt
import bokeh.embed as em
from bokeh.resources import CDN
import sqlite3 as lite
import datetime as dt
import time


def LoadFromSQL(interval, db):
    conn = lite.connect(db)
    cur = conn.cursor()
    with conn:
        cur.execute("""
            select *
            from VS1_GT3
            where Time between "{}" and "{}"
            """
                    .format(
                        time.time() - int(interval),
                        time.time()
                        ))

        data = cur.fetchall()
    data.sort()
    data = [list([dt.datetime.fromtimestamp(int(i[0])), i[1]]) for i in data]
    return data


def bk_plot(data):
    tid = time.time()
    #Resolution
    res = 100
    #pt.figure(x_axis_type='datetime')
    plotten = pt.line([i[0] for i in data[::res]], [i[1] for i in data[::res]])
    print(
        '{} seconds to  plot'.format(time.time()-tid)
    )
    script, div = em.components(plotten, CDN)
    return script, div


if __name__ == '__main__':
    pass
