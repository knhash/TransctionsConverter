import pandas as pd
import streamlit as st

from enum import Enum
import pandas as pd
import streamlit as st

class SBI:
    title = "SBI, Savings Account"
    table = pd.DataFrame()

    def __init__(self):
        self.help = """
        **How to generate report**
        1. Login to your SBI account.
        2. Go to the **Account Statement** section.
        3. Select the **Account Number** and **Date Range**.
        4. Select **Download in PDF** format.
        5. Click on **Go**.
        6. Upload the downloaded PDF file(s) here.
        """

    def transactions(self, table):
        df = pd.DataFrame(table[1:], columns=table[0])
        return df
    
class EPF:
    title = "Employee Provident Fund"
    table = pd.DataFrame()

    def __init__(self):
        self.help = """
        **How to generate report**
        1. Login to your EPF account.
        2. Go to the **Passbook** section.
        3. Select the **Month** and **Year**.
        4. Click on **Download**.
        5. Upload the downloaded PDF file(s) here.
        """

    def transactions(self, table):
        df = pd.DataFrame(table[4:-5], columns=['Wage Month', 'Date', 'Type', 'Particulars', 'EPF', 'EPS', 'Employee', 'Employer', 'Pension'])
        df['Employee'] = df['Employee'].str.replace(',', '').astype(float)
        df['Employer'] = df['Employer'].str.replace(',', '').astype(float)
        df['Pension'] = df['Pension'].str.replace(',', '').astype(float)
        df['Net'] = df['Employee'] + df['Employer'] + df['Pension']
        df = df.dropna(subset=['Date'])
        df.rename({'Date':'Txn Date'}, inplace=True)
        return df
    
class SGB:
    title = "Sovereign Gold Bonds"
    table = pd.DataFrame()

    def __init__(self):
        self.help = """
        **How to generate report**
        1. Login to your SBI account.
        2. Go to the **e-Services** section.
        3. Select the **Sovereign Gold Bond Scheme**.
        4. Click on **Enquiry**.
        5. Print the page as PDF. Download the PDF file.
        5. Upload the downloaded PDF file(s) here.
        """

    def transactions(self, table):
        df = pd.DataFrame(table[1:], columns=table[0])
        df.rename(columns={'Purchase\nDate':'Txn Date'}, inplace=True)
        df.rename(columns={'Purchase\nGold Rate':'Gold Rate'}, inplace=True)
        df['Txn Date'] = pd.to_datetime(df['Txn Date'], format='%d-%b- %Y').dt.date
        df['Order ID'] = df['Order ID'].apply(lambda x: str(x).split('(')[0].strip())
        df = df[['Txn Date', 'Order ID', 'Unit', 'Amount', 'Gold Rate']]
        return df
    
class PPF:
    title = "Public Provident Fund"
    table = pd.DataFrame()

    def __init__(self):
        self.help = """
        **How to generate report**
        1. Login to your SBI account.
        2. Go to the **Account Statement** section.
        3. Select the **PPF Account Number** and **Date Range**.
        4. Select **Download in PDF** format.
        5. Click on **Go**.
        6. Upload the downloaded PDF file(s) here.
        """

    def transactions(self, table):
        # Ignore the first table
        if table[0][0] == "Account Number":
            return pd.DataFrame()
        
        df = pd.DataFrame(table[1:], columns=table[0])
        ref_checq_col = df.keys()[3]
        df.rename(columns={ref_checq_col:'Ref No./Cheque No.'}, inplace=True)
        df['Txn Date'] = pd.to_datetime(df['Txn Date'], format='%d %b %Y').dt.date
        df = df[['Txn Date', 'Description', 'Ref No./Cheque No.', 'Debit', 'Credit', 'Balance']]
        return df

class STK:
    title = "Stocks (Zerodha)"
    table = pd.DataFrame()

    def __init__(self):
        self.help = """
        **How to generate report**
        1. Login to your Kite account, go to Console.
        2. Click on **Funds**.
        3. Click on **Statement**.
        4. Select the **Category**.
        5. Select the date range and click on **View**.
        6. The statement can be downloaded in XLSX or CSV format by clicking on **Download XLSX|CSV**.
        """

    def transactions(self, table):
        df = table.drop(index=[0, len(table)-1])
        df.rename(columns={
            'particulars': 'Description',
            'voucher_type': 'Reference',
            'posting_date': 'Txn Date',
            'debit': 'Debit',
            'credit': 'Credit',
            'net_balance': 'Balance'
        }, inplace=True)
        df['Txn Date'] = pd.to_datetime(df['Txn Date'], format='%Y-%m-%d').dt.date
        df['Debit'] = df.Debit.apply(lambda x: round(x, 2))
        df['Balance'] = df.Balance.apply(lambda x: round(x, 2))
        df['Credit'] = df.Credit.apply(lambda x: round(x, 2))
        df = df[['Txn Date', 'Description', 'Reference', 'Debit', 'Credit', 'Balance']]
        return df


class Variant(Enum):
    SBI=SBI().title
    EPF=EPF().title
    SGB=SGB().title
    PPF=PPF().title
    STK=STK().title