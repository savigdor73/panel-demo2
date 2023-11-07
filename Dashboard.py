import pandas as pd
import panel as pn

# Dashboard Page    
class Dashboard:
    #static variable: df
    if 'df' in pn.state.cache:
        df = pn.state.cache['df']
    else:
        df=pd.read_csv("Electric_Vehicle_Population_Data.csv")
    def __init__(self,tag):
        self.tag = tag