from cartographer import open_file
import pandas as pd
import seaborn as sns 
from matplotlib import pyplot as plt
'''
this file contains the functions that are used to do initial data analysis on a experiment. 
The objective of this is to take every value of metrics and plot them so that I can see what is going 
on in the experiments. 

'''

# dashboard code using dash 
import dash 
import dash_core_components as dcc
import dash_html_components as html 
import plotly.express as px

app = dash.Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

def make_line_graph(x, y, layout_info):
    '''
    inputs: 
    x, y: arrays of same length that need to be plotted 
    layout_info: dictionary that contains the following
    {'title':,
    'theme': 
    }
    '''
    
    graph_fig = px.line(x=x, y=y, title=layout_info['title'], labels=['check'])
    if layout_info['theme'] == 'dark':
        graph_fig.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
        )
    
    return graph_fig


def generate_dcc_graph(figure, id):
    return dcc.Graph(
        id=id,
        figure=figure 
        )

if __name__ == '__main__':
    '''
    This code is the dashboard for initial data assement. Currently there is a problem that all the plots wont show which is bothering me.
    '''
    #TODO: make this alterable in the dashboard so that you can plot all sorts of experiments 
    base_path = 'C:/source/atpeterepymarl/src/results/sacred/'
    # TODO: make this altreable in dashboard so that you can change the ranges without touching the code.
    experiment_range = range(192,222)
    x_data = {}
    y_data = {}
    app_array = []
    for index, experiment in enumerate(experiment_range):
        #loop through all the experiments that are fed to the IDA 
        path = base_path + str(experiment) + '/metrics.json'
        #open each experiment 
        data = open_file(path)
        try: 
            del data['grad_norm']
        except:
            print('it didnt work', str(experiment))
        
        if index == 0: 
            for key in data.keys():
                y_data[key] = []
                x_data[key] = data[key]['steps']

        for datum ,key in enumerate(data.keys()):
            y_data[key].append(data[key]['values'])

    
    li = {
        'title': 'episode length mean',
        'theme': 'dark'
    }
    # fig = make_line_graph(x_data['ep_length_mean'], y_data['ep_length_mean'], li)
    style_ = {'textAlign':'center', 'backgroundColor': colors['background'], 'color': colors['text']}
    text = 'I can make this programatically now'
    app_array.append(html.H1(children=text, style=style_))
    app_array.append(html.Div(children=text, style=style_))
    for key in data.keys():
        #this is where you generate and append all the figures 
        li['title']=key
        fig = make_line_graph(x_data[key], y_data[key], li)
        app_array.append(generate_dcc_graph(fig,key))
    

    

    app.layout = html.Div(style= style_, children=app_array)
    # children is an array [title, div, graph, graph]
    # TODO: make a function that generates the graphs and appends them to the array that has the title and div in it
    app.run_server(debug=True, dev_tools_hot_reload=True)
    
            
            
        

