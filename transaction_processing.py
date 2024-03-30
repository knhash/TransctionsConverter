import pandas as pd
import streamlit as st

from enum import Enum

class Variant(Enum):
    SBI= 'State Bank of India, Saving Account'
    EPF='Employee Provident Fund'

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