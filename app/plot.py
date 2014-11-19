#!/usr/bin/en

READMESTRING = '''
Tänkte försöka mig på att göra en
liten plot klass, där en funktion
är att hämta datan från filerna
som sen skickas in i en plot funktion
som sen används som en embed funktion

Hoppas detta funkar

Har iaf fått färdigt funktionen som hämtar data,
har ej testat, kanske borde göra ett test, hmmmmm

lägger iaf datan i sensordict[givarnamn]{'values': [23.1] , 'dates': [ datum] }

Initiera klassen, Inget händer
Kör main funktion, importera data(med  plot_range), bygg plot, och sen skicka den som embed
Kör main funktion

'''


class PlotClass(object):
    def __init__(self):
        self.SensorDict = {}
        self.sensorDirectory = '/home/pi/Projects/Home-automation/sensors'

    def ImportData(self):
        import datetime as dt
        import os
        import time

        #plot range hours => seconds
        self.plot_range = int(self.plot_range) * 3600

        #Time initizilation
        To = int(time.time())
        From = To - int(self.plot_range)

        #Go to the sensors directory
        os.chdir(self.sensorDirectory)

        #Loop throuch all the sensors
        for i in os.listdir(os.getcwd()):

            #some inits
            self.SensorDict[i] = {'values': [], 'dates': []}
            #Change directory to the current sensor
            os.chdir(i)
            '''
            Make a list of the files in the given time spectra
            (86400) seconds back in time
            '''
            file_list = [
                l for l in os.listdir(os.getcwd())
                if To+self.plot_range > int(l) > From-self.plot_range
            ]
            #Loop through those files
            for j in file_list:
                #Open the files
                with open(j, 'r') as f:
                    #loop through the data
                    for k in f:
                        #Split the time and data values
                        split_list = k.split('|')
                        ''''If the data is within the given time frame,
                        add it to the dict, the first field is time,
                        the second data
                         '''
                        if To > int(split_list[0]) > From:
                            '''
                            self.SensorDict[i]['dates'].append(
                                dt.datetime.fromtimestamp(int(split_list[0]))
                            )
                            '''
                            self.SensorDict[i]['dates'].append(
                                split_list[0]
                            )

                            self.SensorDict[i]['values'].append(
                                split_list[1]
                            )

                #Change the directory for next sensor
            os.chdir('..')

    def bokeh_plot(self):
        import os
        from bokeh.plotting import line
        from bokeh.plotting import hold, figure, show, output_file
        import numpy as np
        import bokeh.embed as embed

        figure()
        hold()

        for i in self.SensorDict:
            line(
                self.SensorDict[i]['dates'], self.SensorDict[i]['values']
            )
            print(len(self.SensorDict[i]['dates']))
            #print(self.SensorDict[i]['dates'][0])
            #print(self.SensorDict[i]['values'][0])
        print('tjo')
        os.chdir('..')
        os.chdir('..')

        output_file('plot.html', title='Plot22')




        show()

    def main(self, plot_range=72):
        self.plot_range = plot_range
        self.ImportData()
        self.bokeh_plot()


if __name__ == '__main__':
    p = PlotClass()
    p.sensorDirectory = "//home//alexander//Projects//Home-automation//Flask//sensors//sensors//"
    p.main(plot_range=2)
