import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from insights.db_queries import sentiment3, sentiment, blob_sentiment, get_mentioned

plotly.tools.set_credentials_file(username='plotEmme', api_key='LHsPkZDem9Y62Opj4bAx')


def pie_chart_sentiment3(collection):
    labels = ['Positive','Neutral','Negative']
    values = sentiment3(collection)
    trace = go.Pie(labels=labels, values=values)
    py.iplot([trace], filename='sentiment3_'+collection+'_pie_chart')


def pie_chart_sentiment_all(chartName,values):
    labels = ['Positive','Neutral','Negative']
    colors = ['green', 'blue', 'red']
    trace = go.Pie(labels=labels, values=values,hoverinfo='label+percent', textinfo='value',
               textfont=dict(size=20,color='black'),marker=dict(colors=colors))
    py.iplot([trace], marker=dict(colors=colors),filename='sentiment_'+chartName+'_pie_chart')

def bar_chart_sentiment(rnn):
    lista=[
        'auto',
        'gesundheit',
        'karriere',
        'kultur',
        'lebenundlernen',
        'netzwelt',
        'panorama',
        'politik',
        'reise',
        'sport',
        'wirtschaft',
        #'wissenschaft'
        ]
    values={}
    if(rnn=='news'):
        for collection in lista:
            values[collection] = sentiment(collection)
    elif(rnn=='zug'):
        for collection in lista:
            values[collection] = sentiment3(collection)
    elif(rnn=='blob'):
        for collection in lista:
            values[collection] = blob_sentiment(collection)
    collezioni=[]
    pos=[]
    neu=[]
    neg=[]
    for collection in values.keys():
        collezioni.append(collection)
        pos.append(values[collection][0])
        neu.append(values[collection][1])
        neg.append(values[collection][2])
    trace_pos= go.Bar(x=collezioni,y=pos,name='Positive',marker = dict(color = 'green'))
    trace_neu = go.Bar(x=collezioni, y=neu, name='Neutral',marker = dict(color = 'blue'))
    trace_neg = go.Bar(x=collezioni, y=neg, name='Negative',marker = dict(color = 'red'))
    data=[trace_pos,trace_neu,trace_neg]
    layout=go.Layout(barmode='stack')
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='sentiment_all_'+rnn+'_bar_chart')
    n_p,n_neu,n_neg=0,0,0
    for n in pos:
        n_p+=n
    for n in neu:
        n_neu+=n
    for n in neg:
        n_neg+=n
    pie_chart_sentiment_all('all_data_'+rnn, [n_p, n_neu, n_neg])


def bar_chart_mentioned(rnn):
    mappa_mentioned={}
    values={}
    if rnn=='auto':
        mappa_mentioned['Audi']=get_mentioned(r'audi',r'Audi',r'AUDI','auto')
        mappa_mentioned['Bmw']=get_mentioned(r'bmw',r'Bmw',r'BMW','auto')
        mappa_mentioned['VW']=get_mentioned(r'Volkswagen',r'Vw',r'VW','auto')
    elif rnn=='politik':
        mappa_mentioned['Merkel']=get_mentioned(r'Merkel', r'merkel', r'MERKEL', 'politik')
        mappa_mentioned['Trump'] = get_mentioned(r'Trump',r'Trump',r'TRUMP','politik')
        mappa_mentioned['Macron'] = get_mentioned(r'Macron',r'macron',r'MACRON','politik')
    for key in mappa_mentioned.keys():
        p=0
        neu=0
        neg=0
        for item in mappa_mentioned[key]:
            if item['sentiment3']=='negative':
                neg+=1
            elif item['sentiment3']=='neutral':
                neu+=1
            else:
                p+=1
        values[key]=[p,neu,neg]
    collezioni = []
    pos = []
    neu = []
    neg = []
    for collection in values.keys():
        collezioni.append(collection)
        pos.append(values[collection][0])
        neu.append(values[collection][1])
        neg.append(values[collection][2])
    trace_pos = go.Bar(x=collezioni, y=pos, name='Positive', marker=dict(color='green'))
    trace_neu = go.Bar(x=collezioni, y=neu, name='Neutral', marker=dict(color='blue'))
    trace_neg = go.Bar(x=collezioni, y=neg, name='Negative', marker=dict(color='red'))
    data = [trace_pos, trace_neu, trace_neg]
    layout = go.Layout(barmode='stack')
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='sentiment_all_' + rnn + '3_bar_chart')



#bar_chart_sentiment('news')

#bar_chart_sentiment('blob')

bar_chart_mentioned('politik')
bar_chart_mentioned('auto')
