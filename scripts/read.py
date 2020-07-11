import pandas as pd


def read_and_parse():
    '''
    This will load data from the Alaska State Department of Health and 
    Human Services  and parse it into a standard format CSV 
    '''

    cases_url = 'https://opendata.arcgis.com/datasets/f2b5073959c247368e4cd28e54cd0cff_0.csv'
    tests_url = 'https://opendata.arcgis.com/datasets/f7fbee9c32304652869dd842248ca4fa_0.csv'
    nonres_cases_url = 'https://opendata.arcgis.com/datasets/f34c6b1e58f34939bb6d2d721eb7a1e7_0.csv'
    report_date_url = 'https://opendata.arcgis.com/datasets/6ed020fa516948b2983e36bba817b1b7_0.csv'

    df_cases= pd.read_csv(cases_url, parse_dates=['Date_'])
    df_tests = pd.read_csv(tests_url, parse_dates=['Date'])
    df_nonres_cases = pd.read_csv(nonres_cases_url, parse_dates=['ReportDate'])
    df_report_date = pd.read_csv(report_date_url, parse_dates=['ReportDate'])

    df_cases.to_csv('../data/raw/cases.csv', index=False)
    df_tests.to_csv('../data/raw/tests.csv', index=False)
    df_nonres_cases.to_csv('../data/raw/nonres_cases.csv', index=False)
    df_report_date.to_csv('../data/raw/reportdate_cases.csv')

    nonres_cases_map = {
        'ReportDate' : 'date',
        'FID' : 'nonresident_cases',
        'Temporary_Region' : 'region',
    }

    df_nonres_cases = df_nonres_cases.groupby(['ReportDate', 'Temporary_Region']).count().copy().reset_index()
    df_nonres_cases = df_nonres_cases.rename(columns=nonres_cases_map)
    df_nonres_cases['region'] = df_nonres_cases['region'].str.replace('Matanuska-Susitna', 'MatSu')
    df_nonres_cases['date'] = pd.to_datetime(df_nonres_cases['date']).dt.date
    df_nonres_cases[['date', 'region', 'nonresident_cases']].to_csv('../data/parsed/nonres_cases.csv', index=False)

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
    df_tests.to_csv('../data/parsed/tests.csv', index=False)


    report_date_cases_map = {
    'ReportDate' : 'date',
    'FID' : 'cases',
    'Region' : 'region',
    }

    df_report_date = df_report_date.groupby(['ReportDate', 'Region']).count().copy().reset_index()
    df_report_date = df_report_date.rename(columns=report_date_cases_map)
    df_report_date['region'] = df_report_date['region'].str.replace('Matanuska-Susitna', 'MatSu')
    df_report_date['date'] = pd.to_datetime(df_report_date['date']).dt.date
    df_report_date[['date', 'region', 'cases']].to_csv('../data/parsed/report_date_cases.csv', index=False)

if __name__ == '__main__':
    read_and_parse()
