import pandas as pd


def read_and_parse():
    '''
    This will load data from the Alaska State Department of Health and 
    Human Services  and parse it into a standard format CSV 
    '''

    cases_url = 'https://opendata.arcgis.com/datasets/f2b5073959c247368e4cd28e54cd0cff_0.csv'
    tests_url = 'https://opendata.arcgis.com/datasets/f7fbee9c32304652869dd842248ca4fa_0.csv'

    df_cases= pd.read_csv(cases_url, parse_dates=['Date_'])
    df_tests = pd.read_csv(tests_url, parse_dates=['Date'])

    df_cases.to_csv('../data/raw/cases.csv', index=False)
    df_tests.to_csv('../data/raw/tests.csv', index=False)

    cases_map ={
        'Date_' : 'date',
        'daily_cases' : 'cases',
        'daily_recoveries' : 'recoveries',
        'daily_deaths' : 'deaths',
        'daily_hospitalizations' : 'hospitalizations',
        'Economic_Region' : 'region',
        'active_cases' : 'active_cases',
    }

    df_cases = df_cases[list(cases_map.keys())].copy()
    df_cases = df_cases.rename(columns=cases_map)
    df_cases['date'] = pd.to_datetime(df_cases['date']).dt.date
    df_cases.to_csv('../data/parsed/cases.csv', index=False)
    
    tests_map = {
        'Date' : 'date',
        'daily_ASPHL' : 'tests_ASPHL',
        'daily_Commercial' : 'tests_commercial',
        'daily_POC' : 'tests_POC', 
        'daily_total' : 'tests_total',
    }

    df_tests = df_tests[list(tests_map.keys())].copy()
    df_tests = df_tests.rename(columns=tests_map)
    df_tests['date'] = pd.to_datetime(df_tests['date']).dt.date
    

if __name__ == '__main__':
    read_and_parse()
