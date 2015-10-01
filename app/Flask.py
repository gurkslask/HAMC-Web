from flask import Flask, render_template, jsonify, request
import pickle
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from bokeh_plot import LoadFromSQL, bk_plot_timeline, bk_plot
from bokeh.resources import Resources
from bokeh.templates import RESOURCES
from bokeh.embed import components
import random
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
    data = bk_plot_timeline(LoadFromSQL(range, app.config['DATABASE_LOCATION'], 'VS1_GT1', 'VS1_GT3', 'VS1_GT2', 'VS1_Setpoint'))
    print(data)
    resources = Resources("inline")
    plot_resources = RESOURCES.render(
        js_raw=resources.js_raw,
        css_raw=resources.css_raw,
        js_files=resources.js_files,
        css_files=resources.css_files,
    )
    plot_script, plot_div = components(
        data, resources)
    #return render_template('bild.html')
    return render_template(
        'bild.html',
        script=plot_script,
        div=plot_div,
        resources=plot_resources)


@app.route('/')
def hello():
    return 'hello world'


class NameForm(Form):
    """docstring for NameForm"""
    ute_temp = StringField('Utetemperatur', validators=[Required()])
    fram_temp = StringField('Framledningstemperatur', validators=[Required()])
    submit = SubmitField('Submit')


@app.route('/interact', methods=['GET', 'POST'])
def interact():
    ute_temp = None
    fram_temp = None
    ute_temp_form = NameForm()
    shared_dict = load_shared_dict()

    data = bk_plot_timeline(shared_dict['komp'])
    resources = Resources("inline")
    plot_resources = RESOURCES.render(
        js_raw=resources.js_raw,
        css_raw=resources.css_raw,
        js_files=resources.js_files,
        css_files=resources.css_files,
    )
    plot_script, plot_div = components(
        data, resources)

    if ute_temp_form.validate_on_submit():
        ute_temp = ute_temp_form.ute_temp.data
        ute_temp_form.ute_temp.data = ''
        fram_temp = ute_temp_form.fram_temp.data
        ute_temp_form.fram_temp.data = ''
        shared_dict['komp'][int(ute_temp)] = int(fram_temp)

    return render_template(
        'interact.html',
        shared_dict=shared_dict,
        ute_temp=ute_temp,
        fram_temp=fram_temp,
        ute_temp_form=ute_temp_form,
        script=plot_script,
        div=plot_div,
        resources=plot_resources
        )


class OpenCloseValves(Form):
    """Form for OpenCloseValves"""
    TimeOpen = StringField('Time for the valve to open')
    TimeClose = StringField('Time for the valve to close')
    submit = SubmitField('Submit')


@app.route('/VS1_SV1', methods=['GET', 'POST'])
def SV1():
    OpenCloseValvesForm = OpenCloseValves()
    shared_dict = load_shared_dict()
    if OpenCloseValvesForm.validate_on_submit():
        save_value('.'.join(
            'IOVariables', 'VS1_SV1', 'Time_Open'),
            OpenCloseValvesForm.TimeOpen.data
        )
        save_value('.'.join(
            'IOVariables', 'VS1_SV1', 'Time_Close'),
            OpenCloseValvesForm.TimeClose.data
        )
    return render_template(
        'valve.html',
        TimeOpen=shared_dict['VS1_SV1']['Time_Open'],
        TimeClose=shared_dict['VS1_SV1']['Time_Close'],
        OpenCloseValvesForm=OpenCloseValvesForm,
        dObject='IOVariables',
        dValve='VS1_SV1',
        dSensor='VS1_GT1',
        dSP='VS1_Setpoint'
        )


@app.route('/VS1_CP1', methods=['GET', 'POST'])
def VS1_CP1():
    return render_template(
        'CP.html',
        dObject='IOVariables',
        dCP='VS1_CP1'
        )

class PumpForm(Form):
    """docstring for NameForm"""
    LarmDelay = StringField('LarmDelay', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/VS1_CP1_new', methods=['GET', 'POST'])
def VS1_CP1_new():
    VS1_CP1_LarmDelay_Form = PumpForm()
    if VS1_CP1_LarmDelay_Form.validate_on_submit():
        print('Heyo! {}'.format(VS1_CP1_LarmDelay_Form.LarmDelay.data))
    return render_template(
        'CP_new.html',
        dObject='VS1_CP1',
        dCP='VS1_CP1',
        LarmDelayForm=VS1_CP1_LarmDelay_Form
        )


@app.route('/VS1_GT1', methods=['GET', 'POST'])
def VS1_GT1():
    return render_template(
        'GT.html',
        dObject='VS1_GT1_Class'
    )

@app.route('/_JsonSharedDict')
@app.route('/_JsonSharedDict/<dObject>')
def JsonSharedDict(dObject=None):
    '''Jsonifies the shared dict'''
    if dObject is None:
        return jsonify(result=load_shared_dict())
    else:
        return jsonify(result=load_shared_dict(dObject))

@app.route('/_JsonSharedDict_new')
@app.route('/_JsonSharedDict_new/<dObject>')
def JsonSharedDict_new(dObject=None):
    '''Jsonifies the shared dict'''
    if dObject is None:
        return render_template('404.html'), 404
    else:
        return jsonify(result=call_server({'r':[str(dObject)]}))


@app.route('/test_internal')
def test_internal():
    call_server({'w':[['test1', 44]]})
    return 'test internal{}'.format(call_server({'r':['test1', 'test2']}))


def load_shared_dict(dObject=None):
    '''loads the shared dict'''
    with open(app.config['PICKLE_LOCATION'], 'rb') as f:
        #Open the shared dict and load it temporary
        shared_dict = pickle.load(f)
    if shared_dict['update_from_main']:
        #Falsify the flag
        shared_dict['update_from_main'] = False
        with open(app.config['PICKLE_LOCATION'], 'wb') as f:
            #And write it down again
            pickle.dump(shared_dict, f, protocol=2)
    #Return the dict as requested
    if dObject is None:
        return shared_dict
    else:
        try:
            return shared_dict[dObject]
        except Exception as e:
            print('{} does not exist in the shared dictionary'.format(e))


def load_values_from_controller(read_list = '', write_list = ''):
    read_message = "'r': read_list" if read_list != None else ''
    write_message = "'w': write_list" if write_list != None else ''
    call_server(''.join([read_message, write_message]))


def save_value(key, value):
    shared_dict[key] = value
    shared_dict['update_from_flask'] = True
    save_shared_dict()


def save_shared_dict():
    with open(app.config['PICKLE_LOCATION'], 'wb') as f:
        pickle.dump(shared_dict, f, protocol=2)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=app.config['DEBUG'])
    #app.run(host='0.0.0.0')
