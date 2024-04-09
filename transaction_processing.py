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
        df['Date (Value Date)'] = df['Date (Value Date)'].apply(lambda x: x.split('(')[0].strip())
        df.rename(columns={'Date (Value Date)':'Txn Date'}, inplace=True)
        df['Txn Date'] = pd.to_datetime(df['Txn Date'], format='%d-%b-%Y').dt.date
        df = df[['Txn Date', 'Narration', 'Ref/Cheque No.', 'Debit', 'Credit', 'Balance']]
        return df


class Variant(Enum):
    SBI=SBI().title
    EPF=EPF().title
    SGB=SGB().title
    PPF=PPF().title