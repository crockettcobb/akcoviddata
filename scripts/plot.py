import pandas as pd
import chartify


def main():
    '''
    This will load data from the Alaska State Department of Health and 
    Human Services  and parse it into a standard format CSV 
    '''
    filter_region = ['Statewide']

    df=pdf.read_csv('./data/parsed.csv')

    regions= ~df['Economic_Region'].isin(filter_region)
    
    ch = chartify.Chart(x_axis_type='datetime', y_axis_type='linear')
    ch.plot.scatter(data_frame=df_cases.loc[regions],  x_column='Date_', y_column='daily_cases', color_column='Economic_Region',)
    ch.show()


if __name__ == '__main__':
    main()
