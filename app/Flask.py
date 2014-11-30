from flask import Flask, render_template
import pickle
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from bokeh_plot import LoadFromSQL, bk_plot
from bokeh.resources import Resources
from bokeh.templates import RESOURCES
from bokeh.embed import components


app = Flask(__name__)
app.config['SECRET_KEY'] = '73ng89rgdsn32qywxaz'
app.config['DATABASE_LOCATION'] = '''/home/pi/Projects/HAMC/data.db'''
PICKLE_LOCATION = '''/home/pi/Projects/HAMC/shared_dict'''
bootstrap = Bootstrap(app)


@app.route('/bokeh_bild')
@app.route('/bokeh_bild/<range>')
def bokeh_bild(range=48):
    print(app.config['DATABASE_LOCATION'])
    data = None
    data = bk_plot(LoadFromSQL(range, app.config['DATABASE_LOCATION'], 'VS1_GT1', 'VS1_GT2'))
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
        ute_temp_form=ute_temp_form)


def load_shared_dict():
    '''loads the shared dict'''
    with open(PICKLE_LOCATION, 'rb') as f:
        return pickle.load(f)


if __name__ == "__main__":
    #app.run(host='0.0.0.0', debug=True)
    app.run(host='0.0.0.0')
