from flask import Flask, render_template, jsonify
import pickle
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from bokeh_plot import LoadFromSQL, bk_plot_timeline
from bokeh.embed import components
import os

configs = {
    'pi_config': {
        'DATABASE_LOCATION': '''/home/pi/Projects/HAMC/data.db''',
        'PICKLE_LOCATION': '''/home/pi/Projects/HAMC/shared_dict''',
        'DEBUG': False,
        'SECRET_KEY': '73ng89rgdsn32qywxaz',
        'CONNECT_TO_SOCKET_METHOD': 'external'
    },
    'pi_test': {
        'DATABASE_LOCATION': '''/home/pi/Projects/HAMC/data.db''',
        'PICKLE_LOCATION': '''/home/pi/Projects/HAMC/shared_dict''',
        'DEBUG': True,
        'SECRET_KEY': '73ng89rgdsn32qywxaz',
        'CONNECT_TO_SOCKET_METHOD': 'external'
    },
    'testing_config': {
        'DATABASE_LOCATION': '''/home/alexander/prg/SQL/data.db''',
        'PICKLE_LOCATION': '''/home/alexander/prg/SQL/shared_dict''',
        'DEBUG': True,
        'SECRET_KEY': '73ng89rgdsn32qywxaz',
        'CONNECT_TO_SOCKET_METHOD': 'external'
    }
}

app = Flask(__name__)
app.config.update(configs[os.environ['FLASK_CONFIG']] or configs['pi_config'])
PICKLE_LOCATION = '''/home/pi/Projects/HAMC/shared_dict'''
bootstrap = Bootstrap(app)

if app.config['CONNECT_TO_SOCKET_METHOD'] == 'external':
    from connect_to_socket import call_server
elif app.config['CONNECT_TO_SOCKET_METHOD'] == 'internal':
    from connect_to_socket_internal import call_server


@app.route('/bokeh_bild')
@app.route('/bokeh_bild/<range>')
def bokeh_bild(range=4800):
    data = bk_plot_timeline(
        LoadFromSQL(
            range,
            app.config['DATABASE_LOCATION'],
            'VS1_GT1',
            'VS1_GT3',
            'VS1_GT2',
            'VS1_Setpoint'
            )
        )
    print(data)
    plot_script, plot_div = components(data)
    # return render_template('bild.html')
    return render_template(
        'bild.html',
        script=plot_script,
        div=plot_div)


@app.route('/', methods=['GET', 'POST'])
def main2():
    return render_template(
        'main.html',
        dVS1_CP1='VS1_CP1',
        dVS1_GT1='VS1_GT1'
    )

@app.route('/dia', methods=['GET', 'POST'])
def main3():
    return render_template(
        'ui.html'
    )

@app.route('/VS1_GT1', methods=['GET', 'POST'])
def VS1_GT1():
    return render_template(
        'GT.html',
        dObject='VS1_GT1_Class'
    )


@app.route('/_JsonSharedDict_new')
@app.route('/_JsonSharedDict_new/<dObject>')
def JsonSharedDict_new(dObject=None):
    '''Jsonifies the shared dict'''
    if dObject is None:
        return render_template('404.html'), 404
    else:
        return jsonify(result=call_server({'r': [str(dObject)]}))


@app.route('/_JsonSharedDict_new_write')
@app.route('/_JsonSharedDict_new_write/<dObject>')
def JsonSharedDict_new_write(dObject=None, value=None):
    '''Jsonifies the shared dict'''
    if dObject is None or value is None:
        return render_template('404.html'), 404
    else:
        return jsonify(result=call_server({'w': [str(dObject), str(value)]}))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=app.config['DEBUG'])
    # app.run(host='0.0.0.0')
