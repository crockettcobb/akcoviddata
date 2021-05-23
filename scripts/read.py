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
        # 'ReportDate' : 'date',
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


def read_reportdate():
    ''' Read and parse the cases counts for resident and nonresidents
    '''

    case_url = 'https://opendata.arcgis.com/datasets/44002fca49af4d5e918174b6acdd92ea_0.csv'
    df_cases = pd.read_csv(case_url, parse_dates=['ReportDate'])
    df_cases.to_csv('../data/raw/cases.csv', index=False)

    cases_map ={
        'ReportDate' : 'date',
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

    df_cases.to_csv('../data/parsed/report_date.csv', index=False)

    return


def read_vaccination():
    """ read in vaccionation data
    """

    vacc_url = 'https://opendata.arcgis.com/datasets/722c84e36ad040c6a75fdec6b768b13f_0.csv'
    df = pd.read_csv(vacc_url, parse_dates=['ADMIN_DATE'])
    df.to_csv('../data/raw/vaccines.csv', index=False)

if __name__ == '__main__':
    # parse_tests()
    parse_cases()
    read_reportdate()