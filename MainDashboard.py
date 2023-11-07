from Dashboard import Dashboard
import panel as pn

class MainDashboard(Dashboard):
    def topmost_and_least_popular_makers(self):
        # Group the DataFrame by the car manufacturer column and count the occurrences
        count_df = self.df['Make'].value_counts()

        # Get the most popular car manufacturer
        most_popular_car_manufacturer = count_df.index[0]

        least_popular_car_manufacturer = count_df.index[count_df.size-1]

        return { "mpcm" : most_popular_car_manufacturer,
                 "lpcm" : least_popular_car_manufacturer }

    def __init__(self):
        fs = "48px"
        fst = "20px"
        
        df_tabulator = pn.widgets.Tabulator(self.df, name='wacca', page_size=10)
        
        total_car_types = self.df['Make'].nunique()
        avg_range = self.df['Electric Range'].mean()
        topmost_and_least_popular_maker = self.topmost_and_least_popular_makers()

        row = pn.Row(
            pn.indicators.Number(name='Total Car Types', value=total_car_types, format='{value}', font_size=fs, title_size=fst),
            pn.indicators.Number(name='Avg. Range', value=avg_range, format='{value:.2f}', font_size=fs, title_size=fst),
            pn.indicators.String(name="Most Popular Maker",value=topmost_and_least_popular_maker["mpcm"],font_size=fs,title_size=fst),
            pn.indicators.String(name='Least Popular Maker', value=topmost_and_least_popular_maker["lpcm"], font_size=fs, title_size=fst)
        )
        
        col = pn.Column(row, pn.Row(df_tabulator))
        self.content = col

    def view(self):
        return self.content