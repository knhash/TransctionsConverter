import pandas as pd
import streamlit as st

from enum import Enum
import pandas as pd
import streamlit as st

class Variant(Enum):
    SBI='State Bank of India, Saving Account'
    EPF='Employee Provident Fund'
    SGB='Sovereign Gold Bond'

def epf_transactions(table):
    df = pd.DataFrame(table[4:-5], columns=['Wage Month', 'Date', 'Type', 'Particulars', 'EPF', 'EPS', 'Employee', 'Employer', 'Pension'])
    df['Employee'] = df['Employee'].str.replace(',', '').astype(float)
    df['Employer'] = df['Employer'].str.replace(',', '').astype(float)
    df['Pension'] = df['Pension'].str.replace(',', '').astype(float)
    df['Net'] = df['Employee'] + df['Employer'] + df['Pension']
    df = df.dropna(subset=['Date'])
    df.rename({'Date':'Txn Date'}, inplace=True)
    return df

def sbi_transactions(table):
    df = pd.DataFrame(table[1:], columns=table[0])
    return df

def sgb_transactions(table):
    df = pd.DataFrame(table[1:], columns=table[0])
    df.rename(columns={'Purchase\nDate':'Txn Date'}, inplace=True)
    df.rename(columns={'Purchase\nGold Rate':'Gold Rate'}, inplace=True)
    df['Txn Date'] = pd.to_datetime(df['Txn Date'], format='%d-%b- %Y').dt.date
    df['Order ID'] = df['Order ID'].apply(lambda x: str(x).split('(')[0].strip())
    df = df[['Txn Date', 'Order ID', 'Unit', 'Amount', 'Gold Rate']]
    return df