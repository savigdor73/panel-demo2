from Dashboard import Dashboard
import pandas as pd
import panel as pn
import numpy as np

class EVBrandsDashboard(Dashboard):
    def __init__(self,metric_name,index_col, values_col,values_header,y_title):
        pivot_table=pd.pivot_table(self.df, index=index_col, values=values_col, aggfunc=np.count_nonzero)
        obj = self.echarts_bar_chart(np.array(pivot_table.index.values),
                                               np.array(pivot_table[values_col].values), 
                                               y_title)
        col = pn.Column(obj)
        self.content = col

    def echarts_bar_chart(self,x,y,y_title):
        echart_bar = {
            'title': {
                'text': y_title
            },
            'tooltip': {},
            'legend': {
                'data':['Index']
            },
            'xAxis': {
                'data': x.tolist()
            },
            'yAxis': {},
            'series': [{
                'name': 'Make',
                'type': 'bar',
                'data': y.tolist()
            }],
        }
        echart_pane = pn.pane.ECharts(echart_bar, height=480, width=640)
        return echart_pane
    
    def view(self):
        return self.content