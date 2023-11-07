import panel as pn
from panel.template import FastListTemplate
from EVBrandsDashboard import EVBrandsDashboard
from MainDashboard import MainDashboard
from CountyInfoDashboard import CountyInfoDashboard

def main():
    pn.state.clear_caches()
    main_area = pn.Column("")
    pn.extension('echarts','tabulator')
    pn.config.sizing_mode="stretch_width"
    # Instantiate pages and add them to the pages dictionarqy
    
    sidebar = None 
    data_source_info = pn.pane.Markdown("""
                                            ***The data describes EV cars in washington state split by makers and regions***
                                            ***Data is taken from [Kaggle](https://www.kaggle.com/datasets/qnqfbqfqo/electric-vehicle-population-in-washington-state)!***
                                        """)
    right_click_here = pn.pane.Markdown("""
                                            ***Right click the Kaggle link to view the data source
                                        """)
    a_list = ['MainDashboard','MakeAggDashboard','CountyInfo']
    tag_param = pn.Param(name='tag')
    setattr(tag_param, 'value', a_list)
    setattr(tag_param, 'type','list')
    pages = {
            "MainDashboard" : MainDashboard(),
            "MakeAggDashboard": EVBrandsDashboard(metric_name="Make",index_col="Make",values_col="County",values_header="Make",y_title="Most Popular Car Makers"),
            "CountyInfo" : CountyInfoDashboard(), 
        }
    
    radio_button_group = pn.widgets.RadioButtonGroup(name='Index', 
                                       options=['Main','EV Popularity','County Info'], 
                                       #behaviour="radio",
                                       button_type='primary',
                                       orientation='vertical',
                                       )

    def update(event):
        main_area.clear()
        obj = pages.get("MainDashboard")
        if event.type == "changed":
           if event.new == "Main":
              obj = pages.get("MainDashboard")
           elif event.new == "EV Popularity":
                obj = pages.get("MakeAggDashboard")
           elif event.new == "County Info":
                obj = pages.get("CountyInfo")
           main_area.append(obj.view())
        else:
            main_area.append(obj.view())
        #main_area.append(pages[radio_button_group.tag[radio_button_group.values.index(radio_button_group.value)]].view())

    radio_button_group.param.watch(update,'value',onlychanged=True)
    radio_button_group.param.trigger('value')
    sidebar = pn.Column(pn.Row(radio_button_group),pn.Row(data_source_info),pn.Row(right_click_here))
        
    template = FastListTemplate(
        title="Washington EV Cars",
        sidebar=[sidebar],
        main=[main_area],
    )

    pn.state.cache["template"] = template
    pn.state.cache["modal"] = template.modal
    
    # Serve the Panel app
    template.servable()

main()  