from flask import Flask, make_response, render_template
import pickle
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from bokeh_plot import LoadFromSQL, bk_plot
from bokeh.resources import Resources
from bokeh.templates import RESOURCES

app = Flask(__name__)
app.config['SECRET_KEY'] = '73ng89rgdsn32qywxaz'
app.config['DATABASE_LOCATION'] = '''
/home/alexander/Projects/Home-automation/data.db'''
bootstrap = Bootstrap(app)


@app.route('/bild')
@app.route('/bild/<range>')
def bild(range=48):
    plot(range)
    return render_template('hello.html')


@app.route('/bokeh_bild')
@app.route('/bokeh_bild/<range>')
def bokeh_bild(range=48):
    data = bk_plot(LoadFromSQL(range, app.config['DATABASE_LOCATION']))
    resources = Resources("inline")
    plot_resources = RESOURCES.render(
        js_raw=resources.js_raw,
        css_raw=resources.css_raw,
        js_files=resources.js_files,
        css_files=resources.css_files,
    )
    #return render_template('bild.html')
    return render_template(
        'bild.html',
        script=data[0],
        div=data[1],
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
    with open('shared_dict', 'rb') as f:
        return pickle.load(f)


@app.route("/simple.png")
def simple():
    import datetime as dt
    import StringIO
    import os
    import time

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    #Some configuration for the matplot
    fig = Figure(figsize=(12, 10))
    ax = fig.add_subplot(111)

    #Time initizilation
    To = int(time.time())
    From = To - 86400

    #Go to the sensors directory
    os.chdir('/home/pi/Projects/Home-automation/sensors')

    #Loop throuch all the sensors
    for i in os.listdir(os.getcwd()):
        #some inits
        dates = []
        values = []
        data_dict = {}
        #Change directory to the current sensor
        os.chdir(i)
        #Make a list of the files in the given time seconds back in time
        file_list = [l for l in os.listdir(os.getcwd()) if To+86400 > int(l) > From-86400]
        #Loop through those files
        for j in file_list:
            #Open the files
            with open(j, 'r') as f:
                #loop through the data
                for k in f:
                    #Split the time and data values
                    split_list = k.split('|')
                    #If the data is within the given time frame,
                    #add it to the dict, the first field is timethe second data
                    if To > int(split_list[0]) > From:
                        data_dict[split_list[0]] = split_list[1]

        #Loop through the created dict
        for key in sorted(data_dict.keys()):
            #Append the lists, List concetation???????????????
            dates.append(dt.datetime.fromtimestamp(int(key)))
            values.append(data_dict[key])
        #Some more configuration of the plot
        ax.plot_date(dates, values, '-', label='aaa')
        #Change the directory for next sensor
        os.chdir('..')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    #fig.legend(loc='upper left')
    canvas = FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


def plot(plot_range=72):
    import datetime as dt
    import os
    import time

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    tid = time.time()
    #plot range hours => seconds
    plot_range = int(plot_range) * 3600

    #Some configuration for the matplot
    fig = Figure(figsize=(12, 10))
    ax = fig.add_subplot(111)

    #Time initizilation
    To = int(time.time())
    From = To - int(plot_range)

    #Go to the sensors directory
    os.chdir('/home/pi/Projects/Home-automation/sensors')

    #Loop throuch all the sensors
    for i in os.listdir(os.getcwd()):

        #some inits
        dates = []
        values = []
        data_dict = {}
        #Change directory to the current sensor
        os.chdir(i)
        #Make a list of the files in the given time spectra (86400) seconds back in time
        file_list = [l for l in os.listdir(os.getcwd()) if To+plot_range > int(l) > From-plot_range]
        #Loop through those files
        for j in file_list:
            #Open the files
            with open(j, 'r') as f:
                #loop through the data
                for k in f:
                    #Split the time and data values
                    split_list = k.split('|')
                    #If the data is within the given time frame, add it to the dict, the first field is time, the second data
                    if To > int(split_list[0]) > From:
                        data_dict[split_list[0]] = split_list[1]

        #Loop through the created dict
        for key in sorted(data_dict.keys()):
            #Append the lists, List concetation???????????????
            dates.append(dt.datetime.fromtimestamp(int(key)))
            values.append(data_dict[key])
        #Some more configuration of the plot
        ax.plot_date(dates, values, '-', label='aaa')
        #Change the directory for next sensor
        os.chdir('..')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    #fig.legend(loc='upper left')
    canvas = FigureCanvas(fig)
    #png_output = StringIO.StringIO()
    print('It took ' + str(time.time() - tid) + 'sec to render page')
    canvas.print_png('/home/pi/Projects/Home-automation/Flask/static/bild.png')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    #app.run(host='0.0.0.0')
