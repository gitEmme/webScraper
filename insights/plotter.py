import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from insights.db_queries import sentiment3, sentiment

plotly.tools.set_credentials_file(username='plotEmme', api_key='LHsPkZDem9Y62Opj4bAx')


def pie_chart_sentiment3(collection):
    labels = ['Positive','Neutral','Negative']
    values = sentiment3(collection)
    trace = go.Pie(labels=labels, values=values)
    py.iplot([trace], filename='sentiment3_'+collection+'_pie_chart')


def pie_chart_sentiment(collection):
    labels = ['Positive','Neutral','Negative']
    values = sentiment(collection)
    trace = go.Pie(labels=labels, values=values)
    py.iplot([trace], filename='sentiment_'+collection+'_pie_chart')



pie_chart_sentiment('reise')
pie_chart_sentiment3('reise')


