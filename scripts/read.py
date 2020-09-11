import pandas as pd


def parse_tests():
    '''Read and parse the tests based on completion date
    '''

    tests_url = 'https://opendata.arcgis.com/datasets/c3c0dc1891454ad5a49b7d9a3438471a_0.csv'                       # corrected for 4 AUG data format change

    df_tests = pd.read_csv(tests_url, parse_dates=['Date_Completed'])
    df_tests.to_csv('../data/raw/tests.csv', index=False)

    tests_map = {
        'Date_Completed' : 'date',
        'ASPHL_Tests' : 'tests_ASPHL',
        'Commercial_Tests' : 'tests_commercial',
        'Hosp_Fac_Tests' : 'tests_POC', 
        'All_Tests' : 'tests_total',
    }

    df_tests = df_tests[list(tests_map.keys())].copy()
    df_tests = df_tests.rename(columns=tests_map)
    df_tests['date'] = pd.to_datetime(df_tests['date']).dt.date
    df_tests.to_csv('../data/parsed/tests.csv', index=False)

    return

def parse_cases():
    ''' Read and parse the cases counts for resident and nonresidents
    '''

    case_url = 'https://opendata.arcgis.com/datasets/c1b6c31d09b44c33962570950456feea_0.csv'
    df_cases = pd.read_csv(case_url, parse_dates=['OnsetDate'])
    df_cases.to_csv('../data/raw/cases.csv', index=False)

    cases_map ={
        'OnsetDate' : 'date',
        'Econ_Name' : 'region',
        'Resident' : 'resident',
    }

    df_cases = df_cases[list(cases_map.keys())].copy()
    df_cases = df_cases.rename(columns=cases_map)
    df_cases['date'] = pd.to_datetime(df_cases['date']).dt.date

    df_res_cases = df_cases[df_cases['resident']=='Y'].copy()
    df_res_cases = df_res_cases.groupby(['date', 'region']).count().copy().reset_index()
    df_res_cases = pd.pivot_table(df_res_cases, columns=['region'], values='resident', index='date').fillna(0)

    regions = df_res_cases.columns.tolist()
    df_res_cases['Statewide'] = df_res_cases[regions].sum(axis=1)
    df_res_cases = pd.melt(df_res_cases.reset_index(), id_vars='date')
    df_res_cases.columns = ['date', 'region', 'resident']

    df_nonres_cases = df_cases[df_cases['resident']=='N'].copy()
    df_nonres_cases = df_nonres_cases.groupby(['date', 'region']).count().copy().reset_index()
    df_nonres_cases = pd.pivot_table(df_nonres_cases, columns=['region'], values='resident', index='date').fillna(0)

    regions = df_nonres_cases.columns.tolist()
    df_nonres_cases['Statewide'] = df_nonres_cases[regions].sum(axis=1)
    df_nonres_cases = pd.melt(df_nonres_cases.reset_index(), id_vars='date')
    df_nonres_cases.columns = ['date', 'region', 'nonresident']
    
    df_cases = df_res_cases.merge(df_nonres_cases, left_on=['date','region'], right_on=['date', 'region'], how='outer').fillna(0)
    df_cases['total'] = df_cases[['resident', 'nonresident']].sum(axis=1)
    df_cases[['total', 'resident', 'nonresident']] = df_cases[['total', 'resident', 'nonresident']] .astype(int)
    df_cases['region'] = df_cases['region'].str.replace('Matanuska-Susitna', 'MatSu')

    df_cases.to_csv('../data/parsed/cases.csv', index=False)

    return

def read_and_parse():
    '''
    This will load data from the Alaska State Department of Health and 
    Human Services  and parse it into a standard format CSV 
    '''

    cases_url = 'https://opendata.arcgis.com/datasets/f2b5073959c247368e4cd28e54cd0cff_0.csv'

    nonres_cases_url = 'https://opendata.arcgis.com/datasets/f34c6b1e58f34939bb6d2d721eb7a1e7_0.csv'
    report_date_url = 'https://opendata.arcgis.com/datasets/6ed020fa516948b2983e36bba817b1b7_0.csv'

    df_cases= pd.read_csv(cases_url, parse_dates=['Date_'])
    df_nonres_cases = pd.read_csv(nonres_cases_url, parse_dates=['ReportDate'])
    df_report_date = pd.read_csv(report_date_url, parse_dates=['ReportDate'])

    df_cases.to_csv('../data/raw/cases.csv', index=False)
    df_nonres_cases.to_csv('../data/raw/nonres_cases.csv', index=False)
    df_report_date.to_csv('../data/raw/reportdate_cases.csv')

    nonres_cases_map = {
        'ReportDate' : 'date',
        'FID' : 'nonresident_cases',
        'Temporary_Region' : 'region',
    }

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

    df = df_cases.merge(df_nonres, left_on=['date', 'region'], right_on=['date', 'region'])
    df['total_cases'] = df[['cases', 'nonresident_cases']].sum(axis=1)
    df.to_csv('../data/parsed/total_cases.csv', index=False)

    return


if __name__ == '__main__':
    # parse_tests()
    parse_cases()